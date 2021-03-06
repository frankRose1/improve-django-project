# Improve A Django Project

The goal is to take a messy, buggy, badly tested Python code base and improve it. Start with a Django app and identify where it's broken and inefficient. Improve the project by making sure database queries are optimized, form validation is correct, model fields are of the correct type, template inheritance is done in a way that reduces overall code, and tests are improved.

## App Features
* template inheritance greatly improved
* tests are written form views, models, and forms
* model fields were improved to be the appropriate type
* model form has been improved with widgets
* pagination has been added for list views

## Tests
- ```django-nose``` is used to run tests and track coverage
- run ```python manage.py test``` to run tests
- tests currently cover 92%

## Technologies used
- django
- django-debug-toolbar
- django-nose
- coverage