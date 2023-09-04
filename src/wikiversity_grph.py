import requests
import json
import re
import networkx as nx
import os
import matplotlib.pyplot as plt
from neo4j import GraphDatabase

from dotenv import load_dotenv
load_dotenv()

class Wikiversity():
    def __init__(self, abb, category, no):
        # init
        self.abb = abb
        self.category = category
        self.no_page = no
        self.file_path = f"data/wiki_link_{abb}_{no}.json"
        self.node_prop = {}

        self.skip_list = ['File', 'Image', 'user', 'User talk', 'fr', 'b', 'cs','de','el','es','fi','it','ja','pt','ru','sv', 'ro', 'Help', 'User', 'image', 'ar', 'Media', 'English language']

        opt2nd = ['link', 'wikt']
        self.skip_list += opt2nd

        self.not_extnd_list = ['w', '/', 'Category:Category name', 'School:{{PAGENAME}}', 'Portal:{{BASEPAGENAME}}','Category:{{ROOTNAME}}/' ] + self.skip_list
        self.portal_list=[]


        if os.path.isfile(self.file_path):
            with open(self.file_path, "r") as json_file:
                data = json.load(json_file)

            # web scrawl
            self.semantic = data['semantic']
            self.pages = data['pages']
            self.links = data['links']
        else:
            self.semantic = [] 
            self.pages = {}
            self.links = {}


        # Graph
        self.DG = nx.Graph()

        # for s in self.semantic:
        #     if self.skipLink(s):
        #         # if len(s) == 6:
        #         print(s)

    def skipLink(self, title):
        for listi in self.skip_list:
            if listi in title:
                return False
        return True

    def page_api(self, title, page_id=False):

        params = {
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "titles": title,
            "rvprop": "content",
        }

        response = requests.get(API_URL, params=params)
        data = response.json()


        if "query" in data and "pages" in data["query"]:
            if not page_id:
                page_id = next(iter(data["query"]["pages"]))  # Get the first (and only) 

            try:
                page_content = data["query"]["pages"][page_id]["revisions"][0]["*"]
            except KeyError:
                return None, None

        else:
            page_content ="Failed to fetch page content."

        return(page_content, page_id)

    def get_page_links(self, page_content, filter=False):
        # Use regex to find wikitext links
        wikitext_links = re.findall(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', page_content)

        # Filter portal
        if filter:
            filterd_links = [link for link in wikitext_links if link[0].startswith(f"{filter}:")]
            return(filterd_links)
        return(wikitext_links)

    def school_api(self):

        API_URL = "https://en.wikiversity.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "cmtitle": "Category:Schools",
            "cmlimit": 50,  # Limit the number of schools
        }

        response = requests.get(API_URL, params=params)
        data = response.json()

        if "query" in data and "categorymembers" in data["query"]:
            schools = data["query"]["categorymembers"]
            for school in schools:
                print("School Title:", school["title"])
                print("School Page ID:", school["pageid"])
                print("School URL:", "https://en.wikiversity.org/wiki/" + school["title"])
                print("-" * 50)
        else:
            print("Failed to fetch school list.")

    def get_semantics(self, links):
        for link in links:
            tag_list  = link[0].split(':')
            if len(tag_list) > 1:
                tag = tag_list[0]
                if not tag in self.semantic:
                    self.semantic.append(tag)

    def extend_walk(self, page_links):

        def not_start_with_list(input_string, string_list):
            for prefix in string_list:
                if input_string.startswith(prefix):
                    return False
            return True

        for page in page_links:
                
                title = page[0]
                con1 = (title not in self.portal_list)
                con2 = (title not in self.pages.values())
                con3 = not_start_with_list(title, self.not_extnd_list)

                if  con1 and con2 and con3:
                    self.portal_list.append(title)
                    print(f'Exten pages: {title}' )
                    self.page_crawl(title)
        
        self.write_json()

    def page_crawl(self, page_title):

        page_content, page_id = self.page_api(page_title)
        if not page_content:
            return
        page_links = self.get_page_links(page_content)
        self.get_semantics(page_links)

        # Write the wikitext to a file
        with open(f"data/wiki/{page_id}.txt", "w") as f:
            f.write(page_content)

        self.pages[page_id] = page_title
        self.links[page_title] = page_links
        # self.extend_walk(page_links)

    def catg_api(self):
        semantic = []
    # 
        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "cmtitle": self.category, 
            "apinprop": "subject",
            "cmlimit":self.no_page,
            # "aplimit": 100,  # Number of results per query
        }
        response = requests.get(API_URL, params=params)
        data = response.json()


        # getting with categories list
        if "query" in data and "categorymembers" in data["query"]:
            course_pages = data["query"]["categorymembers"]

            for page in course_pages:
                page_title = page["title"]
                if page_title in self.pages.values():
                    print(f'skip page: {page_title}, already exists.')
                    # self.extend_walk(self.links[page_title])
                    continue
                self.page_crawl(page_title)
        else:
            print(f"Failed to fetch {self.category} pages.")
        
        self.write_json()
    
    def  write_json(self):

        course_dic = {}
        course_dic['semantic'] = self.semantic
        course_dic['pages'] = self.pages
        course_dic['links'] = self.links

        json_file = json.dumps(course_dic, indent=2)
        with open(self.file_path, "w") as json_file:
            json.dump(course_dic, json_file)

    def mk_graph(self):
        def mk_node(node, ref):

            url = self.page_url(node, ref)          
            if check_url_exists(url):
                if not self.DG.has_node(node):
                    self.DG.add_node(node)
                self.node_prop[node] = {'url': url}
        
        def vis_graph():
            # Draw the graph using NetworkX and Matplotlib
            # nx.draw(self.DG, with_labels=True)
            pos = nx.kamada_kawai_layout(self.DG)
            pagerank_values = nx.pagerank(self.DG)
            node_sizes = [5e4 * pagerank_values[node] for node in self.DG.nodes()]

            fig = plt.figure(figsize=(20, 12)) 

            nx.draw(
                self.DG, with_labels=True, 
                node_size=node_sizes,
                node_color="skyblue", font_size=10, 
                font_color="black", arrows=True,
                pos=pos
                )

        print('-'*50)
        print(' MAKE GRAPH: ')

        mk_node(self.category, '')

        for page in self.links:
            for link in self.links[page]:
                page2 = link[0]
                # url = self.page_url(page2, page)
                
                if not page2=='' and self.skipLink(page2) and page2 !=page:
                    # if check_url_exists(url):

                        mk_node(page, self.category)            
                        mk_node(page2, page)

                        if not self.DG.has_edge(page, page2):
                            self.DG.add_edge(page, page2)
                        if not self.DG.has_edge(page, self.category):
                            self.DG.add_edge(self.category, page)
                    # else:
                    #     print(page, page2)
                    #     input(f'{url} not available')
        # vis_graph()
        # input(nx.is_connected(self.DG))
        # plt.show()
        nx.set_node_attributes(self.DG, self.node_prop)
        print(' DONE! ')

    def page_url(self, page, ref):
        url_page = "%20".join(page.strip().split(' '))
        if page.startswith("/"):
            url = BASE_URL + ref + url_page[:-1]     
        else:          
            url = BASE_URL + url_page
        return(url)

    def nx_g_to_neo4j(self, clean):

        print('-'*50)
        print(' LOAD NEO4J: ')
        username = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD_LOCAL")
        uri = os.getenv('NEO4J_URI_LOCAL')
        
        driver = GraphDatabase.driver(
            uri,
            auth=(username, password)
        )
        clean_query = "MATCH (n) DETACH DELETE n"
        # Clean the database (delete existing data)
        if clean:
            with driver.session() as session:
                session.run(clean_query)

        # Iterate through NetworkX nodes and create corresponding Neo4j nodes
        with driver.session() as session:
            for node, prop in self.DG.nodes(data=True):

                query = (
                    "MERGE (n:Node {name: $name})"
                    "SET n+= $properties "
                    "SET n:Page "
                    "REMOVE n:Node "
                )
                # query = "CREATE (:Node {name: $name})"
                session.run(query, name=node, properties=prop)
                # session.run(query)

        # Iterate through NetworkX edges and create corresponding Neo4j relationships
        with driver.session() as session:
            for edge in self.DG.edges:
                query = """
                MATCH (a:Page {name: $source}), (b:Page {name: $target})
                CREATE (a)-[:CONNECTED]->(b)
                """
                session.run(query, source=edge[0], target=edge[1])

        # Close the Neo4j driver connection
        driver.close()


def check_url_exists(url):
    response = requests.get(url)
    return response.status_code == 200


if __name__ == '__main__':
    API_URL = "https://en.wikiversity.org/w/api.php/"
    BASE_URL = "https://en.wikiversity.org/wiki/"

    wiki = Wikiversity('phys', "Category:Physics", 1000)
    # wiki = Wikiversity('phys-sc', "Category:Physical sciences", 400)
    wiki.catg_api()  #"Category:Wikiversity schools",

    wiki.mk_graph()
    wiki.nx_g_to_neo4j(clean=False)
