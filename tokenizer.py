from tokenizers import ByteLevelBPETokenizer
from transformers import RobertaTokenizerFast
import argparse
import json
import os
import numpy as np

def load_data(filepath, count):
    res = []
    with open(filepath, 'r') as f:
        for i in range(count):
            data = json.loads(f.readline())
            res.append(data['text'])
    return res

def len_stats(tokenizer, data):
    lens = [len(tokenizer.encode(text)) for text in data]
    q1 = np.percentile(lens, 25)
    q3 = np.percentile(lens, 75)
    return {
        'min': min(lens),
        'max': max(lens),
        'avg': sum(lens) / len(lens),
        'q1': q1,
        "q3": q3
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, type=str, help='Input file to train tokenizer')
    parser.add_argument('-c', '--count', required=False, default=10, type=int, help='Number of examples to train tokenizer on')
    parser.add_argument('-s', '--vocab_size', required=False, default=30_000, type=int, help='Desired size of tokenizer vocab')
    parser.add_argument('-f', '--min-freq', required=False, type=int, default=2, help='Minimum frequency of a byte pair to be added to vocab')
    parser.add_argument('-o', '--output', required=True, type=str, help='Folder to output to')

    args = parser.parse_args()

    data = load_data(args.input, args.count)

    special_tokens = ['[PAD]', '[UNK]', '[CLS]', '[SEP]', '[MASK]']

    tokenizer = ByteLevelBPETokenizer(
        lowercase=False
    )

    tokenizer.train_from_iterator(
        data,
        vocab_size = args.vocab_size,
        min_frequency = args.min_freq,
        show_progress = True,
        special_tokens = special_tokens
    )

    print(len_stats(tokenizer, data))

    os.makedirs(args.output, exist_ok=True)
    tokenizer.save(os.path.join(args.output, 'tokenizer.json'))

    sol_tokenizer = RobertaTokenizerFast(
        tokenizer_file=os.path.join(args.output, 'tokenizer.json'),
        max_len=1024
    )

    sol_tokenizer.save_pretrained(args.output)

