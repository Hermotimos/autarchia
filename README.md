# STEPS:
# rename everywhere 'mysite' to the desired project name
# prepare env (requires database setup)
# create & activate virtualenv
# pip install -r requirements.txt (!! remove stuff for Google Storage if not needed together with mysite.storages.py)

# python manage.py migrate
# python manage.py createsuperuser
# python manage.py makemigrations polls
# python manage.py migrate
# python manage.py collectstatic (!! uncomment the right static conf in settings.py)
# python manage.py runserver

# create GCP project

# create GCP instance or a database ina an existing instance
# enable Cloud SQL API for the project: https://console.cloud.google.com/apis/library/sqladmin.googleapis.com?project=autarchia

# create .env on GCP
# enter cloud console and: "gcloud config set project PROJECTNAME"
# git clone your repo
# cd to where manage.py resides and: "gcloud app deploy"

# enable Secrets API for the project
# generate service account key: https://cloud.google.com/iam/docs/creating-managing-service-account-keys

