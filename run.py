from app import app_factory

app, db = app_factory(config_name='development')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)