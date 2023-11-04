class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:it1@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    SECRET_KEY = 'your_production_secret_key'

class TestConfig(Config):
    TESTING = True

# Additional configurations for other environments can be added here
# You can set the active configuration by specifying it in the app creation

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test' : TestConfig
    # Add configurations HERE if needed
}
