import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4
import time
from flask import Flask, request, render_template, session
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = "birdsarentreal"
app.config['SESSION_TYPE'] = "filesystem"
Session(app)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        session['first_name'] = request.form.get('first_name')
        session['last_name'] = request.form.get('last_name')
        session['city'] = request.form.get('city')
        session['state'] = request.form.get('state')
        session['country'] = request.form.get('country')

        weather_info = generate_weather_info(session['city'], session['state'], session['country'])
        print(weather_info)

        return render_template(
            'weather_app_results.html',
            first_name=session['first_name'],
            last_name=session['last_name'],
            city=session['city'],
            state=session['state'],
            country=session['country'],
            temperature=weather_info.get('temperature', 'N/A'),
            precipitation=weather_info.get('precipitation', 'N/A'),
            humidity=weather_info.get('humidity', 'N/A'),
            wind=weather_info.get('wind', 'N/A')
        )
    return render_template('weather_app_template.html')

def generate_weather_info(city, state, country):
    query = f"{city}+{state}+{country}+weather".replace(' ', '+')
    url = f"https://www.google.com/search?q={query}"
    print(f"Fetching weather data from: {url}")

    driver = uc.Chrome()
    weather_data = {
        "temperature": "N/A",
        "precipitation": "N/A",
        "humidity": "N/A",
        "wind": "N/A"
    }

    try:
        driver.get(url)
        print(driver.title)
        print(driver.find_element(By.CLASS_NAME, 'vk_bk TylWce SGNhVe'))
        input("Press enter to close browser")
        time.sleep(5)
        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

        temperature = soup.find("span", {"id": "wob_tm"})
        precipitation = soup.find("span", {"id": "wob_pp"})
        humidity = soup.find("span", {"id": "wob_hm"})
        wind = soup.find("span", {"id": "wob_ws"})

        weather_data = {
            "temperature": temperature.text if temperature else "N/A",
            "precipitation": precipitation.text if precipitation else "N/A",
            "humidity": humidity.text if humidity else "N/A",
            "wind": wind.text if wind else "N/A"
        }

    except Exception as e:
        print(f"Error fetching weather data: {e}")

    finally:
        driver.quit()

    return weather_data

if __name__ == '__main__':
    app.run(debug=True, port=5003, threaded=False)