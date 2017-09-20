import time
import requests
import urllib
from bs4 import BeautifulSoup

start_url = input("please insert a Start link")
target_url = input("please insert a target link")

def find_first_link(url):
    '''get HTML from the url'''

    response = requests.get(url)
    html = response.text

    '''Feed HTMl in beautifulsoup'''

    soup = BeautifulSoup(html,"html.parser")

    '''Get the HTMl code from articles body <div>'''

    content_div = soup.find(id='mw-content-text').find(class_="mw-parser-output")

    article_link = None

    '''Finds all  <a> tags that are direct children content <div> paragraph'''
    for element in content_div.find_all("p", recursive=False):

        '''Finds the first <a> tag that is direct child to <p> tag, while removing links for footnotes & pronounciations '''
        if element.find("a", recursive=False):
            article_link = element.find("a", recursive=False).get("href")
        break

    if not article_link:
        return

    #Build full URl from the relative URL
    first_link = urllib.parse.urljoin('https://en.wikipedia.org/',article_link)
    return first_link


def continue_crawl(search_history,target_url, max_crawls = 25):
    if target_url in search_history[-1]:
        print("The Targeted page has been crawled")
        return False

    elif len(search_history) > max_crawls:
        print("Too much search performed,no more crawling allowed")
        return False

    elif search_history[-1] in search_history[:-1]:
        print("URL has already been visited")
        return False
    else:
        return True
        print("continue crawling")


article_chain = [start_url]

while continue_crawl(article_chain,target_url):
    print(article_chain[-1])

    first_link = find_first_link(article_chain[-1])
    if not first_link:
        print("There are no more articles to be crawled, aborting search!")
        break

    article_chain.append(first_link)
    time.sleep(2)
