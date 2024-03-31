# neo4j-example

Download dataset from 

https://catalog.data.gov/dataset/consumer-complaint-database


To load data into Neo4J database

place csv file in below location
C:\Users\DELL\.Neo4jDesktop\relate-data\dbmss\dbms-c8d8276f-567a-427e-9bb4-c1230984e17c\import


then create below Indexes
CREATE CONSTRAINT FOR (c:Complaint) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT FOR (c:Company) REQUIRE c.name IS UNIQUE;
CREATE CONSTRAINT FOR (c:Response) REQUIRE c.name IS UNIQUE;


Then run below query to load data

CALL {
  // Load data from CSV
  LOAD CSV WITH HEADERS FROM 'file:///complaints.csv' AS line
  // Splitting the date
  WITH line, SPLIT(line.`Date received`, '/') AS date
  LIMIT 50000
  // Create nodes and relationships
  CREATE (complaint:Complaint {id: toInteger(line.`Complaint ID`)})
  SET complaint.year = toInteger(date[2]),
      complaint.month = toInteger(date[0]),
      complaint.day = toInteger(date[1])

  MERGE (company:Company {name: line.Company})
  MERGE (response:Response {name: line.`Company response to consumer`})

  CREATE (complaint)-[:AGAINST]->(company)
  CREATE (response)-[resp:TO]->(complaint)
  
  SET resp.timely = CASE line.`Timely response?` WHEN 'Yes' THEN true ELSE false END,
      resp.disputed = CASE line.`Consumer disputed?` WHEN 'Yes' THEN true ELSE false END
}

