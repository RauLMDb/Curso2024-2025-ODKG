# -*- coding: utf-8 -*-
"""Task08.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18P0xTS31q1P7nR4efg0Yy3QrClOxqMAe

**Task 08: Completing missing data**
"""

# !pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/"

from rdflib import Graph, Namespace, Literal, URIRef

g1 = Graph()
g2 = Graph()
g1.parse(github_storage + "resources/data01.rdf", format="xml")
g2.parse(github_storage + "resources/data02.rdf", format="xml")

"""Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas."""


# Define the namespaces
EX = Namespace("http://example.org/")

# Query to get all persons from the first graph
query_persons = """
    PREFIX ex: <http://example.org/>
    SELECT ?person
    WHERE {
        ?person a ex:Person .
    }
"""

# Query to get given name, family name, and email from the second graph
query_details = """
    PREFIX ex: <http://example.org/>
    SELECT ?person ?givenName ?familyName ?email
    WHERE {
        ?person a ex:Person ;
                ex:givenName ?givenName ;
                ex:familyName ?familyName ;
                ex:email ?email .
    }
"""

# Execute the queries
persons = g1.query(query_persons)
details = g2.query(query_details)

# Create a dictionary to store details from the second graph
details_dict = {}
for row in details:
    details_dict[row.person] = {
        "givenName": row.givenName,
        "familyName": row.familyName,
        "email": row.email,
    }

# Iterate over persons in the first graph and complete missing details
for row in persons:
    person = row.person
    if person in details_dict:
        if (person, EX.givenName, None) not in g1:
            g1.add((person, EX.givenName, details_dict[person]["givenName"]))
        if (person, EX.familyName, None) not in g1:
            g1.add((person, EX.familyName, details_dict[person]["familyName"]))
        if (person, EX.email, None) not in g1:
            g1.add((person, EX.email, details_dict[person]["email"]))

# Print the updated graph
for stmt in g1:
    print(stmt)
