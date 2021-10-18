release: python manage.py migrate
web: gunicorn codepay_project.wsgi --log-file -
worker: celery -A codepay_project worker -E -B --loglevel=DEBUG
