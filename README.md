# PP2I1
## Our first year, first semester project as students at Telecom Nancy.

### __What does it do__ ?

- Runs a small website dedicated to the climate cause : optimizing routes for emptying bins and offering a way to manage the system for the administrators, as well as a shop, and authentification system and some articles on how to have a bigger impact in your own way.

### __Requirements__

- Python 3.10
- Flask and Flask-login, and their dependencies.

### __How to install it on your computer ?__

- Just clone it wherever you want in your computer, using : 
```ps
git clone https://github.com/Esteban795/PP2I1.git
```

- When inside the correct folder, you can run 
```ps
pip3 install -r requirements.txt
``` 
to install Flask and Flask-login, if you don't already have them.

- If you'd rather use a virtual environment, go to the PP2I1 directory and run 
```ps
python3 -m venv
./bin/activate
```
- Once you're in the venv, run `pip3 install -r requirements.txt`.

## __How to use it ?__

- Run it using the basic python3 syntax. Make sure to be in the root folder of the project !
```ps
python3 ./PP2I1/src/backend/app.py
```
- Open your browser and go to the adress that flask gives you.
Default is [27.0.0.1:8080](http://127.0.0.1:8080/)