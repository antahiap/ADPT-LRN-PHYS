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

## SQL Database
`flyctl` is a command-line tool provided by Fly.io, a platform for deploying and managing applications. To access a railway database with flyctl, you would typically follow these steps:

Install [flyctl](https://fly.io/docs/hands-on/install-flyctl/), make an account on [railway](https://railway.app/), and set the database confidential :

```
FLY_POSTGRES_DATABASE="railway"
FLY_POSTGRES_USER="username"
FLY_POSTGRES_PASSWORD="Password"
FLY_POSTGRES_HOSTNAME="HostName"
FLY_POSTGRES_PROXY_PORT="6565"
```

run the database before starting the streamlit. Configure Fly.io: Use flyctl to configure your Fly.io application. You can set environment variables using the flyctl secrets command. For example:

```
flyctl secrets set DATABASE_URL=your_database_connection_string
```
and run it:
```
flyctl deploy
```

if you want to run it locally, for deployment set the .envs under `Manage app> settings> secretes`

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






