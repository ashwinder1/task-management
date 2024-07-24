## Steps to run the API project on reveiwers system
1. ___Clone the repository___

`git clone https://github.com/<username>/<forked-repo>.git`

2. ___Create and activate virtual environment___

`python3 -m venv env`

Activate it on Linux:

`source env/bin/activate`

3.  ___Install Dependencies___

 Run command: `pip install -r requirements.txt`

4. Verify installations:

`pip list`

5. ___Setup and configure Database___
	
- In settings, create .env file with database settings to connect with your database
- _create database in mysql_

`mysql`

`create database taskdb;`

_create migrations_
`python3 manage.py makemigrations`

_run migration_
`python3 manage.py migrate`

5. ___Run the Project___

`python3 manage.py runserver`



**Required Packages:**

- Django
- DRF
- MySQL
- dotenv

https://pypi.org/project/python-dotenv/

>> Steps to create requirements.txt file:

1. Create requirements.txt file in your python project
2. Run command: pip freeze > requirements.txt

How to update a requirements file automatically when new packages are installed?

https://stackoverflow.com/questions/65695906/how-to-update-a-requirements-file-automatically-when-new-packages-are-installed

https://realpython.com/pipenv-guide/

https://mattsegal.dev/django-portable-setup.html

https://alicecampkin.medium.com/setting-up-a-forked-django-project-53d5939b7e9e
