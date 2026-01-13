BACTERIA_GROUPS = {
    "Cyanobacteria": "Cyanobactéries",
    "Proteobacteria": "Protéobactéries"
}

FUNGI_GROUP_1 = {
    "Ascomycota": "Ascomycètes",
    "Basidiomycota": "Basidiomycètes",
    "Chytridiomycota": "Chytridiomycètes",
    "Myxomycota": "Myxomycètes"
}

PLANT_GROUP_1 = {
    "Bryophyta": "Bryophytes",
    "Marchantiophyta": "Bryophytes",
    "Anthocerotophyta": "Bryophytes",
}

TRACHEOPHYTES_CLASSES = {
    "Magnoliopsida",
    "Liliopsida",
    "Pinopsida",
    "Polypodiopsida"
}

ALGAL_PHYLA = {
    "Chlorophyta",
    "Charophyta",
    "Rhodophyta",
    "Ochrophyta",
    "Bacillariophyta"
}


ANIMAL_PHYLA_GROUP_1 = {
    "Chordata": "Chordés",
    "Arthropoda": "Arthropodes",
    "Mollusca": "Mollusques",
    "Echinodermata": "Echinodermes",
    "Porifera": "Porifères",
    "Cnidaria": "Cnidaires",
    "Ctenophora": "Cténaires",
    "Bryozoa": "Bryozoaires",
    "Onychophora": "Onychophores",
    "Tardigrada": "Tardigrades",
    "Rotifera": "Rotifères",
    "Gastrotricha": "Gastrotriches",
    "Sipuncula": "Siponcles"
}


WORM_PHYLA = {
    "Annelida",
    "Nematoda",
    "Platyhelminthes",
    "Nemertea",
    "Acanthocephala"
}


PROTOZOA_PHYLA = {
    "Foraminifera": "Foraminifères"
}


def infer_groupe_1(taxon: dict) -> str:
    kingdom = taxon.get("kingdom")
    phylum = taxon.get("phylum")
    class_ = taxon.get("class")

    # 1. Bacteria
    if kingdom == "Bacteria" and phylum in BACTERIA_GROUPS:
        return BACTERIA_GROUPS[phylum]

    # 2. Algae (legacy grouping)
    if phylum in ALGAL_PHYLA:
        return "Algues"

    # 3. Fungi
    if kingdom == "Fungi" and phylum in FUNGI_GROUP_1:
        return FUNGI_GROUP_1[phylum]

    # 4. Plants
    if kingdom == "Plantae":
        if phylum in PLANT_GROUP_1:
            return PLANT_GROUP_1[phylum]
        if class_ in TRACHEOPHYTES_CLASSES:
            return "Trachéophytes"

    # 5. Animals
    if kingdom == "Animalia":
        if phylum in ANIMAL_PHYLA_GROUP_1:
            return ANIMAL_PHYLA_GROUP_1[phylum]
        if phylum in WORM_PHYLA:
            return "Vers"

    # 6. Protists
    if phylum in PROTOZOA_PHYLA:
        return PROTOZOA_PHYLA[phylum]

    return "Autres"
