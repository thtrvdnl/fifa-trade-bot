import pymongo

import utils

db_client = pymongo.MongoClient(utils.env.str("MONGO_HOST"))

current_db = db_client[utils.env.str("MONGO_DB")]

collection = current_db["MONGO_TABLE"]