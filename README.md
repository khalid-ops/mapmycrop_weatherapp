A weather API project made with Python, Django, Mysql

To setup the project follow these steps:

 1. clone the Repository
 2. create virtual environment on your system, install requirements.txt packages using command "pip install -r requirements.txt"
 3. setup mysql by creating a schema and adding the db details in settings.py file and run migrations and migrate commands
 4. start the server with "python manage.py runserver"
 5. access the app at "http://127.0.0.1:8000"
 6. available endpoints are:
  * http://127.0.0.1:8000/register
  * http://127.0.0.1:8000/auth
  * http://127.0.0.1:8000/authorize
  * http://127.0.0.1:8000/weather
 7. to run tests use command "python manage.py test"
    
Framework Selection:

* Django is a full stack and popular framework with large community support.
* It has too many inbuilt features for better development to name a few would be ORM, Templating engine, security etc.
* for these reasons django framework was selected.

Design decisions:

* User model is made for users data.
* password hashing is done and stored in binary field, since charfield requires typecasting and requires unnecessary computing for any comparison.
* tokens are generated with secret key and algorithm for better security
* authorizer decorator is created for api authorization and can be flexible for using it on every api authorization
* weather api is being called with no tls verification to get results since https api is getting called from http server.

Security Considerations:

* Django provides inbuilt sql injection protection via orm and for extra caution, certain functions can be used
* Django provides csrf token auth middleware for protecting post requests from csrf attacks with this csrf attacks can be stopped
* For api security oauth2 protocol based jwt tokens can be used.
* Django provides xss attack security inbuilt by escaping templates properly
