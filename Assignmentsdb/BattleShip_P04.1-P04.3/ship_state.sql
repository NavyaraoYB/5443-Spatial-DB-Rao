CREATE TABLE IF NOT EXISTS public.ship_state
(
    ship_id numeric NOT NULL,
    bearing double precision,
    speed numeric,
    location json,
    geom geometry,
    CONSTRAINT ship_state_pkey PRIMARY KEY (ship_id),
    CONSTRAINT fk_ship FOREIGN KEY (ship_id)
        REFERENCES public.ship (ship_id)
)

TABLESPACE pg_default;