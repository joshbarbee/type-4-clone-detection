Type 4 clone detection powered via contract source code - decompiled function pairings.

Steps to train / finetune a model

It is important to have the `Heimdall-rs` decompiler installed for data generation. See
`https://github.com/Jon-Becker/heimdall-rs/tree/main` for installation information.

1. Generate data. Assuming you already have the contracts folder that stores the 600,000
contract files, we can proceed with data generation. 
    1. `cd` into the data_generation folder
    2. Generate all required Heimdall intermediate files via `run_degen.sh` with the start
    and stop options (0 and a number around 600,000, or lower)
    3. To pretrain, run `python degen.py pretrain`, which will output results to `train-pretrain.txt`
    4. To finetune, run `python degen.py finetune`, which output results to `train-finetune.txt`
2. After results are finished generating, if DFGs are not used, create the train/test/valid splits by using the respective `split_X.py` file. For pretraining, this should always be `split_pretrain.txt`. For finetuning, use
`split_ft_cb` for a CodeBert-based approach and `split_ft_json` for all other models (Roberta, using HuggingFace script).
3. If DFG generation is required, run `dfg_gen.py` in the `dfg_generation` folder. With the argument `dfg_gen.py pretrain`, DFG-based results for pretraining are outputted to the `data` folder, with pre-determined 70/20/10 splits. With the argument `dfg_gen.py finetune`, DFG-based results are outputted to the `data-ft` folder, with 70/20/10 splits. Function pairs are not altered by DFG generation, only the text of the functions.
4. To train a Roberta Model, used the provided `roberta/run_pretrain.sh` and `roberta/run_finetune.sh` files provided. Arguments in the script will likely need to be changed to reflect your current working directory and location of data files
5. To train a CodeBert model, use the script provided in `codebert/run_finetune.sh`. Again, arguments may need to be changed.

There are also scripts to train a custom tokenizer, in `tokenizer.py`. Usage is relatively simple, use the `tokenizer.py --help` command for more info.