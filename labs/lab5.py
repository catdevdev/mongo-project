from pymongo import MongoClient

# MongoDB setup
client = MongoClient('mongodb://neko-neki:neko-neki@18.153.75.45:32000')
db = client.lab4
col1 = db.collection1
col2 = db.collection2

def fetch_initial_documents(collection, limit):
    """ Fetch the first 'limit' documents from a specified collection """
    return list(collection.find({}, {'_id': 1, 'name': 1, 'friend': 1}).limit(limit))

def display_document_chain(start_id, max_depth):
    """ Display a chain of documents starting from a given document ID """
    current_id = start_id
    current_collection = col1
    other_collection = col2
    chain = []

    for _ in range(max_depth):
        document = current_collection.find_one({'_id': current_id})
        if not document or 'friend' not in document:
            break
        chain.append(document)
        current_id = document['friend']
        current_collection, other_collection = other_collection, current_collection

    for doc in chain:
        print(f"Doc ID: {doc['_id']}, Name: {doc['name']}, Friend: {doc.get('friend', 'None')}")

def main():
    N = 10  # Number of documents to fetch from Collection 1
    M = 10  # Number of documents to fetch from Collection 2
    i = 1000  # Starting document ID for the chain
    MAXK = 10  # Maximum number of elements in the chain

    print("First N documents from Collection 1:")
    initial_docs_col1 = fetch_initial_documents(col1, N)
    for doc in initial_docs_col1:
        print(doc)

    print("\nFirst M documents from Collection 2:")
    initial_docs_col2 = fetch_initial_documents(col2, M)
    for doc in initial_docs_col2:
        print(doc)

    print("\nDocument chain starting from document ID", i, "with maximum length", MAXK)
    display_document_chain(i, MAXK)

if __name__ == "__main__":
    main()
