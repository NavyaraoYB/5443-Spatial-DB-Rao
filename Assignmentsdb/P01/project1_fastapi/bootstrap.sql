create extension if not exists postgis;
DROP table IF EXISTS switzerland_new;


CREATE TABLE switzerland_new

(name varchar,osm_type varchar,class varchar,type varchar, 	lon	float,lat float,	place_rank varchar, importance varchar,	street	varchar,city varchar,	county varchar, state varchar,country	varchar, country_code	varchar, display_name	varchar,west varchar,	south	varchar,east	varchar,north	varchar,wikidata varchar,wikipedia varchar);


COPY switzerland_new FROM '/users/shyam/Downloads/switzerland_new.csv' WITH  (HEADER TRUE, FORMAT csv ) ;


alter table switzerland_new add column distance geometry; 

Update switzerland_new SET distance= ST_Point(lon, lat);