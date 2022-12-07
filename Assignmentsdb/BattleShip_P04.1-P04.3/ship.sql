CREATE TABLE IF NOT EXISTS public.ship
(
    ship_id numeric NOT NULL,
    identifier text COLLATE pg_catalog."default",
    category text COLLATE pg_catalog."default",
    shipclass text COLLATE pg_catalog."default",
    displacement numeric,
    length numeric,
    width numeric,
    torpedolaunchers json,
    armament json,
    armor json,
    speed numeric,
    turn_radius numeric,
    CONSTRAINT ship_pkey PRIMARY KEY (ship_id)
)

TABLESPACE pg_default;