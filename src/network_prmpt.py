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
            Let us consider the following papers as nodes {n1} and {n2}. I want to know how they are similar and how they differ. For the similarities, give me a list of the similarities, max 5 rows, between these two nodes. For differences, list the differences between them, a maximum of 4  for each node {n1} and {n2}.
                    
            Output format: in csv format with delimitar="\t" that the header is " dependent paper\t source paper\t importance weight\t content of the relation". eThe columns content is as follows::

            - col=0: source node, 
            - col=1: target node if similar and None if different
            - col=2: importance weight, from 0.5 to 1, 
            - col=3: the content of each relation in max 5 words, do not say both papers, start with the verb, and don't say the node number.


            Node {n1}, 
            node(color={cntnt1['color']})
            text: {cntnt1['text']}

            Node {n2}, 
            node(color={cntnt2['color']})
            text: {cntnt2['text']}


        '''
        print('prmpt' ,n1, n2)


        result='''dependent paper\tsource paper\tsimilarity weight\tcontent of relation\n6\t45\t0.7\trecurrent neural networks\n6\t45\t0.6\tlong short-term memory\n6\t45\t0.5\tstate of the art approaches\n6\t45\t0.4\tsequence modeling and transduction problems\n6\t45\t0.3\tlanguage modeling\n\n6\tNone\t0.8\tfactor computation along the symbol positions\n6\tNone\t0.7\tinherently sequential nature of computation\n6\tNone\t0.6\tsignificant improvements in computational efficiency\n6\tNone\t0.5\tfactorization tricks\n\n45\tNone\t0.9\tgenerate complex sequences with long-range structure\n45\tNone\t0.8\tpredicting one data point at a time\n45\tNone\t0.7\tdiscrete data for text\n45\tNone\t0.6\treal-valued data for online handwriting
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

        def trans_color(html_color, alpha):
            alpha = min(255, max(0, alpha))
            html_color = html_color.lstrip('#')

            # Extract the RGB components (assuming it's in #RRGGBB format)
            red = int(html_color[0:2], 16)
            green = int(html_color[2:4], 16)
            blue = int(html_color[4:6], 16)

            rgba_color = f"rgba({red}, {green}, {blue}, {alpha/255:.2f})"

            return rgba_color

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

        source_node = f"{cn1['paper']} sec:{cn1['ids']} {cn1['label']}"
        target_node = f"{cn2['paper']} sec:{cn2['ids']} {cn2['label']}"

        G.add_node(source_node, color=cn1['color'], label=source_node_label, title = source_node)
        G.add_node(target_node, color=cn2['color'], label=target_node_label, title = target_node)

        G.add_edge(source_node, target_node)
        
        
        df = pd.read_csv(StringIO('\n'.join(result.split('\n')[1:])), header=None, sep='\t')
        print(df)

        try:
            for index, row in df.iterrows(): 
                info = splt_txt(row[3], 15)
                w = row[2]

                if row[1] == 'None' :
                    try:
                        n = self._read_from_graph(int(float(row[0])))
                        paper_node = f"{n['paper']} sec:{n['ids']} {n['label']}"
                        color = trans_color(n['color'], 150)

                        G.add_node(info, color=color, label=info)
                        G.add_edge(paper_node, info, weight=w)
                    except ValueError:
                        continue

                else:
                    if not info in G.nodes():
                        G.add_node(info, color='#B2BEB5', label=info)
                    G.add_edge(source_node, info, weight=w)
                    G.add_edge(info, target_node, weight=w)

        except KeyError:
            print('issue to iterate')
        return(G)

        layout = nx.spring_layout(G)

        # Draw the graph using Matplotlib
        nx.draw(G, layout, with_labels=True, node_color='skyblue', font_size=10, node_size=500)
        plt.show()





if __name__ == '__main__':


    src_path = "data/article_pdf/txt/"
    papers = [ "2308.16622", "1706.03762", "1308.0850", "2308.16441"]


    th = .5
    g = VisNetwork()
    G_data = g.json_network(th, src_path, papers)
    src, dst = 6,45
    nt_prmpt = NetworkPrmpt(G_data)
    nt_prmpt.diff_paper(src, dst)