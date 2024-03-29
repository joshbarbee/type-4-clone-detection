from pymongo import MongoClient
import itertools
import random
import simhash

def get_mongo_collection():
    client = MongoClient('172.21.128.1', 27017)
    db = client['ethereum']
    collection = db['eth_functions']
    return collection

def get_similar_signatures(client, signature):
    result = client.find({"signature": signature})

    combined = list(itertools.combinations(result, 2))

    print()
    print("Comparing " + str(len(combined)) + " functions")
    print("Signature: " + signature)

    sim = ''

    if len(combined) <= 1:
        return None

    ct = 0
    while sim != 'b':
        if ct > 25:
            return None

        pair = random.randint(0, len(combined) - 1)
        func_a, func_b = combined[pair]

        dist = simhash.Simhash(func_a['function']).distance(simhash.Simhash(func_b['function']))

        if dist <= 10:
            ct += 1
            continue

        ct = 0

        sim = prompt_similar(func_a['function'], func_b['function'])
        if sim == 'y':
            return func_a['codehash'], func_b['codehash'], func_a['function'], func_b['function']

    return None

def pprint_function(func):
    # if semicolon, print next with tabs if next not space
    # skip until not space

    tabs = 0
    next_tab = False
    
    for c in func:
        if c == ';':
            next_tab = True
            print(c)
        elif c == '{':
            next_tab = True
            print(c)
            tabs += 1
        elif c == '}':
            next_tab = True
            print(c)
            tabs += 1
        else:
            if c == ' ' and next_tab:
                continue

            if next_tab == True:
                print('\t' * tabs, end = '')
                next_tab = False
            print(c, end='')

def prompt_similar(func_a, func_b):
    print()
    pprint_function(func_a)
    print()
    pprint_function(func_b)

    response = input("\nAre these functions semantically similar (not code)? (y/n/b): ")

    if response == "y":
        return 'y'
    elif response == "b":
        return 'b'
    else:
        return 'n'

def export_similar(codehash_a, codehash_b, func_a, func_b):
    with open("similar_functions.txt", "a") as f:
        f.write(codehash_a + "<SPLIT>" + codehash_b + "<SPLIT>" + func_a + '<SPLIT>' + func_b + '\n')

def get_random_signatures(client):
    result = client.aggregate([{ "$sample": { "size": 1000 } }])

    for res in result:
        similar = get_similar_signatures(client, res["signature"])
        if similar is not None:
            export_similar(*similar)

if __name__ == "__main__":
    client = get_mongo_collection()
    print(get_random_signatures(client))