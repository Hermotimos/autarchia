# STEPS:

<!-- LOCAL -->
# rename everywhere 'mysite' to the desired project name
# prepare env (requires database setup)
# python -m venv myvenv
# source myvenv\Scripts\activate OR source myvenv/bin/activate
# pip install -r requirements.txt (!! remove stuff for Google Storage if not needed together with mysite.storages.py)

# python manage.py migrate
# python manage.py createsuperuser
# python manage.py makemigrations polls
# python manage.py migrate
# python manage.py collectstatic (!! uncomment the right static conf in settings.py)
# python manage.py runserver

<!-- GCP -->
# create GCP project

# create GCP instance or a database in an existing instance
# enable Cloud SQL API for the project: https://console.cloud.google.com/apis/library/sqladmin.googleapis.com?project=autarchia
# enable Secrets API for the project

# enter cloud console and: "gcloud config set project PROJECTNAME"
# enter Code Editor, open new Terminal and create cd into correct dir
# git clone your repo
# create .env in GCP Code Editor and populate it with correct data
# follow the steps from LOCAL (skip the first step as it should be done with git clone repo)
# cd to where manage.py resides and: "gcloud app deploy"

# generate service account key: https://cloud.google.com/iam/docs/creating-managing-service-account-keys
# add file gcp-service-account-key.json with the generated stuff

