import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import matplotlib.pyplot as plt
import networkx as nx
import re 
from app.action import node_onclick
import app.style as style
from app.div import network_text
from sklearn.metrics.pairwise import cosine_similarity

import embd_pdf_to_vdb as embd


class VisGraph():
    def __init__(self):
        self.pyvis_path = 'src/app/graph.html'
              
        self.titles = []
        self.ids = []
        self.texts = []
        self.emb = []
        self.colors = []

    def grph_embd(self, emb, similarity_threshold):

        def calculate_similarity(par1, par2):
            embedding1 = emb[par1]
            embedding2 = emb[par2]
            similarity = cosine_similarity([embedding1], [embedding2])[0][0]
            return similarity
        
        G = nx.Graph()

        words = self.titles

        for i in range(len(words)):
            label  = '\n'.join(self.titles[i].split(' '))

            G.add_node(
                i, 
                label=self.ids[i], #self.titles[i], #format_txt(self.titles[i], 10),
                title= self.titles[i],
                text=self.texts[i],
                ids=self.ids[i],
                font='25px arial black',
                color=self.colors[i]
                )
            
        for i in range(len(words)):
            for j in range(i + 1, len(words)):
                word1, word2 = i, j
                similarity = calculate_similarity(i, j)

                if similarity > similarity_threshold:
                    G.add_edge(word1, word2, weight=similarity)

        # pos = nx.spring_layout(G, seed=42)  # Layout for visualization
        # edge_labels = nx.get_edge_attributes(G, 'weight')

        # nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10)
        # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        # plt.show()
        return G

    def create_network(self, th):  
        G = self.grph_embd(self.emb, th)

        x = f'{style.gw}px'
        y = f'{style.gh}px'

        nt = Network(x, y, notebook=True)
        nt.from_nx(G)

        nt.show(self.pyvis_path)

        with open(self.pyvis_path, 'r', encoding='utf-8') as HtmlFile:
            self.source_code = HtmlFile.read() 
        self.custom_network()

        return(self.source_code)

    def custom_network(self):

        patterns = [ 
            r'\bdrawGraph\(\);',
            r'<style type="text/css">.*?</style>',
            r'<div class="card" style="width: 100%">.*?</div>'
        ]
        replacements = [
            node_onclick,
            style.network_css, 
            network_text
        ]

        for i, pattern in enumerate(patterns):
            self.source_code = re.sub(pattern, replacements[i], self.source_code,  flags=re.DOTALL )

    def get_embd(self, src_path, papers):

        def random_html_color(n):
            import random

            if n < 1 or n > 6:
                raise ValueError("Invalid length for HTML color code. Length must be between 1 and 6 (inclusive).")

            # Generate random values for the color components (R, G, B)
            color_values = [random.randint(0, 15) for _ in range(n)]

            # Convert the list of values to a hexadecimal string and prepend '#'
            color_code = "#{:0{length}X}".format(int("".join(map(str, color_values)), 16), length=n)

            return color_code

        color = [ '#FF0000',   '#00FF00',   '#0000FF',   '#FFFF00',   '#00FFFF',   '#FF00FF',   '#000000',   '#FFFFFF',   '#808080',   '#FFA500']
        for i, paper in enumerate(papers):
            vdb = embd.Vectordb(src_path, paper)
            self.emb += vdb.embd_sec(readOn=True, nsec=-1)
                  
            self.titles += vdb.titles
            self.ids += vdb.ids
            self.texts += vdb.texts
            self.colors += [color[i] for x in self.ids]


def main():


    papers = ["1706.03762"]
    src_path = "data/article_pdf/txt/"


    st.set_page_config(layout="wide")
    g = VisGraph()
    th = st.slider('Simillarity threshhold', 0.7, 1.0, .85)

        
    # Create the network graph
    papers = ["1706.03762", "1308.0850"]

    # source_code = g.multi_paper_network(th, papers)
    g.get_embd(src_path, papers)
    source_code = g.create_network(th)
    # print(source_code)
    st.title("Network Visualization in Streamlit")


    components.html(source_code, height = style.gh, width=style.gw+style.txtw)


    
    # Display the network graph in Streamlit
    # st.write(nt)

    # fig, ax = plt.subplots()
    # pos = nx.kamada_kawai_layout(G)
    # nx.draw(G,pos, with_labels=True)
    # st.pyplot(fig)



if __name__ == "__main__":
    main()


# create_network(G)
# plt.show()


# vis paragraph embedding
# emb = vdb.embd_paragraph(readOn=True, nsec=-1)
# # vdb.vis_embd(emb)
# vdb.grph_embd(emb)
# plt.show()
