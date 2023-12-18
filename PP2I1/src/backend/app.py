from flask import Flask, request, render_template
app = Flask(__name__,template_folder="../frontend/templates",static_folder="../frontend/static")

@app.route('/accueil', methods=['GET'])
def index():
    return render_template('homepage.html')
    

if __name__ == '__main__':
    app.run(debug=True,port=8080)