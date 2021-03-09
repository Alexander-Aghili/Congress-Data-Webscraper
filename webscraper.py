from bs4 import BeautifulSoup
import requests

senate_URL = " https://www.Senate.gov"
senate_page = requests.get(senate_URL)

senateSoup = BeautifulSoup(senate_page, 'html.parser')



