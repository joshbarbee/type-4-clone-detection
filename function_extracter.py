import os
from glob import glob
import json
from antlr4.InputStream import InputStream
from antlr4 import CommonTokenStream
from data_generation.solidity_lexer.SolidityLexer import SolidityLexer
from Crypto.Hash import keccak
import signal
import contextlib
import multiprocessing as mp
from pymongo import MongoClient

def get_mongo_collection():
    client = MongoClient('172.21.128.1', 27017)
    db = client['ethereum']
    collection = db['eth_functions']
    return collection

filenames = sorted([y for x in os.walk("../contracts") for y in glob(os.path.join(x[0], '*.json'), recursive=True)])
N = 1000
WS = {131, 140, 170, 175, 132, 133, 141, 142, 171, 172, 176, 177}
WORKERS = 12

class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)


def parse_contracts(filenames):
    contract_tokens = {}

    for filename in filenames:
        with open(filename, 'r') as f:
            try:
                data = json.load(f)
            except Exception as e:
                print("Error loading file: " + filename, flush=True)
                continue
    
        if 'source' not in data or data['source'] is None:
            continue

        new_contract = []
        
        try:
            with timeout(seconds=20000):
                for sourcecode in data["source"]["SourceCodes"]:
                    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
                        input_stream = InputStream(sourcecode['Code'])
                        lexer = SolidityLexer(input_stream)

                        stream = CommonTokenStream(lexer)
                        stream.fill()

                    new_contract.extend([(token.text, token.type) for token in stream.tokens])
                new_contract = parse_tokens(new_contract)
                
                contract_tokens[data['codehash']] = new_contract
        except TimeoutError:
            print("Error loading file: " + data['codehash'], flush=True)
            continue
    return contract_tokens

# Get an abstract representation of each function of a contract, with whitespace, comments removed
# Identifiers are converted into meta-representations    

def exhaust_decl(token, _type, tokens):
    func = []

    while _type != 130:
        if _type == 72: # fallback, receive catch
            return None
        
        if tokens:
            token, _type = tokens.pop(0)
            if _type in WS: # replace all ws with single quote
                func.append(" ")
            else:
                func.append(token)
        else:
            return None
    
    return func

def parse_tokens(tokens, is_decomp = False):
    funcs = {}
    
    cur_func = ""
    depth = 0
    fselector = ""
    func = []
    contract_vars = []
    in_func = False

    while tokens:
        token, _type = tokens.pop(0)

        if _type in {30, 43}: # Function, modifier
            func = [token]

            res = exhaust_decl(token, _type, tokens)

            if res is None:
                continue

            func.extend(res)
            cur_func = func[-1]

            fselector = cur_func + "("
            in_func = True

            while _type != 72: # read func decl up to 1st rparen
                if tokens:
                    token, _type = tokens.pop(0)
                    if _type in WS: # replace all ws with single quote
                        func.append(" ")
                    else:
                        func.append(token)
                else:
                    return funcs
                    
                if _type in {3, 7, 9, 56, 58, 66, 27}: # any concrete type in func decl
                    is_arr = False
                    if tokens[0][1] == 73:
                        is_arr = True

                    if token == 'uint':
                        fselector = f"{fselector}{token}256{'[]' if is_arr else ''},"
                    else:
                        fselector = f"{fselector}{token}{'[]' if is_arr else ''},"
                
            # read func decl up to start of braces. Ignore function stubs.
            while _type not in {75, 78}:
                if tokens:
                    token, _type = tokens.pop(0)

                    if _type not in {75, 78}:
                        if _type in WS: # replace all ws with single quote
                            func.append(" ")
                        else:
                            func.append(token)
                else:
                    return funcs

            if _type == 78: # just func decl, don't parse
                in_func = False
            elif _type == 75:
                depth = 0
        
        if in_func: # block so we can keep parsing other things
            if _type in WS: # replace all ws with single space
                func.append(" ")
            else:
                func.append(token)
      
            if _type == 75:
                depth += 1
            elif _type == 76:
                depth -= 1

            if depth == 0:
                in_func = False
                if is_decomp:
                    fselector = cur_func.split('_')[1] 
                    if len(func) > 20:
                        funcs[fselector] = ''.join(func)
                else:
                    fselector = fselector.rstrip(",") + ")"
                    keccak_hash = keccak.new(digest_bits=256)
                    keccak_hash.update(fselector.encode('utf-8'))
                    khash = keccak_hash.hexdigest()[:8]

                    if len(func) > 20:
                        funcs[khash] = ''.join(func)
    return funcs

def get_functions(filenames):
    functions = []
    
    chunk_size = N // WORKERS  # Calculate the chunk size for each worker
    start_indices = list(range(0, N, chunk_size))
    
    with mp.Pool(WORKERS) as pool:
        # issue tasks and process results
        chunks = [filenames[start:start + chunk_size] for start in start_indices]
        res = pool.map(parse_contracts, chunks)
    
        for chunk in res:
            for codehash, contract_tokens in chunk.items():
                for func_sig, func_body in contract_tokens.items():
                    functions.append({
                        'codehash': codehash,
                        'signature': func_sig,
                        'function': func_body
                    })
    return functions

def run_batch(batch_start, batch_end, filenames):
    print(f"Processing batch {batch_start} to {batch_end}")
    functions = get_functions(filenames)
    print(f"Inserting functions from batch {batch_start} to {batch_end}")
    collection = get_mongo_collection()
    collection.insert_many(functions)

if __name__ == "__main__":
    batch_size = N

    for i in range(0, len(filenames), batch_size):
        if i >= 300000:
            break

        run_batch(i, i + batch_size, filenames[i:i + batch_size])