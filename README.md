#Apps:
----------------
1)customer
2)admin_app
3)shop


#Running:
------------
*python manage.py runserver
*Migration : python manage.py makemigrations
             python manage.py migrate
*Collecting static files : python manage.py collectstatic
*creating super user : python manage.py createsuperuser



# apis are in customer app:
---------------------------------
1) Customer sign up : http://127.0.0.1:8000(local host)/customer/customer-register/
2) Customer login :  http://127.0.0.1:8000(local host)/customer/customer-login/
3) List all products : http://127.0.0.1:8000(local host)/customer/listing-products/
4) Listing of Orders with authentication : http://127.0.0.1:8000(local host)/customer/listing-orders/



#install the packages
------------------------------------------------
Package             Version
------------------- -------
asgiref             3.8.1
Django              5.1a1
djangorestframework 3.15.2
drf-yasg            1.21.7
inflection          0.5.1
packaging           24.1
pillow              10.3.0
pip                 22.0.4
pytz                2024.1
PyYAML              6.0.1
setuptools          58.1.0
sqlparse            0.5.0
typing_extensions   4.12.2
tzdata              2024.1
uritemplate         4.1.1


#create virtual environment
-----------------------------
python -m vevn venv
venv\Scripts\activate
