import requests
import json

# Construct the API query URL
base_url = "https://en.wikiversity.org/w/api.php"
action = "query"
format_type = "json"
list_type = "categorymembers"  # You can change this to other available list types
category = "Category:Science"
page_title = "Category:Science"



params = {
    "action": action,
    "format": format_type,
    "list": list_type,
    "cmtitle": category,
    "apinprop": "subject",
    "page": page_title,
    "prop": "text|links",
    "aplimit": 100,  # Number of results per query
}

# Make the API request
response = requests.get(base_url, params=params)
data = response.json()

# Process and print the page titles
if "parse" in data:
    page_content = data["parse"]["text"]["*"]
    links = data["parse"]["links"]
    
    # Print the page content
    print("Page Content:")
    print(page_content)
    
    # Print the list of links
    print("Links:")
    for link in links:
        print(link["*"])
else:
    print("Error fetching data from the API.")

        # j_prmt = json.dumps(page, indent=2)
        # with open('data/wiki_data.json', "a") as f:
            # f.write(j_prmt)
            # f.write(",")
