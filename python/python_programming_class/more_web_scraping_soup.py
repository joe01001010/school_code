import bs4
print(f"Beautiful Soup Versions: {bs4.__version__}", end='\n\n')

def main():
    html_contents = "<!DOCTYPE html>\n<html>\n<head>\n<title>Web Scraping</title>\n</head>\n<body>\n<div class=\"example1\">\n<p class=\"first another_class_name\">First Paragraph</p>\n<p class=\"second\">Second Paragraph</p>\n<p class=\"third\">Third Paragraph</p>\n<p class=\"first\">Another First Paragraph</p>\n<a id=\"one\" class=\"first\" href=\"https://www.google.com/\">Google</a>\n<a class=\"first\" href=\"https://www.bing.com/\">Bing</a>\n<div class=\"example3\">\n<a href=\"https://www.search.brave.com/\">Brave</a>\n</div>\n</div><div class=\"example2\">\n<a href=\"https://www.wikipedia.com/\">Wikipedia</a>\n</div>\n<div class=\"example3\">\n<a href=\"https://www.youtube.com/\">YouTube</a>\n</div>\n</body>\n</html>"
    with open('temp.html', 'w') as output_file:
        output_file.write(html_contents)
    
    with open('temp.html', 'r') as input_file:
        soup = bs4.BeautifulSoup(input_file, 'html.parser')

    title_var = soup.select('title')
    print(type(title_var))
    for title in title_var:
        print(title)
    print()

    div_var = soup.select('div.example2')
    print(type(div_var))
    for div in div_var:
        print(div)
    print()

    print(soup.select('a.first'))
    print()

    a_attribute = soup.select('a#one')
    print(a_attribute)
    for attribute in a_attribute:
        print(attribute['href'])
    print()

    first_h1 = soup.find(id='one')
    print(first_h1)
    print()

    links = soup.find_all('a', href=True)
    http_links = [link['href'] for link in links if link['href'].startswith('http')]
    print(http_links)
    print()

    title_elements = soup.find_all('title')
    print(title_elements)
    print()

    paragraphs = soup.find_all('p', class_ = 'first')
    for paragraph in paragraphs:
        print(paragraph.get_text())
    print()

            


if __name__ == '__main__':
    main()