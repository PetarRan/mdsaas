from src.app import app_factory

app = app_factory(config_name='development')


if __name__ == '__main__':
    app.run(debug=True)
