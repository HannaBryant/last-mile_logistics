import psycopg2
from psycopg2.extras import RealDictCursor
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

    cur.execute("create schema if not exists lmlogistics;")

    cur.execute("""
              create table if not exists lmlogistics.driver (
                driver_id serial primary key,
                name varchar(100),
                license_type varchar(50)
                );
                
                create table if not exists lmlogistics.vehicle (
                vehicle_id serial primary key,
                license_plate varchar(20) unique,
                model varchar(50),
                driver_id int unique,
                foreign key (driver_id) references lmlogistics.driver(driver_id)
                );
                
                create table if not exists lmlogistics.route (
                route_id serial primary key,
                date date,
                service_zone varchar(100),
                driver_id int,
                foreign key (driver_id) references lmlogistics.driver(driver_id)
                );
                
                create table if not exists lmlogistics.package (
                package_id serial primary key,
                description varchar(250),
                weight decimal(10,2) check (weight > 0),
                route_id int,
                foreign key (route_id) references lmlogistics.route(route_id)
                );
                """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("complete!")
#====================================================================================

#==============CRUD==================================================================
#DRIVER

def create_driver(name, license_type):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
       "insert into lmlogistics.driver (name, license_type) values (%s, %s)",
       (name, license_type)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_drivers():
   conn = get_connection()
   cur = conn.cursor(cursor_factory=RealDictCursor)

   cur.execute("select * from lmlogistics.driver")
   data = cur.fetchall()

   cur.close()
   conn.close()
   return data

def update_driver(driver_id, name, license_type):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""update lmlogistics.driver set name=%s, license_type=%s where driver_id=%s""",
    (name, license_type, driver_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_driver(driver_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""delete from lmlogistics.driver where driver_id=%s""", (driver_id,))
    conn.commit()
    cur.close()
    conn.close()




#VEHICLE============================
def create_vehicle(license_plate, model, driver_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        insert into lmlogistics.vehicle (license_plate, model, driver_id)
        values  (%s, %s, %s)
    """, (license_plate, model, driver_id))

    conn.commit()
    cur.close()
    conn.close()


def get_vehicles():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("select * from lmlogistics.vehicle")
    data = cur.fetchall()

    cur.close()
    conn.close()
    return data

def update_vehicle(vehicle_id, license_plate, model):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""update lmlogistics.vehicle set license_plate=%s, model=%s where vehicle_id=%s""",
    (license_plate, model, vehicle_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_vehicle(vehicle_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""delete from lmlogistics.vehicle where vehicle_id=%s""", (vehicle_id,))
    conn.commit()
    cur.close()
    conn.close()

#ROUTE=================

def create_route(date, service_zone, driver_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        insert into lmlogistics.route (date, service_zone, driver_id)
        values  (%s, %s, %s)
    """, (date, service_zone, driver_id))

    conn.commit()
    cur.close()
    conn.close()


def get_routes():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("select * from lmlogistics.route")
    data = cur.fetchall()

    cur.close()
    conn.close()
    return data

def update_route(route_id, service_zone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "update lmlogistics.route set service_zone=%s where route_id=%s",
        (service_zone, route_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_route(route_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "delete from lmlogistics.route where route_id=%s",
        (route_id,)
    )
    conn.commit()
    cur.close()
    conn.close()


    #PACKAGE==============

def create_package(description, weight, route_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        insert into lmlogistics.package (description, weight, route_id)
        values  (%s, %s, %s)
    """, (description, weight, route_id))

    conn.commit()
    cur.close()
    conn.close()


def get_packages():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("select * from lmlogistics.package")
    data = cur.fetchall()

    cur.close()
    conn.close()
    return data

def update_package(package_id, description, weight):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "update lmlogistics.package set description=%s, weight=%s where package_id=%s",
        (description, weight, package_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_package(package_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "delete from lmlogistics.package where package_id=%s",
        (package_id,)
    )
    conn.commit()
    cur.close()
    conn.close()