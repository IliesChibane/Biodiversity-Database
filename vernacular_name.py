import requests

WIKIDATA_SPARQL_URL = "https://query.wikidata.org/sparql"

HEADERS = {
    "User-Agent": "OLGA-Stack/1.0 (contact: ilies.chibane@u-pec.fr)",
    "Accept": "application/sparql-results+json"
}


def get_vernacular_names_from_gbif_taxon(gbif_taxon_id: int) -> dict:
    sparql_query = f"""
    SELECT ?label ?lang WHERE {{
      ?item wdt:P846 "{gbif_taxon_id}" .
      ?item rdfs:label ?label .
      BIND(LANG(?label) AS ?lang)
    }}
    """

    response = requests.get(
        WIKIDATA_SPARQL_URL,
        headers=HEADERS,
        params={
            "query": sparql_query,
            "format": "json"
        },
        timeout=30
    )

    response.raise_for_status()
    data = response.json()

    names = {"fr": [], "en": []}

    for row in data["results"]["bindings"]:
        lang = row["lang"]["value"]
        label = row["label"]["value"]

        if lang in names:
            names[lang].append(label)
    
    if len(names["fr"]) == 0:
        names["fr"] = [None]
    if len(names["en"]) == 0:
        names["en"] = [None]
    return names


if __name__ == "__main__":
    print(get_vernacular_names_from_gbif_taxon(2480537))

