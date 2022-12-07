CREATE TABLE IF NOT EXISTS public.gun
(
    name text COLLATE pg_catalog."default" NOT NULL,
    info text COLLATE pg_catalog."default",
    mm numeric,
    ammocat text COLLATE pg_catalog."default",
    ammotype text COLLATE pg_catalog."default",
    propellantkg numeric,
    rof numeric,
    turnrate numeric,
    CONSTRAINT gun_pkey PRIMARY KEY (name)
)

TABLESPACE pg_default;