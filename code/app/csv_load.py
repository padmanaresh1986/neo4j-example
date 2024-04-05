from neo4j import GraphDatabase
import csv
import json
import re

uri = "bolt://localhost:7687"  # Update with your Neo4j connection details
username = "neo4j"
password = "complaints"


def csv_to_json(csv_file):
    json_data = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            json_data.append(row)
    return json_data


def get_headers(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
    headers = [sanitize(header) for header in headers]
    return headers


def create_node_cypher(label, properties):
    prop_list = ', '.join([f"{key}: ${key}" for key in properties])
    return f"CREATE (:{label} {{{prop_list}}})"


def remove_special_and_numeric(string):
    return re.sub(r'[^a-zA-Z]', '', string)


def create_nodes_from_csv(cypher_query, csv_file, session):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            complaint_data = {sanitize(k): v for k, v in row.items()}  # Remove spaces from keys
            session.run(cypher_query, **complaint_data)


def sanitize(k):
    return remove_special_and_numeric(' '.join(word.capitalize() for word in k.replace("-", " ").split()))


def create_node_queries():
    node_data = {
        "Complaint": ["ComplaintId", "DateReceived", "SubmittedVia",
                      "DateSentToCompany", "Tags", "ConsumerComplaintNarrative"],
        "Company": ["Company", "State", "ZipCode"],
        "Product": ["Product", "SubProduct"],
        "Issue": ["Issue", "SubIssue"],
        "Response": ["TimelyResponse", "ConsumerDisputed", "CompanyResponseToConsumer",
                     "ConsumerConsentProvided", "CompanyPublicResponse"]
    }
    return node_data


def main():
    csv_file = 'resources/complaints_100.csv'
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        node_data = create_node_queries()
        for node, properties in node_data.items():
            cypher_query = create_node_cypher(node, properties)
            create_nodes_from_csv(cypher_query, csv_file, session)
        print("Done")


if __name__ == "__main__":
    main()
