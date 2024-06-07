# P11_ameliorer_une_application_web_python_par_des_teste

Projet numéro 11 du parcour OpenClassrooms "développeur d'application python"

les commandes fournis sont celle utilisé pour windows, celle ci peuvent varier (notament l'utilisation de python) sur d'autre systeme.

## dépendance 

fonctionnel :
- Python 3.12
- Flask

testing :
- pytest
- coverage
- locust


## installation

Après avoir cloner le projet, créer votre environement virtuel et activer le, installer les dépendance avec :
```
pip install -r requirements.txt
```

Lancer l'application avec :
```
flask --app server run
```
Il vous suffit d'ouvrir dans le navigateur l'adresse fournis pour ouvrir l'application.


## test

Pour les tests, ceux ci peuvent être exécuter en utilisant :
```
py -m pytest
``` 

Le coverage peut être fait en utilisant :
```
coverage run -m pytest
```
Et récupérer en HTML avec :
```
coverage html
```

Enfin les test de performance peuvent être fait avec :
```
locust -f BookingLight/tests/test_performance/locustfile.py
```
Ce dernier doit être lancer après l'application et il est possible d'accéder à une interface web avec le lien fournis pour executer les tests.


### Ci-dessous le readme du projet original :

___

# gudlift-registration

1. Why


    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

2. Getting Started

    This project uses the following technologies:

    * Python v3.x+

    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)

        Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. 
     

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 


3. Installation

    - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.

    - Next, type <code>source bin/activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

    - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>

    - Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set the file to be <code>server.py</code>. Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details

    - You should now be ready to test the application. In the directory, type either <code>flask run</code> or <code>python -m flask run</code>. The app should respond with an address you should be able to go to using your browser.

4. Current Setup

    The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:
     
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

5. Testing

    You are free to use whatever testing framework you like-the main thing is that you can show what tests you are using.

    We also like to show how well we're testing, so there's a module called 
    [coverage](https://coverage.readthedocs.io/en/coverage-5.1/) you should add to your project.

