mport os, sys
sys.path.append("/home/alex/django/smarty/")

# В python path добавляется директория проекта
dn = os.path.dirname
PROJECT_ROOT = os.path.abspath( dn(dn(__file__)) )
DJANGO_PROJECT_ROOT = os.path.join(PROJECT_ROOT, 'smarty')
sys.path.append(DJANGO_PROJECT_ROOT)

# Установка файла настроек
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Запуск wsgi-обработчика
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

