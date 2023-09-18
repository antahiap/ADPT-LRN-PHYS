import streamlit as st
import networkx as nx

import app.style as style
from sklearn.metrics.pairwise import cosine_similarity

import embd_pdf_to_vdb as embd
import time
import numpy as np


class VisNetwork():
    def __init__(self):
        self.pyvis_path = 'src/app/graph.html'
              
        self.titles = []
        self.arxiv_id = []
        self.ids = []
        self.texts = []
        self.emb = []
        self.colors = []
        self.papers = []

    def grph_embd(self, similarity_threshold, src_path, papers):

        def set_attributes(G):

            if not len(G.edges()) == 0:
                rank = nx.pagerank(G)
                scale = 100/(max(rank.values()) **2)
                scaled_rank_nl = {node: score ** 2 * scale for node, score in rank.items()}

                nx.set_node_attributes(G, scaled_rank_nl, name='size')
            
            return(G)
        
        start_time = time.time()
        self._get_embd(src_path, papers)
        t2 = time.time()
        print(f'embedding: {t2 - start_time}')

        G = nx.Graph()

        t4 = time.time()
        # Similarity
        embeddings_norm = self.emb / np.linalg.norm(self.emb, axis=1, keepdims=True)
        cosine_similarity_matrix = np.dot(embeddings_norm, embeddings_norm.T)
        adj_matrix = (cosine_similarity_matrix >= similarity_threshold).astype(int)

        num_nodes = adj_matrix.shape[0]
        edge_list = []
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if adj_matrix[i, j] == 1:
                    edge_list.append((i, j))
        
        G.add_edges_from(edge_list)
        G = set_attributes(G)


        t6 = time.time()
        print(f'edges adj: {t6- t4}')

        
        t3 = time.time()
        print(f'make graph: {t3- t2}')
        print('--------------------------------------------')

        return G

    def json_network(self, th, src_path, papers, G=None):

        if not G:
            G = self.grph_embd(th, src_path, papers)
        
        nodes = []
        edges = []
        t0 = time.time()   
        for node_id, node_attrs in G.nodes(data=True):
            try:
                info = {
                "color": self.colors[node_id],
                "label": self.titles[node_id][:12],
                "title": f'{self.papers[node_id]} \n\n {self.ids[node_id]} {self.titles[node_id]}',
                "label_full":self.titles[node_id],
                "text":self.texts[node_id],
                "ids":self.ids[node_id],
                "font":'35px arial black',
                "paper": self.papers[node_id],
                "arxiv_id": self.arxiv_id[node_id]
                }
            except:
                info = {}

            nodes.append({
                "id": node_id, 
                **node_attrs,
                "shape": 'dot',
                **info
                })

        for src, dst, edge_attrs in G.edges(data=True):
            edges.append({"from": src, "to": dst, **edge_attrs})

        graph_data = {"nodes": nodes, "edges": edges}
        
        encoded_dict = {}
        for key, value in graph_data.items():
            if isinstance(value, str):
                encoded_dict[key] = value.encode('utf-8')
            else:
                encoded_dict[key] = value
        t1 = time.time()
        print(f'convert graph to json: {t1-t0}')
        print('--------------------------------------------')
        return encoded_dict

    def create_network(self, th, src_path, papers):  
        from pyvis.network import Network
        
        G = self.grph_embd(th, src_path, papers)

        x = f'{style.gw}px'
        y = f'{style.gh}px'

        nt = Network(x, y, notebook=True)
        nt.from_nx(G)


        nt.show(self.pyvis_path)

        with open(self.pyvis_path, 'r', encoding='utf-8') as HtmlFile:
            self.source_code = HtmlFile.read() 

        return(self.source_code)

    def _get_embd(self, src_path, papers):

        color = ['#e41a1c','#377eb8','#4daf4a','#ff7f00','#ffff33','#a65628','#f781bf',  '#984ea3', '#008000', '#0000FF', '#FFA500', '#800080', '#A52A2A', '#00FFFF', '#008080', '#FFD700', '#4B0082', '#800000', '#808000', '#708090', '#FF6F61', '#006400', '#9932CC', '#FFFF00',     ]


        for i, paper in enumerate(papers):
            print('-------------------')
            print(paper)
            vdb = embd.Vectordb(src_path, paper)
            self.emb += vdb.embd_sec(readOn=True, nsec=-1)
            if vdb.paper.startswith('\n'):
                vdb.paper = vdb.paper[1:]
                  
            self.titles += vdb.titles
            self.ids += vdb.ids
            self.texts += vdb.texts
            self.colors += [color[i] for x in vdb.ids]
            self.papers += [vdb.paper for x in vdb.ids]
            self.arxiv_id += [vdb.arxiv_id for x in vdb.ids]


def main():
    import streamlit.components.v1 as components

    papers = ["1706.03762", "1308.0850"]
    src_path = "data/article_pdf/txt/"


    st.set_page_config(layout="wide")
    g = VisNetwork()
    th = st.slider('Simillarity threshhold', 0.7, 1.0, .85)

        
    # Create the network graph
    source_code = g.create_network(th, src_path, papers)
    st.title("Network Visualization in Streamlit")
    components.html(source_code, height = style.gh, width=style.gw+style.txtw)
   
    expl_edge = st.button("Explode edge", type="primary", key="explodeEdge")
    if expl_edge:
        print('make new graph')
        g = VisNetwork()
        th =.9
        source_code = g.create_network(th, src_path, papers)
        components.html(source_code, height = style.gh, width=style.gw+style.txtw)




if __name__ == "__main__":
    main()

