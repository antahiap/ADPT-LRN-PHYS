import networkx as nx
from pyvis.network import Network
from openai_api import OpenAIApi
from vis_network import VisNetwork


class DiffPaper():
    def __init__(self, cntnt1, cntnt2):
        self.api = OpenAIApi("gpt-3.5-turbo-16k")
        self.api.MAX_RETRIES = 1

        self.prompt= '''
            Considerning the following papers. Give me list of similarities between these two in csv format. col1: dependent paper, col2: source paper, col3: similarity weight, col4: the content of relation.

            paper1, 
            node(color={cntnt1.color})
            text: {cntnt1.text}

            paper2, 
            node(color={cntnt2.color})
            text: {cntnt2.text}
        '''


if __name__ == '__main__':


    src_path = "data/article_pdf/txt/"
    papers = ["1706.03762", "1308.0850"]

    g = VisGraph()
    g.get_embd(src_path, papers)
    source_code = g.grph_embd(.83)

    cntn1 = {
        color: 
        text:
    }

    diff = DiffPaper()
