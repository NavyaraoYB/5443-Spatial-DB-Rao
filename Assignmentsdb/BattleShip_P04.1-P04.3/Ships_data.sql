CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;

CREATE TABLE IF NOT EXISTS public.CardinalDegrees
(
    direction character varying(3) COLLATE pg_catalog."default" NOT NULL,
    start_degree numeric(11,8),
    middle_degree numeric(11,8),
    end_degree numeric(11,8)
);

ALTER TABLE IF EXISTS public.cardinaldegrees
    OWNER to postgres;
	
select * from CardinalDegrees
select * from Ships_data

CREATE TABLE IF NOT EXISTS public.ships
(
    id integer,
    category text,
    shipClass text,
    length integer,
    width integer,
    torpedoLaunchers json NULL,
    armament json,
    hullArmor integer,
    deckArmor integer,
    speed integer,
    turnRadius integer,
    location GEOMETRY(POINT,4326) NULL,
    bearing float,
    CONSTRAINT ships_pkey PRIMARY KEY (id)
);

DROP INDEX IF EXISTS public.ships_location_idx;
