import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
#============================================
def get_connection():
  conn = psycopg2.connect(
    host = os.getenv("DB_HOST"),
    port = os.getenv("DB_PORT"),
    dbname = os.getenv("DB_NAME"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASS")
  )
  return conn
#=============================================

#=============================================================================
def init_db():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
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
                """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("Table Created✅")
#====================================================================================

#==============CRUD==================================================================
#DRIVER

def create_driver(name, license_type):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
       "insert into driver (name, license_type) values (%s, %s)",
       (name, license_type)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_drivers():
   conn = get_connection()
   cur = conn.cursor()

   cur.execute("select * from driver")
   data = cur.fetchall()

   cur.close()
   conn.close()
   return data


#VEHICLE============================
def create_vehicle(license_plate, model, driver_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        insert into vehicle (license_plate, model, driver_id)
        values  (%s, %s, %s)
    """, (license_plate, model, driver_id))

    conn.commit()
    cur.close()
    conn.close()


def get_vehicles():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("select * from vehicle")
    data = cur.fetchall()

    cur.close()
    conn.close()
    return data

#ROUTE=================

def create_route(date, service_zone, driver_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        insert into route (date, service_zone, driver_id)
        values  (%s, %s, %s)
    """, (date, service_zone, driver_id))

    conn.commit()
    cur.close()
    conn.close()


def get_routes():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("select * from route")
    data = cur.fetchall()

    cur.close()
    conn.close()
    return data


    #PACKAGE==============

def create_package(description, weight, route_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        insert into package (description, weight, route_id)
        values  (%s, %s, %s)
    """, (description, weight, route_id))

    conn.commit()
    cur.close()
    conn.close()


def get_packages():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("select * from package")
    data = cur.fetchall()

    cur.close()
    conn.close()
    return data

