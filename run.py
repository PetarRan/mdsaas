from app import app_factory

app, db, User = app_factory(config_name='development')


if __name__ == '__main__':
    app.run(debug=True)
