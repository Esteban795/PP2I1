from flask import Flask, render_template, request, url_for, flash, redirect


app = Flask(__name__,static_folder="../frontend/static")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['email']
        content = request.form['password']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            print(title, content)
            return redirect(url_for('index'))

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)