import os
from glob import glob
import json
from antlr4.InputStream import InputStream
from antlr4 import CommonTokenStream
from solidity_lexer.SolidityLexer import SolidityLexer
import random
import shutil
import subprocess
from Crypto.Hash import keccak
import multiprocessing as mp
import random
import sys
import contextlib
from threading import Timer
import signal


filenames = sorted([y for x in os.walk("./contracts") for y in glob(os.path.join(x[0], '*.json'), recursive=True)])
N = len(filenames)
OUTPUT = 'train-finetune.txt'
OUTPUT_PATH = os.path.join(os.getcwd(), OUTPUT)
WORKERS = 12

WS = {131, 140, 170, 175, 132, 133, 141, 142, 171, 172, 176, 177}

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

def run_heimdall_batch(filenames, start):
    try:
        os.mkdir('./heimdall-output2')
    except:
        print("Error creating directory", flush=True)
    i = 0

    f2b = []

    err_files = 0
    f2r = 0
    successes = 0

    for filename in filenames:
        if i % 100 == 0:
            print("On file ", i + start, " successes: ", successes, "errors: ", err_files, " failed to read: ", f2r, flush=True)
        i += 1
        with open(filename, 'r') as f:
            try:
                data = json.load(f)
            except Exception as e:
                print("Error loading file: " + filename, flush=True)
                err_files += 1
                continue
    
        if 'source' not in data or data['source'] is None:
            err_files += 1
            f2r += 1
            continue
        
        codehash = data['codehash']
        bytecode = data['bytecode']

        if codehash[2:6] not in f2b:
            f2b.append(codehash[2:6])
            os.makedirs(f"./heimdall-output2/{codehash[2:6]}", exist_ok=True)

        proc = subprocess.Popen(['/home/josh/.bifrost/bin/heimdall', 'decompile', '--include-sol', '--skip-resolving', bytecode], cwd=f'./', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        timer = Timer(10, proc.kill)

        try:
            timer.start()
            stdout, stderr = proc.communicate()

            try:
                shutil.move("./output/local/decompiled.sol", f"./heimdall-output2/{codehash[2:6]}/{codehash}.sol")
                successes += 1
            except:
                print("Error moving file: " + filename, flush=True)
                err_files += 1
                continue
        finally:
            timer.cancel()

def parse_contracts(filenames):
    contract_tokens = {}

    for filename in filenames:
        with open(filename, 'r') as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(e)
                print("Error loading file: " + filename, flush=True)
                continue
    
        if 'source' not in data or data['source'] is None:
            continue

        new_contract = [[],[]]
        
        try:
            with timeout(seconds=20000):
                for sourcecode in data["source"]["SourceCodes"]:
                    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
                        input_stream = InputStream(sourcecode['Code'])
                        lexer = SolidityLexer(input_stream)

                        stream = CommonTokenStream(lexer)
                        stream.fill()

                    new_contract[0].extend([(token.text, token.type) for token in stream.tokens])
                new_contract[0] = parse_tokens(new_contract[0])

                try:
                    with open(f"./heimdall-output2/{data['codehash'][2:6]}/{data['codehash']}.sol", 'r') as _if:
                        with open(os.devnull, "w") as f, contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
                            input_stream = InputStream(_if.read())
                            lexer = SolidityLexer(input_stream)

                            stream = CommonTokenStream(lexer)
                            stream.fill()
                            new_contract[1] = parse_tokens([(token.text, token.type) for token in stream.tokens], is_decomp=True)

                    if len(new_contract[0]) != 0 and len(new_contract[1]) != 0:
                        contract_tokens[data['codehash']] = (new_contract[0], new_contract[1])
                except FileNotFoundError:
                    print("FNFE: Error loading file: " + data['codehash'], flush=True)
                    continue
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
    in_contract = False
    in_func = False

    while tokens:
        token, _type = tokens.pop(0)

        if _type == 15:
            in_contract = True

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
                        funcs[fselector] = func
                else:
                    fselector = fselector.rstrip(",") + ")"
                    keccak_hash = keccak.new(digest_bits=256)
                    keccak_hash.update(fselector.encode('utf-8'))
                    khash = keccak_hash.hexdigest()[:8]

                    if len(func) > 20:
                        funcs[khash] = func
                        
    for h in funcs.keys():
        t = contract_vars.copy()
        t.extend(funcs[h])
        funcs[h] = t
    return funcs

def gen_disasm_pair(codehash, rand_codehash, contract_tokens, decompiled_tokens, label):    
    func_tokens = ''.join(contract_tokens)
    decomp_tokens = ''.join(decompiled_tokens)

    return ''.join(f"{label}<CODESPLIT>{codehash}<CODESPLIT>{rand_codehash}<CODESPLIT>{func_tokens}<CODESPLIT>{decomp_tokens}".splitlines()) + '\n'


def export(contract_functions, decompiled_functions):
    successes = 0

    with open(OUTPUT_PATH, 'a+') as buffer:
        for codehash in list(decompiled_functions.keys()):
            if len(contract_functions[codehash]) == 0:
                continue
                
            cf = contract_functions[codehash]
            df = decompiled_functions[codehash]
            cf_set = set(cf.keys())
            df_set = set(df.keys())
            found_funcs = list(cf_set.intersection(df_set))

            if not found_funcs: 
                continue
                
            contract_func = random.choice(found_funcs)
            contract_tokens = cf[contract_func]

            if random.random() > 0.5:
                decompiled_tokens = df[contract_func]
                try:
                    buffer.write(gen_disasm_pair(codehash, codehash, contract_tokens, decompiled_tokens, 1))
                    successes += 1
                except Exception as e:
                    raise e
            else:
                rand_codehash = random.choice(list(set(decompiled_functions.keys()) - {codehash}))
                rf = decompiled_functions[rand_codehash]
                rand_func = random.choice(list(decompiled_functions[rand_codehash].keys()))
                decompiled_tokens = decompiled_functions[rand_codehash][rand_func]
                try:
                    buffer.write(gen_disasm_pair(codehash, rand_codehash, contract_tokens, decompiled_tokens, 0))
                    successes += 1
                except Exception as e:
                    raise e
    
    return successes

def export_pretrain(contract_functions, decompiled_functions, start_id):
    successes = 0
    res = []

    with open(OUTPUT_PATH, 'a+') as buffer:
        for codehash in list(decompiled_functions.keys()):
            if len(contract_functions[codehash]) == 0:
                continue
                    
            cf = contract_functions[codehash]
            df = decompiled_functions[codehash]
            cf_set = set(cf.keys())
            df_set = set(df.keys())
            found_funcs = list(cf_set.intersection(df_set))

            if not found_funcs: 
                continue
                
            for sig in found_funcs:
                res_cf = {
                    'id': start_id,
                    'text': ''.join(cf[sig]),
                    'type': 'contract',
                    'codehash': codehash
                }

                start_id += 1

                res_df = {
                    'id': start_id,
                    'text': ''.join(df[sig]),
                    'type': 'decompiled',
                    'codehash': codehash
                }

                start_id += 1

                res.append(res_cf)
                res.append(res_df)

                successes += 2

    random.shuffle(res)

    with open(OUTPUT_PATH, 'a+') as buffer:
        for r in res:
            buffer.write(json.dumps(r) + '\n')
    
    return (start_id, successes)

def get_functions(filenames):
    contract_functions = {}
    decompiled_functions = {}
    
    N = len(filenames)
    chunk_size = N // WORKERS  # Calculate the chunk size for each worker
    start_indices = list(range(0, N, chunk_size))
    
    with mp.Pool(WORKERS) as pool:
        # issue tasks and process results
        chunks = [filenames[start:start + chunk_size] for start in start_indices]
        res = pool.map(parse_contracts, chunks)
    
        for chunk in res:
            for codehash, (contract_tokens, decompiled_tokens) in chunk.items():
                contract_functions[codehash] = contract_tokens
                decompiled_functions[codehash] = decompiled_tokens

    return (contract_functions, decompiled_functions)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'gen':
        run_heimdall_batch(filenames[int(sys.argv[2]):int(sys.argv[2]) + 500], int(sys.argv[2]))
        ddirs = glob('./output*')
        for dir in ddirs:
            shutil.rmtree(dir)
    else:
        STEP = 1000
        successes = 0
        start_id = 0
        print("Starting generating functions for pretraining, total ", os.popen("find ./heimdall-output2/. -type f | wc -l").read())
        for i in range(416500, N, STEP):
            print("On interval ", i)
            contract_functions, decomp_functions = get_functions(filenames[i:min(len(filenames), i+STEP)])
            print("Exporting Contracts")

            if len(sys.argv) > 1 and sys.argv[2] == 'pretrain':
                OUTPUT = 'train-pretrain.txt'
                start_id, successes = export_pretrain(contract_functions, decomp_functions, start_id)
            else:
                successes = export(contract_functions, decomp_functions)

        print("++++++++++ FINISHED ++++++++++")
        print(f"Succesfully outputted {successes} examples out of {N} total files read")

        
