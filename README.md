# dataproj

Django project running in a docker container


### quickstart:

  clone project
  
  `docker-compose build`
  
  `docker-compose up -d db`    *database container needs to be started first
  
  `docker-compose up web`
  
  
  
  should now be running on port 8001, but still need to run some django commands
  
  need to 'ssh' into docker container:
  
  `docker exec -it dataproj_web_1 bash`   *`winpty docker exec -it dataproj_web_1 bash` in windows
  
  
  
  `python manage.py migrate`  *runs default migrations to ceate user tables, etc
  
  `python manage.py createsuperuser`   *create a login for yourself
  
  `python manage.py makemigrations students`  *initially create migration files for each app
  
  `python manage.py makemigrations studyareas`
  
  `python manage.py makemigrations codetables`
  
  `python manage.py migrate`


### notes:

There are three apps within the project containing various models

`codetables`
`studyareas`
`sudents`

`codetables` and `studyareas` contain only models and admin files, for status, etc codes and subjects/programs/specializations respectively

The fourth app, extended_filters, is from here: https://bitbucket.org/legion_an/django-extended-filters and is included for checkbox filters in admin


The bulk of the logic is within the `students` app.  Templates, static files, views, and RiotJS files are all included here.  Only URLs are not, all stored under the project.

Django templating capabilities are not used extensively, and forms are not used. The only django templates are `index.html`, and `login.html`. All other views and urls are for REST calls. Django-Rest-Framework is used for this.  `student/static/javascript/ajaxhelpers.js` contains various helper functions for ajax calls, particularly for permissions on POST requests.

Thus this essentially functions as 1-page app, with ajax calls making up the bulk of interactions between front and back end.

The front end uses JQuery and RiotJS. The riot files are under `/students/static/riot_tags/` and the tags are loaded from `index.html` Each riot file includes html, javascript and css. LeafletJS is used to create the map, as well as leaflet-markerclusters https://github.com/Leaflet/Leaflet.markercluster

#### Admin:
django-import-export - https://django-import-export.readthedocs.io/en/latest/ - is included in order to allow uploading CSV files. Thus most models have a Resource class defined as well as Admin.

#### Models:
There is an 'AbstractModel' defined which most of the other models inherit from, in order to included created and edited dates, as well as user for each model. Likewise in Admin ExtendedAdmin and ExtendedResource are defined to ovverride save functions.

In order to reduce query time, there are some redundancies in the database.  There are various 'signals' (esentially database triggers) defined in models.py files. For example, while there is a many-to-may table between Specialization and Enroll, fields 'specialization_1' and 'specialization_2' and also included in Enroll, as foreign keys to Specialization.  There are also some calculated values. The 'total_award_amount' for a student is saved to a field in Student whenever an award to them is saved.
