from matplotlib import pyplot as plt
import networkx as nx
import pandas as pd
from io import StringIO

from pyvis.network import Network
from openai_api import OpenAIApi
from network_vis import VisNetwork


class NetworkPrmpt():
    def __init__(self, g_data):
        self.api = OpenAIApi("gpt-3.5-turbo-16k")
        self.api.MAX_RETRIES = 1
        self.Gd = g_data

    def diff_paper(self, n1, n2):

        cntnt1 = self._read_from_graph(self.Gd, n1)
        cntnt2 = self._read_from_graph(self.Gd, n2)

        prompt= f'''
            Considerning the following papers. Give me list of similarities between these two in csv format zjat os as:
            - col1: dependent paper, 
            - col2: source paper, 
            - col3: similarity weight, from 0 to 1, 
            - col4: the content of each relation in max 5 words, dont say both papers, start with the werb.

            Node {n1}, 
            node(color={cntnt1['color']})
            text: {cntnt1['text']}

            Node {n2}, 
            node(color={cntnt2['color']})
            text: {cntnt2['text']}
        '''

        result = '''
        Node 19,Node 26,0.072,"The Transformer generalizes well"
        Node 19,Node 26,0.083,"experiments on English constituency parsing"
        Node 19,Node 26,0.078,"RNN sequence-to-sequence models"
        Node 19,Node 26,0.097,"trained a 4-layer transformer"
        Node 19,Node 26,0.060,"vocabulary of 16K tokens"
        Node 19,Node 26,0.073,"trained it in a semi-supervised setting"
        Node 19,Node 26,0.057,"small number of experiments"
        Node 19,Node 26,0.073,"dropout, attention and residual"
        Node 19,Node 26,0.083,"learning rates and beam size"
        Node 19,Node 26,0.071,"the Transformer outperforms the Berkeley-Parser"
        Node 19,Node 26,0.075,"small text corpus"
        Node 19,Node 26,0.065,"language modelling benchmark"
        Node 19,Node 26,0.066,"network architecture was a single hidden layer"
        Node 19,Node 26,0.083,"character-level network"
        Node 19,Node 26,0.084,"performance of word and character-level LSTM predictors"
        Node 19,Node 26,0.082,"number of weights in total"
        Node 19,Node 26,0.091,"use of weight noise for regularisation"
        Node 19,Node 26,0.070,"dynamic evaluation"
        Node 19,Node 26,0.063,"regularisation is considerably faster"
        Node 19,Node 26,0.080,"word-level RNN performed better"
        Node 19,Node 26,0.083,"results compare favourably with those collected"
        Node 19,Node 26,0.071,"beneft of dynamic evaluation"
        Node 19,Node 26,0.082,"LSTM is better at rapidly adapting"

        
        '''

        # result, _, _ = self.api.call_api(prompt)
        print(result)
        return self._to_network(result, cntnt1, cntnt2)

    def _read_from_graph(self, gd, n):

        cntnt = {}
        cntnt['color'] = gd['nodes'][n]['color']
        cntnt['text'] = gd['nodes'][n]['text']

        return cntnt

    def _to_network(self, input, cn1, cn2):

        df = pd.read_csv(StringIO(input), header=None)
        G =nx.Graph()

        for index, row in df.iterrows():
            source_node = row[0]
            target_node = row[1]
            info = row[3]
            w = row[2]
            if index == 0:
                G.add_node(source_node, color=cn1['color'])
                G.add_node(target_node, color=cn2['color'])
            if not info in G.nodes():
                G.add_node(info)

            G.add_edge(source_node, info, weight=w)
            G.add_edge(info, target_node, weight=w)
            

        # layout = nx.spring_layout(G)

        # # Draw the graph using Matplotlib
        # nx.draw(G, layout, with_labels=True, node_color='skyblue', font_size=10, node_size=500)
        # plt.show()
        return(G)



if __name__ == '__main__':


    src_path = "data/article_pdf/txt/"
    papers = ["1706.03762", "1308.0850"]


    th = .5
    g = VisNetwork()
    G_data = g.json_network(th, src_path, papers)
    src, dst = 19, 26
    nt_prmpt = NetworkPrmpt(G_data)
    nt_prmpt.diff_paper(src, dst)