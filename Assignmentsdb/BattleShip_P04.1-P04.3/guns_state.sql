CREATE TABLE IF NOT EXISTS public.gun_state
(
    ship_id numeric NOT NULL,
    gun_id numeric NOT NULL,
    bearing double precision,
    elevation double precision,
    ammo numeric,
    CONSTRAINT gun_state_pkey PRIMARY KEY (ship_id, gun_id),
    CONSTRAINT pk_ship FOREIGN KEY (ship_id)
        REFERENCES public.ship (ship_id) 
)

TABLESPACE pg_default;