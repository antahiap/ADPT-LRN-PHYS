# from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
# from langchain.document_loaders import TextLoader
# from langchain.vectorstores import FAISS

import json
import re
from pathlib import Path
import numpy as np
import os
import pinecone
import matplotlib.pyplot as plt
import networkx as nx
from pdf_file_reader import PDFFileReader

# import getpass


from dotenv import load_dotenv
load_dotenv()

import database as DB

class Vectordb():
    def __init__(self, file_path, doc_id):
        self.db_index = []
        self.sql = DB.Database()

        self.doc_id = doc_id
        self.embd_path = f'data/embeddings_{doc_id}.pkl'

        json_file = Path(file_path+f'{doc_id}.json')
        with open(json_file, 'r') as json_file:
            self.data = json.load(json_file)

    def get_section_info(self, section):
        if not 'missing' in section.keys():
            text = section['text']
            id = section['id']
            title = section['section']
            subsections = section['subsection']

            if not text =='':
                self.texts.append(text)
                self.ids.append(id)
                self.titles.append(title)

            if subsections == []:
                return
            else:
                for subsection in subsections: 
                    self.get_section_info(subsection)
        return

    def get_sections(self):
        self.texts = []
        self.ids = []
        self.titles = []

        for section in self.data:
            self.get_section_info(section)

    def insert_db(self):
        self.get_sections()
        
        for i in range(len(self.ids)):
            paragraphs =  re.split(r'\s*\.\n', self.texts[i])

            for pi, paragraph in enumerate(paragraphs):
                print(paragraph)
                db_index = self.sql.insert(
                    self.doc_id,        # paper
                    str(self.ids[i]),   # secId
                    str(pi+1),          # pId
                    self.titles[i],      # title
                    paragraph          # text
                )
                self.db_index.append(db_index)
      
    def embd_sec(self, readOn=True, nsec=2):
        import pickle
        
        self.get_sections()
        if nsec==-1:
            nsec = len(self.ids)+1

        # Get embeddigs
        if not readOn:
            from langchain.embeddings.openai import OpenAIEmbeddings
            embeddings = OpenAIEmbeddings()
            sec_result = embeddings.embed_documents(self.texts[:nsec])
            with open(self.embd_path, 'wb') as file:
                 pickle.dump(sec_result, file)
        else:
            with open(self.embd_path, 'rb') as file:
                sec_result = pickle.load(file)
        return(sec_result)
    
    def embd_paragraph(self, readOn=True, nsec=2):
        import pickle
        
        self.get_sections()
        if nsec==-1:
            nsec = len(self.ids)+1
            
        paragraphs = []
        ids = []
        for i in range(len(self.texts[:nsec])):
            paragraphs_i=  re.split(r'\s*\.\n', self.texts[i])
            paragraphs += paragraphs_i

            for pi, _ in enumerate(paragraphs_i):
                index_name = f"s{self.ids[i]}-p{str(pi+1)}" #d{self.doc}-
                ids.append(index_name)
        self.ids = ids

        # Get embeddigs
        if not readOn:
            from langchain.embeddings.openai import OpenAIEmbeddings
            embeddings = OpenAIEmbeddings()
            sec_result = embeddings.embed_documents(paragraphs)

            with open('data/embeddings_paragraph.pkl', 'wb') as file:
                 pickle.dump(sec_result, file)

        else:
            with open('data/embeddings_paragraph.pkl', 'rb') as file:
                sec_result = pickle.load(file)
        return(sec_result)

    def insert_vdb(self, embeddings):

        # initialize pinecone
        pinecone.init(
            api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
            environment=os.getenv("PINECONE_ENV"),  # next to api key in console
        )

        index_name = 'arxiv-' + '-'.join(self.doc_id.split('.'))
        # First, check if our index already exists. If it doesn't, we create it
        if index_name not in pinecone.list_indexes():
            # we create a new index
            pinecone.create_index(
              name=index_name,
              metric='cosine',
              dimension=1536  
        )
        # The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`
        docsearch = Pinecone.from_documents(self.texts[:2], embeddings, index_name=index_name)

        # if you already have an index, you can load it like this
        # docsearch = Pinecone.from_existing_index(index_name, embeddings)
        # query = "What did the president say about Ketanji Brown Jackson"
        # docs = docsearch.similarity_search(query)
    
    def vis_embd(self, emb):
        from sklearn.manifold import TSNE

        # Extract vectors and pars from embeddings
        vectors = np.asarray([np.asarray(x) for x in emb])
        pars = list(self.ids[:len(emb)])

        # Apply t-SNE for dimensionality reduction
        tsne = TSNE(n_components=2, random_state=42, perplexity=10)
        reduced_embeddings = tsne.fit_transform(vectors)

        # Create a scatter plot
        plt.figure(figsize=(10, 8))
        plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], alpha=0.5)

        # Annotate points with pars
        for i, par in enumerate(pars):
            plt.annotate(par, (reduced_embeddings[i, 0], reduced_embeddings[i, 1]))

        plt.title('t-SNE Visualization of Text Embeddings')
        plt.xlabel('Dimension 1')
        plt.ylabel('Dimension 2')
        plt.grid(True)



if __name__ == '__main__':

    paper = "1308.0850"
    pdf_src =PDFFileReader(Path(f"data/article_pdf/{paper}.pdf"))
    # pdf_src.batch_read_pdf('data/article_pdf/')
    pdf_src.read_pdf()

    vdb =Vectordb(f"data/article_pdf/txt/",  paper)

    # vdb.insert_db()
    # res = vdb.sql.select(paper)
    # for ri in res:
    #     print(ri)
    

    # # vis section embedding
    emb = vdb.embd_sec(readOn=False, nsec=-1)
    # vdb.vis_embd(emb)
    # plt.show()

    # vis paragraph embedding
    # emb = vdb.embd_paragraph(readOn=True, nsec=-1)
    # # vdb.vis_embd(emb)
    # plt.show()




