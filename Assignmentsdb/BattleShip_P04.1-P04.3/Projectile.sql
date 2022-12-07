
-- Table: public.projectile

-- DROP TABLE IF EXISTS public.projectile;

CREATE TABLE IF NOT EXISTS public.projectile
(
    name text COLLATE pg_catalog."default" NOT NULL,
    mm numeric,
    kg numeric,
    CONSTRAINT projectile_pkey PRIMARY KEY (name)
)

TABLESPACE pg_default;

-- ALTER TABLE IF EXISTS public.projectile
--     OWNER to postgres;

