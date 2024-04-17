import socket
import urllib.parse
from urllib.parse import urlparse
import selenium
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import whois
from datetime import datetime
from datetime import timedelta


url = input("Enter a url: ")
urlparse(url).hostname

# Code to extact webiste data to turn into data to train bot
# 1 if the data relates to not phishy activity
# 0 if the data relates to suspicious activity
# -1 if the data relates to phishy activity

# 1 IP adress in url 
def is_ip_address_legit(url):
    return socket.gethostbyname(urlparse(url).hostname) != url


# 2 Long url
def check_url_legitimacy(url):
    url_length = len(url)
    
    if url_length < 54:
        return "Legit"
    elif 54 <= url_length <= 75:
        return "Suspicious"
    else:
        return "Phishy"

# 3 url contains "@"
def check_url_for_at_symbol(url):
    if '@' in url:
        return "Phishy"
    else:
        return "Legit"

# 4 url has a fake prefix or suffix
def check_url_for_prefix_suffix(url):
    # Extract the domain part of the URL
    domain = url.split("//")[-1].split("/")[0]
    
    if '-' in domain:
        return "Phishy"
    else:
        return "Legit"

# 5 sub domains
def check_url_for_subdomains(url):
    # Extract the domain part of the URL
    domain = url.split("//")[-1].split("/")[0]
    
    # Count the number of dots in the domain
    dot_count = domain.count('.')
    
    if dot_count < 3:
        return "Legit"
    elif dot_count == 3:
        return "Suspicious"
    else:
        return "Phishy"


# 6 Fake HTTPS protocols 

def check_website_legitimacy(url):
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            if response.url.startswith('https'):
                cert_info = response.raw._connection.sock.getpeercert()
                issuer = cert_info['issuer']
                not_after = datetime.strptime(cert_info['notAfter'], '%b %d %H:%M:%S %Y %Z')
                not_before = datetime.strptime(cert_info['notBefore'], '%b %d %H:%M:%S %Y %Z')
                today = datetime.now()
                
                # Check if the issuer is trusted
                trusted_issuers = ['GeoTrust', 'GoDaddy', 'VeriSign']
                if any(issuer_item in issuer for issuer_item in trusted_issuers):
                    # Check if the certificate is not expired and issued within the past 2 years
                    if today < not_after and today - not_before < timedelta(days=730):
                        return "Legit"
                    else:
                        return "Suspicious"
                else:
                    return "Phishy"
            else:
                return "Phishy"
        else:
            return "Phishy"
    except requests.exceptions.RequestException:
        return "Connection Error"

# 7 Request URL


def check_objects_domain(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            total_objects = 0
            external_objects = 0
            
            for tag in soup.find_all(['img', 'video', 'audio', 'script', 'link', 'iframe']):
                src = tag.get('src') or tag.get('href')
                if src:
                    total_objects += 1
                    parsed_url = urlparse(src)
                    if parsed_url.netloc != '':
                        external_objects += 1
            
            if total_objects == 0:
                return "Legit"
            
            percentage = (external_objects / total_objects) * 100
            
            if percentage < 22:
                return "Legit"
            elif 22 <= percentage < 61:
                return "Suspicious"
            else:
                return "Phishy"
        else:
            return "Phishy"
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return "Phishy"

# 8 URL of anchor

def check_anchor_urls(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            anchor_tags = soup.find_all('a')
            total_anchor_urls = 0
            external_anchor_urls = 0
            
            for tag in anchor_tags:
                href = tag.get('href')
                if href:
                    total_anchor_urls += 1
                    parsed_url = urlparse(href)
                    if parsed_url.netloc != '':
                        external_anchor_urls += 1
            
            if total_anchor_urls == 0:
                return "Legit"
            
            percentage = (external_anchor_urls / total_anchor_urls) * 100
            
            if percentage < 31:
                return "Legit"
            elif 31 <= percentage <= 67:
                return "Suspicious"
            else:
                return "Phishy"
        else:
            return "Phishy"
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return "Phishy"

# 9 SFH 

def check_server_form_handler(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            form = soup.find('form')
            if form:
                action = form.get('action')
                if not action or action == "about:blank":
                    return "Phishy"
                elif "://" in action and urlparse(action).netloc != urlparse(url).netloc:
                    return "Suspicious"
                else:
                    return "Legit"
            else:
                return "Phishy"
        else:
            return "Phishy"
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return "Phishy"

# 10 whois database
    
def check_url_host(url):
    parsed_url = urlparse(url)
    if not parsed_url.hostname:
        return "Phishy"
    else:
        return "Legit"

# 11 using popup window

def check_right_click_behavior(url):
    try:
        # Initialize a headless browser
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        
        # Open the webpage
        driver.get(url)
        
        # Get the body element
        body = driver.find_element_by_tag_name('body')
        
        # Check if right-click is disabled
        if body.get_attribute('oncontextmenu') == 'return false;':
            return "Phishy"
        # Check if right-click shows an alert
        elif body.get_attribute('oncontextmenu') == 'alert(\'Right click disabled\');':
            return "Suspicious"
        else:
            return "Legit"
    except Exception as e:
        print("Error:", e)
        return "Phishy"
    finally:
        # Close the browser
        driver.quit()

# 12 redirect page

def check_redirections(url):
    try:
        response = requests.get(url, allow_redirects=False)
        redirect_count = len(response.history)
        
        if redirect_count == 1:
            return "Legit"
        elif 1 < redirect_count < 4:
            return "Suspicious"
        else:
            return "Phishy"
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return "Phishy"

# Example usage
url = "https://example.com"
print(check_redirections(url))

# 13 DNS record

def check_dns_record(domain):
    try:
        # Resolve the domain's IP address
        ip_address = socket.gethostbyname(domain)
        if ip_address:
            return "Legit"
        else:
            return "Phishy"
    except socket.gaierror:
        return "Phishy"

# 14 Hidden links

def check_status_bar_behavior(url):
    try:
        # Initialize a browser
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        
        # Navigate to the webpage
        driver.get(url)
        
        # Find all links on the webpage
        links = driver.find_elements_by_tag_name('a')
        
        # Simulate mouse movements over each link to trigger onMouseOver events
        for link in links:
            webdriver.ActionChains(driver).move_to_element(link).perform()
        
        # Check if the status bar content changes
        status_bar_content = driver.execute_script("return window.status;")
        if status_bar_content != "":
            return "Phishy"
        else:
            return "Suspicious"
    except Exception as e:
        print("Error:", e)
        return "Phishy"
    finally:
        # Close the browser
        driver.quit()

# 15 website traffic (may need api)

def check_web_traffic(url):
    try:
        # Send a request to Alexa API to get the traffic rank
        response = requests.get(f"https://awis.api.alexa.com/api?Action=UrlInfo&Url={url}")
        if response.status_code == 200:
            # Parse the XML response to extract the traffic rank
            traffic_rank = int(response.text.split('<aws:Rank>')[1].split('</aws:Rank>')[0])
            
            # Check the traffic rank against the threshold
            if traffic_rank <= 150000:
                return "Legit"
            else:
                return "Suspicious"
        else:
            return "Phishy"
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return "Phishy"

# 16 Age of domain

def check_domain_age(domain):
    try:
        # Perform a WHOIS lookup
        domain_info = whois.whois(domain)
        
        # Extract the creation date of the domain
        creation_date = domain_info.creation_date
        
        # Check if creation_date is a list or a single datetime object
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        
        # Calculate the age of the domain
        today = datetime.now()
        domain_age = today - creation_date
        
        # Check if the domain age is less than or equal to 6 months
        if domain_age.days <= 180:
            return "Legit"
        else:
            return "Phishy"
    except whois.parser.PywhoisError as e:
        print("Error:", e)
        return "Phishy"
