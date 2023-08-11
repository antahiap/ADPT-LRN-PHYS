# ADPT-LRN-PHYS
Adaptive learning platform for physics concepts built on ChatGPT knowledge. 

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
