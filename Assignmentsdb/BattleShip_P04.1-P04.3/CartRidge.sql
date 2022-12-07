
CREATE TABLE IF NOT EXISTS public.cartridge
(
    name text COLLATE pg_catalog."default" NOT NULL,
    mm numeric,
    kg numeric,
    ms numeric,
    explosive numeric,
    CONSTRAINT cartridge_pkey PRIMARY KEY (name)
)
TABLESPACE pg_default;

