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
        self.Gd = g_data

    def diff_paper(self, n1, n2):
        print('prmpt' ,n1, n2)

        cntnt1 = self._read_from_graph(self.Gd, n1)
        cntnt2 = self._read_from_graph(self.Gd, n2)

        prompt= f'''
            Considerning the following papers. Give me list of similarities, maximum 5 rows, between these two Nodes in csv format with delimitar="\t" that the header is " dependent paper,source paper,similarity weight,content of relation".each column is formated as:

            - col=0: dependent paper, 
            - col=1: source paper, 
            - col=2: similarity weight, from 0 to 1, 
            - col=3: the content of each relation in max 5 words, dont say both papers, start with the werb.

            Node {n1}, 
            node(color={cntnt1['color']})
            text: {cntnt1['text']}

            Node {n2}, 
            node(color={cntnt2['color']})
            text: {cntnt2['text']}
        '''


        result='''dependent paper	source paper	similarity weight	content of relation
0	39	0.8	recurrent neural networks
0	39	0.6	long short-term memory
0	39	0.5	sequence modeling
0	39	0.7	generate complex sequences
0	39	0.9	handwriting synthesis
'''


        # result, _, _ = self.api.call_api_single(prompt)
        print(type(result))
        # print(cntnt1['color'], cntnt2['color'])
        network = self._to_network(result, cntnt1, cntnt2)
        return network
        # return None

    def _read_from_graph(self, gd, n):

        cntnt = {}
        cntnt['color'] = gd['nodes'][n]['color']
        cntnt['text'] = gd['nodes'][n]['text']
        cntnt['label'] = gd['nodes'][n]['label']
        cntnt['paper'] = gd['nodes'][n]['paper']

        return cntnt

    def _to_network(self, result, cn1, cn2):

        def splt_txt(txt, value):
            words = txt.split()
            lines = []
            current_line = ""

            for word in words:
                if len(current_line) + len(word) + 1 <= value:
                    if current_line:
                        current_line += " "
                    current_line += word
                else:
                    lines.append(current_line)
                    current_line = word

            if current_line:
                lines.append(current_line)

            txt_cut = "\n".join(lines)
            return(txt_cut)

        G =nx.Graph()
        source_node_label = f"{cn1['paper'][:5]} sec:{cn1['label'][:5]}"
        target_node_label = f"{cn2['paper'][:5]} sec:{cn2['label'][:5]}"

        source_node = splt_txt(f"{cn1['paper']} sec:{cn1['label']}", 10)
        target_node = splt_txt(f"{cn2['paper']} sec:{cn2['label']}", 10)

        G.add_node(source_node, color=cn1['color'], label=source_node_label, title = source_node)
        G.add_node(target_node, color=cn2['color'], label=target_node_label, title = target_node)

        G.add_edge(source_node, target_node)
        
        
        df = pd.read_csv(StringIO('\n'.join(result.split('\n')[1:])), header=None, sep='\t')
        print(df)

        try:
            for index, row in df.iterrows():  
                info = splt_txt(row[3], 10)
                w = row[2]
                if not info in G.nodes():
                    G.add_node(info, color='#B2BEB5', label=info)
                G.add_edge(source_node, info, weight=w)
                G.add_edge(info, target_node, weight=w)

        except KeyError:
            print('issue to iterate')
        return(G)

        # layout = nx.spring_layout(G)

        # Draw the graph using Matplotlib
        # nx.draw(G, layout, with_labels=True, node_color='skyblue', font_size=10, node_size=500)
        # plt.show()





if __name__ == '__main__':


    src_path = "data/article_pdf/txt/"
    papers = ["1706.03762", "1308.0850"]


    th = .5
    g = VisNetwork()
    G_data = g.json_network(th, src_path, papers)
    src, dst = 3,2
    nt_prmpt = NetworkPrmpt(G_data)
    nt_prmpt.diff_paper(src, dst)