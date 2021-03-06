# Background

We benchmark three state-of-the-art variational autoencoders (VAE) designed for molecular optimization. Specifically, we reproduce the results of Jin et al. by retraining their VAEs -- the junction tree variational autoencoder (JT-VAE), the junction tree encoder-decoder with attention mechanism and graph-to-graph translation (JTNN), and the hierarchical junction tree encoder-decoder (HierVAE). The goal of these autoencoders is to efficiently generate new molecules with improved performance properties suitable for drug discovery applications. 

This git repo contains code that was used to perform our benchmark study for team Drugs"R"Us (DLH final project, 2021 Spring at UIUC). All models were retrained on AWS. Instructions for setting up each conda environment for successful model training can be found in the following readme's.

# Final Report

- See `final_report.pdf`
- WandB Dashboard of our Select Trained Models: [https://wandb.ai/peterzhang/drugsrus/reports/Wandb-Reports-A-benchmark-study-for-molecular-optimization--Vmlldzo2Njk1MzU](https://wandb.ai/peterzhang/drugsrus/reports/Wandb-Reports-A-benchmark-study-for-molecular-optimization--Vmlldzo2Njk1MzU)


# Readme for JTNN

https://github.com/pingjiewang/sagemaker-dlh/tree/main/code/graph2graph#readme

# Readme for HierVAE

https://github.com/pingjiewang/sagemaker-dlh/tree/main/code/hiervae#readme

# Readme for JT-VAE

https://github.com/pingjiewang/sagemaker-dlh/tree/main/code/jtnn#readme

# Often used command

- bash

- pwd

- cd /home/ec2-user/SageMaker


# How to clone the code
- cd /home/ec2-user/SageMaker

- git clone https://github.com/pingjiewang/sagemaker-dlh.git

- Cloning into 'sagemaker-dlh'...

- Username for 'https://github.com/pingjiewang/sagemaker-dlh.git': peterzhangon@gmail.com

- Password for 'https://peterzhangon@gmail.com@github.com/pingjiewang/sagemaker-dlh.git':

- cd sagemaker-dlh/

# How to know your local status

- git status

# How to commit all the local changes 
- git commit 

- i ---- so you can input comment

- ESC + W + q --- save comment

- enter ----done the commit

- git push --- to push the local changes to the git repository

# How to commit several partial files 

- git status   ----------- list the new changed files

- git commit -m " comment" file_1 file_2

# SSH to git

- Step 1: set up SSH locally https://docs.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

- Step 2: to add your info into github https://docs.github.com/en/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account

# Wandb

- Welcome to Weights & Biases - Introduction Walkthrough (2020) https://www.youtube.com/watch?v=91HhNtmb0B4&t=191s

- Doc of Weights & Biases  https://docs.wandb.ai/

- An example / How to use wandb / Step 1 - 4  https://github.com/pingjiewang/sagemaker-dlh/blob/main/code/hiervae/gnn_train.py
