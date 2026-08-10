release: python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py ensure_tv_live_charts
web: gunicorn config.wsgi:application --bind 0.0.0.0:${PORT}
