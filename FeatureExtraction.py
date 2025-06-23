import ipaddress
import re
import urllib.request
from bs4 import BeautifulSoup
import socket
import requests
from googlesearch import search
import whois
from datetime import date, datetime
import time
from dateutil.parser import parse as date_parse
from urllib.parse import urlparse
import subprocess  # Missing in original

class FeatureExtraction:

    shortening_services = r"bit\.ly|goo\.gl|shorte\.st|tinyurl\.com|tr\.im|is\.gd|cli\.gs|yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|ow\.ly|bit\.ly|ity\.im|q\.gs|po\.st|bc\.vc|ic\.li|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|link\.zip\.net"

    def parse_whois_info(self, whois_output):
        creation_date = None
        expiration_date = None

        creation_match = re.search(r'Creation Date:\s*(\d{4}-\d{2}-\d{2})', whois_output)
        expiration_match = re.search(r'Registry Expiry Date:\s*(\d{4}-\d{2}-\d{2})', whois_output)

        if creation_match:
            creation_date = creation_match.group(1).strip()
        if expiration_match:
            expiration_date = expiration_match.group(1).strip()

        return creation_date, expiration_date

    def getDomain(self, url):  
        domain = urlparse(url).netloc
        if domain.startswith("www."):
            domain = domain.replace("www.", "")
        return domain

    def havingIP(self, url):
        try:
            ipaddress.ip_address(url)
            return 1
        except ValueError:
            return 0

    def haveAtSign(self, url):
        return 1 if "@" in url else 0

    def getLength(self, url):
        return 1 if len(url) >= 54 else 0
        
    def getDepth(self, url):
        return sum(1 for part in urlparse(url).path.split('/') if part)

    def redirection(self, url):
        return 1 if url.rfind('//') > 7 else 0

    def httpDomain(self, url):
        return 1 if 'https' in urlparse(url).netloc else 0

    def tinyURL(self, url):
        return 1 if re.search(self.shortening_services, url) else 0

    def prefixSuffix(self, url):
        return 1 if '-' in urlparse(url).netloc else 0

    def domainAge(self, creation_date):
        if creation_date:
            try:
                age_days = (datetime.now() - datetime.strptime(creation_date, '%Y-%m-%d')).days
                return 0 if age_days > 365 else 1
            except Exception:
                return 1
        return 1  

    def domainEnd(self, expiration_date):
        if expiration_date:
            try:
                days_left = (datetime.strptime(expiration_date, '%Y-%m-%d') - datetime.now()).days
                return 0 if days_left > 365 else 1
            except Exception:
                return 1
        return 1  

    def featureExtraction(self, url, label):
        features = []
        
        try:
            domain = self.getDomain(url)
            features.append(domain)  

            features.append(self.havingIP(url))
            features.append(self.haveAtSign(url))
            features.append(self.getLength(url))
            features.append(self.getDepth(url))
            features.append(self.redirection(url))
            features.append(self.httpDomain(url))
            features.append(self.tinyURL(url))
            features.append(self.prefixSuffix(url))

            dns = 0
            creation_date, expiration_date = None, None

            try:
                print(f"Running WHOIS for domain: {domain}")
                result = subprocess.run(["whois", domain], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=10)
                
                if result.returncode == 0:
                    whois_output = result.stdout
                    creation_date, expiration_date = self.parse_whois_info(whois_output)
                else:
                    print(f"WHOIS failed for {domain}")
                    dns = 1
            except Exception as e:
                print(f"WHOIS exception: {e}")
                dns = 1

            features.append(dns)
            features.append(self.domainAge(creation_date) if dns == 0 else 1)
            features.append(self.domainEnd(expiration_date) if dns == 0 else 1)

            features.append(label)  

        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            features = [None] * 13  # Total number of features (including domain and label)

        return features
