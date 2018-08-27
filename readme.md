### Heroku Production

#### pushes production branch as master in heroku origin
- git push heroku production:master  
- heroku run python manage.py makemigrations
- heroku run python manage.py migrate