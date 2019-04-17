# Halcyon-Wanderers-Site
tech nerds that play game do thing

Temporarily at http://54.71.46.4/

## How to ssh to prod
Ask Albin either for key or give him your public key to add to the authorized-keys

## How to develop locally
0. Have python 3.6 and pip installed
1. `git clone https://github.com/jjkjiang/Halcyon-Wanderers-Site`
2. Change directory to cloned repo
OPTIONAL: Use a virtual environment for development https://packaging.python.org/guides/installing-using-pip-and-virtualenv/#installing-virtualenv
3. `pip install -r requirements.txt' Install the requirements
4. 'python manage.py runserver'
5. Development server is up, any change you make can be done there
6. See https://docs.djangoproject.com/en/2.2/intro/ for how to work with Django

## How to push to prod
0. One day CD Pog, maybe later
1. Manual deployment involves sshing into the prod server and `git pull` in the srv directory
2. `python manage.py collectstatic`
3. `python manage.py makemigrations`
4. `python manage.py migrate`
5. `sudo systemctl gunicorn restart`
6. `sudo systemctl nginx restart`

## How this was made
AWS Lightsail and this guy's guide almost exactly: 
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04
