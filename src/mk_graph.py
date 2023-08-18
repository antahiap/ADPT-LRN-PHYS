

# def load_neo4j(self):
#     # Driver instantiation
#     driver = GraphDatabase.driver(
#         NEO4J_URI,
#         auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
#     )


import networkx as nx
import matplotlib.pyplot as plt
from neo4j import GraphDatabase
from tqdm import tqdm
import json
import os


from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file


class GraphGeneration():
    def __init__(self, course_name):

        course_name = '_'.join(course_name.split(' '))

        self.frmt = 'gml'
        self.path = 'data/'
        self.max_tokens=2000
        self.G_in= f'graph_{course_name}'
        self.G_out= f'graph_{course_name}'
        self.DG = nx.DiGraph()

    def mk_graph(self, domain, topics):

        if not self.DG.has_node(domain):
            self.DG.add_node(domain)

        for topic in topics:
            if not self.DG.has_edge(domain, topic):
                self.DG.add_edge(domain, topic)

    def vis_graph(self):
        # Draw the graph using NetworkX and Matplotlib
        # nx.draw(self.DG, with_labels=True)
        pos = nx.kamada_kawai_layout(self.DG)
        pagerank_values = nx.pagerank(self.DG)
        node_sizes = [5e5 * pagerank_values[node] for node in self.DG.nodes()]

        nx.draw(
            self.DG, with_labels=True, 
            node_size=node_sizes,
            node_color="skyblue", font_size=10, 
            font_color="black", arrows=True,
            pos=pos
            )


    def read_graph(self):
        in_path =os.path.join(self.path, f'{self.G_in}.{self.frmt}')
        self.GD = nx.read_gml(in_path)


    def write_graph(self):     
        out_path =os.path.join(self.path, f'{self.G_out}.{self.frmt}')
        nx.write_gml(self.DG, out_path)


    def nx_g_to_neo4j(self):

        username = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")
        uri = os.getenv('NEO4J_URI')
        
        driver = GraphDatabase.driver(
            uri,
            auth=(username, password)
        )

        # Iterate through NetworkX nodes and create corresponding Neo4j nodes
        with driver.session() as session:
            for node in self.DG.nodes:
                query = "CREATE (:Node {name: $name})"
                session.run(query, name=node)

        # Iterate through NetworkX edges and create corresponding Neo4j relationships
        with driver.session() as session:
            for edge in self.DG.edges:
                query = """
                MATCH (a:Node {name: $source}), (b:Node {name: $target})
                CREATE (a)-[:CONNECTED]->(b)
                """
                session.run(query, source=edge[0], target=edge[1])

        # Close the Neo4j driver connection
        driver.close()
    

    def nx_to_cytoscape(self, fName='cytoscape_vis.json'):
        
        out_path =os.path.join(self.path, fName)

        cytoscape_data = {
            'nodes': [],
            'edges': []
        }

        for node in self.DG.nodes():
            cytoscape_data['nodes'].append({
                'data': {
                    'id': str(node)
                    # 'name': str()
                    }})

        for edge in self.DG.edges():
            source, target = edge
            cytoscape_data['edges'].append({'data': {'source': str(source), 'target': str(target)}})

        with open(out_path, "w") as json_file:
            json.dump(cytoscape_data, json_file)




if __name__ == '__main__':



    extrct_data_path = "data/data_sample.json"
    extrct_data_path = "data/datascience-topics.json"

    # Open and read the JSON file
    with open(extrct_data_path, "r") as json_file:
        extract_data = json.load(json_file)

    course = GraphGeneration('data science')
    # course.read_graph()
    # course.vis_graph()
    # plt.show()


    for di in tqdm(extract_data):
        domain = di['domain']
        topics = di['topics']

        course.mk_graph(domain, topics)

    # course.write_graph()
    course.read_graph()
    course.nx_to_cytoscape()

    # Show the plot
    # course.vis_graph()
    # plt.show()

    # course.nx_g_to_neo4j()
