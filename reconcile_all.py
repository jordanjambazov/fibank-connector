import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "connector.settings")
django.setup()


def main():
    from connector.engine import Engine
    engine = Engine()
    engine.reconcile_all()


if __name__ == '__main__':
    main()
