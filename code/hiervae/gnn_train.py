import torch
import torch.nn as nn
import torch.optim as optim
import torch.optim.lr_scheduler as lr_scheduler
from torch.utils.data import DataLoader

import math, random, sys
import numpy as np
import argparse

from hgraph import *
import rdkit
import time

import wandb

# 1. Start a W&B run
wandb.init()

# 2. Save model inputs and hyperparameters
config = wandb.config
config.learning_rate = 0.9

lg = rdkit.RDLogger.logger() 
lg.setLevel(rdkit.RDLogger.CRITICAL)

parser = argparse.ArgumentParser()
parser.add_argument('--train', required=True)
parser.add_argument('--vocab', required=True)
parser.add_argument('--atom_vocab', default=common_atom_vocab)
parser.add_argument('--save_dir', required=True)
parser.add_argument('--load_epoch', type=int, default=-1)

parser.add_argument('--conditional', action='store_true')
parser.add_argument('--novi', action='store_true')
parser.add_argument('--cond_size', type=int, default=4)

parser.add_argument('--rnn_type', type=str, default='LSTM')
parser.add_argument('--hidden_size', type=int, default=270)
parser.add_argument('--embed_size', type=int, default=270)
parser.add_argument('--batch_size', type=int, default=32)
parser.add_argument('--latent_size', type=int, default=8)
parser.add_argument('--depthT', type=int, default=20)
parser.add_argument('--depthG', type=int, default=20)
parser.add_argument('--diterT', type=int, default=1)
parser.add_argument('--diterG', type=int, default=3)
parser.add_argument('--dropout', type=float, default=0.0)

parser.add_argument('--lr', type=float, default=1e-3)
parser.add_argument('--clip_norm', type=float, default=20.0)
parser.add_argument('--beta', type=float, default=0.3)

parser.add_argument('--epoch', type=int, default=20)
parser.add_argument('--anneal_rate', type=float, default=0.9)
parser.add_argument('--print_iter', type=int, default=50)
parser.add_argument('--save_iter', type=int, default=-1)

args = parser.parse_args()
print(args)

vocab = [x.strip("\r\n ").split() for x in open(args.vocab)] 
args.vocab = PairVocab(vocab)

if args.conditional:
    model = HierCondVGNN(args).cuda()
elif args.novi:
    model = HierGNN(args).cuda()
else:
    model = HierVGNN(args).cuda()

for param in model.parameters():
    if param.dim() == 1:
        nn.init.constant_(param, 0)
    else:
        nn.init.xavier_normal_(param)

if args.load_epoch >= 0:
    model.load_state_dict(torch.load(args.save_dir + "/model." + str(args.load_epoch)))

print("Model #Params: %dK" % (sum([x.nelement() for x in model.parameters()]) / 1000,))

optimizer = optim.Adam(model.parameters(), lr=args.lr)
scheduler = lr_scheduler.ExponentialLR(optimizer, args.anneal_rate)

param_norm = lambda m: math.sqrt(sum([p.norm().item() ** 2 for p in m.parameters()]))
grad_norm = lambda m: math.sqrt(sum([p.grad.norm().item() ** 2 for p in m.parameters() if p.grad is not None]))

# 3. Log gradients and model parameters
wandb.watch(model)

total_step = 0
beta = args.beta
meters = np.zeros(6)
total_time = 0
for epoch in range(args.load_epoch + 1, args.epoch):
    dataset = DataFolder(args.train, args.batch_size)
    print("train dataset is located at ", args.train)
    start_time = time.time()
    for batch in dataset:
        total_step += 1
        batch = batch + (beta,)
        model.zero_grad()
        loss, kl_div, wacc, iacc, tacc, sacc = model(*batch)

        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), args.clip_norm)
        optimizer.step()

        meters = meters + np.array([kl_div, loss.item(), wacc * 100, iacc * 100, tacc * 100, sacc * 100])

        if total_step % args.print_iter == 0:
            meters /= args.print_iter
            # 4. Log metrics to visualize performance
            wandb.log({"loss": meters[1]})
            print("[%d] Beta: %.3f, KL: %.2f, loss: %.3f, Word: %.2f, %.2f, Topo: %.2f, Assm: %.2f, PNorm: %.2f, GNorm: %.2f" % (total_step, beta, meters[0], meters[1], meters[2], meters[3], meters[4], meters[5], param_norm(model), grad_norm(model)))
            sys.stdout.flush()
            meters *= 0
        
        if args.save_iter >= 0 and total_step % args.save_iter == 0:
            n_iter = total_step // args.save_iter - 1
            torch.save(model.state_dict(), args.save_dir + "/model." + str(n_iter))
            scheduler.step()
            print("learning rate: %.6f" % scheduler.get_lr()[0])

    del dataset
    if args.save_iter == -1:
        torch.save(model.state_dict(), args.save_dir + "/model." + str(epoch))
        scheduler.step()
        print("learning rate: %.6f" % scheduler.get_lr()[0])

    end_time = time.time()
    total_time += (end_time-start_time)

    print("finished training epoch " + str(epoch+1) + " of " + str(args.epoch))
    print("training time (s) of epoch: "+ str(end_time-start_time))
    print("total time (s): " + str(total_time))

print ("Finished!")
print ("total time (s): " + str(total_time))
