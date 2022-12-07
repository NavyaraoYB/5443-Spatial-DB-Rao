CREATE TABLE IF NOT EXISTS public.ships_guns
(
    ship_id numeric NOT NULL,
    gun_id numeric NOT NULL,
    type text COLLATE pg_catalog."default",
    pos numeric,
    CONSTRAINT ships_guns_pkey PRIMARY KEY (ship_id, gun_id),
    CONSTRAINT fk_ship FOREIGN KEY (ship_id)
        REFERENCES public.ship (ship_id)
)

TABLESPACE pg_default;