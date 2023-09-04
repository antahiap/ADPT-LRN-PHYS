from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS

import json
import re
import os
import getpass
import pinecone


from dotenv import load_dotenv
load_dotenv()

import database as DB


def get_section_info(section, texts=[], ids=[]):
    if not 'missing' in section.keys():
        text = section['text']
        id = section['id']
        subsections = section['subsection']

        if subsections == []:
            texts.append(text)
            ids.append(id)
            return(texts, ids)
        else:
            for subsection in subsections: 
                get_section_info(subsection, texts=texts, ids=ids)

    return(texts, ids)


doc = '1706.03762'
json_file = f"data/article_pdf/txt/{doc}.json"

with open(json_file, 'r') as json_file:
    data = json.load(json_file)

db = DB.Database()

for section in data:
    texts, ids = get_section_info(section)#, texts=[], ids=[])

for i in range(len(ids)):
    paragraphs =  re.split(r'\s*\.\n', texts[i])
    
    for pi, paragraph in enumerate(paragraphs):
        db.insert(doc, ids, '', pi+1)
        break
    break

for i in range(10):
    res = db.select("paragraph")
    print(res)
    

# initialize pinecone
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
    environment=os.getenv("PINECONE_ENV"),  # next to api key in console
)





# index_name = f"d{doc}-s{}-p{}"

# # First, check if our index already exists. If it doesn't, we create it
# if index_name not in pinecone.list_indexes():
#     # we create a new index
#     pinecone.create_index(
#       name=index_name,
#       metric='cosine',
#       dimension=1536  
# )
# # The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`
# docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)

# # if you already have an index, you can load it like this
# # docsearch = Pinecone.from_existing_index(index_name, embeddings)

# query = "What did the president say about Ketanji Brown Jackson"
# docs = docsearch.similarity_search(query)