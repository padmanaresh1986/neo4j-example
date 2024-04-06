from neo4j import GraphDatabase
import csv
import re
import os

from app.config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD


class Neo4jService:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def get_headers(self, csv_file):
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)
        headers = [self.sanitize(header) for header in headers]
        return headers

    @staticmethod
    def create_node_cypher(label, properties):
        prop_list = ', '.join([f"{key}: ${key}" for key in properties])
        return f"MERGE (c:{label} {{{prop_list}}})"

    @staticmethod
    def create_constraint_cypher(label, node_property):
        return f"CREATE CONSTRAINT IF NOT EXISTS FOR (c:{label}) REQUIRE c.{node_property} IS UNIQUE"

    @staticmethod
    def remove_special_and_numeric(string):
        return re.sub(r'[^a-zA-Z]', '', string)

    def create_nodes_from_csv(self, cypher_query, csv_file, session):
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                complaint_data = {self.sanitize(k): v for k, v in row.items()}  # Remove spaces from keys
                session.run(cypher_query, **complaint_data)

    def sanitize(self, k):
        return self.remove_special_and_numeric(' '.join(word.capitalize() for word in k.replace("-", " ").split()))

    def create_nodes(self, node_data, file_name):
        with self.driver.session() as session:
            for node, properties in node_data.items():
                cypher_query = self.create_node_cypher(node, properties)
                self.create_nodes_from_csv(cypher_query, file_name, session)
        print("Nodes created successfully.")

    def create_constraints(self, constraints):
        with self.driver.session() as session:
            for label, node_property in constraints.items():
                cypher_query = self.create_constraint_cypher(label, node_property)
                session.run(cypher_query)
        print("Constraints created successfully.")

    def create_edges(self, edges_data, file_name):
        with self.driver.session() as session:
            for edge in edges_data:
                cypher_query = self.create_edge_cypher(edge)
                self.create_nodes_from_csv(cypher_query, file_name, session)
        print("Edges created successfully.")

    @staticmethod
    def create_edge_cypher(edge):
        source = edge["source"]
        dest = edge["destination"]
        return f'MATCH (b:{dest["node"]}), (a:{source["node"]}) WHERE a.{source["key"]} = ${source["key"]} AND b.{dest["key"]} = ${dest["key"]} CREATE (b)-[:{edge["label"]}]->(a)'

