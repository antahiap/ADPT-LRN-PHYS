# Adaptive Learning
Wanna be able to read a paper from a domain you know nothing about? Use our tool to get explanations of every term used in the paper and gain quick overview of the domain. A concept is used in the explanation that you don’t know? Go deeper again until you reach the explanation of for example addition or any simple concept that a 5 years old could understand, if he knows how to read of course ! Built using ChatGPT and other sources.


<img src="static\graph_ref.png" style="width:600px;"/>


## Installation 

- Install the dependencies via pip or conda, e.g., python=3.9.6

```
    python -m venv ens
    pip install -r requirements.txt
```

- Get your [OPENAI_API_KEY](https://platform.openai.com/account/api-keys) and store it in var for linux as follow, [other setup](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety)


```
echo "export OPENAI_API_KEY='yourkey'" >> ~/.zshrc
source ~/.zshrc

```
- Put your api key in .env file, exemple of .env file:

```
OPENAI_API_KEY="you-key"
```

## Streamlit

- Run:
```
streamlit run src/home.py
```

## Neo4j

- Port 7474: 1000 pages with url check
- port 6464: test server 

using the community docker image, [link](https://hub.docker.com/_/neo4j/)
```
docker pull neo4j:5.11.0-community-ubi8
```

- runing the server, [more info](https://github.com/neo4j/docker-neo4j)
```
docker run \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=./neo4j/data:/data \
    --volume=./neo4j/logs:/logs \
    neo4j:5.11.0-community-ubi8 
```

```
docker run \
    --publish=6474:7474 --publish=6687:7687 \
    --volume=./neo4j2/data:/data \
    --volume=./neo4j2/logs:/logs \
    neo4j:5.11.0-community-ubi8 
```

stoping the serve
```
docker ps -a
docker stop image-id
```

## GOAls
Pyhsic-math
- Having personaliozed agent, showing the path learning
  - making database
  - find ML method
- Visualization
  - connecting concepts with images
  - videos Avators
- Teaching method, e.g. 
    - doing experiments
    - 1b3b videos
- webcam on to recognized board,  






