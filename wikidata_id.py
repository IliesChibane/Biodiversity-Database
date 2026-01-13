import requests

WIKIDATA_SPARQL_URL = "https://query.wikidata.org/sparql"

HEADERS = {
    "User-Agent": "OLGA-Stack/1.0 (contact: ilies.chibane@u-pec.fr)",
    "Accept": "application/sparql-results+json"
}

def get_external_ids_from_gbif_taxon(gbif_taxon_id: int) -> dict:
    sparql_query = f"""
    SELECT ?propertyLabel ?value WHERE {{
      ?item wdt:P846 "{gbif_taxon_id}" .
      ?item ?prop ?value .
      ?property wikibase:directClaim ?prop .

      FILTER(STRSTARTS(STR(?prop), STR(wdt:)))

      SERVICE wikibase:label {{
        bd:serviceParam wikibase:language "en".
      }}
    }}
    """

    response = requests.post(
        WIKIDATA_SPARQL_URL,
        headers=HEADERS,
        data={"query": sparql_query},
        timeout=30
    )

    response.raise_for_status()

    if not response.text.strip():
        raise RuntimeError("Wikidata SPARQL returned an empty response")

    data = response.json()

    identifiers = {}

    for row in data["results"]["bindings"]:
        prop_label = row["propertyLabel"]["value"]
        value = row["value"]["value"]

        # 🔧 Normalize TAXREF → CD_REF
        if prop_label == "TAXREF ID":
            prop_label = "CD_REF"

        identifiers.setdefault(prop_label, []).append(value)

    return identifiers


# ids = get_external_ids_from_gbif_taxon(2480537)

# for k, v in ids.items():
#     print(f"{k}: {v}")
