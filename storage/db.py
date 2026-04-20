from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import yaml

with open("/config/storage_config.yml", "r") as file:
    app_config = yaml.safe_load(file.read())

db_user = app_config["datastore"]["user"]
db_password = app_config["datastore"]["password"]
db_hostname = app_config["datastore"]["hostname"]
db_port = app_config["datastore"]["port"]
db_name = app_config["datastore"]["db"]

ENGINE = create_engine(
    f"mysql+mysqldb://{db_user}:{db_password}@{db_hostname}:{db_port}/{db_name}", # Tells SQLAlchemy to use mysqlclient
    pool_size=20, # Maximum number of connections in the pool
    pool_recycle=1800, # Recycle old DB connections after 1800 seconds
    pool_pre_ping=True # Prevents dead-connection issues if MySQL restarts
    )

def make_session():
    return sessionmaker(bind=ENGINE)()