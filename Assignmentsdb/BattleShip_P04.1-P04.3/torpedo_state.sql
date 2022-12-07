CREATE TABLE IF NOT EXISTS public.torpedo_state
(
    ship_id numeric NOT NULL,
    torpedo_id numeric NOT NULL,
    speed numeric,
    location text COLLATE pg_catalog."default",
    name text COLLATE pg_catalog."default",
    CONSTRAINT torpedo_state_pkey PRIMARY KEY (ship_id, torpedo_id),
    CONSTRAINT fk_name FOREIGN KEY (name)
        REFERENCES public.torpedo (name),
    CONSTRAINT fk_ship FOREIGN KEY (ship_id)
        REFERENCES public.ship (ship_id) 
)

TABLESPACE pg_default;