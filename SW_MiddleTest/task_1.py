from SPARQLWrapper import SPARQLWrapper, JSON

# Define the SPARQL endpoint
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

# Define your SPARQL query
query = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?city ?cityName ?foundingDate
WHERE {
  ?city a dbo:City ;
        dbo:country dbr:Ukraine ;
        dbo:foundingDate ?foundingDate;
        rdfs:label ?cityName .
  FILTER (lang(?cityName) = "uk")
}
ORDER BY DESC(?foundingDate)
LIMIT 1
"""

# Set the query and the return format
sparql.setQuery(query)
sparql.setReturnFormat(JSON)

# Execute the query and get results
results = sparql.query().convert()

# Print the results
for result in results["results"]["bindings"]:
    city = result["city"]["value"]
    city_name = result["cityName"]["value"]
    founding_date = result["foundingDate"]["value"]
    print(f"City: {city_name}, URI: {city}, Founding Date: {founding_date}")
