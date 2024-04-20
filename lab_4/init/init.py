from mongo_init.init_data import MongoConnector
from postgres_init.data_init import PSQLManager

print("Start initializing all databases")

users_ids = PSQLManager.init_database()
MongoConnector().init(users_ids=users_ids)
