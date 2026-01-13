create index idx_taxa_classe on taxa (classe);
create index idx_taxa_genre on taxa (genre);
create index idx_taxa_nom_scientifique on taxa (nom_scientifique);
create index idx_taxa_payload_gin on taxa using gin (payload);