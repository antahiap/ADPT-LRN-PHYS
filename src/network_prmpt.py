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

        cntnt1 = self._read_from_graph(n1)
        cntnt2 = self._read_from_graph(n2)

        prompt= f'''
            Considerning the following papers. Give me list of similarities, maximum 5 rows, between these two Nodes in csv format with delimitar="\t" that the header is " dependent paper,source paper,similarity weight,content of relation".each column is formated as:

            - col=0: dependent paper, 
            - col=1: source paper, 
            - col=2: similarity weight, from 0 to 1, 
            - col=3: the content of each relation in max 5 words, dont say both papers, start with the verb.


            additionally, for each paper add the differences between them, that is store as,

            - col=0: the paper, 
            - col=1: None, 
            - col=2: importance weight, from 0 to 1, 
            - col=3: the content of each relation in max 5 words,  start with the verb.

            Node {n1}, 
            node(color={cntnt1['color']})
            text: {cntnt1['text']}

            Node {n2}, 
            node(color={cntnt2['color']})
            text: {cntnt2['text']}


        '''
        print('prmpt' ,n1, n2)


        result='''dependent paper\tsource paper\tsimilarity weight\tcontent of relation\n6\t28\t0.384\trecurrent neural networks\n6\t28\t0.317\tRNNs are a rich class\n6\t28\t0.221\tgenerate sequences\n6\t28\t0.182\tstore and access information\n6\tNone\t0.298\tglobal dependencies between input and output\n6\tNone\t0.254\tattention mechanisms\n6\tNone\t0.217\tcomputational efficiency through factorization tricks\n6\tNone\t0.185\tmodel architecture eschewing recurrence\n28\tNone\t0.298\tthe prediction network can be applied to real-valued data\n28\tNone\t0.254\tcondition its outputs on a short annotation sequence\n28\tNone\t0.217\tthe network itself is deterministic\n28\tNone\t0.185\tsynthesise and reconstitute the training data"
'''


        result, _, _ = self.api.call_api_single(prompt)
        network = self._to_network(result, cntnt1, cntnt2)
        return network
        # return None

    def _read_from_graph(self, n):

        cntnt = {}
        cntnt['color'] = self.Gd['nodes'][n]['color']
        cntnt['text'] = self.Gd['nodes'][n]['text']
        cntnt['label'] = self.Gd['nodes'][n]['label']
        cntnt['paper'] = self.Gd['nodes'][n]['paper']
        cntnt['ids'] = self.Gd['nodes'][n]['ids']

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
        source_node_label = f"{cn1['paper'][:5]} sec:{cn1['ids']}"
        target_node_label = f"{cn2['paper'][:5]} sec:{cn2['ids']}"

        source_node = f"{cn1['paper']} sec:{cn1['ids']} sec:{cn1['label']}"
        target_node = f"{cn2['paper']} sec:{cn2['ids']} sec:{cn1['label']}"

        G.add_node(source_node, color=cn1['color'], label=source_node_label, title = source_node)
        G.add_node(target_node, color=cn2['color'], label=target_node_label, title = target_node)

        G.add_edge(source_node, target_node)
        
        
        df = pd.read_csv(StringIO('\n'.join(result.split('\n')[1:])), header=None, sep='\t')

        try:
            for index, row in df.iterrows():  
                info = splt_txt(row[3], 10)
                w = row[2]

                if row[1] == 'None' :
                    n = self._read_from_graph(row[0])
                    paper_node = f"{n['paper']} sec:{n['ids']} sec:{n['label']}"

                    G.add_node(info, color=n['color'], label=info)
                    G.add_edge(paper_node, info, weight=w)

                else:
                    print(row[1])
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