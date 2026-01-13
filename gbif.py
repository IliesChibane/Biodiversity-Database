import requests
import json
import os
import time
import sys
import logging
from datetime import datetime
from group_1 import infer_groupe_1
from group_2 import infer_groupe_2
from wikidata_id import get_external_ids_from_gbif_taxon
from images import get_images
from vernacular_name import get_vernacular_names_from_gbif_taxon
from publish_supabase import publish_to_supabase, query_supabase

BASE = "https://api.gbif.org/v1"

# -----------------------
# Setup logging
# -----------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gbif_processing.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# -----------------------
# Load whitelist
# -----------------------
with open("species_zip/whitelist.txt") as f:
    species_whitelist = {
        int(line.strip())
        for line in f
        if line.strip().isdigit()
    }

print(f"✅ Loaded {len(species_whitelist)} GBIF species IDs from whitelist")

# -----------------------
# Main loop with auto-restart
# -----------------------
while True:
    try:
        counter = 1
        logger.info(f"Starting processing run at {datetime.now()}")
        
        # -----------------------
        # Iterate ONLY whitelist
        # -----------------------
        for taxon_key in species_whitelist:
            print(f"\n=== [{counter}/{len(species_whitelist)}] ===")
            counter += 1
            print(f"\n🔍 Processing taxon {taxon_key}")
            
            if query_supabase(gbif_key=taxon_key):
                print("⏩ Already in Supabase, skipping")
                continue

            # Skip already processed
            if (
                os.path.exists(f"With_cdref/{taxon_key}.json")
                or os.path.exists(f"Without_cdref/{taxon_key}.json")
            ):
                print("⏩ Already processed, skipping")
                continue

            # -----------------------
            # Fetch species core data
            # -----------------------
            r = requests.get(
                f"{BASE}/species/{taxon_key}",
                timeout=60
            )

            if r.status_code != 200:
                print(f"[WARN] Failed to fetch species {taxon_key}")
                continue

            sp = r.json()

            # -----------------------
            # Extract taxonomy
            # -----------------------
            scientific_name = sp.get("scientificName")
            kingdom = sp.get("kingdom")
            phylum = sp.get("phylum")
            class_ = sp.get("class")
            order = sp.get("order")
            family = sp.get("family")
            genus = sp.get("genus")
            rank = sp.get("rank")
            habitat = sp.get("habitats")

            taxa = {
                "kingdom": kingdom,
                "phylum": phylum,
                "class": class_,
                "order": order
            }

            # -----------------------
            # External IDs
            # -----------------------
            ids = get_external_ids_from_gbif_taxon(taxon_key)
            cdref = ids.get("CD_REF", [None])[0]

            # -----------------------
            # Media + vernaculars
            # -----------------------
            images = get_images(taxon_key)
            vernaculars = get_vernacular_names_from_gbif_taxon(taxon_key)

            french_name = vernaculars.get("fr", [None])[0]
            english_name = vernaculars.get("en", [None])[0]

            # -----------------------
            # Final object
            # -----------------------
            template = {
                "Nom scientifique": scientific_name,
                "Rank_Id": "",
                "Classification EEE": "",
                "Status": {"CDG": ""},
                "Genre": genus,
                "Habitat": habitat,
                "Nom anglais": english_name,
                "images": images,
                "Classe": class_,
                "Nom francais": french_name,
                "Embranchement": phylum,
                "Regne": kingdom,
                "Famille": family,
                "Groupe_2": infer_groupe_2(taxa),
                "Groupe_3": "",
                "Groupe_1": infer_groupe_1(taxa),
                "Ordre": order,
                "Type espece": "",
                "CD_REF": cdref,
                "other_ids": {
                        "GBIF": taxon_key,
                        "INaturalist": ids.get("iNaturalist taxon ID", [])
                    }
            }

            # -----------------------
            # Save
            # -----------------------
            print(f"💾 Saving taxon {taxon_key} (CD_REF: {cdref})")
            publish_to_supabase(template)

            time.sleep(0.2)  # be polite
        
        # If we complete all items, exit successfully
        logger.info("✅ All items processed successfully")
        break
        
    except KeyboardInterrupt:
        logger.info("⚠️ Script interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Error occurred: {type(e).__name__}: {str(e)}")
        logger.error(f"Restarting in 5 seconds...")
        time.sleep(5)  # Wait before restart to avoid rapid restart loops
        continue
