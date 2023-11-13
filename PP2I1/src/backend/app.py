from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    default_value = 'jean mich'
    data = request.form.get('submitted-name', default_value)
    print(data)
    return f'Hello {data}!'

if __name__ == '__main__':
    app.run(debug=True)