# Adaptive Learning
Wanna be able to read a paper from a domain you know nothing about? Use our tool to get explanations of every term used in the paper and gain quick overview of the domain. A concept is used in the explanation that you don’t know? Go deeper again until you reach the explanation of for example addition or any simple concept that a 5 years old could understand, if he knows how to read of course ! Built using ChatGPT and other sources, [Documentation]()

<div style="text-align:center;">
  <img src="static/ADPTL.gif" style="max-width:100%; width:800px;">
</div>


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

## Future works

- More features (UI)
  - Learned keyword
  - Study-path recommendation
- Scientific-writing recommendation
- Improve keyword explanation
- Scalability
- Robustness
- Extend Pdf extraction
  - images 
  - tables
- Extend to more than arXiv papers and include book






