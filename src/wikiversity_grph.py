import requests
import json

# Construct the API query URL
base_url = "https://en.wikiversity.org/w/api.php"
action = "query"
format_type = "json"
list_type = "categorymembers"  # You can change this to other available list types
category = "Category:*"

params = {
    "action": action,
    "format": format_type,
    "list": list_type,
    "cmtitle": category,
    "apinprop": "subject",
    "aplimit": 100,  # Number of results per query
}

# Make the API request
response = requests.get(base_url, params=params)
data = response.json()

# Process and print the page titles
if "query" in data and "categorymembers" in data["query"]:
    for page in data["query"]["categorymembers"]:
        
        page_title = page["title"]
        categories = page.get("subject", [])
        category_names = [cat["title"] for cat in categories]
        print("Page:", page_title)
        print("Categories:", ", ".join(category_names))
        print()

        j_prmt = json.dumps(page, indent=2)
        with open('data/wiki_data.json', "a") as f:
            f.write(j_prmt)
            f.write(",")
