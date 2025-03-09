import requests, bs4
from flask import Flask, request, render_template
app = Flask(__name__)

website_list = [
    'https://www.google.com/search?q=Colorado+Springs+Colorado+USA+weather',
    'https://www.google.com/search?q=Winter+Park+Colorado+USA+weather',
    'https://www.google.com/search?q=Winter+Park+Florida+USA+weather',
    'https://www.google.com/search?q=Alexandria+Virginia+USA+weather',
    'https://www.google.com/search?q=Alexandria+Ontario+Canada+weather',
    'https://www.google.com/search?q=Melbourne+Florida+USA+weather',
    'https://www.google.com/search?q=Melbourne+Victoria+Australia+weather'
]


def main():
    app.run(debug=True)
    form()


def convert_to_celsius(temp):
    return ((float(temp) - 32) * 5) / 9


def download_url(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    with open('html_page.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
        file.close()


def parse_html(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        web_page_response = file.read()
    soup = bs4.BeautifulSoup(web_page_response, 'html.parser')

    temperature_element    = soup.find(id='wob_tm')
    precipitation_element  = soup.find(id='wob_pp')
    humidity_element       = soup.find(id='wob_hm')
    wind_element           = soup.find(id='wob_ws')
    temperature            = temperature_element.get_text(strip=True) if temperature_element else "Not found"
    celsius_temperature    = convert_to_celsius(temperature)
    precipitation          = precipitation_element.get_text(string=True) if precipitation_element else "Not found"
    humidity               = humidity_element.get_text(string=True) if humidity_element else "Not found"
    wind                   = wind_element.get_text(string=True) if wind_element else "Not found"
    return temperature, celsius_temperature, precipitation, wind, humidity


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        download_url(website_list[0])
        temp_fahrenheit, temp_celsius, precipitation, wind, humidity = parse_html('html_page.html')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')
        
        return render_template('weather_app_results.html', 
                             first_name=first_name,
                             last_name=last_name,
                             city=city,
                             state=state,
                             country=country)
    
    return render_template('weather_app_template.html')

if __name__ == '__main__':
    main()