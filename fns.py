import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from crewai_tools import ScrapeWebsiteTool

def scrape_website(website_url):
    """Scrapes all the information from the given website.       
    Args:
        website_url: A url of a company website.
    Returns:
        Scraped information from the given website.
    """
    scrapper = ScrapeWebsiteTool()
    data = scrapper.run(website_url=website_url)

    return data

def extract_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')  
    links = set()
    for a_tag in soup.find_all('a', href=True):
        full_url = urljoin(url, a_tag['href'])
        links.add(full_url)   
    return list(links)

def extract_content(website_url):
    # website_url = 'https://python.langchain.com/v0.2/docs/introduction/'
    all_links = extract_links(website_url)

    scraped_contents = []
    for link in all_links:
        print(f"Scraping {link}")
        try:
            content = scrape_website(link)
        except Exception as e:
            print(e)
        if content:
            scraped_contents.append({'url': link, 'content': content})

    # for item in scraped_contents:
    #     print(f"URL: {item['url']}")
    #     print(f"Content: {item['content'][:500]}")  # Print first 500 characters of content
    #     print('-' * 80)
    return scraped_contents