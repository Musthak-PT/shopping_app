3 apps created:
----------------
1)customer
2)admin_app
3)shop

# apis are in customer app
1) Customer sign up : http://127.0.0.1:8000(local host)/customer/customer-register/
2) Customer login :  http://127.0.0.1:8000(local host)/customer/customer-login/
3) List all products : http://127.0.0.1:8000(local host)/customer/listing-products/
4) Listing of Orders with authentication : http://127.0.0.1:8000(local host)/customer/listing-orders/

#creating super use : python manage.py createsuperuser

#install the packages
pip install django

#create virtual environment
python -m vevn venv
venv\Scripts\activate
