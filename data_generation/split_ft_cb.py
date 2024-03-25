from sklearn.model_selection import train_test_split
import json
import os

with open('train-finetune.txt', 'r') as f:
    lines = f.readlines()

train, valid = train_test_split(lines, test_size=0.3)

valid, test = train_test_split(valid, test_size=0.33333)

os.makedirs('data-ft', exist_ok=True)

with open('data/train.txt', 'w') as f:
    f.writelines('\n'.join(train))

with open('data/valid.txt', 'w') as f:
    f.writelines('\n'.join(valid))

with open('data/test.txt', 'w') as f:
    f.writelines('\n'.join(test))