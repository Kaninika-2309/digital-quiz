from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/quiz')
def get_quiz():
    category = request.args.get('category', '9')  # default General Knowledge
    amount = request.args.get('amount', '5')      # default 5 questions

    url = f'https://opentdb.com/api.php?amount={amount}&category={category}&type=multiple'
    response = requests.get(url)
    data = response.json()
    return jsonify(data)

@app.route('/api/categories')
def get_categories():
    url = 'https://opentdb.com/api_category.php'
    response = requests.get(url)
    data = response.json()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
