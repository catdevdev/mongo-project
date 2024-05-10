from pymongo import MongoClient
from faker import Faker
import logging

logging.basicConfig(level=logging.INFO)

client = MongoClient('mongodb://neko-neki:neko-neki@18.153.75.45:32000')
db = client.lab9
peoples = db.peoples

fake = Faker()

def generate_and_insert_documents(num_docs):
    bulk_ops = []
    for i in range(1, num_docs + 1):
        person = {
            "_id": i,
            "peoplename": fake.name(),
            "age": fake.random_int(min=18, max=99),
            "peoplefriend": i - 1 if i > 1 else None  
        }
        bulk_ops.append(person)
        
        if i % 1000 == 0: 
            logging.info(f"Prepared {i} documents for insertion.")

    peoples.insert_many(bulk_ops)
    logging.info("All documents inserted successfully.")

def query_and_sort_friends():
    pipeline = [
        {"$match": {"peoplefriend": {"$ne": None}}},  
        {"$lookup": {
            "from": "peoples",
            "localField": "peoplefriend",
            "foreignField": "_id",
            "as": "friendinfo"
        }},
        {"$unwind": "$friendinfo"},
        {"$sort": {"peoplename": 1, "age": 1}},  
        {"$limit": 50},  
    ]
    results = peoples.aggregate(pipeline)
    
    for result in results:
        print(f"Name: {result['peoplename']}, Age: {result['age']}, Friend: {result['friendinfo']}")

def main():
    num_docs = 10000
    logging.info("Starting document generation...")
    generate_and_insert_documents(num_docs)
    
    logging.info("Querying and sorting friends...")
    query_and_sort_friends()

if __name__ == "__main__":
    main()
