from application import app
from application.views import add_url_rules


def main():
    add_url_rules(app)
    config = app.config

    app.run(**config['APP_CONF'])

if __name__ == "__main__":
    main()
