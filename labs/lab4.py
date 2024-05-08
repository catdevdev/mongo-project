from pymongo import MongoClient
from faker import Faker
import random

fake = Faker()

# MongoDB setup
client = MongoClient('mongodb://neko-neki:neko-neki@3.79.243.95:32000')
db = client.lab4
col1 = db.collection1
col2 = db.collection2

def create_documents():
    col1_data = [{'_id': i, 'name': fake.name()} for i in range(1, 1000001)]
    col2_data = [{'_id': i, 'name': fake.name()} for i in range(1, 1000001)]

    # Insert data into collections
    col1.insert_many(col1_data)
    col2.insert_many(col2_data)

    # Update documents with cross-references
    for i in range(1000, 1000001):
        col1.find_one_and_update({'_id': i}, {'$set': {'friend': random.randint(1, 999999)}})
        col2.find_one_and_update({'_id': i}, {'$set': {'friend': random.randint(1, 999999)}})
        if i % 10000 == 0:
            print(f'Updated {i} documents...')

def main():
    print("Starting document creation...")
    create_documents()
    print("Finished creating documents.")

if __name__ == "__main__":
    main()
