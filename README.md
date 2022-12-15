export DJANGO_SETTINGS_MODULE=django_pytest.settings

python manage.py test companies/test/

to run with timetracker:
pytest -v -s --durations=0


