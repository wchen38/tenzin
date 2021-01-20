Start a python virtual environment, then use the following command to install all the packages:
```
pip install -r requirements.txt
```

#Run the application:
for Linux and Mac:
```
export FLASK_APP=tenzin
export FLASK_ENV=development
flask run
```
for Windows cmd, use set instead of export:
```
set FLASK_APP=tenzin
set FLASK_ENV=development
flask run
```
for Windows PowerShell, use env: instead of export:
```
env:FLASK_APP = "tenzin"
env:FLASK_ENV = "development"
flask run
```

Visit http://127.0.0.1:5000/hello in a browser and you should see the “Hello, World!” message. Congratulations, you’re now running your Flask web application!

