create database taxi;
use taxi;
create table taxi_bkgs(bkgid int primary key,start varchar(50),end varchar(50),jdate date,jtime time);
create table users(uuid varchar(5) primary key,uname varchar(50),passwd varchar(50));
