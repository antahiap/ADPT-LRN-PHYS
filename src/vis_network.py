import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import matplotlib.pyplot as plt
import networkx as nx
import re 
from app.action import node_onclick
from app.style import network_css
from app.div import network_text

import embd_pdf_to_vdb as embd


paper = "1706.03762"
vdb = embd.Vectordb(f"data/article_pdf/txt/",  paper)


def main():
    st.title("Network Visualization in Streamlit")
    
    # Create the network graph
    emb = vdb.embd_sec(readOn=True, nsec=-1)
    th = st.slider('Simillarity threshhold', 0.7, 1.0, .9)
    G = vdb.grph_embd(emb, th)

    nt = Network("500px", "500px",notebook=True,heading='')
    nt.from_nx(G)
    

    nt.show('test.html')

    HtmlFile = open("test.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 


    patterns = [ 
        r'\bdrawGraph\(\);',
        r'<style type="text/css">.*?</style>',
        r'<div class="card" style="width: 100%">.*?</div>'
    ]
    replacements = [
        node_onclick,
        network_css, 
        network_text
    ]
    
    for i, pattern in enumerate(patterns):
        source_code = re.sub(pattern, replacements[i], source_code,  flags=re.DOTALL )
        

    components.html(source_code, height = 500,width=1000)


    
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
