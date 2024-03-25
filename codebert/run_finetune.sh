#!/bin/bash

lang=solidity
pretrained_model=microsoft/codebert-base

torchrun train.py \
    --model_type roberta \
    --task_name codesearch \
    --do_train \
    --do_eval \
    --eval_all_checkpoints \
    --train_file train.txt \
    --dev_file valid.txt \
    --max_seq_length 512 \
    --per_gpu_train_batch_size 32 \
    --per_gpu_eval_batch_size 32 \
    --learning_rate 1e-5 \
    --num_train_epochs 20 \
    --gradient_accumulation_steps 1 \
    --overwrite_output_dir \
    --data_dir ./data-ft \
    --output_dir ./models/$lang  \
    --model_name_or_path $pretrained_model
