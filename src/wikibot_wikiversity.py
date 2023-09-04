import pywikibot
import re

# Set up the pywikibot instance
site = pywikibot.Site("en", "wikiversity")
page_title = "Category:Science"  
page = pywikibot.Page(site, page_title)


categories = page.categories()
# input(categories)

# Create a dictionary to store category names and URLs
category_dict = {}

# Populate the dictionary with category names and URLs
for category in categories:
    category_name = category.title(with_ns=False)  # Get the category name without namespace
    category_url = category.full_url()
    category_dict[category_name] = category_url

# Print the dictionary
for category_name, category_url in category_dict.items():
    print(f"Category: {category_name}, URL: {category_url}")


category_name = "Category:Science"  # Replace with the desired category name
category = pywikibot.Category(site, category_name)
category_info = category.categoryinfo['pages']
input(category_info)

# Get the pages in the category
category_pages = category.members(namespaces=[4])  # Limit to namespace 0 (main namespace)

# Print the titles of the pages in the category
for page in category_pages:
    print(page.title())

input('test')


# Get the subcategories of the category
subcategories = category.subcategories()

# Print the names of the subcategories
for subcategory in subcategories:
    s_category = pywikibot.Category(site, subcategory)
    input(s_category)
    s_category_info = category.categoryinfo()
    print(s_category_info)

    site_s = site
    page_title = subcategory.title(with_ns=False)

    page_s = pywikibot.Page(site, page_title)
    print(page_title)
    if page_s == []:
        site_s = pywikibot.Site("en", "wikipedia")
        page_s = pywikibot.Page(site_s, page_title)


