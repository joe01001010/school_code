import requests
from flask import Flask, request, render_template
app = Flask(__name__)


def main():
    app.run(debug=True)
    form()
    website_list = [
        'https://www.google.com/search?q=Colorado+Springs+Colorado+USA+weather',
        'https://www.google.com/search?q=Winter+Park+Colorado+USA+weather',
        'https://www.google.com/search?q=Winter+Park+Florida+USA+weather',
        'https://www.google.com/search?q=Alexandria+Virginia+USA+weather',
        'https://www.google.com/search?q=Alexandria+Ontario+Canada+weather',
        'https://www.google.com/search?q=Melbourne+Florida+USA+weather',
        'https://www.google.com/search?q=Melbourne+Victoria+Australia+weather'
    ]


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
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