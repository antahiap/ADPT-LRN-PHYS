import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import networkx as nx

import app.style as style
from sklearn.metrics.pairwise import cosine_similarity

import embd_pdf_to_vdb as embd


class VisNetwork():
    def __init__(self):
        self.pyvis_path = 'src/app/graph.html'
              
        self.titles = []
        self.ids = []
        self.texts = []
        self.emb = []
        self.colors = []
        self.papers = []

    def grph_embd(self, similarity_threshold, src_path, papers):

        def calculate_similarity(par1, par2):
            embedding1 = self.emb[par1]
            embedding2 = self.emb[par2]
            similarity = cosine_similarity([embedding1], [embedding2])[0][0]
            return similarity      

        self._get_embd(src_path, papers)
        G = nx.Graph()

        words = self.titles

        for k in range(len(words)):
            label  = '\n'.join(self.titles[k].split(' '))

            G.add_node(
                k, 
                label=self.titles[k][:5], #
                title= f'{self.papers[k]} \n\n {self.ids[k]}{self.titles[k]}',
                text=self.texts[k],
                ids=self.ids[k],
                font='25px arial black',
                color=self.colors[k],
                paper = self.papers[k],
                )
            
        for i in G.nodes():
            for j in G.nodes():
                if  i == j:
                    continue
                similarity = calculate_similarity(i, j)

                if similarity > similarity_threshold:
                    G.add_edge(i, j, width=similarity)

        return G

    def json_network(self, th, src_path, papers, G=None):

        if not G:
            G = self.grph_embd(th, src_path, papers)

        nodes = []
        edges = []   
        for node_id, node_attrs in G.nodes(data=True):
            nodes.append({"id": node_id, **node_attrs})

        for src, dst, edge_attrs in G.edges(data=True):
            edges.append({"from": src, "to": dst, **edge_attrs})

        graph_data = {"nodes": nodes, "edges": edges}
        
        encoded_dict = {}
        for key, value in graph_data.items():
            if isinstance(value, str):
                encoded_dict[key] = value.encode('utf-8')
            else:
                encoded_dict[key] = value


        return encoded_dict

    def create_network(self, th, src_path, papers):  
        
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

        color = ['#e41a1c','#377eb8','#4daf4a','#ff7f00','#ffff33','#a65628','#f781bf',  '#984ea3'      ]


        for i, paper in enumerate(papers):
            vdb = embd.Vectordb(src_path, paper)
            self.emb += vdb.embd_sec(readOn=True, nsec=-1)
            if vdb.paper.startswith('\n'):
                vdb.paper = vdb.paper[1:]
                  
            self.titles += vdb.titles
            self.ids += vdb.ids
            self.texts += vdb.texts
            self.colors += [color[i] for x in vdb.ids]
            self.papers += [vdb.paper for x in vdb.ids]


def main():

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

