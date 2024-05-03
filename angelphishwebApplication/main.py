from datetime import datetime as dt

from pyscript import document
from pyweb import pydom
import selenium

urls = []

def q(selector, root=document):
    return root.querySelector(selector)

# Define the URL template that will be used to render new URLs to the page
url_template = pydom.Element(q("#url-template").content.querySelector(".url"))

url_list = pydom["#list-urls-container"][0]
new_url_content = pydom["#new-url-content"][0]

def add_url(e):
    # Ignore empty URL
    if not new_url_content.value:
        return None

    # Create URL
    url_id = f"url-{len(urls)}"
    url = {
        "id": url_id,
        "content": new_url_content.value,
        "checked": False,
        "created_at": dt.now(),
    }

    urls.append(url)

    # Add the URL element to the page by cloning from the template
    url_html = url_template.clone()
    url_html.id = url_id

    url_html_content = url_html.find("p")[0]
    url_html_content._js.textContent = url["content"]
    url_list.append(url_html)

    new_url_content.value = ""

def add_url_event(e):
    if e.key == "Enter":
        add_url(e)

new_url_content.onkeypress = add_url_event
