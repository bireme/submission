rm database.db
python manage.py syncdb --noinput
python manage.py loaddata fixtures/*
