import json
from faker import Faker
fake = Faker()

def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def generate_document(field_config):
    document = {}
    for field, details in field_config.items():
        if details['type'] == 'name':
            document[field] = fake.name()
        elif details['type'] == 'address':
            document[field] = fake.address()
        elif details['type'] == 'email':
            document[field] = fake.email()
        elif details['type'] == 'text':
            document[field] = fake.text()
    return document

def main():
    doc_config = load_config('config_doc.json')
    general_config = load_config('config.json')

    documents = []
    for _ in range(general_config['num_documents']):
        documents.append(generate_document(doc_config['fields']))

    print(documents)

if __name__ == "__main__":
    main()
