from flask import Flask, render_template, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °C 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    try:
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

@app.route('/commits/')
def commits():
    try:
        response = requests.get('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
        response.raise_for_status()  # Vérifie les erreurs de requête HTTP
        commits_data = response.json()

        minutes_count = [0] * 60
        for commit in commits_data:
            commit_date = commit['commit']['author']['date']
            date_object = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
            minutes = date_object.minute
            minutes_count[minutes] += 1

        data_rows = [[f'{i} min', count] for i, count in enumerate(minutes_count)]
        return render_template("commits.html", data_rows=data_rows)
    except requests.RequestException as e:
        return str(e), 500  # Retourne l'erreur sous forme de chaîne pour le débogage

if __name__ == "__main__":
    app.run(debug=True)
