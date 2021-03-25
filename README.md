Start a python virutal environment, then use the following command to install all the packages:
```
pip install -r requirements.txt
```

#Run the applicaiton:
for Linux and Mac:
```
export FLASK_APP=tenzin
export FLASK_ENV=development
flask run
```
For Windows cmd, use set instead of export:
```
set FLASK_APP=tenzin
set FLASK_ENV=development
flask run
```
For Windows PowerShell, use env: instead of export:
```
env:FLASK_APP = "tenzin"
env:FLASK_ENV = "development"
flask run
```

Visit http://127.0.0.1:5000/hello in a browser and you should see the “Hello, World!” message. Congratulations, you’re now running your Flask web application!

#Test code
To test code:
```
py.test -v
```
To measure the code coverage of your tests, use the coverage command to run pytest instead of running it directly.:
```
coverage run -m pytest
```
To view a simple coverage report in the terminal
```
coverage report
```
An HTML report allows you to see which lines were covered in each file:
```
coverage html
```

