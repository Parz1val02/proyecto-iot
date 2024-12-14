--tabla de los labs
create table iot.lab( id serial primary key, name varchar(255), module varchar (255) );


--tabla de conteo
create table iot.message( id serial primary key, lab_id INT not null, count INT not null, timestamp timestamptz not null, constraint fk_lab foreign key (lab_id) references iot.lab(id) )
