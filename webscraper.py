from bs4 import BeautifulSoup
import urllib3

page_string = " https://www.Senate.gov"
page = urllib3.proxy_from_url(page_string)


senta = BeautifulSoup(page, 'html.parser')
