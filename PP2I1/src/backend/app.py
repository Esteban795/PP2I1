from flask import Flask, request, render_template
app = Flask(__name__,template_folder="../frontend/templates",static_folder="../frontend/static")

@app.route('/shop', methods=['GET'])
def index():
    return render_template('shop.html')
    

if __name__ == '__main__':
    app.run(debug=True)