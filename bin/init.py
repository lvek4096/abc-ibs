import tkinter as tk
import os
import mysql.connector as ms
from tkinter import scrolledtext


con=ms.connect(host='localhost',user='john',password='123456')
cur=con.cursor()

#initial creation of db and tables if not existing in system.
cur.execute('create database if not exists taxi')
cur.execute('use taxi')
cur.execute('create table if not exists taxi_bkgs(bkgid int primary key,start varchar(50),end varchar(50),taxitype varchar(50))')
cur.execute('create table if not exists bus_bkgs(bkgid int primary key,pass_no int,start varchar(50),end varchar(50),jdate date,jtime time,bustype varchar(50))')
cur.execute('create table if not exists users(uuid varchar(5) primary key,uname varchar(50),passwd varchar(50))')
cur.execute('create table if not exists payment_details(pay_id varchar(5) primary key,bkgid int,amt int,payment_type varchar(20),cardno int(16),cardname varchar(50),cvv int(3),exp_month int(2),exp_year int(4))')
cur.execute('create table if not exists employees(emp_id varchar(5) primary key,emp_uname varchar(50),emp_name varchar(50),emp_passwd varchar(50))')
cur.execute('create table if not exists admin(admin_id varchar(5) primary key,admin_uname varchar(50),admin_name varchar(50),admin_passwd varchar(50))')
con.commit()