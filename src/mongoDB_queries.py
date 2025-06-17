from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi

from dotenv import load_dotenv
import os

def pymongo_error_handler(func):
    def inner(*args):
        try:
            return func(*args)
        except errors.ServerSelectionTimeoutError:
            print("Error: Failed to connect to MongoDB.")
        except errors.PyMongoError as e:
            print(f"Error PyMongo: {e}")
        except ValueError as e:
            print(f"Value Error: {e}")

    return inner

# Реалізуйте функцію для виведення всіх записів із колекції.
@pymongo_error_handler
def find_all(db):
    result = db.cats.find()

    return list(result)

# Реалізуйте функцію, яка дозволяє користувачеві ввести ім'я кота та виводить інформацію про цього кота.
@pymongo_error_handler
def find_by_name(name, db):
    document = db.cats.find_one({'name': name})

    if document is None:
        print(f"Document with name = '{name}' not found.")
        return None
    else:
        return document

# Створіть функцію, яка дозволяє користувачеві оновити вік кота за ім'ям.
@pymongo_error_handler
def update_age(name, age, db):
    document = db.cats.update_one({"name": name}, {"$set": {"age": age}})

    if age is not int:
        raise ValueError('Expecting age to be integer')

    if document.matched_count == 0:
        print(f"Document with name = '{name}' not found.")
        return False
    elif document.modified_count == 0:
        print(f"Document with name = '{name}' was found, but not modified.")
        return False
    else:
        print(f"Document updated successfully.")
        return True

# Створіть функцію, яка дозволяє додати нову характеристику до списку features кота за ім'ям.
@pymongo_error_handler
def add_features(name, feature, db):
    document = db.cats.update_one({'name': name}, {'$push': {'features': feature}})
    if document is None:
        print(f"Document with name = '{name}' not found.")
        return None
    else:
        return document

# Реалізуйте функцію для видалення запису з колекції за ім'ям тварини.
@pymongo_error_handler
def delete_by_name(name, db):
    document = db.cats.delete_one({"name": name})

    if document is None:
        print(f"Document with name = '{name}' not found.")
        return None
    else:
        return document

# Реалізуйте функцію для видалення всіх записів із колекції.
@pymongo_error_handler
def delete_all(db):
    result = db.cats.delete_many({})
    return result

load_dotenv()
db_string = os.getenv("DB_STRING")
client = MongoClient(
    db_string,
    server_api=ServerApi('1')
)
db = client.book

name = 'Liza'
age = 'fsa'
print(update_age(name, age, db))


client.close()
