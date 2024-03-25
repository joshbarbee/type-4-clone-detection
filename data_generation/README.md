Scripts in folder used for data generation. 

## degen.py
degen.py is used to generate function pairs from contract files, for both pretraining and
fine tuning. Using degen.py is a two-step process. First, we must decompile all contracts
to be used for analysis, which is outputted to an intermediate folder (./heimdall-output).
```
    python degen.py gen start stop
```

The `gen` command requires a start and stop parameter to indicate the starting and stopping
number of which files to parse. Memory leaks can occur from `gen`, causing the programming
and computer to crash, so it is typically best to only run in 500 contract intervals. The 
`run_degen.sh` script can be used to generate Heimdall decompilations over a range larger
than 500. For example
```
    sh run_degen.sh 0 100000
```
will generate heimdall decompilations for contracts 0 to 100000. The contract ID (0, 1, 1000000, etc.)
is determined by the `filenames` parameter in the program and should not be changed. As long
as there is no change to the underlying `contracts` folder, no issue should arrise

Then, to create function pairs between a function in a contract and its decompiled functions, we 
reuse `degen.py`. By providing no arguments (i.e `python degen.py`), the program will output function
pairs suitable for finetuning, and with the argument `python degen.py finetune`, functions will be 
outputted for fine-tuning. The structure of a function output is as follows:

For pretraining
```
    {
        'id': a unique function ID, incremented by one
        'text': the text of the function
        'type': whether the function comes from a regular function or a decompiled function
        'codehash': the codehash of the original contract the function came from
    }
```

For finetuning
```
    <CODESPLIT>label
    <CODESPLIT>func 1 codehash
    <CODESPLIT>func 2 codehash 
    <CODESPLIT>func 1 text
    <CODESPLIT>func 2 text
```

When outputting, the output file is written to every 500 functions, to avoid having to store a large
number of functions in memory. It is crucial to not modify or move the output file (either `train-pretrain.txt` or `train-finetune.txt`). In the finetuning case, function pairs are from a regular-decompiled contract pair where
the functions are equivalent (determined by function signature, labeled 1) or a random pairing of some function and a random decompiled function (labeled 0), with a 50% split. 

## split_ft_json.py
`split_ft_json.py` is used to create a 70/20/10 training/validation/test split for functions not requiring DFG conversion. Requires `train-finetune.txt` file to be in working directory. Will output to folder `./data-ft`. This should be used for finetuning for models based on the Roberta training from huggingface, NOT codebert. See `split_ft_cb_json.py` for the CodeBert equivalent