import requests
from bs4 import BeautifulSoup


def scraping_bdm(keyword: str, page: int = 1) -> dict:
    paginated_url = f"https://www.blogdumoderateur.com/page/{page}/?s={keyword}"
    response_bdm = requests.get(paginated_url)
    soup_bdm = BeautifulSoup(response_bdm.text, 'html.parser')
    articles = soup_bdm.find_all('article')
    print(articles)
    data = {}

    for article in articles:

        try:
            image_link = article.find('img')['src']  # Image
        except:
            image_link = None

        title = article.h3.text  # Title

        try:
            link = article.find('a')['href']  # Link
        except:
            link = article.parent['href']

        time = article.time['datetime'].split('T')[0]  # Time

        try:
            label = article.find('span', 'favtag color-b').text  # label
        except:
            try:
                label = article.parent.parent.parent.parent.h2.text
            except:
                label = None

        data[article['id']] = {
            'title': title,
            'image': image_link,
            'link': link,
            'label': label,
            'time': time
        }
    return data
