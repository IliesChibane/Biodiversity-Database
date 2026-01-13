from supabase import create_client

supabase = create_client(
    "http://127.0.0.1:54321",
    "secret key"
)

def publish_to_supabase(doc: dict):
    row = {
    "regne": doc.get("Regne"),
    "embranchement": doc.get("Embranchement"),
    "classe": doc.get("Classe"),
    "ordre": doc.get("Ordre"),
    "famille": doc.get("Famille"),
    "genre": doc.get("Genre"),
    "nom_scientifique": doc.get("Nom scientifique"),
    "payload": doc
}

    supabase.table("taxa").insert(row).execute()
    print(f"Published {doc.get('Nom scientifique')} to Supabase")
    
def query_supabase(taxon_name: str = None, classe: str = None, gbif_key: int = None):
    if taxon_name:
        response = supabase.table("taxa").select("*").eq("nom_scientifique", taxon_name).execute()
        return response.data
    if classe:
        response = supabase.table("taxa").select("*").eq("classe", classe).execute()
        return response.data
    if gbif_key:
        response = supabase.table("taxa").select("*").eq("payload->other_ids->>GBIF", str(gbif_key)).execute()
        return True if response.data else False
    return []

