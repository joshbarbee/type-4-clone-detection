import json
import os

with open('train-pretrain.txt', 'r') as f:
    lines = f.readlines()

train = []
valid = []
test = []
res = []

t_len = len(lines)
train_len = int(0.7 * t_len)
valid_len = int(0.2 * t_len)
test_len = int(0.1 * t_len)

for line in lines:
    line = line.split('<CODESPLIT>')
    data = {
        'label': int(line[0]),
        'codehash1': line[1],
        'codehash2': line[2],
        'func1': line[3],
        'func2': line[4].replace('\n', ' ')
    }

    res.append(data)

train = res[0: train_len]
valid = res[train_len: train_len + valid_len]
test = res[train_len + valid_len:]

os.makedirs('data', exist_ok=True)

with open('data/train-ft.json', 'w') as f:
    json.dump(train, f)

with open('data/valid-ft.json', 'w') as f:
    json.dump(valid, f)

with open('data/test-ft.json', 'w') as f:
    json.dump(test, f)