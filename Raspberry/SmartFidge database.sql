CREATE TABLE fridge
(
    fid integer NOT NULL,
    name varchar(25) NOT NULL,
    actualtemperature real,
    desiredtemperature real,
    humidity real,
    CONSTRAINT fridge_pkey PRIMARY KEY (fid)
);

CREATE TABLE product
(
    pid character varying(10) NOT NULL,
    name character varying(50) NOT NULL,
    expirationdate date,
    weight real,
    infridge boolean NOT NULL,
    fridge integer,
    CONSTRAINT product_pkey PRIMARY KEY (pid),
    CONSTRAINT product_fridge_fkey FOREIGN KEY (fridge)
        REFERENCES public.fridge (fid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE public.transaction
(
    tid integer NOT NULL,
    userphoto bytea,
    "timestamp" timestamp without time zone,
    product character varying(10) ,
    gotin boolean,
    CONSTRAINT transaction_pkey PRIMARY KEY (tid),
    CONSTRAINT transaction_product_fkey FOREIGN KEY (product)
        REFERENCES public.product (pid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE OR REPLACE FUNCTION check_infridge_f() RETURNS TRIGGER AS
$BODY$
BEGIN
    
  UPDATE product
  set infridge = NEW.gotIn
  WHERE pID = NEW.product;
  RETURN NEW;

END;
$BODY$
language plpgsql;

CREATE TRIGGER check_infridge AFTER INSERT ON transaction FOR EACH ROW EXECUTE PROCEDURE check_infridge_f();

insert into fridge values ('0', 'SmartFridge', 26, 5, 50);
