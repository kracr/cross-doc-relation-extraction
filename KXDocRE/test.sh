#!/bin/bash

CUDA_VISIBLE_DEVICES=0 python main.py  --test  --load_model_checkpoint /home/ecrim/ecrim/r/20/output/checkpoint-29415/pytorch_model.bin  --per_gpu_train_batch_size 1 --per_gpu_eval_batch_size 1 --learning_rate 3e-5 --epochs 10


