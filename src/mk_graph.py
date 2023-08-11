

# def load_neo4j(self):
#     # Driver instantiation
#     driver = GraphDatabase.driver(
#         NEO4J_URI,
#         auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
#     )


import networkx as nx
import matplotlib.pyplot as plt
import json
import os

class GraphGeneration():
    def __init__(self, course_name):

        course_name = '_'.join(course_name.split(' '))

        self.frmt = 'pickle'
        self.path = 'data/'
        self.max_tokens=2000
        self.G_in= f'graph_{course_name}'
        self.G_out= f'graph_{course_name}'
        self.DG = nx.DiGraph()

    def mk_graph(self, tomain, topics):

        if not self.DG.has_node(domain):
            self.DG.add_node(domain)

        for topic in topics:
            if not self.DG.has_edge(domain, topic):
                self.DG.add_edge(domain, topic)


        # Draw the graph using NetworkX and Matplotlib
        # nx.draw(self.DG, with_labels=True)
        nx.draw(self.DG, with_labels=True, node_size=1000, node_color="skyblue", font_size=10, font_color="black", arrows=True)


        # Show the plot
        plt.show()

    def read_graph(self):
        in_path =os.path.join(self.path, f'{self.G_in}.{self.frmt}')
        nx.write_gpickle(self.DG, in_path)


    def write_graph(self):     
        out_path =os.path.join(self.path, f'{self.G_out}.{self.frmt}')
        nx.write_gpickle(self.DG, out_path)


# if __name__ == '__main__':



#     extrct_data_path = "data/data_sample.json"

#     # Open and read the JSON file
#     with open(extrct_data_path, "r") as json_file:
#         extract_data = json.load(json_file)

#     course = GraphGeneration('data science')

    # for di in extract_data:
    #     domain = di['domain']
    #     topics = di['topics']

    #     course.mk_graph(domain, topics)

    #     print(domain, topics)

import matplotlib.pyplot as plt

# Sample data
x_values = [1, 2, 3, 4, 5]
y_values = [10, 20, 15, 25, 30]

# Create a line plot
plt.plot(x_values, y_values, marker='o')

# Add labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Simple Line Plot')

# Display the plot
plt.show()
