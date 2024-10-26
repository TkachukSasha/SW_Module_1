from SPARQLWrapper import SPARQLWrapper, JSON


def query_wikidata():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """
    SELECT ?company ?companyLabel ?foundingDate WHERE {
          ?company wdt:P31 wd:Q4830453;  # Q4830453 - business enterprise
                  wdt:P17 wd:Q212;        # Q212 - Ukraine
                  wdt:P452 wd:Q11661;     # Q11661 - Information technology
                  wdt:P571 ?foundingDate. # P571 - founding date
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    ORDER BY ASC(?foundingDate)
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


def query_dbpedia():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?company ?label ?foundingDate
    WHERE {
        ?company dbo:location dbr:Ukraine .
        ?company dbo:industry ?industry .
        ?company rdfs:label ?label .
        OPTIONAL { ?company dbo:foundingDate ?foundingDate }
        FILTER (lang(?label) = "en")
        FILTER (?industry IN (dbr:Information_technology, dbr:Software_industry, dbr:Technology_company))
    }
    ORDER BY ASC(?foundingDate)
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


def main():
    print("Choose the source for your query:")
    print("1. Wikidata")
    print("2. DBpedia")

    choice = input("Enter 1 or 2: ")

    if choice == '1':
        results = query_wikidata()
    elif choice == '2':
        results = query_dbpedia()
    else:
        print("Invalid choice.")
        return

    print("\nResults:")
    for result in results["results"]["bindings"]:
        company_name = result.get("companyLabel", {}).get("value", "N/A")
        founding_date = result.get("foundingDate", {}).get("value", "N/A")
        print(f"Company: {company_name}, Founding Date: {founding_date}")


if __name__ == "__main__":
    main()
