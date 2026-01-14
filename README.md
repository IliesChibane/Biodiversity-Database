# Documentation Projet Scrapping Data Biodiversité

## Etape 1 : Créer un compte sur GBIF

Il est essentiel de créer un compte sur GBIF pour pouvoir accéder aux données.

Un compte peut etre créer sur le site de GBIF : https://www.gbif.org/

## Etape 2 : Setup le projet

- Installer Supabase sur votre ordinateur (via npm) :bash
  

```bash
npm install supabase --save-dev
```

- Installer Python3
  
- Récupérer le projet via Github : [GitHub - IliesChibane/Biodiversity-Database](https://github.com/IliesChibane/Biodiversity-Database#)
  
  ```bash
  git clone https://github.com/IliesChibane/Biodiversity-Database.git
  cd Biodiversity-Database
  ```
  
- Une fois dans le projet lancer la commande dans le terminal :
  

```bash
pip install -r requirements.txt
```

- Lancer la commande :
  

```bash
npx supabase start
```

Une fois fait vous aurez accès a une secrète key copier la et ajouter au script python `publish_supabase.py` a l'endroit assigner.

## Etape 3 : Télécharger les données de Gbif

Pour récupérer les occurrences d’espèces via l’API GBIF, il faut lancer la commande suivante dans un terminal :

```bash
curl -u "<nom_utilisateur_Gbif>:<mdp_gbif>" \
  -X POST "https://api.gbif.org/v1/occurrence/download/request" \
  -H "Content-Type: application/json" \
  -d '{
    "creator": "<nom_utilisateur_Gbif>",
    "notification_address": ["<email_utilisateur_Gbif>"],
    "predicate": {
      "type": "and",
      "predicates": [
        { "type": "equals", "key": "COUNTRY", "value": "<code_pays>" },
        { "type": "equals", "key": "TAXON_KEY", "value": "<code_espece>" }
      ]
    }
  }'
```

- `<nom_utilisateur_GBIF>` : **votre login GBIF** (pas l’email)
  
- `<mot_de_passe_GBIF>` : **le mot de passe associé** à ce compte
  
- `"creator"` : doit **exactement correspondre au login GBIF** utilisé pour `-u`
  
- `"notification_address"` : **adresse email**
  
- `<code_pays>` : code ISO-2 du pays pour lequel vous voulez les occurrences  
  Exemples :
  
  - France → `FR`
    
  - Italie → `IT`
    
  - Roumanie → `RO`
    
  - Croatie → `HR`
    
- `<code_espece>` : **GBIF Taxon Key** du groupe ou de l’espèce que vous voulez  
  Exemples  :
  
  | Groupe/Classe | TAXON_KEY |
  | --- | --- |
  | Mammalia | 359 |
  | Aves (Oiseaux) | 212 |
  | Reptilia | 358 |
  | Amphibia | 131 |
  | Insecta | 216 |
  | Tracheophyta | 6   |
  

La commande renvoie un **ID de téléchargement**, par exemple :

```bash
0069742-251120083545085
```

**Note importante :** GBIF ne permet que 3 téléchargement simultanément créer donc 2 comptes pour faire un seul et meme pays en meme temps est donc conseillé.

Pour suivre l'état du téléchargement il faut utiliser la commande suivante :

```bash
curl -s https://api.gbif.org/v1/occurrence/download/<ID_de_téléchargement>| jq
```

Quand le statut est `SUCCEEDED`, le fichier est téléchargeable au format ZIP (DWCA) via la commande :

```bash
curl -L -o <Nom_fichier>.zip "https://api.gbif.org/v1/occurrence/download/request/<ID_de_téléchargement>.zip"
```

**Note Importante :** dans le terminal avant de lancer cette commande assurer d'etre dans le dossier **species_zip** du projet.

## Etape 4 : Extraire les ID unique des espèces

Une fois les zip dans le dossier **species_zip** retourner dans le projet et lancer et lancer cette commande :

```bash
python3 species_zip/extract.py <path/to/input.zip> <path/to/output.txt>
```

`<path/to/input.zip>` : le path du fichier ZIP

`<path/to/output.txt>` : le path du fichier txt généré (Appelez le a chaque `species_keys_<specie>.txt`)

Lancer cette commande pour chaque zip a la suite pour économiser du temps ils seront tous exécuter en parralèle.

Une fois tout les txt pour les espèces d'un pays obtenu lancer la commande :

```bash
python3 combine_species_keys.py
```

Vous obtiendrez ainsi la whitelist.txt pour le pays concerné

## Etape 5 : Ajouter les espèces a supabase :

Une fois la whitelist d'un pays obtenu lancer simplement la commande :

```bash
python3 gbif.py
```

Le script est fait de manière à gérer automatiquement les doublons et à se relancer en cas de crash donc il suffit juste de le lancer tourner jusqu'a la fin de l'exécution (cela peut prendre quelques heures ou meme quelques jours)
