from solidity_lexer.SolidityLexer import SolidityLexer
from solidity_lexer.SolidityParser import SolidityParser
from CustomVisitor import CustomVisitor, CustomErrorListener, ParserException
from antlr4 import CommonTokenStream
from antlr4.InputStream import InputStream
import json
from tqdm import tqdm
import contextlib
import os
import sys

def make_postfix(exception_count, written_count):
    return f"Exceptions: {exception_count} | Written: {written_count}"

def format_pretrain():
    res = []
    exception_count, written_count, ids = 0, 0, 0
    with open('train-pretrain.txt', 'r') as f:
        codes = f.readlines()
    with tqdm(enumerate(codes), total=len(codes), postfix=exception_count, bar_format="{postfix} | Elapsed: {elapsed} | {rate_fmt} | {n_fmt}/{total_fmt}") as t:
        for i, data in t:
            if i % 1000 == 0:
                with open('data/train-pretrain.txt', 'a') as f:
                    for r in res:
                        f.write(json.dumps(r) + '\n')
                res = []

            data = json.loads(data)

            with open(os.devnull, "w") as f, contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
                input_stream = InputStream(data['text'])
                lexer = SolidityLexer(input_stream)
                lexer.addErrorListener(CustomErrorListener())
                stream = CommonTokenStream(lexer)

                try:
                    parser = SolidityParser(stream)
                    parser.addErrorListener(CustomErrorListener())
                    ast = CustomVisitor()
                    r = ast.visit(getattr(parser, "functionDefinition")())

                    data['id'] = ids
                    data['text'] = r
                    res.append(data)
                    ids += 1
                except Exception as e:
                    with open('error.log', 'a') as f:
                        f.write(f"Exception at {i}: {e}\n")
                    exception_count += 1
                    t.postfix = make_postfix(exception_count, written_count)
                    t.refresh()
                    continue    
                
                written_count += 1
                t.postfix = make_postfix(exception_count, written_count)
                t.refresh()

def split_pretrain():
    from sklearn.model_selection import train_test_split
    import json
    import os

    with open('./data/train-pretrain.txt', 'r') as f:
        lines = f.readlines()

    res = []

    for line in lines:
        res.append(json.loads(line)['text'])


    train, valid = train_test_split(res, test_size=0.3)

    valid, test = train_test_split(valid, test_size=0.33333)

    with open('data/train.txt', 'w') as f:
        f.writelines('\n'.join(train))

    with open('data/valid.txt', 'w') as f:
        f.writelines('\n'.join(valid))

    with open('data/test.txt', 'w') as f:
        f.writelines('\n'.join(test))

    os.remove('./data/train-pretrain.txt')


def format_finetune():
    res = []
    exception_count, written_count, ids = 0, 0, 0

    with open('train-finetune.txt', 'r') as f:
        codes = f.readlines()

    with tqdm(enumerate(codes), total=len(codes), postfix=exception_count, bar_format="{postfix} | Elapsed: {elapsed} | {rate_fmt} | {n_fmt}/{total_fmt}") as t:
        for i, line in t:
            line = line.split('<CODESPLIT>')
            data = {
                'label': int(line[0]),
                'codehash1': line[1],
                'codehash2': line[2],
                'func1': line[3],
                'func2': line[4]
            }
            with open(os.devnull, "w") as f, contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
                input_stream1 = InputStream(data['func1'])
                lexer1 = SolidityLexer(input_stream1)
                lexer1.addErrorListener(CustomErrorListener())
                stream1 = CommonTokenStream(lexer1)

                input_stream2 = InputStream(data['func2'])
                lexer2 = SolidityLexer(input_stream2)
                lexer2.addErrorListener(CustomErrorListener())
                stream2 = CommonTokenStream(lexer2)

                try:
                    parser1 = SolidityParser(stream1)
                    parser1.addErrorListener(CustomErrorListener())
                    ast1 = CustomVisitor()
                    r1 = ast1.visit(getattr(parser1, "functionDefinition")())

                    parser2 = SolidityParser(stream2)
                    parser2.addErrorListener(CustomErrorListener())
                    ast2 = CustomVisitor()
                    r2 = ast2.visit(getattr(parser2, "functionDefinition")())

                    data['func1'] = r1
                    data['func2'] = r2

                    res.append(data)

                    ids += 2
                except Exception as e:
                    with open('error.log', 'a') as f:
                        f.write(f"Exception at {i}: {e}\n")
                    exception_count += 1
                    t.postfix = make_postfix(exception_count, written_count)
                    t.refresh()
                    continue    
                
                written_count += 1
                t.postfix = make_postfix(exception_count, written_count)
                t.refresh()

    train_len = int(0.7 * len(res))
    valid_len = int(0.2 * len(res))

    train = res[0: train_len]
    valid = res[train_len: train_len + valid_len]
    test = res[train_len + valid_len:]

    with open('data-ft/train-ft.json', 'w') as f:
        json.dump(train, f)

    with open('data-ft/valid-ft.json', 'w') as f:
        json.dump(valid, f)

    with open('data-ft/test-ft.json', 'w') as f:
        json.dump(test, f)

if __name__ == "__main__":
    if sys.argv[1] == 'pretrain':
        os.makedirs('data', exist_ok=True)
        format_pretrain()
        split_pretrain()
    elif sys.argv[1] == 'finetune':
        os.makedirs('data-ft', exist_ok=True)
        format_finetune()