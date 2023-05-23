def initdb():
	import mysql.connector as ms

	con=ms.connect(host='192.168.0.175',user='ubuntu',password='123456')
	cur=con.cursor()

	#initial creation of db and tables if not existing in MySQL database'
	cur.execute('create database if not exists taxi')
	cur.execute('use taxi')
	cur.execute('create table if not exists taxi_bkgs(bkgid varchar(6) primary key,bkgtime datetime,start varchar(50),end varchar(50),jdate date,jtime time,taxitype varchar(50))')
	cur.execute('create table if not exists bus_bkgs(bkgid varchar(6) primary key,bkgtime datetime,pass_no int,start varchar(50),end varchar(50),jdate date,jtime time,bustype varchar(50))')
	cur.execute('create table if not exists users(uuid varchar(6) primary key,fname varchar(50),email varchar(50),num varchar(10),uname varchar(50),passwd varchar(50))')
	cur.execute('create table if not exists payment_details(pay_id varchar(6) primary key,paytime datetime,bkgid varchar(6),amt int,payment_type varchar(20),cardno varchar(16),cardname varchar(50),cvv int(3),exp_month int(2),exp_year int(4))')
	cur.execute('create table if not exists employees(emp_id varchar(5) primary key,emp_uname varchar(50),emp_name varchar(50),emp_passwd varchar(50))')
	cur.execute('create table if not exists admin(admin_id varchar(5) primary key,admin_uname varchar(50),admin_name varchar(50),admin_passwd varchar(50))')

	try:	#creates root and demo users IF NOT EXISTS
		cur.execute("insert into admin values('A0001','root','System Administrator','123456')")
		cur.execute("insert into employees values('E0001','demoagent','Demonstration Agent','demoagent')")
		cur.execute("insert into users values('U00001','Demonstration User','demo@abc.com','1234567890','demo','demo')")
	except:
		pass

	con.commit()
