from pymongo import MongoClient


# if 'db' not in g:
def get_db():

    client = MongoClient(
        "mongodb+srv://darpanguptaris:fitness2da@cluster0.hviltwt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    return client["Fitness2DA_database"]
