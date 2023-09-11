import streamlit as st
from pyvis.network import Network
import networkx as nx
import tempfile

class PyvisNetworkComponent:
    def __init__(self, graph=None):
        self.graph = graph if graph else nx.Graph()
        self.net = Network()

    def add_edge(self, source, target, label=None):
        self.graph.add_edge(source, target, label=label)

    def render(self):
        for source, target, label in self.graph.edges(data="label"):
            self.net.add_node(source)
            self.net.add_node(target)
            self.net.add_edge(source, target, title=label)

        # Generate the HTML file for the network visualization
        tmp_dir = tempfile.mkdtemp()
        html_file_path = f"{tmp_dir}/network.html"
        self.net.show(html_file_path)

        # Display the HTML file in Streamlit using an iframe
        st.components.v1.html(open(html_file_path, 'r').read(), height=600, width=800)

# Usage example
if __name__ == "__main__":
    st.title("Custom Pyvis Network Component")

    # Create an instance of the PyvisNetworkComponent
    network_component = PyvisNetworkComponent()

    # Add edges to the network
    network_component.add_edge("A", "B", label="Edge AB")
    network_component.add_edge("B", "C", label="Edge BC")
    network_component.add_edge("C", "A", label="Edge CA")

    # Render the network component
    network_component.render()
