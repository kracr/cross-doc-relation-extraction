# KDocRE
<h3>KDocRE:Knowledge-Driven Cross-Document Relation Extraction</h3>
##Accepted in ACL 2024, findings conference## 

![alt text](https://github.com/MonikaJain19/Crossdoc/blob/main/modeldiagramcrossdoc1.drawio.png)


## Acknowledgments
This repository contains code adapted from the following research papers for the purpose of cross document-level relation extraction. We extend our gratitude to the authors for generously sharing their clean and valuable code implementations. 

### 1. Entity-centered Cross-document Relation Extraction

- **Paper**: [Entity-centered Cross-document Relation Extraction](https://arxiv.org/pdf/2210.16541.pdf)
- **Authors**: Wang, Fengqi  and
      Li, Fei  and
      Fei, Hao  and
      Li, Jingye  and
      Wu, Shengqiong  and
      Su, Fangfang  and
      Shi, Wenxuan  and
      Ji, Donghong  and
      Cai, Bo",Wang Xu, Kehai Chen, Tiejun Zhao
- **Year**: 2022

- **Code implementation can be found here: [https://github.com/MakiseKuurisu/ecrim]

### Requirements
- Follow the guideliens from : https://github.com/thunlp/CodRED
- pip install torch-geometric
- pip install a2t
- sudo apt install redis-server
- start Redis-server using: sudo service redis-server start
### Alternative using Docker
- docker build -t doc:v0 .
- docker run --gpus all -it -d --shm-size=20gb --name=doc doc:v0
- login Docker and install the following:

- apt-get update && \
      apt-get -y install sudo
- pip install torch-geometric
- pip install a2t
- sudo apt install redis-server
- start Redis-server using: sudo service redis-server start

- Navigate to data/rawdata folder
- wget https://thunlp.oss-cn-qingdao.aliyuncs.com/wiki_ent_link.jsonl
-  wget https://thunlp.oss-cn-qingdao.aliyuncs.com/distant_documents.jsonl
-  wget https://thunlp.oss-cn-qingdao.aliyuncs.com/popular_page_ent_link.jsonl

- Navigate to data directory:
- python3 load_data_doc.py
- python3 redis_doc.py

<h3>Directory structure</h3>

In this directory structure, you have a folder named "C" containing a subdirectory "code." Within the "code" directory, there are several files and subdirectories:
- `data`: Directory to store data
- `context`: Files for creating context.
- `r/`: Directory to store model checkpoints.
- `main.py`: File for training the code.
- `explanation_withrelevance.py`: File to generate explanation.



## Datasets

This project utilizes the following datasets:

- **CoDRED Dataset:** The DocRED dataset can be accessed ( https://github.com/thunlp/CodRED) place in data/ directory

# Training

Follow the steps below to start the training process:
1. Train reasoning module: 
 Navigate to the `KDocRE` directory using the following command:
   
   cd/ KDocRE
   bash train.sh
   

# Testing

Navigate to the `KDocRE` directory using the following command:

  cd/ KDocRE
   bash test.sh
   

#  Explanation   
- explaination is generated in explanation.txt
- explaination with relevance is stored in relevance.txt
