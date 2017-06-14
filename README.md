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
  
