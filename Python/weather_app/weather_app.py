from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Get form data
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
    app.run(debug=True)