import requests
import bs4
import pandas as pd


def main():
    url2022 = "https://openaccess.thecvf.com/CVPR2022?day=all"
    url2023 = "https://openaccess.thecvf.com/CVPR2023?day=all"
    url2024 = "https://openaccess.thecvf.com/CVPR2024?day=all"
    output_file = 'most_contributions.xlsx'

    most_contributions_2022_response = get_most_contributions(url=url2022)
    print(most_contributions_2022_response)


def get_most_contributions(**kwargs):
    url = kwargs.get('url')
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    author_tags = soup.find_all('a', href=True)
    authors = []
    for tag in author_tags:
        if 'author' in tag['href']:
            authors.append(tag.text)
    return authors
    









if __name__ == "__main__":
    main()