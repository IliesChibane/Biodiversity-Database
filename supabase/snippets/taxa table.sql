create table public.taxa (
    id uuid primary key default gen_random_uuid(),

    -- Core taxonomy (queryable)
    regne text,
    embranchement text,
    classe text,
    ordre text,
    famille text,
    genre text,
    nom_scientifique text,

    -- Your Firebase document (as-is)
    payload jsonb not null,

    created_at timestamptz default now()
);
