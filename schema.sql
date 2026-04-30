create table if not exists driver (
                driver_id serial primary key,
                name varchar(100),
                license_type varchar(50)
                );
                
                create table if not exists vehicle (
                vehicle_id serial primary key,
                license_plate varchar(20) unique,
                model varchar(50),
                driver_id int unique,
                foreign key (driver_id) references driver(driver_id)
                );
                
                create table if not exists route (
                route_id serial primary key,
                date date,
                service_zone varchar(100),
                driver_id int,
                foreign key (driver_id) references driver(driver_id)
                );
                
                create table if not exists package (
                package_id serial primary key,
                description varchar(250),
                weight decimal(10,2) check (weight > 0),
                route_id int,
                foreign key (route_id) references route(route_id)
                );