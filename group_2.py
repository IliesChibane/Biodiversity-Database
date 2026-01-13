CLASS_TO_GROUPE2 = {
    "Aves": "Oiseaux",
    "Mammalia": "Mammifères",
    "Amphibia": "Amphibiens",
    "Reptilia": "Reptiles",
    "Actinopterygii": "Poissons",
    "Chondrichthyes": "Poissons",
    "Ascidiacea": "Ascidies",
    "Sarcopterygii": "Poissons",
    "Myxini": "Poissons",
    "Petromyzonti": "Poissons",
    "Elasmobranchii": "Poissons", # Subclass of Chondrichthyes often used
    "Holocephali": "Poissons"
}

PHYLUM_CLASS_COMBOS = {
    ("Arthropoda", "Insecta"): "Insectes",
    ("Arthropoda", "Arachnida"): "Arachnides",
    ("Arthropoda", "Crustacea"): "Crustacés",
    ("Arthropoda", "Myriapoda"): "Myriapodes",
    ("Arthropoda", "Pycnogonida"): "Pycnogonides",
    ("Arthropoda", "Entognatha"): "Entognathes"
}

MOLLUSCA_CLASSES = {
    "Bivalvia": "Bivalves",
    "Cephalopoda": "Céphalopodes",
    "Gastropoda": "Gastéropodes"
}


PLANT_DIVISIONS = {
    "Magnoliopsida": "Angiospermes",
    "Liliopsida": "Angiospermes",
    "Pinopsida": "Gymnospermes",
    "Polypodiopsida": "Ptéridophytes",
    "Bryophyta": "Mousses",
    "Marchantiophyta": "Hépatiques et Anthocérotes",
    "Anthocerotophyta": "Hépatiques et Anthocérotes",
    "Lycopodiopsida": "Ptéridophytes", # Often grouped with ferns
    "Equisetopsida": "Ptéridophytes"
}

ALGAL_GROUPS = {
    "Chlorophyta": "Chlorophytes et Charophytes",
    "Charophyta": "Chlorophytes et Charophytes",
    "Ochrophyta": "Ochrophytes",
    "Rhodophyta": "Rhodophytes",
    "Bacillariophyta": "Diatomées"
}

FUNGI_GROUPS = {
    "Ascomycota": "Lichens",
    "Basidiomycota": "Lichens"
}


PHYLUM_ONLY = {
    "Annelida": "Annélides",
    "Nematoda": "Nématodes",
    "Nemertea": "Némertes",
    "Platyhelminthes": "Plathelminthes",
    "Acanthocephala": "Acanthocéphales",
    "Cnidaria": "Hydrozoaires",  # refined below
    "Chordata": None  # handled by class rules
}


CNIDARIA_ORDER = {
    "Octocorallia": "Octocoralliaires",
    "Scleractinia": "Scléractiniaires",
    "Hydrozoa": "Hydrozoaires"
}

def infer_groupe_2(taxon: dict) -> str:
    kingdom = taxon.get("kingdom")
    phylum = taxon.get("phylum")
    class_ = taxon.get("class")
    order = taxon.get("order")

    # 1. Class-based vertebrates
    if class_ in CLASS_TO_GROUPE2:
        return CLASS_TO_GROUPE2[class_]

    # 2. Arthropods
    if (phylum, class_) in PHYLUM_CLASS_COMBOS:
        return PHYLUM_CLASS_COMBOS[(phylum, class_)]

    # 3. Molluscs
    if phylum == "Mollusca" and class_ in MOLLUSCA_CLASSES:
        return MOLLUSCA_CLASSES[class_]

    # 4. Plants
    if kingdom == "Plantae" and class_ in PLANT_DIVISIONS:
        return PLANT_DIVISIONS[class_]

    # 5. Algae
    if phylum in ALGAL_GROUPS:
        return ALGAL_GROUPS[phylum]

    # 6. Fungi / lichens
    if kingdom == "Fungi" and phylum in FUNGI_GROUPS:
        return FUNGI_GROUPS[phylum]

    # 7. Cnidarians
    if phylum == "Cnidaria":
        if class_ in CNIDARIA_ORDER:
            return CNIDARIA_ORDER[class_]
        return "Hydrozoaires"

    # 8. Other phyla
    if phylum in PHYLUM_ONLY:
        return PHYLUM_ONLY[phylum]

    return "Autres"


if __name__ == "__main__":
    taxon_example = {
        "kingdom": "Animalia",
        "phylum": "Chordata",
        "class": "Aves",
        "order": "Acciptriformes",
    }

    groupe_2 = infer_groupe_2(taxon_example)
    print(f"Groupe 2: {groupe_2}")  # Expected: "Oiseaux"