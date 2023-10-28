class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/database_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    SECRET_KEY = 'your_production_secret_key'

# Additional configurations for other environments can be added here
# You can set the active configuration by specifying it in the app creation

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    # Add configurations HERE if needed
}
