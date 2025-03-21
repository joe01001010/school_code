import undetected_chromedriver as uc
from bs4 import BeautifulSoup

def main():
    website_list = [
        'https://www.google.com/search?q=Colorado+Springs+Colorado+USA+weather',
        'https://www.google.com/search?q=Winter+Park+Colorado+USA+weather',
        'https://www.google.com/search?q=Winter+Park+Florida+USA+weather',
        'https://www.google.com/search?q=Alexandria+Virginia+USA+weather',
        'https://www.google.com/search?q=Alexandria+Ontario+Canada+weather',
        'https://www.google.com/search?q=Melbourne+Florida+USA+weather',
        'https://www.google.com/search?q=Melbourne+Victoria+Australia+weather'
    ]
    browser = uc.Chrome()

    for website in website_list:
        browser.get(website)
        html_content = browser.page_source
        temperature, city, state = extract_weather_data(html_content)
        print(f"Temperature: {temperature}, City: {city}, State: {state}")
        input("Press enter to get the next website")

    input("Press enter to close browser")
    browser.quit()


def extract_weather_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    temperature = soup.find('span', {'id': 'wob_tm'})
    if temperature:
        temperature = temperature.text
    else:
        temperature = "N/A"

    location = soup.find('div', {'class': 'vqkKIe wHYlTd mzYw6b'})
    if location:
        location_text = location.text
        if ',' in location_text:
            city, state = location_text.split(',')
            city = city.strip()
            state = state.strip()
        else:
            city = location_text.strip()
            state = "N/A"
    else:
        city = "N/A"
        state = "N/A"

    return temperature, city, state



if __name__ == '__main__':
    main()