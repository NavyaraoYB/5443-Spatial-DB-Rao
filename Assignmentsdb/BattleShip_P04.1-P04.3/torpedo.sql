CREATE TABLE IF NOT EXISTS public.torpedo
(
    name text COLLATE pg_catalog."default" NOT NULL,
    guidance text COLLATE pg_catalog."default",
    diameter numeric,
    speed numeric,
    kg numeric,
    warheadsize numeric,
    range numeric,
    CONSTRAINT torpedo_pkey PRIMARY KEY (name)
)

TABLESPACE pg_default;