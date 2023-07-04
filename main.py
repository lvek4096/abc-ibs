#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Separator
from tkinter import scrolledtext

import pandas as pd
import mysql.connector as ms
import ctypes
import random as rd
import os
import platform as pf
from datetime import datetime,timedelta
from escpos.printer import Network

# Build string
build='ibs.beta-334'
build_timestamp='2023-07-04 16:46:21'	

dev_string=str('[UNDER CONSTRUCTION] '+build+', '+build_timestamp)

# Fonts for GUI
if pf.system()=='Windows':
	fnt=('Cascadia Mono',12)
	fntb=('Cascadia Mono',12,'bold')
	fntit=('Cascadia Mono',12,'italic')
	fntbit=('Cascadia Mono',12,'bold italic')
	h1fnt=('Segoe UI Variable Display',24,'bold')
	h2fnt=('Segoe UI Variable Text',12)
	menufnt=('Cascadia Mono',11)
elif pf.system()=='Linux':
	fnt=('Ubuntu Mono',12)
	fntb=('Ubuntu Mono',12,'bold')
	fntit=('Ubuntu Mono',12,'italic')
	fntbit=('Ubuntu Mono',12,'bold italic')
	h1fnt=('Ubuntu',24)
	h2fnt=('Ubuntu',12)
	menufnt=('Ubuntu Mono',11)

# Enables DPI scaling awareness on supported Windows versions
if pf.system()=='Windows':
	try:
		ctypes.windll.shcore.SetProcessDpiAwareness(True)
	except:
		pass

# Defines stops
locations=['Blackcastle','Westerwitch','Ironlyn','North Ganking','Goldsnow','Aldcourt','Bridgehedge','Glasspond','Winterglass','Northcrest','Orlake','Clearhedge','Estermount','Shorebush','Greenfay']

def init():																						# Initalisation function
	
	def init_program():																			# Initialises IBS.
	
		def initdb():															# Initialises database.
			# ensure MySQL connection and cursor variables are global (i.e. accessible across the entire program, and not confined to a single function)
			global con
			global cur
			host=inp_host.get()
			uname=inp_uname.get()
			passwd=inp_passwd.get()

			try:																# Tries connecting to db with provided credentials
				con=ms.connect(host=host,user=uname,password=passwd)
			except:
				try:															# If providec credentials are invalid, fall back to defaults (root@localhost)
					messagebox.showerror('Error','Incorrect hostname or credentials provided.\nFalling back to default credentials.')
					con=ms.connect(host='localhost',user='root',password='123456')
				except:															# Terminates the program if no database is found on localhost						
					messagebox.showerror('Error','RDBMS not found on localhost.\nThe program will terminate.')
					quit()

			if con.is_connected():												# Successful connection message
				messagebox.showinfo('','Successfully connected to database on '+con.server_host+'.',parent=ibs_init_win)
				ibs_init_win.destroy()
			cur=con.cursor()

			# initial creation of db and tables (if not exists) in MySQL database
			cur.execute('create database if not exists taxi')
			cur.execute('use taxi')
			cur.execute('create table if not exists taxi_bkgs(bkgid varchar(6) primary key,bkgtime datetime,start varchar(50),end varchar(50),jdate date,jtime time,taxitype varchar(50))')
			cur.execute('create table if not exists bus_bkgs(bkgid varchar(6) primary key,bkgtime datetime,pass_no int,start varchar(50),end varchar(50),jdate date,jtime time,bustype varchar(50))')
			cur.execute('create table if not exists tkt_details(tktid char(9) primary key, bkgid varchar(6), timestamp datetime)')
			# cur.execute('create table if not exists users(uuid varchar(6) primary key,fname varchar(50),email varchar(50),num varchar(10),uname varchar(50),passwd varchar(50))')
			cur.execute('create table if not exists payment_details(pay_id varchar(6) primary key,paytime datetime,bkgid varchar(6),amt int,payment_type varchar(20),cardno varchar(16),cardname varchar(50),cvv int(3),exp_month int(2),exp_year int(4))')
			cur.execute('create table if not exists employees(emp_id varchar(5) primary key,emp_uname varchar(50),emp_name varchar(50),emp_passwd varchar(50))')
			cur.execute('create table if not exists admin(admin_id varchar(5) primary key,admin_uname varchar(50),admin_name varchar(50),admin_passwd varchar(50))')
			
			# creates root and demo users IF NOT EXISTS
			try:	
				cur.execute("insert into admin values('A0001','root','System Administrator','root')")
				cur.execute("insert into employees values('E0001','demo','Demonstration Agent','demo')")
				# cur.execute("insert into users values('U00001','Demonstration User','demo@abc.com','1234567890','demo','demo')")
			except:
				pass
			
			con.commit()
		
		def prconnect():																		# Initialises printer.
			# ensure printer status variable is global (i.e. accessible across the entire program, and not confined to a single function)
			global isPrintingEnabled
			isPrintingEnabled=False

			# Enables or disables printer support
			if pr_con_type.get()=='N':	
				if not printer_ip_input.get()=='' and not printer_ip_input.get().isspace():
					global pr_ip
					pr_ip=printer_ip_input.get()
					try:										# Test connection to printer, disable printing if connection fails.
						Network(pr_ip)
						isPrintingEnabled=True
					except:
						messagebox.showerror('Error','Unable to connect to printer.\nThe printing functionality will be disabled.',parent=ibs_init_win)
						isPrintingEnabled=False
				else:											# Disables printing if IP address for printer is left blank
					messagebox.showerror('Error','No IP address for printer specified.\nThe printing functionality will be disabled.',parent=ibs_init_win)
					isPrintingEnabled=False

			elif pr_con_type.get()=='D':							
				messagebox.showinfo('Info','The printing functionality will be disabled.',parent=ibs_init_win)
				isPrintingEnabled=False

		if pr_con_type.get() in ['N','D']:														# Invokes init functions if printer choice is correct.
			prconnect()
			initdb()
			emp_main()
			con.close()
		else:
			messagebox.showerror('Error','Please select printer connection option.')

	# Disable/enables N/W printer IP address  entry box
	def disable_nw_ip():
		printer_ip_input.configure(state='disabled')
		printer_ip_input.update()

	def enable_nw_ip():
		printer_ip_input.configure(state='normal')
		printer_ip_input.update()

	ibs_init_win=tk.Tk()
	ibs_init_win.title('ABC-IBS '+dev_string)
	ibs_init_win.resizable(False, False)
	icon=tk.PhotoImage(file='img/icon.png')
	ibs_init_win.iconphoto(False,icon)

	tk.Label(ibs_init_win,text='IBS configuration options',font=h1fnt,justify=tk.LEFT).grid(column=0,row=0,padx=10,columnspan=2,sticky=tk.W)
	
	tk.Label(ibs_init_win,text='RDBMS Configuration',font=h2fnt,justify=tk.LEFT).grid(column=0,row=1,padx=10,columnspan=2,sticky=tk.W)
	tk.Label(ibs_init_win,text='If no RDBMS login credentials are specified,\nit will fall back to those of root@localhost.',font=menufnt,justify=tk.LEFT).grid(column=0,row=4,padx=10,pady=10,columnspan=2,sticky=tk.W)

	tk.Label(ibs_init_win,text='Host',font=fnt).grid(column=0,row=8,sticky=tk.E,padx=10,pady=10)
	inp_host=tk.Entry(ibs_init_win,font=fnt)
	inp_host.grid(column=1,row=8,sticky=tk.EW,padx=10,pady=10)

	tk.Label(ibs_init_win,text='User',font=fnt).grid(column=0,row=9,sticky=tk.E,padx=10,pady=10)
	inp_uname=tk.Entry(ibs_init_win,font=fnt)
	inp_uname.grid(column=1,row=9,sticky=tk.EW,padx=10,pady=10)

	tk.Label(ibs_init_win,text='Password',font=fnt).grid(column=0,row=10,sticky=tk.E,padx=10,pady=10)
	inp_passwd=tk.Entry(ibs_init_win,show='*',font=fnt)
	inp_passwd.grid(column=1,row=10,sticky=tk.EW,padx=10,pady=10)

	tk.Label(ibs_init_win,text='ESC/POS Printer Configuration',font=h2fnt,justify=tk.LEFT).grid(column=0,row=12,padx=10,columnspan=2,sticky=tk.W)
	tk.Label(ibs_init_win,text='If connection to printer cannot be made,\nprinting functionality will be automatically disabled.',font=menufnt,justify=tk.LEFT).grid(column=0,row=13,padx=10,pady=10,columnspan=2,sticky=tk.W)

	pr_con_type=tk.StringVar(ibs_init_win)
	# ttk.Radiobutton(init_window, text = 'USB',variable = pr_con_type,value = 'U',command=disable_nw_ip).grid(column=0,row=14,sticky=tk.W,padx=10)
	
	ttk.Radiobutton(ibs_init_win, text = 'Network (enter IP address: )',variable = pr_con_type,value = 'N',command=enable_nw_ip).grid(column=0,row=15,sticky=tk.W,padx=10)
	printer_ip_input=tk.Entry(ibs_init_win,font=fnt,state='disabled')
	printer_ip_input.grid(column=1,row=15,sticky=tk.EW,padx=10,pady=10)

	ttk.Radiobutton(ibs_init_win, text = 'Disable printing',variable = pr_con_type,value = 'D',command=disable_nw_ip).grid(column=0,row=16,sticky=tk.W,padx=10)

	submit=tk.Button(ibs_init_win,text='Continue',command=init_program,font=fntit)
	submit.grid(column=1,row=20,padx=10,pady=10,sticky=tk.E)
	ibs_init_win.bind('<Return>',lambda event:init_program())

	submit=tk.Button(ibs_init_win,text='About ABC-IBS',command=about,font=fntit)
	submit.grid(column=0,row=20,padx=10,pady=10,sticky=tk.W)

	ibs_init_win.mainloop()

def about():																		# About page

	credits_txt='''
Developed by
Amadeus Software
for ABC Lines
'''
	about=tk.Toplevel()
	abttitle='About this program'
	about.resizable(False, False)
	about.title(abttitle)
	icon=tk.PhotoImage(file='img/icon.png')
	about.iconphoto(False,icon)

	# Headings
	tk.Label(about,text='Integrated Booking System (IBS)',font=h1fnt).grid(column=0,row=0,columnspan=3)
	tk.Label(about,text=(''+build+'\n('+build_timestamp+')'),font=fnt).grid(column=0,row=1,columnspan=3)
	
	logo_img=tk.PhotoImage(file='img/amadeus.png')
	logo=tk.Label(about,image=logo_img)
	logo.grid(column=0,row=2,padx=10,pady=10)
	logo.image=logo_img

	credits=tk.Label(about,font=fntbit,text=credits_txt,justify=tk.LEFT)
	credits.grid(row=2,column=2,sticky=tk.NSEW,padx=10,pady=10)
	
	Separator(about,orient='horizontal').grid(column=0,row=5,sticky=tk.EW,padx=10,pady=10,columnspan=3)
	
	# Platform information
	pyimgsrc=tk.PhotoImage(file='img/python.png')
	pyimg=tk.Label(about,image=pyimgsrc)
	pyimg.image=pyimgsrc
	pyimg.grid(column=0,row=6)

	tk.Label(about,text=('Python',pf.python_version()),font=fnt).grid(column=0,row=7,padx=10)
	tk.Label(about,text=('Tkinter',tk.TkVersion),font=fnt).grid(column=0,row=8,padx=10)
	try:
		tk.Label(about,text=('MySQL',con.get_server_info()),font=fnt).grid(column=0,row=9,padx=10)
	except:
		tk.Label(about,text=('MySQL server is inactive.'),font=fntit).grid(column=0,row=9,padx=10)

	if pf.system()=='Windows':
		src=tk.PhotoImage(file='img/win.png')
	elif pf.system()=='Darwin':										# Darwin - macOS
		src=tk.PhotoImage(file='img/macos.png')	
	elif pf.system()=='Linux':
		src=tk.PhotoImage(file='img/linux.png')

	osimg=tk.Label(about,image=src)
	osimg.image=src
	osimg.grid(column=2,row=6,padx=10,pady=10)

	# OS info
	if pf.system()=='Windows':										# Additional info - Windows ONLY
		tk.Label(about,text=(pf.system()+' '+pf.release()+'\n(Build '+pf.version()+')'),font=fntb).grid(column=2,row=7,padx=10)
	else:
		tk.Label(about,text=(pf.system(),pf.release()),font=fntb).grid(column=2,row=7,padx=10)
	
	if pf.system()=='Linux':										# Additional distribution info - Linux ONLY
		try:
			linux=pf.freedesktop_os_release()
			tk.Label(about,text=(linux['NAME']+' '+linux['VERSION']),font=fntit).grid(column=2,row=8,padx=10)
		except:
			pass
	else:
		pass

	Separator(about,orient='horizontal').grid(column=0,row=10,sticky=tk.EW,padx=10,pady=10,columnspan=3)
	
	# Hostname and CPU type (e.g.i386 (32-bit); AMD64/x86_64 (64-bit) etc.)
	tk.Label(about,text=pf.node(),font=fntbit).grid(column=0,row=11,columnspan=3,padx=10)
	tk.Label(about,text=(pf.machine()+' system'),font=fnt).grid(column=0,row=12,columnspan=3,padx=10)
	Separator(about,orient='horizontal').grid(column=0,row=16,sticky=tk.EW,padx=10,pady=10,columnspan=3)
	
	# Database additional details
	try:
		dbinfohdg=tk.Label(about,text='MySQL database details:',font=fntbit)
		dbinfohdg.grid(column=0,row=18,columnspan=3,padx=10)
		
		dbinfo=tk.Label(about,text='Connected to database \''+con.database+'\''+' on '+con.server_host,font=fnt)
		dbinfo.grid(column=0,row=19,columnspan=3,padx=10)
	except:
		dbinfohdg=tk.Label(about,text='MySQL database inactive',font=fntbit)
		dbinfohdg.grid(column=0,row=18,columnspan=3,padx=10)
		
		dbinfo=tk.Label(about,text='Database details not available!',font=fnt)
		dbinfo.grid(column=0,row=19,columnspan=3,padx=10)
	Separator(about,orient='horizontal').grid(column=0,row=24,sticky=tk.EW,padx=10,pady=10,columnspan=3)

	img1=tk.PhotoImage(file='icons/close.png')
	cls=tk.Button(about,font=fnt,text='Close',image=img1,command=about.destroy)
	cls.grid(column=0,row=25,padx=10,pady=10,columnspan=3)
	cls.image=img1

def bus_booking():																	# Bus booking

	# Initialising the bus booking function
	busbkg_id='B'+str(rd.randint(10000,99999))													# Booking ID
	bus_type=['','Standard','Express','Premium']										# Bus type

	# Defining the window
	busbkg_win=tk.Toplevel()
	busbkg_win.title('Bus Booking')
	busbkg_win.resizable(False, False)
	icon=tk.PhotoImage(file='img/icon.png')
	busbkg_win.iconphoto(False,icon)

	def payment():									# The payment function
		
		# Taking of inputs
		origin=from_inp.get().capitalize()
		destination=to_inp.get().capitalize()
		date_of_journey=date_inp.get()
		time_of_journey=time_inp.get()
		bus_type=bustype_inp.get()
		passno=passno_inp.get()

		# Conversion and checking of datetime
		datetime_format='%Y-%m-%d %H:%M'												# YYYY-MM-DD HH:MM; MySQL datetime format
		x=datetime.now()+timedelta(minutes=45)											# minimum bkg time - 45 min from current time
		min_bkgtime_str=x.strftime(datetime_format)										# Converts above datetime to string to MySQL date format
		min_bkgtime=datetime.strptime(min_bkgtime_str,datetime_format)					# Converts string back to datetime object for comparision
		inpdate_str=date_of_journey+' '+time_of_journey														# Combines date and time inputs into correct format for comparision purpose

		isInpDateinFormat=True	
		try:																			# is date and time inputted in format?
			isInpDateinFormat=bool(datetime.strptime(inpdate_str,datetime_format))  	
		except ValueError:		
			isInpDateinFormat=False

		if isInpDateinFormat==True:		
			inp_dt=datetime.strptime(inpdate_str,datetime_format)						# Converts combined input to datetime for comparision

			if inp_dt >= min_bkgtime:													# Minimum bkg time - 45 min from now
				isNotPast=True
			else:
				isNotPast=False

			if inp_dt <= min_bkgtime+timedelta(days=1096):								# 3-year limit on dates entered
				isNotDistFuture=True
			else:
				isNotDistFuture=False

		# Checking of user inputs before proceeding to payment function
		if (not origin=='' and not origin.isspace()) and (not destination=='' and not destination.isspace()) and (not date_of_journey=='' and not date_of_journey.isspace()) and (not time_of_journey=='' and not time_of_journey.isspace()) and (not bus_type=='' and not bus_type.isspace()):
			if origin in locations and destination in locations:		
				if not origin == destination:
					if isInpDateinFormat==True and len(date_of_journey)==10 and len(time_of_journey)==5: 
						if isNotPast==True and isNotDistFuture==True:
							if payment_method.get() in ['R','C']:
							
								# calculation of fare on basis of type
								if bustype_inp.get()=='Standard':
									rate=5
								elif bustype_inp.get()=='Express':
									rate=10
								elif bustype_inp.get()=='Premium':
									rate=15

								payment_id='P'+str(rd.randint(10000,99999))	

								o=from_inp.get()
								d=to_inp.get()
								distance=abs((locations.index(d))-(locations.index(o)))*4	#distance between locations - 4 km.
								total_fare=(rate*distance)*passno

								# is it card (R) or cash?
								if payment_method.get()=='R':

									def card_payment():		# Card payment function
										# Takes inputs of payment details
										card_type=cardtype_inp.get()
										card_no=cardno_inp.get()
										card_name=cardname_inp.get()
										exp_year=expyear_inp.get()
										exp_month=expmonth_inp.get()
										cvv=cvv_inp.get()
										
										# Gets current month and year for card expiry date checking
										cur_dt=datetime.now()
										cur_mth=cur_dt.month
										cur_yr=cur_dt.year

										def bkg_confirmed():

											def clipboard():
												confirmmsg_win.clipboard_clear()
												confirmmsg_win.clipboard_append(summary_text)
												clipbd_btn.configure(fg='green',text='Copied!')
											
											def exit():
												confirmmsg_win.destroy()
												cardpay_window.destroy()
												busbkg_win.destroy()

											card_brand=''
											if card_no[0] == '3':
												card_brand='AMEX'
											elif card_no[0] == '4':
												card_brand='VISA'
											elif card_no[0] == '5':
												card_brand='MASTER'
											elif card_no[0] == '6':
												card_brand='DISCOVER'

											# Adding booking details to database
											bkg_time=datetime.now()									# 	Timestamp to mark bookings
											bkg_timestamp=bkg_time.strftime('%Y-%m-%d %H:%M:%S')	#	Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM
											
											sql='insert into bus_bkgs values (%s,%s,%s,%s,%s,%s,%s,%s)'
											val=(busbkg_id,bkg_timestamp,passno,origin,destination,date_of_journey,time_of_journey,bus_type)
											cur.execute(sql,val)
											con.commit()

											# Adds payment details to database
											pay_time=datetime.now()									#	Timestamp to mark payment
											pay_timestamp=pay_time.strftime('%Y-%m-%d %H:%M:%S')	#	Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM
											
											sql=('insert into payment_details values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
											val=(payment_id,pay_timestamp,busbkg_id,total_fare,card_type,card_no,card_name,cvv,exp_month,exp_year)
											cur.execute(sql,val)
											con.commit()

											# Confirmation popup
											confirmmsg_win=tk.Toplevel()
											confirmmsg_win.resizable(False,False)
											confirmmsg_win.title('Booking successful')
											icon=tk.PhotoImage(file='img/icon.png')
											confirmmsg_win.iconphoto(False,icon)

											tk.Label(confirmmsg_win,text='The booking has been\nsuccessfully made.',font=h1fnt,justify=tk.LEFT).grid(row=0,column=0,sticky=tk.W,padx=10,pady=10)

											summary=scrolledtext.ScrolledText(confirmmsg_win,font=fnt,width=30,height=8)
											summary.grid(column=0,row=3,sticky=tk.EW,padx=10,pady=10,columnspan=2)

											summary_text='\nBus Booking\n-----------\n\nBooking ID: '+busbkg_id+'\nBooking Timestamp: \n'+bkg_timestamp+'\n\nFrom: '+o+'\nTo: '+d+'\nType: '+bustype_inp.get()+'\n\nDate: '+date_of_journey+'\nTime: '+time_of_journey+'\n\nRate: $'+str(rate)+' per km\nDistance: '+str(distance)+' km\nNumber of passengers: '+str(passno)+'\n\nTotal fare: $'+str(total_fare)+'\n\nPayment\n-------\n\n'+'Payment ID: '+payment_id+'\nPaid by: '+cardtype_inp.get()+'\nCardholder name: '+cardname_inp.get()+'\nCard number: XXXX-XXXX-XXXX-'+cardno_inp.get()[-4:]+'\nCard type: '+card_brand+'\nAmount paid: $'+str(total_fare)+'\n\n------------------'+'\nPAYMENT SUCCESSFUL'+'\n------------------\n'
											summary.insert(tk.INSERT,summary_text)
											summary.configure(state='disabled')

											clipbd_btn=tk.Button(confirmmsg_win,text='Copy to clipboard',font=fnt,command=clipboard,justify=tk.CENTER)
											clipbd_btn.grid(row=5,column=0,padx=10,pady=10)
											
											if isPrintingEnabled==True:

												def receipt():

													def print_receipt():
														
														tkt_time=datetime.now()									#timestamp to mark ticket
														tkt_timestamp=tkt_time.strftime('%Y-%m-%d %H:%M:%S')	#Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM
														
														bar_no=str(rd.randint(1000000000000,9999999999999))
														tktid='TKT'+str(rd.randint(100000,999999))														
																		# title										# ticket details									# journey																																												# fare
														receipt_text='\nBus Booking '+busbkg_id+'\n------------\n\nTicket '+tktid+'\nTimestamp: \n'+tkt_timestamp+'\n\nNumber of passengers:'+str(passno)+'\nFrom: '+o+'\nTo: '+d+'\nType: '+bustype_inp.get()+'\n\nDate: '+date_of_journey+'\nTime: '+time_of_journey+'\nDistance: '+str(distance)+' km'+'\n\nTotal fare: $'+str(total_fare)+'\n\nPaid by: '+cardtype_inp.get()+'\n\nEnjoy your journey! Thank you for choosing ABC LINES!'+'\n------------------\n'
														
														sql=('insert into tkt_details values(%s,%s,%s)')
														#print(tktid,busbkg_id,tkt_timestamp)
														val=(tktid,busbkg_id,tkt_timestamp)
														cur.execute(sql,val)
														con.commit()

														pr.image('img/icon-2.png')
														pr.text(receipt_text)
														pr.barcode(bar_no, 'EAN13')
														pr.text('\n')
														pr.text('Powered by Amadeus')
														pr.text('\n')
														pr.text('Version: '+build+' ('+build_timestamp+')')
														pr.text('\n')
														
														if pf.system()=='Windows':
															pr.text('Platform: '+pf.system()+' '+pf.version())
														elif pf.system()=='Linux':
															pr.text('Platform: '+pf.system()+' '+pf.release())

														pr.cut()
														pr.close()
													
													try:
														pr = Network(pr_ip)
														print_receipt()
													except:
														messagebox.showerror('Error','Unable to print receipt.',parent=confirmmsg_win)

												print_btn=tk.Button(confirmmsg_win,text='Print...',font=fnt,command=receipt,justify=tk.CENTER)
												print_btn.grid(row=6,column=0,padx=10,pady=10)

											ok_btn=tk.Button(confirmmsg_win,text='OK',font=fnt,command=exit,justify=tk.CENTER)
											ok_btn.grid(row=8,column=0,padx=10,pady=10)
											confirmmsg_win.bind('<Return>',lambda event:exit())		
										
										#Payment details input checking
										if (not card_type=='' and not card_type.isspace()) and (not card_no=='' and not card_no.isspace()) and (not card_name=='' and not card_name.isspace()) and (not exp_year=='' and not exp_year.isspace()) and (not exp_month=='' and not exp_month.isspace()) and (not cvv=='' and not cvv.isspace()):
											if len(card_no) == 16 and card_no[0] in '3456':
												if len(exp_year) == 4 and int(exp_year) >= cur_yr:
													if int(exp_year) == cur_yr:						# If expiry year is same as current year
														if (len(exp_month) == 2) and (int(exp_month)>= 1 and int(exp_month) <= 12) and (int(exp_month) > cur_mth):
															if len(cvv)==3:
																bkg_confirmed()
															else:
																messagebox.showerror('Error','CVV must be a 3-digit number.',parent=cardpay_window)
														else:
															messagebox.showerror('Error','Invalid expiry month.',parent=cardpay_window)
													elif int(exp_year) > cur_yr:					# If expiry year is ahead of current year			
														if (len(exp_month) == 2) and (int(exp_month)>= 1 and int(exp_month) <= 12):
															if len(cvv)==3:
																bkg_confirmed()
															else:
																messagebox.showerror('Error','CVV must be a 3-digit number.',parent=cardpay_window)
														else:
															messagebox.showerror('Error','Invalid expiry month.',parent=cardpay_window)
													else:
														pass
												else:
													messagebox.showerror('Error','Invalid expiry year.',parent=cardpay_window)
											else:
												messagebox.showerror('Error','Invalid card number.',parent=cardpay_window)
										else:
											messagebox.showerror('Error','Please enter all required\npayment details.',parent=cardpay_window)

									cardpay_window=tk.Toplevel()
									cardpay_window.title('Payment Gateway')
									cardpay_window.resizable(False,False)
									icon=tk.PhotoImage(file='img/icon.png')
									cardpay_window.iconphoto(False,icon)

									f3=tk.Frame(cardpay_window)
									f3.grid(row=0,column=0)

									img1=tk.PhotoImage(file='icons/make-payment.png')
									img=tk.Label(f3,image=img1,font=h1fnt)
									img.grid(column=0,row=0,padx=10,pady=10)
									img.image=img1

									tk.Label(f3,text='Payment',font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

									f4=tk.Frame(cardpay_window)
									f4.grid(row=1,column=0)

									payment_summary=scrolledtext.ScrolledText(f4,font=fnt,width=25,height=5)
									payment_summary.grid(column=1,row=2,sticky=tk.EW,padx=10,pady=10)

									text='Booking ID: '+busbkg_id+'\nFrom: '+o+'\nTo: '+d+'\nType: '+bustype_inp.get()+'\n\nDate: '+date_of_journey+'\nTime: '+time_of_journey+'\n\nRate: $'+str(rate)+' per km\nDistance: '+str(distance)+' km\nNumber of passengers: '+str(passno)+'\n\nTotal fare: $'+str(total_fare)
									payment_summary.insert(tk.INSERT,text)
									payment_summary.configure(state='disabled')

									tk.Label(f4,text='Payment ID',font=fnt).grid(column=0,row=3,sticky=tk.E,padx=10,pady=10)
									payid=tk.Label(f4,text=payment_id,font=fnt)
									payid.grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

									cardtype_inp=tk.StringVar()
									tk.Label(f4,text='Pay by',font=fnt).grid(column=0,row=4,sticky=tk.E,padx=10,pady=10)
									card=('','Debit card','Credit card')
									pay_type=ttk.OptionMenu(f4,cardtype_inp,*card)
									pay_type.grid(column=1,row=4,sticky=tk.W,padx=10,pady=10)

									tk.Label(f4,text='Accepted cards',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
									
									img2=tk.PhotoImage(file='img/cards.png')
									cards_images=tk.Label(f4,image=img2,font=fnt)
									cards_images.grid(column=1,row=5,sticky=tk.W,padx=10,pady=10)
									cards_images.image=img2

									tk.Label(f4,text='Card number',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
									cardno_inp=tk.Entry(f4,font=fnt)
									cardno_inp.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

									tk.Label(f4,text='Cardholder name',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
									cardname_inp=tk.Entry(f4,font=fnt)
									cardname_inp.grid(column=1,row=7,sticky=tk.EW,padx=10,pady=10)

									tk.Label(f4,text='Expiry Year and Month\n[YYYY-MM]',font=fnt,justify=tk.RIGHT).grid(column=0,row=8,sticky=tk.E,padx=10,pady=10)
									expyear_inp=tk.Entry(f4,font=fnt,width=10)
									expyear_inp.grid(column=1,row=8,sticky=tk.EW,padx=10,pady=10)

									tk.Label(f4,text='-',font=fnt).grid(column=2,row=8,sticky=tk.EW,padx=10,pady=10)
									expmonth_inp=tk.Entry(f4,font=fnt,width=10)
									expmonth_inp.grid(column=3,row=8,sticky=tk.W,padx=10,pady=10)

									tk.Label(f4,text='CVV number',font=fnt).grid(column=0,row=9,sticky=tk.E,padx=10,pady=10)
									cvv_inp=tk.Entry(f4,font=fnt)
									cvv_inp.grid(column=1,row=9,sticky=tk.EW,padx=10,pady=10)

									submit_button=tk.Button(f4,font=fntit,text='Pay',command=card_payment,fg='green');submit_button.grid(column=1,row=10,padx=10,pady=10,sticky=tk.W)
									
									return_icon=tk.PhotoImage(file='icons/return.png')
									return_button=tk.Button(f4,font=fnt,image=return_icon,command=cardpay_window.destroy)
									return_button.grid(column=0,row=15,padx=10,pady=10,sticky=tk.SW)
									return_button.img=return_icon

									cardpay_window.bind('<Return>',lambda event:card_payment())		

								elif payment_method.get()=='C':
									
									def clipboard():
										confirmmsg_win.clipboard_clear()
										confirmmsg_win.clipboard_append(summary_text)
										clipbd_btn.configure(fg='green',text='Copied!')
									
									def exit():
										confirmmsg_win.destroy()
										busbkg_win.destroy()

									# Adding booking details to database
									bkg_time=datetime.now()									#	Timestamp to mark bookings
									bkg_timestamp=bkg_time.strftime('%Y-%m-%d %H:%M:%S')	#	Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM
								
									sql='insert into bus_bkgs values (%s,%s,%s,%s,%s,%s,%s,%s)'
									val=(busbkg_id,bkg_timestamp,passno,origin,destination,date_of_journey,time_of_journey,bus_type)
									cur.execute(sql,val)
									con.commit()

									# Adds payment details to database
									pay_time=datetime.now()									# 	Timestamp to mark payment
									pay_timestamp=pay_time.strftime('%Y-%m-%d %H:%M:%S')	#	Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM
									
									sql=('insert into payment_details values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
									val=(payment_id,pay_timestamp,busbkg_id,total_fare,'Cash',None,None,None,None,None)
									cur.execute(sql,val)
									con.commit()

									# Confirmation popup
									confirmmsg_win=tk.Toplevel()
									confirmmsg_win.resizable(False,False)
									confirmmsg_win.title('Booking successful')
									icon=tk.PhotoImage(file='img/icon.png')
									confirmmsg_win.iconphoto(False,icon)

									tk.Label(confirmmsg_win,text='The booking has been\nsuccessfully made.',font=h1fnt,justify=tk.LEFT).grid(row=0,column=0,sticky=tk.W,padx=10,pady=10)

									summary=scrolledtext.ScrolledText(confirmmsg_win,font=fnt,width=30,height=8)
									summary.grid(column=0,row=3,sticky=tk.EW,padx=10,pady=10,columnspan=2)

									summary_text='\nBus Booking\n-----------\n\nBooking ID: '+busbkg_id+'\nBooking Timestamp: \n'+bkg_timestamp+'\n\nFrom: '+o+'\nTo: '+d+'\nType: '+bustype_inp.get()+'\n\nDate: '+date_of_journey+'\nTime: '+time_of_journey+'\n\nRate: $'+str(rate)+' per km\nDistance: '+str(distance)+' km\nNumber of passengers: '+str(passno)+'\n\nTotal fare: $'+str(total_fare)+'\n\nPayment\n-------\n\n'+'Payment ID: '+payment_id+'\nPaid by: Cash'+'\nAmount paid: $'+str(total_fare)+'\n\n------------------'+'\nPAYMENT SUCCESSFUL'+'\n------------------\n'
									summary.insert(tk.INSERT,summary_text)
									summary.configure(state='disabled')
									
									clipbd_btn=tk.Button(confirmmsg_win,text='Copy to clipboard',font=fnt,command=clipboard,justify=tk.CENTER)
									clipbd_btn.grid(row=5,column=0,padx=10,pady=10)
									
									# Printing function
									if isPrintingEnabled==True:
										def receipt():

											def print_receipt():
												tkt_time=datetime.now()									#timestamp to mark ticket
												tkt_timestamp=tkt_time.strftime('%Y-%m-%d %H:%M:%S')	#Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM

												bar_no=str(rd.randint(1000000000000,9999999999999))
												tktid='TKT'+str(rd.randint(100000,999999))
															# title										# ticket details										# journey																																											# fare																																						
												receipt_text='\nBus Booking '+busbkg_id+'\n------------\n\nTicket '+tktid+'\nTimestamp: \n'+tkt_timestamp+'\n\nNumber of passengers:'+str(passno)+'\nFrom: '+o+'\nTo: '+d+'\nType: '+bustype_inp.get()+'\n\nDate: '+date_of_journey+'\nTime: '+time_of_journey+'\nDistance: '+str(distance)+' km'+'\n\nTotal fare: $'+str(total_fare)+'\n\nPaid by: Cash'+'\n\nEnjoy your journey! Thank you for choosing ABC LINES!'+'\n------------------\n'
												
												sql=('insert into tkt_details values(%s,%s,%s)')
												print(tktid,busbkg_id,tkt_timestamp)
												val=(tktid,busbkg_id,tkt_timestamp)
												cur.execute(sql,val)
												con.commit()

												pr.image('img/icon-2.png')
												pr.text(receipt_text)
												pr.barcode(bar_no, 'EAN13')
												pr.text('\n')
												pr.text('Powered by Amadeus')
												pr.text('\n')
												pr.text('Version: '+build+' ('+build_timestamp+')')
												pr.text('\n')
												
												if pf.system()=='Windows':
													pr.text('Platform: '+pf.system()+' '+pf.version())
												elif pf.system()=='Linux':
													pr.text('Platform: '+pf.system()+' '+pf.release())

												pr.cut()
												pr.close()

											try:
												pr = Network(pr_ip)
												print_receipt()
											except:
												messagebox.showerror('Error','Unable to print receipt.',parent=confirmmsg_win)

										print_btn=tk.Button(confirmmsg_win,text='Print...',font=fnt,command=receipt,justify=tk.CENTER)
										print_btn.grid(row=6,column=0,padx=10,pady=10)

									ok_btn=tk.Button(confirmmsg_win,text='OK',font=fnt,command=exit,justify=tk.CENTER)
									ok_btn.grid(row=10,column=0,padx=10,pady=10)
									confirmmsg_win.bind('<Return>',lambda event:exit())		

							else:
								messagebox.showerror('Error','Please select payment method',parent=busbkg_win)	
						else:
							messagebox.showerror('Error','Invalid timing entered.',parent=busbkg_win)
					else:
						messagebox.showerror('Error','Invalid date or time format entered.',parent=busbkg_win)
				else:
					messagebox.showerror('Error','The origin and destination are the same.',parent=busbkg_win)
			else:
				messagebox.showerror('Error','Invalid origin or destination.',parent=busbkg_win)
		else:
			messagebox.showerror('Error','Please do not leave any fields blank.',parent=busbkg_win)
	
	#FRAME 1
	f1=tk.Frame(busbkg_win)
	f1.grid(row=0,column=0)

	tk.Label(f1,text='BUS BOOKING',font=h1fnt,fg='blue').grid(column=1,row=0,padx=10,pady=10)

	#FRAME 2
	f2=tk.Frame(busbkg_win)
	f2.grid(row=1,column=0)

	#Booking ID
	tk.Label(f2,text='ID',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
	bkgid_label=tk.Label(f2,text=busbkg_id,font=fnt)
	bkgid_label.grid(column=1,row=5,sticky=tk.W,padx=10,pady=10)

	#Input fields
	tk.Label(f2,text='Number of passengers',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
	passno_inp=tk.IntVar()
	pass_no=tk.Scale(f2,from_=1,to=10,orient='horizontal',variable=passno_inp,font=fnt)
	pass_no.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

	bustype_inp=tk.StringVar()
	tk.Label(f2,text='Bus Type',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
	bustype=ttk.OptionMenu(f2,bustype_inp,*bus_type)
	bustype.grid(column=1,row=7,sticky=tk.W,padx=10,pady=10)

	tk.Label(f2,text='From',font=fnt).grid(column=0,row=8,sticky=tk.E,padx=10,pady=10)
	l=tk.StringVar()
	from_inp=ttk.Combobox(f2,textvariable=l,font=fnt,width=19,state='readonly')
	from_inp.grid(column=1,row=8,sticky=tk.EW,padx=10,pady=10)
	from_inp['values']=locations

	tk.Label(f2,text='To',font=fnt).grid(column=0,row=9,sticky=tk.E,padx=10,pady=10)
	m=tk.StringVar()
	to_inp=ttk.Combobox(f2,textvariable=m,font=fnt,width=19,state='readonly')
	to_inp.grid(column=1,row=9,sticky=tk.EW,padx=10,pady=10)
	to_inp['values']=locations

	tk.Label(f2,text='Date',font=fnt).grid(column=0,row=10,sticky=tk.E,padx=10,pady=10)
	date_inp=tk.Entry(f2,font=fnt)
	date_inp.grid(column=1,row=10,sticky=tk.EW,padx=10,pady=10)
	tk.Label(f2,text='[YYYY-MM-DD]',font=fnt).grid(column=2,row=10,padx=10,pady=10)

	tk.Label(f2,text='Time',font=fnt).grid(column=0,row=11,sticky=tk.E,padx=10,pady=10)
	time_inp=tk.Entry(f2,font=fnt)
	time_inp.grid(column=1,row=11,sticky=tk.EW,padx=10,pady=10)
	tk.Label(f2,text='24h [HH:MM]',font=fnt).grid(column=2,row=11,padx=10,pady=10)

	Separator(f2,orient='horizontal').grid(row=14,column=0,columnspan=3,sticky=tk.EW,pady=10)

	# Payment method - Card or cash?
	payment_method=tk.StringVar(f2)	
	tk.Label(f2,text='Payment method',font=fnt).grid(column=0,row=15,sticky=tk.E,padx=10,pady=10)
	ttk.Radiobutton(f2, text = 'Credit/Debit Card',variable = payment_method,value = 'R').grid(column=1,row=15,sticky=tk.W,padx=10)
	ttk.Radiobutton(f2, text = 'Cash',variable = payment_method,value = 'C').grid(column=1,row=16,sticky=tk.W,padx=10)

	# Submit
	tk.Label(f2,text='Proceed to checkout',font=fnt,justify=tk.RIGHT).grid(column=0,row=20,sticky=tk.E,padx=10,pady=10)
	submit_icon=tk.PhotoImage(file='icons/checkout.png')
	submit_btn=tk.Button(f2,font=fnt,text='Continue to Payment',image=submit_icon,command=payment)
	submit_btn.grid(column=1,row=20,padx=10,pady=10,sticky=tk.W)
	submit_btn.image=submit_icon

	busbkg_win.bind('<Return>',lambda event:payment()) 							# Binds enter key to submit function

def taxi_booking():																	# Taxi booking
	
	#definitions
	taxibkg_id='T'+str(rd.randint(10000,99999))	#random number for ID
	ctype=['','Standard','XL','Luxury']	#defines coach type

	#timestamp to mark bookings
	t=datetime.now()

	# Defining the window
	taxibkg_win=tk.Toplevel()
	taxibkg_win.title('Taxi Booking')
	taxibkg_win.resizable(False, False)
	icon=tk.PhotoImage(file='img/icon.png')
	taxibkg_win.iconphoto(False,icon)

	def payment():									# The payment function
		
		# Defining 'today' and 'tomorrow'
		inpdate_str=''
		if 'Today' in p.get():
			inpdate_str=today.strftime('%Y-%m-%d')
		elif 'Tomorrow' in p.get():
			inpdate_str=tomrw.strftime('%Y-%m-%d')
		else:
			pass
		
		# Taking of inputs
		origin=from_inp.get().capitalize()
		destination=to_inp.get().capitalize()
		date_of_journey=inpdate_str
		time_of_journey=time.get()
		taxi_type=n.get()

		datetime_format='%Y-%m-%d %H:%M'								# YYYY-MM-DD HH:MM; MySQL datetime format
		x=datetime.now()+timedelta(minutes=10)				# timestamp for reference - 10 min from current time
		min_bkgtime_str=x.strftime(datetime_format)						# Converts datetime to string in MySQL time format 
		min_bkgtime=datetime.strptime(min_bkgtime_str,datetime_format)	# Converts string back to datetime object for comparision
		inpdate_str=date_of_journey+' '+time_of_journey

		isInpDateinFormat=True
		try:
			isInpDateinFormat=bool(datetime.strptime(inpdate_str,datetime_format))		#Is date and time inputted in correct format?
		except ValueError:
			isInpDateinFormat=False

		if isInpDateinFormat==True:
			inp_dt=datetime.strptime(inpdate_str,datetime_format)		#Converts inputs to datetime format

			if inp_dt >= min_bkgtime:							#Is input in the past?
				isNotPast=True
			else:
				isNotPast=False

			if inp_dt <= min_bkgtime+timedelta(days=2):		#Is input greater than 2 days?
				isNotDistFuture=True
			else:
				isNotDistFuture=False

		# Checking of user inputs before proceeding to payment function
		if (not origin=='' and not origin.isspace()) and (not destination=='' and not destination.isspace()) and (not date_of_journey=='' and not date_of_journey.isspace()) and (not time_of_journey=='' and not time_of_journey.isspace()) and (not taxi_type=='' and not taxi_type.isspace()):
			if origin in locations and destination in locations:
				if not origin == destination:
					if isInpDateinFormat==True and len(date_of_journey)==10 and len(time_of_journey)==5:
						if isNotPast==True and isNotDistFuture==True:
							if payment_method.get() in ['R','C']:

								# calculation of fare on basis of type
								if n.get()=='Standard':
									base_rate=15
								elif n.get()=='XL':
									base_rate=25
								elif n.get()=='Luxury':
									base_rate=40
								
								if n.get()=='Standard':
									rate=3
								elif n.get()=='XL':
									rate=5
								elif n.get()=='Luxury':
									rate=10
								
								payment_id='P'+str(rd.randint(10000,99999))

								o=from_inp.get()
								d=to_inp.get()
								distance=abs((locations.index(d))-(locations.index(o)))*4	#distance between locations - 4 km.
								if distance > 5:
									total_fare=(base_rate+(rate*(distance-5)))
								else:
									total_fare=(base_rate+0)

								# is it card (R) or cash?
								if payment_method.get()=='R':

									def card_payment():		# Card payment function
										# Takes inputs of payment details
										card_type=cardtype_inp.get()
										card_no=cardno_inp.get()
										card_name=cardname_inp.get()
										exp_year=expyear_inp.get()
										exp_month=expmonth_inp.get()
										cvv=cvv_inp.get()

										# Gets current month and year for card expiry date checking
										cur_dt=datetime.now()
										cur_mth=cur_dt.month
										cur_yr=cur_dt.year

										def bkg_confirmed():		

											def clipboard():
												confirmmsg_win.clipboard_clear()
												confirmmsg_win.clipboard_append(summary_text)
												clipbd_button.configure(fg='green',text='Copied!')
																										
											def exit():
												confirmmsg_win.destroy()
												cardpay_window.destroy()
												taxibkg_win.destroy()

											card_brand=''
											if card_no[0] == '3':
												card_brand='AMEX'
											elif card_no[0] == '4':
												card_brand='VISA'
											elif card_no[0] == '5':
												card_brand='MASTER'
											elif card_no[0] == '6':
												card_brand='DISCOVER'

											# Adding booking details to database
											bkg_time=datetime.now()
											bkg_timestamp=bkg_time.strftime('%Y-%m-%d %H:%M:%S')	#Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM
											
											sql='insert into taxi_bkgs values (%s,%s,%s,%s,%s,%s,%s)'
											val=(taxibkg_id,bkg_timestamp,origin,destination,date_of_journey,time_of_journey,taxi_type)
											cur.execute(sql,val)
											con.commit()

											# Adds payment details to database
											pay_time=datetime.now()
											pay_timestamp=pay_time.strftime('%Y-%m-%d %H:%M:%S')	#Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM

											sql=('insert into payment_details values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
											val=(payment_id,pay_timestamp,taxibkg_id,total_fare,card_type,card_no,card_name,cvv,exp_month,exp_year)
											cur.execute(sql,val)
											con.commit()

											# Confirmation popup
											confirmmsg_win=tk.Toplevel()
											confirmmsg_win.resizable(False,False)
											confirmmsg_win.title('Booking successful')
											icon=tk.PhotoImage(file='img/icon.png')
											confirmmsg_win.iconphoto(False,icon)

											tk.Label(confirmmsg_win,text='The booking has been\nsuccessfully made.',font=h1fnt,justify=tk.LEFT).grid(row=0,column=0,sticky=tk.W,padx=10,pady=10)

											summary=scrolledtext.ScrolledText(confirmmsg_win,font=fnt,width=30,height=8)
											summary.grid(column=0,row=3,sticky=tk.EW,padx=10,pady=10,columnspan=2)

											summary_text='\nTaxi Booking\n------------\n\nBooking ID: '+taxibkg_id+'\nBooking Timestamp: \n'+bkg_timestamp+'\n\nFrom: '+o+'\nTo: '+d+'\nType: '+taxi_type+'\n\nDate: '+date_of_journey+'\nTime: '+time_of_journey+'\n\nBase rate: $'+str(base_rate)+' for first 5 km\n$'+str(rate)+' per additional km\nDistance: '+str(distance)+' km'+'\n\nTotal fare: $'+str(total_fare)+'\n\nPayment\n-------\n\n'+'Payment ID: '+payment_id+'\nPaid by: '+cardtype_inp.get()+'\nCardholder name: '+cardname_inp.get()+'\nCard number: XXXX-XXXX-XXXX-'+cardno_inp.get()[-4:]+'\nCard type: '+card_brand+'\nAmount paid: $'+str(total_fare)+'\n\n------------------'+'\nPAYMENT SUCCESSFUL'+'\n------------------\n'
											summary.insert(tk.INSERT,summary_text)
											summary.configure(state='disabled')
											
											clipbd_button=tk.Button(confirmmsg_win,text='Copy to clipboard',font=fnt,command=clipboard,justify=tk.CENTER)
											clipbd_button.grid(row=5,column=0,padx=10,pady=10)
											
											if isPrintingEnabled==True:
												
												def receipt():
													
													def print_receipt():

														tkt_time=datetime.now()									#timestamp to mark ticket
														tkt_timestamp=tkt_time.strftime('%Y-%m-%d %H:%M:%S')	#Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM
														
														bar_no=str(rd.randint(1000000000000,9999999999999))
														tktid='TKT'+str(rd.randint(100000,999999))														
																		# title									# ticket details									# journey																																			# fare
														receipt_text='\nTaxi Booking '+taxibkg_id+'\n------------\n\nTicket '+tktid+'\nTimestamp: \n'+tkt_timestamp+'\n\nFrom: '+o+'\nTo: '+d+'\nType: '+taxi_type+'\n\nDate: '+date_of_journey+'\nTime: '+time_of_journey+'\nDistance: '+str(distance)+' km'+'\n\nTotal fare: $'+str(total_fare)+'\n\nPaid by: '+cardtype_inp.get()+'\n\nEnjoy your journey! Thank you for choosing ABC LINES!'+'\n------------------\n'
														
														sql=('insert into tkt_details values(%s,%s,%s)')
														#print(tktid,taxibkg_id,tkt_timestamp)
														val=(tktid,taxibkg_id,tkt_timestamp)
														cur.execute(sql,val)
														con.commit()

														pr.image('img/icon-2.png')
														pr.text(receipt_text)
														pr.barcode(bar_no, 'EAN13')
														pr.text('\n')
														pr.text('Powered by Amadeus')
														pr.text('\n')
														pr.text('Version: '+build+' ('+build_timestamp+')')
														pr.text('\n')
														
														if pf.system()=='Windows':
															pr.text('Platform: '+pf.system()+' '+pf.version())
														elif pf.system()=='Linux':
															pr.text('Platform: '+pf.system()+' '+pf.release())

														pr.cut()
														pr.close()

													try:
														pr = Network(pr_ip)
														print_receipt()
													except:
														messagebox.showerror('Error','Unable to connect to printer via network.',parent=confirmmsg_win)

												print_btn=tk.Button(confirmmsg_win,text='Print...',font=fnt,command=receipt,justify=tk.CENTER)
												print_btn.grid(row=6,column=0,padx=10,pady=10)

											ok_btn=tk.Button(confirmmsg_win,text='OK',font=fnt,command=exit,justify=tk.CENTER)
											ok_btn.grid(row=8,column=0,padx=10,pady=10)
											confirmmsg_win.bind('<Return>',lambda event:exit())


										if (not card_type=='' and not card_type.isspace()) and (not card_no=='' and not card_no.isspace()) and (not card_name=='' and not card_name.isspace()) and (not exp_year=='' and not exp_year.isspace()) and (not exp_month=='' and not exp_month.isspace()) and (not cvv=='' and not cvv.isspace()):
											if len(card_no) == 16 and card_no[0] in '3456':
												if len(exp_year) == 4 and int(exp_year) >= cur_yr:
													if int(exp_year) == cur_yr:
														if (len(exp_month) == 2) and (int(exp_month)>= 1 and int(exp_month) <= 12) and (int(exp_month) > cur_mth):
															if len(cvv)==3:
																bkg_confirmed()
															else:
																messagebox.showerror('Error','CVV must be a 3-digit number.',parent=cardpay_window)
														else:
															messagebox.showerror('Error','Invalid expiry month.',parent=cardpay_window)
													elif int(exp_year) > cur_yr:							
														if (len(exp_month) == 2) and (int(exp_month)>= 1 and int(exp_month) <= 12):
															if len(cvv)==3:
																bkg_confirmed()
															else:
																messagebox.showerror('Error','CVV must be a 3-digit number.',parent=cardpay_window)
														else:
															messagebox.showerror('Error','Invalid expiry month..',parent=cardpay_window)
													else:
														pass
												else:
													messagebox.showerror('Error','Invalid expiry year.',parent=cardpay_window)
											else:
												messagebox.showerror('Error','Invalid card number.',parent=cardpay_window)
										else:
											messagebox.showerror('Error','Please enter all required\npayment details.',parent=cardpay_window)
									
									cardpay_window=tk.Toplevel()
									cardpay_window.title('Payment Gateway')
									cardpay_window.resizable(False,False)
									icon=tk.PhotoImage(file='img/icon.png')
									cardpay_window.iconphoto(False,icon)

									f3=tk.Frame(cardpay_window)
									f3.grid(row=0,column=0)

									img1=tk.PhotoImage(file='icons/make-payment.png')
									img=tk.Label(f3,image=img1,font=h1fnt)
									img.grid(column=0,row=0,padx=10,pady=10)
									img.image=img1

									tk.Label(f3,text='Payment',font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

									f4=tk.Frame(cardpay_window)
									f4.grid(row=1,column=0)

									payment_summary=scrolledtext.ScrolledText(f4,font=fnt,width=25,height=5)
									payment_summary.grid(column=1,row=2,sticky=tk.EW,padx=10,pady=10)

									text='Booking ID: '+taxibkg_id+'\nFrom: '+o+'\nTo: '+d+'\nType: '+n.get()+'\n\nDate: '+date_of_journey+'\nTime: '+time_of_journey+'\n\nBase rate: $'+str(base_rate)+' for first 5 km\n$'+str(rate)+' per additional km\nDistance: '+str(distance)+' km'+'\n\nTotal fare: $'+str(total_fare)
									payment_summary.insert(tk.INSERT,text)
									payment_summary.configure(state='disabled')

									tk.Label(f4,text='Payment ID',font=fnt).grid(column=0,row=3,sticky=tk.E,padx=10,pady=10)
									payid=tk.Label(f4,text=payment_id,font=fnt)
									payid.grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

									cardtype_inp=tk.StringVar()
									tk.Label(f4,text='Pay by',font=fnt).grid(column=0,row=4,sticky=tk.E,padx=10,pady=10)
									card=('','Debit card','Credit card')
									pay_type=ttk.OptionMenu(f4,cardtype_inp,*card)
									pay_type.grid(column=1,row=4,sticky=tk.W,padx=10,pady=10)
									
									tk.Label(f4,text='Accepted cards',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
									
									img2=tk.PhotoImage(file='img/cards.png')
									card_image=tk.Label(f4,image=img2,font=fnt)
									card_image.grid(column=1,row=5,sticky=tk.W,padx=10,pady=10)
									card_image.image=img2

									tk.Label(f4,text='Card number',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
									cardno_inp=tk.Entry(f4,font=fnt)
									cardno_inp.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

									tk.Label(f4,text='Cardholder name',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
									cardname_inp=tk.Entry(f4,font=fnt)
									cardname_inp.grid(column=1,row=7,sticky=tk.EW,padx=10,pady=10)

									tk.Label(f4,text='Expiry Year and Month\n[YYYY-MM]',font=fnt,justify=tk.RIGHT).grid(column=0,row=8,sticky=tk.E,padx=10,pady=10)
									expyear_inp=tk.Entry(f4,font=fnt,width=10)
									expyear_inp.grid(column=1,row=8,sticky=tk.EW,padx=10,pady=10)

									tk.Label(f4,text='-',font=fnt).grid(column=2,row=8,sticky=tk.EW,padx=10,pady=10)
									expmonth_inp=tk.Entry(f4,font=fnt,width=10)
									expmonth_inp.grid(column=3,row=8,sticky=tk.W,padx=10,pady=10)

									tk.Label(f4,text='CVV number',font=fnt).grid(column=0,row=9,sticky=tk.E,padx=10,pady=10)
									cvv_inp=tk.Entry(f4,font=fnt)
									cvv_inp.grid(column=1,row=9,sticky=tk.EW,padx=10,pady=10)

									btn=tk.Button(f4,font=fntit,text='Pay',command=card_payment,fg='green');btn.grid(column=1,row=10,padx=10,pady=10,sticky=tk.W)

									retimg=tk.PhotoImage(file='icons/return.png')
									btn4=tk.Button(f4,font=fnt,image=retimg,command=cardpay_window.destroy)
									btn4.grid(column=0,row=15,padx=10,pady=10,sticky=tk.SW)
									btn4.img=retimg

									cardpay_window.bind('<Return>',lambda event:card_payment())
								
								elif payment_method.get()=='C':
									
									def clipboard():
										confirmmsg_win.clipboard_clear()
										confirmmsg_win.clipboard_append(summary_text)
										clipbd_btn.configure(fg='green',text='Copied!')
									
									def exit():
										confirmmsg_win.destroy()
										taxibkg_win.destroy()

									# Adding booking details to database
									bkg_time=datetime.now()									#	Timestamp to mark bookings
									bkg_timestamp=bkg_time.strftime('%Y-%m-%d %H:%M:%S')	#	Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM
								
									sql='insert into taxi_bkgs values (%s,%s,%s,%s,%s,%s,%s)'
									val=(taxibkg_id,bkg_timestamp,origin,destination,date_of_journey,time_of_journey,taxi_type)
									cur.execute(sql,val)
									con.commit()

									# Adds payment details to database
									pay_time=datetime.now()									# 	Timestamp to mark payment
									pay_timestamp=pay_time.strftime('%Y-%m-%d %H:%M:%S')	#	Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM
									
									sql=('insert into payment_details values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
									val=(payment_id,pay_timestamp,taxibkg_id,total_fare,'Cash',None,None,None,None,None)
									cur.execute(sql,val)
									con.commit()

									# Confirmation popup
									confirmmsg_win=tk.Toplevel()
									confirmmsg_win.resizable(False,False)
									confirmmsg_win.title('Booking successful')
									icon=tk.PhotoImage(file='img/icon.png')
									confirmmsg_win.iconphoto(False,icon)

									tk.Label(confirmmsg_win,text='The booking has been\nsuccessfully made.',font=h1fnt,justify=tk.LEFT).grid(row=0,column=0,sticky=tk.W,padx=10,pady=10)

									summary=scrolledtext.ScrolledText(confirmmsg_win,font=fnt,width=30,height=8)
									summary.grid(column=0,row=3,sticky=tk.EW,padx=10,pady=10,columnspan=2)

									summary_text='\nBus Booking\n-----------\n\nBooking ID: '+taxibkg_id+'\nBooking Timestamp: \n'+bkg_timestamp+'\n\nFrom: '+o+'\nTo: '+d+'\nType: '+taxi_type+'\n\nDate: '+date_of_journey+'\nTime: '+time_of_journey+'\n\nRate: $'+str(rate)+' per km\nDistance: '+str(distance)+' km'+'\n\nTotal fare: $'+str(total_fare)+'\n\nPayment\n-------\n\n'+'Payment ID: '+payment_id+'\nPaid by: Cash'+'\nAmount paid: $'+str(total_fare)+'\n\n------------------'+'\nPAYMENT SUCCESSFUL'+'\n------------------\n'
									summary.insert(tk.INSERT,summary_text)
									summary.configure(state='disabled')
									
									clipbd_btn=tk.Button(confirmmsg_win,text='Copy to clipboard',font=fnt,command=clipboard,justify=tk.CENTER)
									clipbd_btn.grid(row=5,column=0,padx=10,pady=10)
									
									# Printing function
									if isPrintingEnabled==True:
										def receipt():

											def print_receipt():
												tkt_time=datetime.now()									#timestamp to mark ticket
												tkt_timestamp=tkt_time.strftime('%Y-%m-%d %H:%M:%S')	#Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM

												bar_no=str(rd.randint(1000000000000,9999999999999))
												tktid='TKT'+str(rd.randint(100000,999999))
															# title									# ticket details									# journey																																		# fare																																						
												receipt_text='\nBus Booking '+taxibkg_id+'\n------------\n\nTicket '+tktid+'\nTimestamp: \n'+tkt_timestamp+'\n\nFrom: '+o+'\nTo: '+d+'\nType: '+taxi_type+'\n\nDate: '+date_of_journey+'\nTime: '+time_of_journey+'\nDistance: '+str(distance)+' km'+'\n\nTotal fare: $'+str(total_fare)+'\n\nPaid by: Cash'+'\n\nEnjoy your journey! Thank you for choosing ABC LINES!'
												
												sql=('insert into tkt_details values(%s,%s,%s)')
												#print(tktid,taxibkg_id,tkt_timestamp)
												val=(tktid,taxibkg_id,tkt_timestamp)
												cur.execute(sql,val)
												con.commit()

												pr.image('img/icon-2.png')
												pr.text(receipt_text)
												pr.barcode(bar_no, 'EAN13')
												pr.text('\n')
												pr.text('Powered by Amadeus')
												pr.text('\n')
												pr.text('Version: '+build+' ('+build_timestamp+')')
												pr.text('\n')
												
												if pf.system()=='Windows':
													pr.text('Platform: '+pf.system()+' '+pf.version())
												elif pf.system()=='Linux':
													pr.text('Platform: '+pf.system()+' '+pf.release())

												pr.cut()
												pr.close()

											try:
												pr = Network(pr_ip)
												print_receipt()
											except:
												messagebox.showerror('Error','Unable to print receipt.',parent=confirmmsg_win)

										print_btn=tk.Button(confirmmsg_win,text='Print...',font=fnt,command=receipt,justify=tk.CENTER)
										print_btn.grid(row=6,column=0,padx=10,pady=10)

									ok_btn=tk.Button(confirmmsg_win,text='OK',font=fnt,command=exit,justify=tk.CENTER)
									ok_btn.grid(row=10,column=0,padx=10,pady=10)
									confirmmsg_win.bind('<Return>',lambda event:exit())
							else:
								messagebox.showerror('Error','Please select payment method',parent=taxibkg_win)	
						else:
							messagebox.showerror('Error','Invalid timing entered.',parent=taxibkg_win)
					else:
						messagebox.showerror('Error','Invalid time format entered.',parent=taxibkg_win)
				else:
					messagebox.showerror('Error','The origin and destination are the same.',parent=taxibkg_win)
			else:
				messagebox.showerror('Error','Invalid origin or destination.',parent=taxibkg_win)
		else:
			messagebox.showerror('Error','Please do not leave any fields blank.',parent=taxibkg_win)
	
	#FRAME 1
	f1=tk.Frame(taxibkg_win)
	f1.grid(row=0,column=0)

	tk.Label(f1,text='TAXI BOOKING',font=h1fnt,bg='yellow').grid(column=1,row=0,padx=10,pady=10)

	#FRAME 2
	f2=tk.Frame(taxibkg_win)
	f2.grid(row=1,column=0)

	#Booking ID
	tk.Label(f2,text='ID',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
	bkgid=tk.Label(f2,text=taxibkg_id,font=fnt)
	bkgid.grid(column=1,row=5,sticky=tk.W,padx=10,pady=10)

	#Input fields
	n=tk.StringVar()
	tk.Label(f2,text='Taxi Type',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
	taxitype=ttk.OptionMenu(f2,n,*ctype)
	taxitype.grid(column=1,row=7,sticky=tk.W,padx=10,pady=10)

	tk.Label(f2,text='From',font=fnt).grid(column=0,row=8,sticky=tk.E,padx=10,pady=10)
	l=tk.StringVar()
	from_inp=ttk.Combobox(f2,textvariable=l,font=fnt,width=19,state='readonly')
	from_inp.grid(column=1,row=8,sticky=tk.EW,padx=10,pady=10)
	from_inp['values']=locations

	tk.Label(f2,text='To',font=fnt).grid(column=0,row=9,sticky=tk.E,padx=10,pady=10)
	m=tk.StringVar()
	to_inp=ttk.Combobox(f2,textvariable=m,font=fnt,width=19,state='readonly')
	to_inp.grid(column=1,row=9,sticky=tk.EW,padx=10,pady=10)
	to_inp['values']=locations

	today=(t+timedelta(minutes=10))				#today
	tomrw=(t+timedelta(days=1,minutes=10))		#tomorrow
	datetype=('','Today '+today.strftime('%Y-%m-%d'),'Tomorrow '+tomrw.strftime('%Y-%m-%d'))

	p=tk.StringVar()
	tk.Label(f2,text='Date',font=fnt).grid(column=0,row=10,sticky=tk.E,padx=10,pady=10)
	date=ttk.OptionMenu(f2,p,*datetype)
	date.grid(column=1,row=10,sticky=tk.W,padx=10,pady=10)

	tk.Label(f2,text='Time',font=fnt).grid(column=0,row=11,sticky=tk.E,padx=10,pady=10)
	time=tk.Entry(f2,font=fnt)
	time.grid(column=1,row=11,sticky=tk.EW,padx=10,pady=10)
	tk.Label(f2,text='24h [HH:MM]',font=fnt).grid(column=2,row=11,padx=10,pady=10)

	Separator(f2,orient='horizontal').grid(row=14,column=0,columnspan=3,sticky=tk.EW)

	# Payment method - Card or cash?
	payment_method=tk.StringVar(f2)	
	tk.Label(f2,text='Payment method',font=fnt).grid(column=0,row=15,sticky=tk.E,padx=10,pady=10)
	ttk.Radiobutton(f2, text = 'Credit/Debit Card',variable = payment_method,value = 'R').grid(column=1,row=15,sticky=tk.W,padx=10)
	ttk.Radiobutton(f2, text = 'Cash',variable = payment_method,value = 'C').grid(column=1,row=16,sticky=tk.W,padx=10)

	# Submit
	tk.Label(f2,text='Proceed to checkout',font=fnt,justify=tk.RIGHT).grid(column=0,row=20,sticky=tk.E,padx=10,pady=10)
	submit_icon=tk.PhotoImage(file='icons/checkout.png')
	submit_btn=tk.Button(f2,font=fnt,text='Continue to Payment',image=submit_icon,command=payment)
	submit_btn.grid(column=1,row=20,padx=10,pady=10,sticky=tk.W)
	submit_btn.image=submit_icon

	taxibkg_win.bind('<Return>',lambda event:payment())

def emp_main():																		
	#main window
	emp_login_win=tk.Tk()
	emp_login_win.title('ABC IBS '+dev_string)
	icon=tk.PhotoImage(file='img/icon.png')
	emp_login_win.iconphoto(False,icon)

	#maximises window
	try:
		emp_login_win.state('zoomed')
	except:
		w,h=emp_login_win.winfo_screenwidth(),emp_login_win.winfo_screenheight()
		emp_login_win.geometry(str(w)+'x'+str(h))

	def on_login():																	# Action on login

		# Main functions
		def manage_busbkg():														# Manage bus bookings

			manage_bbkg_win=tk.Toplevel()
			manage_bbkg_win.title('Manage bus bookings')
			icon=tk.PhotoImage(file='img/icon.png')
			manage_bbkg_win.iconphoto(False,icon)

			def viewbkg_all():															# View all bookings
				viewall_win=tk.Toplevel()
				viewall_win.title('All bus bookings')
				viewall_win.resizable(False,False)
				icon=tk.PhotoImage(file='img/icon.png')
				viewall_win.iconphoto(False,icon)
				
				header=('Booking ID','Timestamp','Number of Passengers','Origin','Destination','Date','Time','Bus Type')

				sql2=str('select * from bus_bkgs')										# getting data from table

				cur.execute(sql2)
				data=[header]+cur.fetchall()											# appending header to data
				
				rows=len(data)
				cols=len(data[0])

				for i in range(rows):													# drawing the table in GUI
					for j in range(cols):
						entry = tk.Label(viewall_win,borderwidth=1,relief='solid',padx=10,height=2,font=fnt)
						entry.grid(row=i, column=j,padx=2,pady=2,sticky=tk.EW)
						entry.configure(text=data[i][j])
						if i==0:
							entry.configure(fg='red',font=fntit)							# colors and italicises header

			def viewbkg_single():
																			# View single booking
				def get_busbkginfo():
					if not bkgid_input.get()=='' and not bkgid_input.get().isspace():
						if bkgid_input.get() in bus_bkgid_list:
							sql='select * from bus_bkgs where bkgid=%s'
							val=(bkgid_input.get(),)
							cur.execute(sql,val)
							c=cur.fetchall()
							bkg_id=c[0][0]
							bkg_ts=c[0][1]
							bkg_passno=c[0][2]
							bkg_org=c[0][3]
							bkg_dest=c[0][4]
							bkg_date=c[0][5]
							bkg_time=c[0][6]
							bkg_type=c[0][7]
							
							data=[('Booking ID',bkg_id),('Timestamp',bkg_ts),('Number of passengers',bkg_passno),('Origin',bkg_org),('Destination',bkg_dest),('Date',bkg_date),('Time',bkg_time),('Bus Type',bkg_type)]
							
							
							rows=len(data)
							cols=len(data[0])
							tk.Label(frame3,font=fntit,text='Data').grid(row=0,column=0,sticky=tk.W)
							for i in range(rows):											#drawing the table in GUI
								for j in range(cols):
									entry = tk.Label(frame2,borderwidth=1,relief='solid',padx=10,width=30,height=2,font=fnt)
									entry.grid(row=i,column=j,padx=2,pady=2,sticky=tk.EW)
									entry.configure(text=data[i][j])
									if j==0:
										entry.configure(fg='red',font=fntit) 				#colors and italicises header
						else:
							messagebox.showerror('Error','Booking \''+bkgid_input.get()+'\' does not exist.',parent=viewone_win)
					else:
						messagebox.showerror('Error','Please enter the booking.',parent=viewone_win)
				
				viewone_win=tk.Toplevel()
				viewone_win.title('View bus booking')
				viewone_win.resizable(False,False)
				icon=tk.PhotoImage(file='img/icon.png')
				viewone_win.iconphoto(False,icon)
				
				frame1=tk.Frame(viewone_win)
				frame1.grid(row=0,column=0,padx=10,pady=10,sticky=tk.EW)

				frame2=tk.Frame(viewone_win)
				frame2.grid(row=2,column=0,padx=10,pady=10,sticky=tk.EW)

				frame3=tk.Frame(viewone_win)
				frame3.grid(row=1,column=0,padx=10,pady=10,sticky=tk.W)

				cur.execute('select bkgid from bus_bkgs')
				a=cur.fetchall()
				bus_bkgid_list=[]
				for i in a:
					bus_bkgid_list.append(i[0])

				search_icon=tk.PhotoImage(file='icons/searchusr.png')
				search_btn=tk.Label(frame1,image=search_icon,font=h1fnt)
				search_btn.grid(column=0,row=0,padx=10,pady=10)
				search_btn.image=search_icon

				tk.Label(frame1,font=h1fnt,text='View bus booking details').grid(row=0,column=1,padx=10,pady=10,sticky=tk.W)

				tk.Label(frame1,font=fnt,text='Enter booking ID.').grid(row=4,column=1,padx=10,pady=10,sticky=tk.W)
				bkgid=tk.StringVar()
				bkgid_input=ttk.Combobox(frame1,textvariable=bkgid,font=fnt)
				bkgid_input.grid(row=5,column=1,padx=10,pady=10,sticky=tk.EW)
				bkgid_input['values']=bus_bkgid_list
				
				submit_btn=tk.Button(frame1,font=fntit,text='Submit',command=get_busbkginfo)
				submit_btn.grid(row=5,column=2,padx=10,pady=10)
				viewone_win.bind('<Return>',lambda event:get_busbkginfo())

			def delbkg():
																						# Delete booking menu
				delete_win=tk.Toplevel()
				delete_win.resizable(False,False)
				delete_win.title('Delete bus booking')
				icon=tk.PhotoImage(file='img/icon.png')
				delete_win.iconphoto(False,icon)

				cur.execute('select bkgid,pay_id from payment_details')
				bkgid_list=dict(cur.fetchall())
				
				def delete_busbkg():															# Delete booking function
					if not bkgid_inp.get()=='' and not bkgid_inp.get().isspace():
						if bkgid_inp.get() in bus_bkgid_list:
							messagebox.showwarning('','This operation will delete\nthe booking selected permanently.\nContinue?',parent=delete_win)
							confirm=messagebox.askyesno('','Do you wish to delete the booking '+bkgid_inp.get()+'?',parent=delete_win)
							if confirm == True:
								sql='delete from bus_bkgs where bkgid =%s'						# Deletes booking from database
								val=(bkgid_inp.get(),)
								cur.execute(sql,val)
								
								sql2='delete from payment_details where bkgid=%s'				# Deletes payment details from database
								cur.execute(sql2,val)
								con.commit()
								
								sql3='delete from tkt_details where bkgid=%s'					# Deletes ticket info from database
								cur.execute(sql3,val)
								con.commit()
								
								messagebox.showinfo('','Booking '+bkgid_inp.get()+' deleted;\nTransaction '+bkgid_list[bkgid_inp.get()]+' cancelled, and corresponding tickets deleted.',parent=delete_win)
								delete_win.destroy()
							else:
								messagebox.showinfo('','Booking '+bkgid_inp.get()+' not deleted.\nThe database has not been modified.',parent=delete_win)
						else:
							messagebox.showerror('Error','Booking \''+bkgid_inp.get()+'\' does not exist.',parent=delete_win)
					else:
						messagebox.showerror('','Please enter the booking ID.',parent=delete_win)
					
				delete_icon2=tk.PhotoImage(file='icons/delete_bkgs.png')
				header_img=tk.Label(delete_win,image=delete_icon2,font=h1fnt)
				header_img.grid(column=0,row=0,padx=10,pady=10)
				header_img.image=delete_icon2

				tk.Label(delete_win,text='Delete bus booking',font=h1fnt).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

				cur.execute('select bkgid from bus_bkgs')
				bkgid_list2=cur.fetchall()
				bus_bkgid_list=[]
				for i in bkgid_list2:
					bus_bkgid_list.append(str(i[0]))

				tk.Label(delete_win,text='Select the booking to be deleted.',font=fntit).grid(column=1,row=3,padx=10,pady=10,sticky=tk.W)
				tk.Label(delete_win,text='NOTE: The corresponding transaction will\nalso be cancelled.',font=('Cascadia Mono',12,'bold italic'),justify=tk.LEFT).grid(column=1,row=4,padx=10,pady=10,sticky=tk.W)

				bkgid=tk.StringVar()
				bkgid_inp=ttk.Combobox(delete_win,textvariable=bkgid,font=fnt,width=19)
				bkgid_inp.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
				bkgid_inp['values']=bus_bkgid_list

				delete_btn=tk.Button(delete_win,text='Delete',font=fntit,command=delete_busbkg,fg='red')
				delete_btn.grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)
				delete_win.bind('<Return>',lambda event:delete_busbkg())

			tk.Grid.columnconfigure(manage_bbkg_win,0,weight=1)

			#FRAME 1
			tk.Grid.rowconfigure(manage_bbkg_win,0,weight=1)
			f1=tk.Frame(manage_bbkg_win)
			f1.grid(row=0,column=0,sticky=tk.NSEW)

			#frame 1 grid
			tk.Grid.columnconfigure(f1,0,weight=1)
			tk.Grid.columnconfigure(f1,1,weight=1)

			tk.Grid.rowconfigure(f1,0,weight=1)
			bus_icon=tk.PhotoImage(file='icons/bus.png')
			header_img=tk.Label(f1,image=bus_icon)
			header_img.grid(column=0,row=0,sticky=tk.E,padx=10,pady=10)
			header_img.image=bus_icon
			tk.Label(f1,text=('Manage the bus booking...'),font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)
			tk.Label(f1,text=('Connected to database: '+con.database),font=h2fnt,justify=tk.LEFT,fg='green').grid(column=1,row=1,sticky=tk.W,padx=10,pady=10)
			ttk.Separator(f1,orient='horizontal').grid(column=0,row=2,sticky=tk.EW,padx=10,pady=10,columnspan=2)
			#FRAME 2
			tk.Grid.rowconfigure(manage_bbkg_win,1,weight=1)
			f2=tk.Frame(manage_bbkg_win)
			f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

			#frame 2 grid
			tk.Grid.columnconfigure(f2,0,weight=1)
			tk.Grid.columnconfigure(f2,1,weight=1)
			tk.Grid.columnconfigure(f2,2,weight=1)
			tk.Grid.columnconfigure(f2,3,weight=1)

			tk.Label(f2,text='You can:',font=fntit,justify=tk.LEFT).grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

			tk.Grid.rowconfigure(f2,5,weight=1)
			viewall_icon=tk.PhotoImage(file='icons/preview.png')
			viewall_btn=tk.Button(f2,text='view all',image=viewall_icon,font=fnt,command=viewbkg_all)
			viewall_btn.grid(column=0,row=5,padx=10,pady=10,sticky=tk.E)
			viewall_btn.image=viewall_icon
			tk.Label(f2,text='View all booking details.',font=fnt,fg='blue').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

			viewone_icon=tk.PhotoImage(file='icons/search_bkgs.png')
			viewone_btn=tk.Button(f2,text='viewone',image=viewone_icon,font=fnt,command=viewbkg_single)
			viewone_btn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
			viewone_btn.image=viewone_icon
			tk.Label(f2,text='View a single booking details.',font=fnt).grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)

			tk.Grid.rowconfigure(f2,7,weight=1)
			delete_icon=tk.PhotoImage(file='icons/delete_bkgs.png')
			delete_btn=tk.Button(f2,text='del',image=delete_icon,font=fnt,command=delbkg)
			delete_btn.grid(column=0,row=7,padx=10,pady=10,sticky=tk.E)
			delete_btn.image=delete_icon
			tk.Label(f2,text='Delete a booking.',font=fnt,fg='red').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)
			tk.Grid.rowconfigure(f2,8,weight=1)
			tk.Message(f2,text='WARNING: This will delete\nthe booking selected\nfrom the system permanently.',width=500,font=fnt,fg='white',bg='red').grid(column=1,row=8,padx=10,pady=10,sticky=tk.NW)


			tk.Grid.rowconfigure(f2,16,weight=1)

		def manage_taxibkg():														# Manage taxi bookings
			manage_tbkg_win=tk.Toplevel()
			manage_tbkg_win.title('Manage taxi bookings')
			icon=tk.PhotoImage(file='img/icon.png')
			manage_tbkg_win.iconphoto(False,icon)

			def viewbkg_all():  													# View all bookings
				viewall_win=tk.Toplevel()
				viewall_win.title('All taxi bookings')
				viewall_win.resizable(False,False)
				icon=tk.PhotoImage(file='img/icon.png')
				viewall_win.iconphoto(False,icon)
				
				header=('Booking ID','Timestamp','Origin','Destination','Date','Time','Taxi Type')

				sql2=str('select * from taxi_bkgs')							# getting data from table
				cur.execute(sql2)
				data=[header]+cur.fetchall()								# appending header to data
				
				rows=len(data)
				cols=len(data[0])

				for i in range(rows):											#drawing the table in GUI
					for j in range(cols):
						entry = tk.Label(viewall_win,borderwidth=1,relief='solid',padx=10,height=2,font=fnt)
						entry.grid(row=i, column=j,padx=2,pady=2,sticky=tk.EW)
						entry.configure(text=data[i][j])
						if i==0:
							entry.configure(fg='red',font=fntit)				#colors and italicises header

			def viewbkg_single():													# View a single booking
				def get_taxibkginfo():
					if not bkgid.get()=='' and not bkgid.get().isspace():
						if bkgid.get() in taxi_bkgid_list:
							sql='select * from taxi_bkgs where bkgid=%s'
							val=(bkgid.get(),)
							cur.execute(sql,val)
							c=cur.fetchall()
							bkg_id=c[0][0]
							bkg_ts=c[0][1]
							bkg_org=c[0][2]
							bkg_dest=c[0][3]
							bkg_date=c[0][4]
							bkg_time=c[0][5]
							bkg_type=c[0][6]
							
							e=[('Booking ID',bkg_id),('Timestamp',bkg_ts),('Origin',bkg_org),('Destination',bkg_dest),('Date',bkg_date),('Time',bkg_time),('Taxi Type',bkg_type)]
							
							rows=len(e)
							cols=len(e[0])
							tk.Label(frame3,font=fntit,text='Data').grid(row=0,column=0,sticky=tk.W)
							for i in range(rows):									# drawing the table in GUI
								for j in range(cols):
									entry = tk.Label(frame2,borderwidth=1,relief='solid',padx=10,width=30,height=2,font=fnt)
									entry.grid(row=i,column=j,padx=2,pady=2,sticky=tk.EW)
									entry.configure(text=e[i][j])
									if j==0:
										entry.configure(fg='red',font=fntit) 		# colors and italicises header
						else:
							messagebox.showerror('Error','Booking \''+bkgid.get()+'\' does not exist.',parent=viewone_win)
					else:
						messagebox.showerror('Error','Please enter the booking.',parent=viewone_win)
				viewone_win=tk.Toplevel()
				viewone_win.title('View taxi booking')
				viewone_win.resizable(False,False)
				icon=tk.PhotoImage(file='img/icon.png')
				viewone_win.iconphoto(False,icon)
				
				frame1=tk.Frame(viewone_win)
				frame1.grid(row=0,column=0,padx=10,pady=10,sticky=tk.EW)

				frame2=tk.Frame(viewone_win)
				frame2.grid(row=2,column=0,padx=10,pady=10,sticky=tk.EW)

				frame3=tk.Frame(viewone_win)
				frame3.grid(row=1,column=0,padx=10,pady=10,sticky=tk.W)

				cur.execute('select bkgid from taxi_bkgs')
				a=cur.fetchall()
				taxi_bkgid_list=[]
				for i in a:
					taxi_bkgid_list.append(i[0])

				img14=tk.PhotoImage(file='icons/searchusr.png')
				img=tk.Label(frame1,image=img14,font=h1fnt)
				img.grid(column=0,row=0,padx=10,pady=10)
				img.image=img14

				tk.Label(frame1,font=h1fnt,text='View taxi booking details...').grid(row=0,column=1,padx=10,pady=10,sticky=tk.W)

				tk.Label(frame1,font=fnt,text='Enter booking ID.').grid(row=4,column=1,padx=10,pady=10,sticky=tk.W)
				n=tk.StringVar()
				bkgid=ttk.Combobox(frame1,textvariable=n,font=fnt)
				bkgid.grid(row=5,column=1,padx=10,pady=10,sticky=tk.EW)
				bkgid['values']=taxi_bkgid_list
				
				submit=tk.Button(frame1,font=fntit,text='Submit',command=get_taxibkginfo)
				submit.grid(row=5,column=2,padx=10,pady=10)
				viewone_win.bind('<Return>',lambda event:get_taxibkginfo())

			def delbkg(): 															# Delete bookings menu
				delete_win=tk.Toplevel()
				delete_win.resizable(False,False)
				delete_win.title('Delete taxi booking')
				icon=tk.PhotoImage(file='img/icon.png')
				delete_win.iconphoto(False,icon)

				cur.execute('select bkgid,pay_id from payment_details')
				bkgid_list=dict(cur.fetchall())

				def delete_taxi_bkg():															# Delete bookings function
					
					if not bkgid_inp.get()=='' and not bkgid_inp.get().isspace():
						if bkgid_inp.get() in taxi_bkgid_list:
							messagebox.showwarning('','This operation will delete\nthe booking selected permanently.\nContinue?',parent=delete_win)
							confirm=messagebox.askyesno('','Do you wish to delete the booking '+bkgid_inp.get()+'?',parent=delete_win)
							if confirm == True:
								
								sql='delete from taxi_bkgs where bkgid =%s'						# Deletes booking from database
								val=(bkgid_inp.get(),)
								cur.execute(sql,val)
								
								sql2='delete from payment_details where bkgid=%s'				# Deletes transaction from database
								cur.execute(sql2,val)
								con.commit()
								
								sql3='delete from tkt_details where bkgid=%s'					# Deletes ticket info from database
								cur.execute(sql3,val)
								con.commit()
								
								messagebox.showinfo('','Booking '+bkgid_inp.get()+' deleted;\nTransaction '+bkgid_list[bkgid_inp.get()]+' cancelled, and corresponding tickets deleted.',parent=delete_win)
								delete_win.destroy()
							else:
								messagebox.showinfo('','Booking '+bkgid_inp.get()+' not deleted.\nThe database has not been modified.',parent=delete_win)
						else:
							messagebox.showerror('Error','Booking \''+bkgid_inp.get()+'\' does not exist.',parent=delete_win)
					else:
						messagebox.showerror('','Please enter the booking ID.',parent=delete_win)
				
				delete_icon=tk.PhotoImage(file='icons/delete_bkgs.png')
				header_img=tk.Label(delete_win,image=delete_icon,font=h1fnt)
				header_img.grid(column=0,row=0,padx=10,pady=10)
				header_img.image=delete_icon

				tk.Label(delete_win,text='Delete a taxi booking',font=h1fnt).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

				# Gets list of booking IDs
				cur.execute('select bkgid from taxi_bkgs')
				bkgid_list2=cur.fetchall()
				taxi_bkgid_list=[]
				for i in bkgid_list2:
					taxi_bkgid_list.append(str(i[0]))

				tk.Label(delete_win,text='Select the booking to be deleted.',font=fntit).grid(column=1,row=3,padx=10,pady=10,sticky=tk.W)
				tk.Label(delete_win,text='NOTE: The corresponding transaction will\nalso be cancelled.',font=('Cascadia Mono',12,'bold italic'),justify=tk.LEFT).grid(column=1,row=4,padx=10,pady=10,sticky=tk.W)

				bkgid=tk.StringVar()
				bkgid_inp=ttk.Combobox(delete_win,textvariable=bkgid,font=fnt,width=19)
				bkgid_inp.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
				bkgid_inp['values']=taxi_bkgid_list

				delete_btn=tk.Button(delete_win,text='Delete',font=fntit,command=delete_taxi_bkg,fg='red')
				delete_btn.grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)
				delete_win.bind('<Return>',lambda event:delete_taxi_bkg())

			tk.Grid.columnconfigure(manage_tbkg_win,0,weight=1)

			#FRAME 1
			tk.Grid.rowconfigure(manage_tbkg_win,0,weight=1)
			f1=tk.Frame(manage_tbkg_win)
			f1.grid(row=0,column=0,sticky=tk.NSEW)

			#frame 1 grid
			tk.Grid.columnconfigure(f1,0,weight=1)
			tk.Grid.columnconfigure(f1,1,weight=1)

			tk.Grid.rowconfigure(f1,0,weight=1)
			taxi_icon=tk.PhotoImage(file='icons/taxi.png')
			header_img=tk.Label(f1,image=taxi_icon)
			header_img.grid(column=0,row=0,sticky=tk.E,padx=10,pady=10)
			header_img.image=taxi_icon
			tk.Label(f1,text=('Manage the taxi booking...'),font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)

			tk.Label(f1,text=('Connected to database: '+con.database),font=h2fnt,justify=tk.LEFT,fg='green').grid(column=1,row=1,sticky=tk.W,padx=10,pady=10)
			ttk.Separator(f1,orient='horizontal').grid(column=0,row=2,sticky=tk.EW,padx=10,pady=10,columnspan=2)
			#FRAME 2
			tk.Grid.rowconfigure(manage_tbkg_win,1,weight=1)
			f2=tk.Frame(manage_tbkg_win)
			f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

			#frame 2 grid
			tk.Grid.columnconfigure(f2,0,weight=1)
			tk.Grid.columnconfigure(f2,1,weight=1)
			tk.Grid.columnconfigure(f2,2,weight=1)
			tk.Grid.columnconfigure(f2,3,weight=1)

			tk.Label(f2,text='You can:',font=fntit,justify=tk.LEFT).grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

			tk.Grid.rowconfigure(f2,5,weight=1)
			viewall_icon=tk.PhotoImage(file='icons/preview.png')
			viewall_btn=tk.Button(f2,text='view all',image=viewall_icon,font=fnt,command=viewbkg_all)
			viewall_btn.grid(column=0,row=5,padx=10,pady=10,sticky=tk.E)
			viewall_btn.image=viewall_icon
			tk.Label(f2,text='View all booking details.',font=fnt,fg='blue').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

			viewone_icon=tk.PhotoImage(file='icons/search_bkgs.png')
			viewone_btn=tk.Button(f2,text='viewone',image=viewone_icon,font=fnt,command=viewbkg_single)
			viewone_btn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
			viewone_btn.image=viewone_icon
			tk.Label(f2,text='View a single booking details.',font=fnt).grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)

			tk.Grid.rowconfigure(f2,7,weight=1)
			delete_icon=tk.PhotoImage(file='icons/delete_bkgs.png')
			delete_btn=tk.Button(f2,text='del',image=delete_icon,font=fnt,command=delbkg)
			delete_btn.grid(column=0,row=7,padx=10,pady=10,sticky=tk.E)
			delete_btn.image=delete_icon
			tk.Label(f2,text='Delete a booking.',font=fnt,fg='red').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)
			tk.Grid.rowconfigure(f2,8,weight=1)
			tk.Message(f2,text='WARNING: This will delete\nthe booking selected\nfrom the system permanently.',width=500,font=fnt,fg='white',bg='red').grid(column=1,row=8,padx=10,pady=10,sticky=tk.NW)

			tk.Grid.rowconfigure(f2,16,weight=1)
			
			manage_tbkg_win.mainloop()

		def manage_payments():														# Manage payment details

			manage_pay_win=tk.Toplevel()
			manage_pay_win.title('Transaction Manager')
			icon=tk.PhotoImage(file='img/icon.png')
			manage_pay_win.iconphoto(False,icon)

			def viewpay_all():  #View all transactions
				viewall_win=tk.Toplevel()
				viewall_win.title('All transactions')
				viewall_win.resizable(False,False)
				icon=tk.PhotoImage(file='img/icon.png')
				viewall_win.iconphoto(False,icon)
				
				header=('Payment ID','Timestamp','Booking ID','Amount ($)','Payment Type','Card Number','Card Name','CVV','Expiry Month','Expiry Year')

				sql2=str('select * from payment_details')			#getting data from table
				cur.execute(sql2)
				data=[header]+cur.fetchall()						#appending header to data
				
				rows=len(data)
				cols=len(data[0])

				for i in range(rows):							#drawing the table in GUI
					for j in range(cols):
						entry = tk.Label(viewall_win,borderwidth=1,relief='solid',padx=10,height=2,font=fnt)
						entry.grid(row=i, column=j,padx=2,pady=2,sticky=tk.EW)
						entry.configure(text=data[i][j])
						if i==0:
							entry.configure(fg='red',font=fntit)	#colors and italicises header

			def viewpay_single():	#View single transaction
				
				def get_payinfo():
					if (not payid.get()=='' and not payid.get().isspace()) and (not payid.get()=='' and not payid.get().isspace()):
						if payid.get() in payment_id_list:
							sql='select * from payment_details where pay_id=%s'
							val=(payid.get(),)
							cur.execute(sql,val)
							c=cur.fetchall()
							pay_id=c[0][0]
							pay_ts=c[0][1]
							bkgid=c[0][2]
							amt=c[0][3]
							pay_type=c[0][4]
							cardno=c[0][5]
							cardname=c[0][6]
							cvv=c[0][7]
							exp_mo=c[0][8]
							exp_yr=c[0][9]
							
							e=[('Payment ID',pay_id),('Timestamp',pay_ts),('Booking ID',bkgid),('Amount ($)',amt),('Payment Type',pay_type),('Card Number',cardno),('Cardholder Name',cardname),('CVV',cvv),('Expiry Month',exp_mo),('Expiry Year',exp_yr)]
							
							rows=len(e)
							cols=len(e[0])
							tk.Label(frame3,font=fntit,text='Data').grid(row=0,column=0,sticky=tk.W)
							for i in range(rows):							#drawing the table in GUI
								for j in range(cols):
									entry = tk.Label(frame2,borderwidth=1,relief='solid',padx=10,width=30,height=2,font=fnt)
									entry.grid(row=i,column=j,padx=2,pady=2,sticky=tk.EW)
									entry.configure(text=e[i][j])
									if j==0:
										entry.configure(fg='red',font=fntit) #colors and italicises header
						else:
							messagebox.showerror('Error','Transaction \''+payid.get()+'\' does not exist.',parent=viewone_win)
					else:
						messagebox.showerror('Error','Please enter the transaction (payment) ID.',parent=viewone_win)
				viewone_win=tk.Toplevel()
				viewone_win.title('View transaction details')
				viewone_win.resizable(False,False)
				icon=tk.PhotoImage(file='img/icon.png')
				viewone_win.iconphoto(False,icon)
				
				frame1=tk.Frame(viewone_win)
				frame1.grid(row=0,column=0,padx=10,pady=10,sticky=tk.EW)

				frame2=tk.Frame(viewone_win)
				frame2.grid(row=2,column=0,padx=10,pady=10,sticky=tk.EW)

				frame3=tk.Frame(viewone_win)
				frame3.grid(row=1,column=0,padx=10,pady=10,sticky=tk.W)

				cur.execute('select pay_id from payment_details')
				a=cur.fetchall()
				payment_id_list=[]
				for i in a:
					payment_id_list.append(i[0])

				img14=tk.PhotoImage(file='icons/searchusr.png')
				img=tk.Label(frame1,image=img14,font=h1fnt)
				img.grid(column=0,row=0,padx=10,pady=10)
				img.image=img14

				tk.Label(frame1,font=h1fnt,text='View transaction details...').grid(row=0,column=1,padx=10,pady=10,sticky=tk.W)

				tk.Label(frame1,font=fnt,text='Enter transaction (payment) ID.').grid(row=4,column=1,padx=10,pady=10,sticky=tk.W)
				n=tk.StringVar()
				payid=ttk.Combobox(frame1,textvariable=n,font=fnt)
				payid.grid(row=5,column=1,padx=10,pady=10,sticky=tk.EW)
				payid['values']=payment_id_list
				
				submit=tk.Button(frame1,font=fntit,text='Submit',command=get_payinfo)
				submit.grid(row=5,column=2,padx=10,pady=10)
				viewone_win.bind('<Return>',lambda event:get_payinfo())

			def delpay(): 																		# Delete transaction page
				delete_win=tk.Toplevel()
				delete_win.resizable(False,False)
				delete_win.title('Cancel transaction')
				icon=tk.PhotoImage(file='img/icon.png')
				delete_win.iconphoto(False,icon)
				
				cur.execute('select pay_id,bkgid from payment_details')
				pay_bkg_dict=dict(cur.fetchall())
				
				def delete_transaction():														# Delete transactions
					if not payid_inp.get()=='' and not payid_inp.get().isspace():
						if payid_inp.get() in payment_id_list:
							messagebox.showwarning('','This operation will cancel the transaction selected.\nContinue?',parent=delete_win)
							confirm=messagebox.askyesno('','Do you wish to cancel the transaction '+payid_inp.get()+'?',parent=delete_win)
							if confirm == True:
								sql='delete from payment_details where pay_id=%s'				# Deletes payment entry from payment db
								val=(payid_inp.get(),)
								cur.execute(sql,val)
								
								if pay_bkg_dict[payid_inp.get()][0]=='B':							# Deletes booking entry from booking db
									sql2='delete from bus_bkgs where bkgid=%s'
								elif pay_bkg_dict[payid_inp.get()][0]=='T':
									sql2='delete from taxi_bkgs where bkgid=%s'
								val2=(pay_bkg_dict[payid_inp.get()],)
								cur.execute(sql2,val2)
								
								sql3='delete from tkt_details where bkgid=%s'					# Delete correpsonding ticket records
								cur.execute(sql3,val2)
								
								con.commit()
								messagebox.showinfo('','Transaction '+payid_inp.get()+' reversed;\nBooking '+pay_bkg_dict[payid_inp.get()]+' cancelled, and corresponding tickets cancelled',parent=delete_win)
								delete_win.destroy()
							else:
								messagebox.showinfo('','Transaction '+payid_inp.get()+' not cancelled.\nThe database has not been modified.',parent=delete_win)
						else:
							messagebox.showerror('Error','Transaction \''+payid_inp.get()+'\' does not exist.',parent=delete_win)
					else:
						messagebox.showerror('','Please enter the transaction (payment) ID.',parent=delete_win)
					
				delete_icon3=tk.PhotoImage(file='icons/delete.png')
				header_img=tk.Label(delete_win,image=delete_icon3,font=h1fnt)
				header_img.grid(column=0,row=0,padx=10,pady=10)
				header_img.image=delete_icon3

				tk.Label(delete_win,text='Cancel a transaction',font=h1fnt).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

				cur.execute('select pay_id from payment_details')
				d=cur.fetchall()
				payment_id_list=[]
				for i in d:
					payment_id_list.append(str(i[0]))

				tk.Label(delete_win,text='Select the transaction to be cancelled.',font=fntit,justify=tk.LEFT).grid(column=1,row=3,padx=10,pady=10,sticky=tk.W)
				tk.Label(delete_win,text='NOTE: The corresponding booking will\nalso be deleted.',font=('Cascadia Mono',12,'bold italic'),justify=tk.LEFT).grid(column=1,row=4,padx=10,pady=10,sticky=tk.W)

				pay_id=tk.StringVar()
				payid_inp=ttk.Combobox(delete_win,textvariable=pay_id,font=fnt,width=19)
				payid_inp.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
				payid_inp['values']=payment_id_list

				delete_btn=tk.Button(delete_win,text='Delete',font=fntit,command=delete_transaction,fg='red')
				delete_btn.grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)
				delete_win.bind('<Return>',lambda event:delete_transaction())

			tk.Grid.columnconfigure(manage_pay_win,0,weight=1)

			#FRAME 1
			tk.Grid.rowconfigure(manage_pay_win,0,weight=1)
			f1=tk.Frame(manage_pay_win)
			f1.grid(row=0,column=0,sticky=tk.NSEW)

			#frame 1 grid
			tk.Grid.columnconfigure(f1,0,weight=1)
			tk.Grid.columnconfigure(f1,1,weight=1)

			tk.Grid.rowconfigure(f1,0,weight=1)
			pay_icon=tk.PhotoImage(file='icons/make-payment.png')
			header_img=tk.Label(f1,image=pay_icon)
			header_img.grid(column=0,row=0,sticky=tk.E,padx=10,pady=10)
			header_img.image=pay_icon
			tk.Label(f1,text=('Manage transactions...'),font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)

			tk.Label(f1,text=('Connected to database: '+con.database),font=h2fnt,justify=tk.LEFT,fg='green').grid(column=1,row=1,sticky=tk.W,padx=10,pady=10)
			ttk.Separator(f1,orient='horizontal').grid(column=0,row=2,sticky=tk.EW,padx=10,pady=10,columnspan=2)
			#FRAME 2
			tk.Grid.rowconfigure(manage_pay_win,1,weight=1)
			f2=tk.Frame(manage_pay_win)
			f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

			#frame 2 grid
			tk.Grid.columnconfigure(f2,0,weight=1)
			tk.Grid.columnconfigure(f2,1,weight=1)
			tk.Grid.columnconfigure(f2,2,weight=1)
			tk.Grid.columnconfigure(f2,3,weight=1)

			tk.Label(f2,text='You can:',font=fntit,justify=tk.LEFT).grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

			tk.Grid.rowconfigure(f2,5,weight=1)
			viewall_icon=tk.PhotoImage(file='icons/preview.png')
			viewall_btn=tk.Button(f2,text='view all',image=viewall_icon,font=fnt,command=viewpay_all)
			viewall_btn.grid(column=0,row=5,padx=10,pady=10,sticky=tk.E)
			viewall_btn.image=viewall_icon
			tk.Label(f2,text='View all transaction details.',font=fnt,fg='blue').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

			viewone_icon=tk.PhotoImage(file='icons/search_bkgs.png')
			viewone_btn=tk.Button(f2,text='viewone',image=viewone_icon,font=fnt,command=viewpay_single)
			viewone_btn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
			viewone_btn.image=viewone_icon
			tk.Label(f2,text='View a single transaction\'s details.',font=fnt).grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)

			tk.Grid.rowconfigure(f2,7,weight=1)
			delete_icon=tk.PhotoImage(file='icons/delete.png')
			delete_btn=tk.Button(f2,text='del',image=delete_icon,font=fnt,command=delpay)
			delete_btn.grid(column=0,row=7,padx=10,pady=10,sticky=tk.E)
			delete_btn.image=delete_icon
			tk.Label(f2,text='Cancel a transaction.',font=fnt,fg='red').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)
			tk.Grid.rowconfigure(f2,8,weight=1)
			tk.Message(f2,text='WARNING: This will cancel\nthe transaction selected\nfrom the system permanently.',width=500,font=fnt,fg='white',bg='red').grid(column=1,row=8,padx=10,pady=10,sticky=tk.NW)

			tk.Grid.rowconfigure(f2,16,weight=1)
			
			manage_pay_win.mainloop()

		def admin_menu():															# Admin menu
			root=tk.Tk()
			root.title('Admin menu')
			icon=tk.PhotoImage(file='img/icon.png')
			root.iconphoto(False,icon)

			try:
				root.state('zoomed')
			except:
				w,h=root.winfo_screenwidth(),root.winfo_screenheight()
				root.geometry(str(w)+'x'+str(h))

			def logout():
				root.destroy()
				emp_main()

			def bookings():
				booking_portal()

			def manage_admin():	#Manage admins

				#Creating Toplevel window
				mgadmin_win=tk.Toplevel()
				mgadmin_win.title('Administrator Manager')
				icon=tk.PhotoImage(file='img/icon.png')
				mgadmin_win.iconphoto(False,icon)

				def viewadmin_all():	#Show all Administrators
					viewall_win=tk.Toplevel()
					viewall_win.title('All administrators')
					viewall_win.resizable(False,False)
					icon=tk.PhotoImage(file='img/icon.png')
					viewall_win.iconphoto(False,icon)
					
					header=('Admin ID','Admin Username','Admin Name','Admin Password')

					sql2=str('select * from admin')			#getting data from table
					cur.execute(sql2)
					data=[header]+cur.fetchall()						#appending header to data
					
					rows=len(data)
					cols=len(data[0])

					for i in range(rows):							#drawing the table in GUI
						for j in range(cols):
							entry = tk.Label(viewall_win,borderwidth=1,relief='solid',padx=10,height=2,font=fnt)
							entry.grid(row=i, column=j,padx=2,pady=2,sticky=tk.EW)
							entry.configure(text=data[i][j])
							if i==0:
								entry.configure(fg='red',font=fntit)	#colors and italicises header

				def viewadmin_single():	#View details of administrator
					def getadmninfo():	#Gets data from DB

						if not uname.get()=='' and not uname.get().isspace():
							if uname.get() in admin_list:
								sql='select * from admin where admin_uname=%s'
								val=(uname.get(),)
								cur.execute(sql,val)
								c=cur.fetchall()
								admin_id=c[0][0]
								admin_uname=c[0][1]
								admin_name=c[0][2]
								admin_passwd=c[0][3]
								
								data=[('Administrator ID',admin_id),('Administrator Username',admin_uname),('Administrator Full Name',admin_name),('Administrator Password',admin_passwd)]
								
								rows=len(data)
								cols=len(data[0])
								tk.Label(frame3,font=fntit,text='Data').grid(row=0,column=0,sticky=tk.W)
								for i in range(rows):							#drawing the table in GUI
									for j in range(cols):
										entry = tk.Label(frame2,borderwidth=1,relief='solid',padx=10,width=30,height=2,font=fnt)
										entry.grid(row=i,column=j,padx=2,pady=2,sticky=tk.EW)
										entry.configure(text=data[i][j])
										if j==0:
											entry.configure(fg='red',font=fntit) #colors and italicises header
							else:
								messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=viewone_win)
						else:
							messagebox.showerror('Error','Please enter the administrator username.',parent=viewone_win)
					
					#Creating Toplevel window
					viewone_win=tk.Toplevel()
					viewone_win.title('View admin details')
					viewone_win.resizable(False,False)
					icon=tk.PhotoImage(file='img/icon.png')
					viewone_win.iconphoto(False,icon)
					
					#Dividing window into frames
					frame1=tk.Frame(viewone_win)
					frame1.grid(row=0,column=0,padx=10,pady=10,sticky=tk.EW)

					frame2=tk.Frame(viewone_win)
					frame2.grid(row=2,column=0,padx=10,pady=10,sticky=tk.EW)

					frame3=tk.Frame(viewone_win)
					frame3.grid(row=1,column=0,padx=10,pady=10,sticky=tk.W)

					#Creates list of admins for dropdown
					cur.execute('select admin_uname from admin')
					a=cur.fetchall()
					admin_list=[]
					for i in a:
						admin_list.append(i[0])

					img14=tk.PhotoImage(file='icons/searchusr.png')
					img=tk.Label(frame1,image=img14,font=h1fnt)
					img.grid(column=0,row=0,padx=10,pady=10)
					img.image=img14

					tk.Label(frame1,font=h1fnt,text='View administrator details').grid(row=0,column=1,padx=10,pady=10,sticky=tk.W)

					tk.Label(frame1,font=fnt,text='Enter username of administrator.').grid(row=4,column=1,padx=10,pady=10,sticky=tk.W)
					n=tk.StringVar()
					uname=ttk.Combobox(frame1,textvariable=n,font=fnt)
					uname.grid(row=5,column=1,padx=10,pady=10,sticky=tk.EW)
					uname['values']=admin_list
					
					submit=tk.Button(frame1,font=fntit,text='Submit',command=getadmninfo)
					submit.grid(row=5,column=2,padx=10,pady=10)
					
					#Binds Enter key to submit function
					viewone_win.bind('<Return>',lambda event:getadmninfo())

				def deladmin():	#Deletes an administrator.
					delone_win=tk.Toplevel()
					delone_win.resizable(False,False)
					delone_win.title('Delete adminstrator')
					icon=tk.PhotoImage(file='img/icon.png')
					delone_win.iconphoto(False,icon)
					
					#Creates list of admins and respective full names.
					cur.execute('select admin_uname,admin_name from admin')
					a=cur.fetchall()
					admin_namelist=dict(a)

					def delete_admin():		#Delets from DB.
						if not uname.get()=='' and not uname.get().isspace():
							if uname.get() in admin_list:
								messagebox.showwarning('','This operation will delete\nthe username of the administrator permanently.\nContinue?',parent=delone_win)
								confirm=messagebox.askyesno('','Do you wish to delete the administrator '+admin_namelist[uname.get()]+'?',parent=delone_win)
								if confirm == True:
									sql='delete from admin where admin_uname =%s'
									val=(uname.get(),)
									cur.execute(sql,val)
									con.commit()
									messagebox.showinfo('','Administrator '+admin_namelist[uname.get()]+' deleted.',parent=delone_win)
									delone_win.destroy()
								else:
									messagebox.showinfo('','Administrator '+admin_namelist[uname.get()]+' not deleted.\nThe database has not been modified.',parent=delone_win)
							else:
								messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=delone_win)
						else:
							messagebox.showerror('','Please enter the administrator username.',parent=delone_win)
					
					img14=tk.PhotoImage(file='icons/ban_user.png')
					img=tk.Label(delone_win,image=img14,font=h1fnt)
					img.grid(column=0,row=0,padx=10,pady=10)
					img.image=img14

					tk.Label(delone_win,text='Delete an administrator...',font=h1fnt).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

					cur.execute('select admin_uname from admin')
					d=cur.fetchall()
					admin_list=[]
					for i in d:
						admin_list.append(i[0])

					tk.Label(delone_win,text='Select an administrator.',font=fntit).grid(column=1,row=4,padx=10,pady=10,sticky=tk.W)

					n=tk.StringVar()
					uname=ttk.Combobox(delone_win,textvariable=n,font=fnt,width=19)
					uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
					uname['values']=admin_list

					delbtn=tk.Button(delone_win,text='Delete',font=fntit,command=delete_admin,fg='red')
					delbtn.grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

					#Binds Enter key to submit function.
					delone_win.bind('<Return>',lambda event:delete_admin())

				def chpasswd_admin():	#Change password for administrator currently logged in
					passwd_win=tk.Toplevel()
					passwd_win.resizable(False,False)
					passwd_win.title('Change password for administrator')
					icon=tk.PhotoImage(file='img/icon.png')
					passwd_win.iconphoto(False,icon)

					cur.execute('select admin_uname,admin_name from admin')
					a=cur.fetchall()
					admin_namelist=dict(a)

					def change_admin_passwd():	#Changes admin password in DB
						if (not uname.get()=='' and not uname.get().isspace()) and (not npass.get()=='' and not npass.get().isspace()):
							if uname.get() in admin_list:
					
								confirm=messagebox.askyesno('','Do you wish to change the password of '+admin_namelist[uname.get()]+'?',parent=passwd_win)
								if confirm == True:
									sql='update admin set admin_passwd=%s where admin_uname=%s'
									val=(npass.get(),uname.get())
									cur.execute(sql,val)
									con.commit()
									messagebox.showinfo('','Password for '+admin_namelist[uname.get()]+'\nchanged.',parent=passwd_win)
									passwd_win.destroy()
								else:
									messagebox.showinfo('','Password for '+admin_namelist[uname.get()]+' has not been changed..\nThe databasehas not\nbeen modified.',parent=passwd_win)
							else:
								messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=passwd_win)
						else:
							messagebox.showerror('','Do not leave any fields blank.',parent=passwd_win)
					
					img14=tk.PhotoImage(file='icons/passwd.png')
					img=tk.Label(passwd_win,image=img14,font=h1fnt)
					img.grid(column=0,row=0,padx=10,pady=10)
					img.image=img14

					tk.Label(passwd_win,text='Change password\nfor administrator...',font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

					cur.execute('select admin_uname from admin')
					d=cur.fetchall()
					admin_list=[]
					for i in d:
						admin_list.append(i[0])

					n=tk.StringVar()
					tk.Label(passwd_win,text='Username',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
					uname=ttk.Combobox(passwd_win,textvariable=n,font=fnt,width=19)
					uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
					uname['values']=admin_list
					uname.current(0)

					tk.Label(passwd_win,text='New password',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
					npass=tk.Entry(passwd_win,font=fnt,show='*')
					npass.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

					subbtn=tk.Button(passwd_win,text='Make changes',font=fntit,command=change_admin_passwd)
					subbtn.grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)
					passwd_win.bind('<Return>',lambda event:change_admin_passwd())

				def register_admin():	#Register a new administrator.
					
					reg_win=tk.Toplevel()
					reg_win.resizable(False,False)
					reg_win.title('Add administrator')
					icon=tk.PhotoImage(file='img/icon.png')
					reg_win.iconphoto(False,icon)

					def add_admin():	#Adds admin in DB
						uname_inp=uname.get().lower()
						fname_inp=fname.get()
						passwd_inp=passwd.get()

						cur.execute('select admin_uname from admin')
						a=cur.fetchall()
						admin_list=[]
						for i in a:
							admin_list.append(i[0])

						if (not uname_inp=='' and not uname_inp.isspace()) and (not fname_inp=='' and not fname_inp.isspace()) and (not passwd_inp=='' and not passwd_inp.isspace()):
							if uname_inp not in admin_list:
								sql='insert into admin values (%s,%s,%s,%s)'
								val=(id,uname_inp,fname_inp,passwd_inp)
								cur.execute(sql,val)
								con.commit()
								messagebox.showinfo('','Administrator '+fname_inp+' registered successfully.',parent=reg_win)
								reg_win.destroy()
							else:
								messagebox.showerror('Error','Username \''+uname_inp+'\'\nalready exists.',parent=reg_win)			
						else:
							messagebox.showerror('Error','Please do not leave any fields blank.',parent=reg_win)
					
					id='A'+str(rd.randint(1000,9999))

					img14=tk.PhotoImage(file='icons/adduser.png')
					img=tk.Label(reg_win,image=img14,font=h1fnt)
					img.grid(column=0,row=0,padx=10,pady=10)
					img.image=img14

					tk.Label(reg_win,text='Register administrator...',font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)

					tk.Label(reg_win,text='UID',font=fnt).grid(column=0,row=3,sticky=tk.E,padx=10,pady=10)
					bkgid=tk.Label(reg_win,text=id,font=fnt)
					bkgid.grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

					#Input fields
					tk.Label(reg_win,text='Full Name',font=fnt).grid(column=0,row=4,sticky=tk.E,padx=10,pady=10)
					fname=tk.Entry(reg_win,font=fnt)
					fname.grid(column=1,row=4,sticky=tk.EW,padx=10,pady=10)

					tk.Label(reg_win,text='Username',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
					uname=tk.Entry(reg_win,font=fnt)
					uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)

					tk.Label(reg_win,text='Password',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
					passwd=tk.Entry(reg_win,font=fnt,show='*')
					passwd.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

					subbtn=tk.Button(reg_win,font=fntit,text='Register',command=add_admin)
					subbtn.grid(column=1,row=12,padx=10,pady=10,sticky=tk.W)

					#Binds Enter to submit function.
					reg_win.bind('<Return>',lambda event:add_admin())

				tk.Grid.columnconfigure(mgadmin_win,0,weight=1)

				#FRAME 1
				tk.Grid.rowconfigure(mgadmin_win,0,weight=1)
				f1=tk.Frame(mgadmin_win)
				f1.grid(row=0,column=0,sticky=tk.NSEW)

				#frame 1 grid
				tk.Grid.columnconfigure(f1,0,weight=1)
				tk.Grid.columnconfigure(f1,1,weight=1)

				tk.Grid.rowconfigure(f1,0,weight=1)
				img6=tk.PhotoImage(file='icons/supervisor.png')
				himg=tk.Label(f1,image=img6)
				himg.grid(column=0,row=0,sticky=tk.E,padx=10,pady=10)
				himg.image=img6
				tk.Label(f1,text=('Manage the administrators...'),font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)

				tk.Label(f1,text=('Connected to database: '+con.database),font=h2fnt,justify=tk.LEFT,fg='green').grid(column=1,row=1,sticky=tk.W,padx=10,pady=10)
				ttk.Separator(f1,orient='horizontal').grid(column=0,row=2,sticky=tk.EW,padx=10,pady=10,columnspan=2)
				#FRAME 2
				tk.Grid.rowconfigure(mgadmin_win,1,weight=1)
				f2=tk.Frame(mgadmin_win)
				f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

				#frame 2 grid
				tk.Grid.columnconfigure(f2,0,weight=1)
				tk.Grid.columnconfigure(f2,1,weight=1)
				tk.Grid.columnconfigure(f2,2,weight=1)
				tk.Grid.columnconfigure(f2,3,weight=1)

				tk.Label(f2,text='You can:',font=fntit,justify=tk.LEFT).grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

				tk.Grid.rowconfigure(f2,5,weight=1)
				img8=tk.PhotoImage(file='icons/preview.png')
				tbviewbtn=tk.Button(f2,text='view all',image=img8,font=fnt,command=viewadmin_all)
				tbviewbtn.grid(column=0,row=5,padx=10,pady=10,sticky=tk.E)
				tbviewbtn.image=img8
				tk.Label(f2,text='View all administrator details.',font=fnt,fg='blue').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

				img10=tk.PhotoImage(file='icons/searchusr.png')
				viewbtn=tk.Button(f2,text='viewone',image=img10,font=fnt,command=viewadmin_single)
				viewbtn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
				viewbtn.image=img10
				tk.Label(f2,text='View a single admin\'s details.',font=fnt).grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)

				tk.Grid.rowconfigure(f2,6,weight=1)
				img7=tk.PhotoImage(file='icons/adduser.png')
				tbviewbtn=tk.Button(f2,text='add',image=img7,font=fnt,command=register_admin)
				tbviewbtn.grid(column=0,row=6,padx=10,pady=10,sticky=tk.E)
				tbviewbtn.image=img7
				tk.Label(f2,text='Register an administrator.',font=fnt,fg='green').grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

				img11=tk.PhotoImage(file='icons/passwd.png')
				passbtn=tk.Button(f2,text='passwd',image=img11,font=fnt,command=chpasswd_admin)
				passbtn.grid(column=2,row=6,padx=10,pady=10,sticky=tk.E)
				passbtn.image=img11
				tk.Label(f2,text='Change the password for an administrator.',font=fnt).grid(column=3,row=6,padx=10,pady=10,sticky=tk.W)

				tk.Grid.rowconfigure(f2,7,weight=1)
				img12=tk.PhotoImage(file='icons/deluser.png')
				delbtn=tk.Button(f2,text='del',image=img12,font=fnt,command=deladmin)
				delbtn.grid(column=0,row=7,padx=10,pady=10,sticky=tk.E)
				delbtn.image=img12
				tk.Label(f2,text='Delete an administrator.',font=fnt,fg='red').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)
				tk.Grid.rowconfigure(f2,8,weight=1)
				tk.Message(f2,text='WARNING: This will delete\nan admin\'s profile\nfrom the system permanently.',width=500,font=fnt,fg='white',bg='red').grid(column=1,row=8,padx=10,pady=10,sticky=tk.NW)

				tk.Grid.rowconfigure(f2,16,weight=1)

			def manage_agents():	#Manage agents (employees)
				#Creating Toplevel window
				manage_agentwin=tk.Toplevel()
				manage_agentwin.title('Agent Manager')
				icon=tk.PhotoImage(file='img/icon.png')
				manage_agentwin.iconphoto(False,icon)

				def viewagent_all():	#View all Agent
					viewall_win=tk.Toplevel()
					viewall_win.title('All Agents')
					viewall_win.resizable(False,False)
					icon=tk.PhotoImage(file='img/icon.png')
					viewall_win.iconphoto(False,icon)
					
					#Headers for table
					header=('Agent ID','Agent Username','Agent Name','Agent Password')

					sql2=str('select * from employees')			
					cur.execute(sql2)
					data=[header]+cur.fetchall()						#appending header to data
					
					rows=len(data)
					cols=len(data[0])

					for i in range(rows):							#drawing the table in GUI
						for j in range(cols):
							entry = tk.Label(viewall_win,borderwidth=1,relief='solid',padx=10,height=2,font=fnt)
							entry.grid(row=i, column=j,padx=2,pady=2,sticky=tk.EW)
							entry.configure(text=data[i][j])
							if i==0:
								entry.configure(fg='red',font=fntit)	#colors and italicises header

				def viewagent_single():	#Show an agent's info
					def getagentinfo():	#Gets data from DB

						if not uname.get()=='' and not uname.get().isspace():
							if uname.get() in agent_list:
								sql='select * from employees where emp_uname=%s'
								val=(uname.get(),)
								cur.execute(sql,val)
								c=cur.fetchall()
								agent_id=c[0][0]
								agent_uname=c[0][1]
								agent_name=c[0][2]
								agent_passwd=c[0][3]
								
								e=[('Agent ID',agent_id),('Agent Username',agent_uname),('Agent Full Name',agent_name),('Agent Password',agent_passwd)]
								
								
								rows=len(e)
								cols=len(e[0])
								tk.Label(frame3,font=fntit,text='Data').grid(row=0,column=0,sticky=tk.W)
								for i in range(rows):							#drawing the table in GUI
									for j in range(cols):
										entry = tk.Label(frame2,borderwidth=1,relief='solid',padx=10,width=30,height=2,font=fnt)
										entry.grid(row=i,column=j,padx=2,pady=2,sticky=tk.EW)
										entry.configure(text=e[i][j])
										if j==0:
											entry.configure(fg='red',font=fntit,width=20) #colors and italicises header
							else:
								messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=viewone_win)
						else:
							messagebox.showerror('Error','Please enter the agent username.',parent=viewone_win)
					viewone_win=tk.Toplevel()
					viewone_win.title('View agent details')
					viewone_win.resizable(False,False)
					icon=tk.PhotoImage(file='img/icon.png')
					viewone_win.iconphoto(False,icon)
					
					frame1=tk.Frame(viewone_win)
					frame1.grid(row=0,column=0,padx=10,pady=10,sticky=tk.EW)

					frame2=tk.Frame(viewone_win)
					frame2.grid(row=2,column=0,padx=10,pady=10,sticky=tk.EW)

					frame3=tk.Frame(viewone_win)
					frame3.grid(row=1,column=0,padx=10,pady=10,sticky=tk.W)

					#Creating list of agent
					cur.execute('select emp_uname from employees')
					a=cur.fetchall()
					agent_list=[]
					for i in a:
						agent_list.append(i[0])

					img14=tk.PhotoImage(file='icons/searchusr.png')
					img=tk.Label(frame1,image=img14,font=h1fnt)
					img.grid(column=0,row=0,padx=10,pady=10)
					img.image=img14

					tk.Label(frame1,font=h1fnt,text='View agent details').grid(row=0,column=1,padx=10,pady=10,sticky=tk.W)

					tk.Label(frame1,font=fnt,text='Enter username of agent.').grid(row=4,column=1,padx=10,pady=10,sticky=tk.W)
					n=tk.StringVar()
					uname=ttk.Combobox(frame1,textvariable=n,font=fnt)
					uname.grid(row=5,column=1,padx=10,pady=10,sticky=tk.EW)
					uname['values']=agent_list
					
					submit=tk.Button(frame1,font=fntit,text='Submit',command=getagentinfo)
					submit.grid(row=5,column=2,padx=10,pady=10)

					#Binds Enter to submit function.
					viewone_win.bind('<Return>',lambda event:getagentinfo())

				def delagent():	#Delete an agent
					delone_win=tk.Toplevel()
					delone_win.resizable(False,False)
					delone_win.title('Delete agent')
					icon=tk.PhotoImage(file='img/icon.png')
					delone_win.iconphoto(False,icon)
					cur.execute('select emp_uname,emp_name from employees')
					a=cur.fetchall()
					agent_namelist=dict(a)
					def delete_agent():	#Delete agent from db
						if not uname.get()=='' and not uname.get().isspace():
							if uname.get() in agent_list:
								messagebox.showwarning('','This operation will delete\nthe profile of the agent permanently.\nContinue?',parent=delone_win)
								confirm=messagebox.askyesno('','Do you wish to delete the agent '+agent_namelist[uname.get()]+'?',parent=delone_win)
								if confirm == True:
									sql='delete from employees where emp_uname =%s'
									val=(uname.get(),)
									cur.execute(sql,val)
									con.commit()
									messagebox.showinfo('','Agent '+agent_namelist[uname.get()]+' deleted.',parent=delone_win)
									delone_win.destroy()
								else:
									messagebox.showinfo('','Agent '+agent_namelist[uname.get()]+' not deleted.\nThe database has not been modified.',parent=delone_win)
							else:
								messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=delone_win)
						else:
							messagebox.showerror('','Please enter the agent username.',parent=delone_win)
					
					img14=tk.PhotoImage(file='icons/ban_user.png')
					img=tk.Label(delone_win,image=img14,font=h1fnt)
					img.grid(column=0,row=0,padx=10,pady=10)
					img.image=img14

					tk.Label(delone_win,text='Delete an agent...',font=h1fnt).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

					cur.execute('select emp_uname from employees')
					d=cur.fetchall()
					agent_list=[]
					for i in d:
						agent_list.append(i[0])

					tk.Label(delone_win,text='Select an agent.',font=fntit).grid(column=1,row=4,padx=10,pady=10,sticky=tk.W)

					n=tk.StringVar()
					uname=ttk.Combobox(delone_win,textvariable=n,font=fnt,width=19)
					uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
					uname['values']=agent_list

					delbtn=tk.Button(delone_win,text='Delete',font=fntit,command=delete_agent,fg='red')
					delbtn.grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)
					delone_win.bind('<Return>',lambda event:delete_agent())

				def chpasswd_agent():	#Change password for agent
					passwd_win=tk.Toplevel()
					passwd_win.resizable(False,False)
					passwd_win.title('Change password for employee')
					icon=tk.PhotoImage(file='img/icon.png')
					passwd_win.iconphoto(False,icon)

					cur.execute('select emp_uname,emp_name from employees')
					a=cur.fetchall()
					agent_namelist=dict(a)
					def change_emp_passwd():	#Changes agent passwd in DB
						if (not uname.get()=='' and not uname.get().isspace()) and (not npass.get()=='' and not npass.get().isspace()):
							if uname.get() in agent_list:
					
								confirm=messagebox.askyesno('','Do you wish to change the password of '+agent_namelist[uname.get()]+'?',parent=passwd_win)
								if confirm == True:
									sql='update employees set emp_passwd=%s where emp_uname=%s'
									val=(npass.get(),uname.get())
									cur.execute(sql,val)
									con.commit()
									messagebox.showinfo('','Password for '+agent_namelist[uname.get()]+'\nchanged.',parent=passwd_win)
									passwd_win.destroy()
								else:
									messagebox.showinfo('','Password for '+agent_namelist[uname.get()]+' has not been changed..\nThe databasehas not\nbeen modified.',parent=passwd_win)
							else:
								messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=passwd_win)
						else:
							messagebox.showerror('','Do not leave any fields blank.',parent=passwd_win)
					
					img14=tk.PhotoImage(file='icons/passwd.png')
					img=tk.Label(passwd_win,image=img14,font=h1fnt)
					img.grid(column=0,row=0,padx=10,pady=10)
					img.image=img14

					tk.Label(passwd_win,text='Change password\nfor agent...',font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

					cur.execute('select emp_uname from employees')
					d=cur.fetchall()
					agent_list=[]
					for i in d:
						agent_list.append(i[0])

					n=tk.StringVar()
					tk.Label(passwd_win,text='Username',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
					uname=ttk.Combobox(passwd_win,textvariable=n,font=fnt,width=19)
					uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
					uname['values']=agent_list
					uname.current(0)

					tk.Label(passwd_win,text='New password',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
					npass=tk.Entry(passwd_win,font=fnt,show='*')
					npass.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

					subbtn=tk.Button(passwd_win,text='Make changes',font=fntit,command=change_emp_passwd)
					subbtn.grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)
					passwd_win.bind('<Return>',lambda event:change_emp_passwd())

				def register_agent():	#Add an agent.
					reg_win=tk.Toplevel()
					reg_win.resizable(False,False)
					reg_win.title('Add agent')
					icon=tk.PhotoImage(file='img/icon.png')
					reg_win.iconphoto(False,icon)

					def add_agent():	#Adds agent to DB.
						uname_inp=uname.get().lower()
						fname_inp=fname.get()
						passwd_inp=passwd.get()
						
						#Creates list of employees
						cur.execute('select emp_uname from employees')
						a=cur.fetchall()
						agent_list=[]
						for i in a:
							agent_list.append(i[0])

						if (not uname_inp=='' and not uname_inp.isspace()) and (not fname_inp=='' and not fname_inp.isspace()) and (not passwd_inp=='' and not passwd_inp.isspace()):
							if uname_inp not in agent_list:
								sql='insert into employees values (%s,%s,%s,%s)'
								val=(id,uname_inp,fname_inp,passwd_inp)
								cur.execute(sql,val)
								con.commit()
								messagebox.showinfo('','Agent '+fname_inp+' registered successfully.',parent=reg_win)
								reg_win.destroy()
							else:
								messagebox.showerror('Error','Username \''+uname_inp+'\'\nalready exists.',parent=reg_win)
						else:
							messagebox.showerror('Error','Please do not leave any fields blank.',parent=reg_win)
					
					id='E'+str(rd.randint(1000,9999))

					img14=tk.PhotoImage(file='icons/adduser.png')
					img=tk.Label(reg_win,image=img14,font=h1fnt)
					img.grid(column=0,row=0,padx=10,pady=10)
					img.image=img14

					tk.Label(reg_win,text='Register agent...',font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)

					tk.Label(reg_win,text='UID',font=fnt).grid(column=0,row=3,sticky=tk.E,padx=10,pady=10)
					bkgid=tk.Label(reg_win,text=id,font=fnt)
					bkgid.grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

					tk.Label(reg_win,text='Full Name',font=fnt).grid(column=0,row=4,sticky=tk.E,padx=10,pady=10)
					fname=tk.Entry(reg_win,font=fnt)
					fname.grid(column=1,row=4,sticky=tk.EW,padx=10,pady=10)

					tk.Label(reg_win,text='Username',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
					uname=tk.Entry(reg_win,font=fnt)
					uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)

					tk.Label(reg_win,text='Password',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
					passwd=tk.Entry(reg_win,font=fnt,show='*')
					passwd.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

					subbtn=tk.Button(reg_win,font=fntit,text='Register',command=add_agent)
					subbtn.grid(column=1,row=12,padx=10,pady=10,sticky=tk.W)

					reg_win.bind('<Return>',lambda event:add_agent())
				tk.Grid.columnconfigure(manage_agentwin,0,weight=1)

				#FRAME 1
				tk.Grid.rowconfigure(manage_agentwin,0,weight=1)
				f1=tk.Frame(manage_agentwin)
				f1.grid(row=0,column=0,sticky=tk.NSEW)

				#frame 1 grid
				tk.Grid.columnconfigure(f1,0,weight=1)
				tk.Grid.columnconfigure(f1,1,weight=1)

				tk.Grid.rowconfigure(f1,0,weight=1)
				img6=tk.PhotoImage(file='icons/employee.png')
				himg=tk.Label(f1,image=img6)
				himg.grid(column=0,row=0,sticky=tk.E,padx=10,pady=10)
				himg.image=img6
				tk.Label(f1,text=('Manage the agents...'),font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)

				tk.Label(f1,text=('Connected to database: '+con.database),font=h2fnt,justify=tk.LEFT,fg='green').grid(column=1,row=1,sticky=tk.W,padx=10,pady=10)
				ttk.Separator(f1,orient='horizontal').grid(column=0,row=2,sticky=tk.EW,padx=10,pady=10,columnspan=2)
				#FRAME 2
				tk.Grid.rowconfigure(manage_agentwin,1,weight=1)
				f2=tk.Frame(manage_agentwin)
				f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

				#frame 2 grid
				tk.Grid.columnconfigure(f2,0,weight=1)
				tk.Grid.columnconfigure(f2,1,weight=1)
				tk.Grid.columnconfigure(f2,2,weight=1)
				tk.Grid.columnconfigure(f2,3,weight=1)

				tk.Label(f2,text='You can:',font=fntit,justify=tk.LEFT).grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

				tk.Grid.rowconfigure(f2,5,weight=1)
				img8=tk.PhotoImage(file='icons/preview.png')
				tbviewbtn=tk.Button(f2,text='view all',image=img8,font=fnt,command=viewagent_all)
				tbviewbtn.grid(column=0,row=5,padx=10,pady=10,sticky=tk.E)
				tbviewbtn.image=img8
				tk.Label(f2,text='View all agent details.',font=fnt,fg='blue').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

				img10=tk.PhotoImage(file='icons/searchusr.png')
				viewbtn=tk.Button(f2,text='viewone',image=img10,font=fnt,command=viewagent_single)
				viewbtn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
				viewbtn.image=img10
				tk.Label(f2,text='View a single agent\'s details.',font=fnt).grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)

				tk.Grid.rowconfigure(f2,6,weight=1)
				img7=tk.PhotoImage(file='icons/adduser.png')
				tbviewbtn=tk.Button(f2,text='add',image=img7,font=fnt,command=register_agent)
				tbviewbtn.grid(column=0,row=6,padx=10,pady=10,sticky=tk.E)
				tbviewbtn.image=img7
				tk.Label(f2,text='Register an agent.',font=fnt,fg='green').grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

				img11=tk.PhotoImage(file='icons/passwd.png')
				passbtn=tk.Button(f2,text='passwd',image=img11,font=fnt,command=chpasswd_agent)
				passbtn.grid(column=2,row=6,padx=10,pady=10,sticky=tk.E)
				passbtn.image=img11
				tk.Label(f2,text='Change the password for an agent.',font=fnt).grid(column=3,row=6,padx=10,pady=10,sticky=tk.W)

				tk.Grid.rowconfigure(f2,7,weight=1)
				img12=tk.PhotoImage(file='icons/deluser.png')
				delbtn=tk.Button(f2,text='del',image=img12,font=fnt,command=delagent)
				delbtn.grid(column=0,row=7,padx=10,pady=10,sticky=tk.E)
				delbtn.image=img12
				tk.Label(f2,text='Delete an agent.',font=fnt,fg='red').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)
				tk.Grid.rowconfigure(f2,8,weight=1)
				tk.Message(f2,text='WARNING: This will delete\nan agent\'s profile\nfrom the system permanently.',width=500,font=fnt,fg='white',bg='red').grid(column=1,row=8,padx=10,pady=10,sticky=tk.NW)

				tk.Grid.rowconfigure(f2,16,weight=1)
			
			'''def manage_users():	#Manage users
				manageuserwin=tk.Toplevel()
				manageuserwin.title('User Manager')
				icon=tk.PhotoImage(file='img/icon.png')
				manageuserwin.iconphoto(False,icon)


				def viewuser_all():		#View all users
					viewall_win=tk.Toplevel()
					viewall_win.title('All users')
					viewall_win.resizable(False,False)
					icon=tk.PhotoImage(file='img/icon.png')
					viewall_win.iconphoto(False,icon)

					
					header=('User ID','Full Name','Electronic Mail','Number','Username','Password')

					sql2=str('select * from users')	

					cur.execute(sql2)
					data=[header]+cur.fetchall()						#appending header to data
					
					rows=len(data)
					cols=len(data[0])

					for i in range(rows):							#drawing the table in GUI
						for j in range(cols):
							entry = tk.Label(viewall_win,borderwidth=1,relief='solid',padx=10,height=2,font=fnt)
							entry.grid(row=i,column=j,padx=2,pady=2,sticky=tk.EW)
							entry.configure(text=data[i][j])
							if i==0:
								entry.configure(fg='red',font=fntit)	#colors and italicises header

				def viewuser_single():	#view single user

					def getuserinfo():	#gets user info from DB

						if not uname.get()=='' and not uname.get().isspace():
							if uname.get() in user_list:
								sql='select * from users where uname=%s'
								val=(uname.get(),)
								cur.execute(sql,val)
								c=cur.fetchall()
								user_id=c[0][0]
								user_fname=c[0][1]
								user_email=c[0][2]
								user_num=c[0][3]
								user_uname=c[0][4]
								user_passwd=c[0][5]
								
								data=[('User ID',user_id),('Full Name',user_fname),('Electronic Mail',user_email),('Phone Number',user_num),('Username',user_uname),('Password',user_passwd)]
								
								rows=len(data)
								cols=len(data[0])
								tk.Label(frame3,font=fntit,text='Data').grid(row=0,column=0,sticky=tk.W)
								for i in range(rows):							#drawing the table in GUI
									for j in range(cols):
										entry = tk.Label(frame2,borderwidth=1,relief='solid',padx=10,height=2,width=25,font=fnt)
										entry.grid(row=i,column=j,padx=2,pady=2,sticky=tk.EW)
										entry.configure(text=data[i][j])
										if j==0:
											entry.configure(fg='red',font=fntit,width=15) #colors and italicises header
							else:
								messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=viewone_win)
						else:
							messagebox.showerror('Error','Please enter the username.',parent=viewone_win)
					
					viewone_win=tk.Toplevel()
					viewone_win.title('View user details')
					viewone_win.resizable(False,False)
					icon=tk.PhotoImage(file='img/icon.png')
					viewone_win.iconphoto(False,icon)
					
					frame1=tk.Frame(viewone_win)
					frame1.grid(row=0,column=0,padx=10,pady=10,sticky=tk.EW)

					frame2=tk.Frame(viewone_win)
					frame2.grid(row=2,column=0,padx=10,pady=10,sticky=tk.EW)

					frame3=tk.Frame(viewone_win)
					frame3.grid(row=1,column=0,padx=10,pady=10,sticky=tk.W)

					cur.execute('select uname from users')
					a=cur.fetchall()
					user_list=[]
					for i in a:
						user_list.append(i[0])

					img14=tk.PhotoImage(file='icons/searchusr.png')
					img=tk.Label(frame1,image=img14,font=h1fnt)
					img.grid(column=0,row=0,padx=10,pady=10)
					img.image=img14

					tk.Label(frame1,font=h1fnt,text='View user details').grid(row=0,column=1,padx=10,pady=10,sticky=tk.W)

					tk.Label(frame1,font=fnt,text='Enter username.').grid(row=4,column=1,padx=10,pady=10,sticky=tk.W)
					n=tk.StringVar()
					uname=ttk.Combobox(frame1,textvariable=n,font=fnt)
					uname.grid(row=5,column=1,padx=10,pady=10,sticky=tk.EW)
					uname['values']=user_list
					
					submit=tk.Button(frame1,font=fntit,text='Submit',command=getuserinfo)
					submit.grid(row=5,column=2,padx=10,pady=10)
					
					#Binds Enter to submit function.
					viewone_win.bind('<Return>',lambda event:getuserinfo())

				def deluser():	#delete user
					delone_win=tk.Toplevel()
					delone_win.resizable(False,False)
					delone_win.title('Delete user')
					icon=tk.PhotoImage(file='img/icon.png')
					delone_win.iconphoto(False,icon)

					cur.execute('select uname,fname from users')
					a=cur.fetchall()
					user_namelist=dict(a)

					def delete_user(): #deletes user from DB.
						
						if not uname.get()=='' and not uname.get().isspace():
							if uname.get() in users_list:
								messagebox.showwarning('','This operation will delete\nthe user permanently.\nContinue?',parent=delone_win)
								confirm=messagebox.askyesno('','Do you wish to delete the user '+user_namelist[uname.get()]+'?',parent=delone_win)
								if confirm == True:
									sql='delete from users where uname =%s'
									val=(uname.get(),)
									cur.execute(sql,val)
									con.commit()
									messagebox.showinfo('','User '+user_namelist[uname.get()]+' deleted.',parent=delone_win)
									delone_win.destroy()
								else:
									messagebox.showinfo('','User '+user_namelist[uname.get()]+' not deleted.\nThe database has not been modified.',parent=delone_win)
							else:
								messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=delone_win)
						else:
							messagebox.showerror('','Please enter the username.',parent=delone_win)
					
					img14=tk.PhotoImage(file='icons/ban_user.png')
					img=tk.Label(delone_win,image=img14,font=h1fnt)
					img.grid(column=0,row=0,padx=10,pady=10)
					img.image=img14

					tk.Label(delone_win,text='Delete a user.',font=h1fnt).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

					cur.execute('select uname from users')
					d=cur.fetchall()
					users_list=[]
					for i in d:
						users_list.append(i[0])

					tk.Label(delone_win,text='Select a user.',font=fntit).grid(column=1,row=4,padx=10,pady=10,sticky=tk.W)

					n=tk.StringVar()
					uname=ttk.Combobox(delone_win,textvariable=n,font=fnt,width=19)
					uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
					uname['values']=users_list

					delbtn=tk.Button(delone_win,text='Delete',font=fntit,command=delete_user,fg='red')
					delbtn.grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)
					delone_win.bind('<Return>',lambda event:delete_user())

				def chpasswd_user():	#changes password for user
					passwd_win=tk.Toplevel()
					passwd_win.resizable(False,False)
					passwd_win.title('Change password for user')
					icon=tk.PhotoImage(file='img/icon.png')
					passwd_win.iconphoto(False,icon)


					def ch_user_passwd():	#changes password in db
						if (not uname.get()=='' and not uname.get().isspace()) and (not npass.get()=='' and not npass.get().isspace()):
							if uname.get() in users_list:
					
								confirm=messagebox.askyesno('','Do you wish to change the password of '+uname.get()+'?',parent=passwd_win)
								if confirm == True:
									sql='update users set passwd=%s where uname=%s'
									val=(npass.get(),uname.get())
									cur.execute(sql,val)
									con.commit()
									messagebox.showinfo('','Password for '+uname.get()+'\nchanged.',parent=passwd_win)
									passwd_win.destroy()
								else:
									messagebox.showinfo('','Password for '+uname.get()+' has not been changed..\nThe databasehas not\nbeen modified.',parent=passwd_win)
							else:
								messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=passwd_win)
						else:
							messagebox.showerror('','Do not leave any fields blank.',parent=passwd_win)
					
					img14=tk.PhotoImage(file='icons/passwd.png')
					img=tk.Label(passwd_win,image=img14,font=h1fnt)
					img.grid(column=0,row=0,padx=10,pady=10)
					img.image=img14

					tk.Label(passwd_win,text='Change password\nfor user',font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

					cur.execute('select uname from users')
					d=cur.fetchall()
					users_list=[]
					for i in d:
						users_list.append(i[0])

					n=tk.StringVar()
					tk.Label(passwd_win,text='Username',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
					uname=ttk.Combobox(passwd_win,textvariable=n,font=fnt,width=19)
					uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
					uname['values']=users_list
					uname.current(0)

					tk.Label(passwd_win,text='New password',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
					npass=tk.Entry(passwd_win,font=fnt,show='*')
					npass.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

					subbtn=tk.Button(passwd_win,text='Make changes',font=fntit,command=ch_user_passwd)
					subbtn.grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)
					passwd_win.bind('<Return>',lambda event:ch_user_passwd())

				def register_user():	#adds user
					uuid='U'+str(rd.randint(10000,99999))
					
					def add_user():	#adds user to db
						
						reg_fname_inp=reg_fname.get()
						reg_email_inp=reg_email.get()
						reg_num_inp=reg_num.get()
						reg_uname_inp=reg_uname.get().lower()
						reg_passwd_inp=reg_passwd.get()

						cur.execute('select uname from users')
						users=cur.fetchall()

						b=(reg_uname_inp,)
						if (not reg_fname_inp.isspace()==True and not reg_fname_inp=='') and (not reg_email_inp.isspace()==True and not reg_email_inp=='') and (not reg_num_inp.isspace()==True and not reg_num_inp=='') and (not reg_uname_inp.isspace()==True and not reg_uname_inp=='') and (not reg_passwd_inp.isspace()==True and not reg_passwd_inp==''):		#checks if inputs are not empty or contains spaces
							if b not in users:
								if '@' in reg_email_inp and '.' in reg_email_inp:
									if len(reg_num_inp) == 10:
										regsql='insert into users values(%s,%s,%s,%s,%s,%s)'
										regval=(uuid,reg_fname_inp,reg_email_inp,reg_num_inp,reg_uname_inp,reg_passwd_inp)

										cur.execute(regsql,regval)
										con.commit()

										messagebox.showinfo('','The new user '+reg_fname_inp+'\nhas been successfully registered.',parent=reg_win)
										reg_win.destroy()
									else:
										messagebox.showerror('Error','Invalid phone number entered.',parent=reg_win)
								else:
									messagebox.showerror('Error','Invalid electronic mail ID entered.',parent=reg_win)		
							else:

								messagebox.showerror('Error','Username '+reg_uname_inp+'\nalready exists.',parent=reg_win)
						else:
							messagebox.showerror('Error','Please do not leave any fields blank.',parent=reg_win)
					
					reg_win=tk.Toplevel()
					reg_win.title('Add user')
					reg_win.resizable(False, False)
					icon=tk.PhotoImage(file='img/icon.png')
					reg_win.iconphoto(False,icon)


					img15=tk.PhotoImage(file='icons/adduser.png')
					img=tk.Label(reg_win,image=img15,font=h1fnt)
					img.grid(column=0,row=0,padx=10,pady=10,sticky=tk.E)
					img.image=img15

					tk.Label(reg_win,text='Add user...',font=h1fnt).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)
					
					tk.Label(reg_win,text='ID',font=fnt).grid(column=0,row=3,sticky=tk.E,padx=10,pady=10)
					tk.Label(reg_win,text=uuid,font=fnt).grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)
					
					tk.Label(reg_win,text='1. Personal info',font=fntit).grid(column=0,row=5,sticky=tk.W,padx=10,pady=10)

					tk.Label(reg_win,text='Name',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
					reg_fname=tk.Entry(reg_win,font=fnt)
					reg_fname.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

					tk.Label(reg_win,text='Electronic mail ID',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
					reg_email=tk.Entry(reg_win,font=fnt)
					reg_email.grid(column=1,row=7,sticky=tk.EW,padx=10,pady=10)

					tk.Label(reg_win,text='Phone number',font=fnt).grid(column=0,row=8,sticky=tk.E,padx=10,pady=10)
					reg_num=tk.Entry(reg_win,font=fnt)
					reg_num.grid(column=1,row=8,sticky=tk.EW,padx=10,pady=10)

					tk.Label(reg_win,text='2. Login info',font=fntit).grid(column=0,row=10,sticky=tk.W,padx=10,pady=10)

					tk.Label(reg_win,text='Username',font=fnt).grid(column=0,row=11,sticky=tk.E,padx=10,pady=10)
					reg_uname=tk.Entry(reg_win,font=fnt)
					reg_uname.grid(column=1,row=11,sticky=tk.EW,padx=10,pady=10)

					tk.Label(reg_win,text='Password',font=fnt).grid(column=0,row=12,sticky=tk.E,padx=10,pady=10)
					reg_passwd=tk.Entry(reg_win,show='*',font=fnt)
					reg_passwd.grid(column=1,row=12,sticky=tk.EW,padx=10,pady=10)

					regsubmit=tk.Button(reg_win,text='Register',command=add_user,font=fntit)
					regsubmit.grid(column=1,row=14,padx=10,pady=10,sticky=tk.W)
					reg_win.bind('<Return>',lambda event:add_user())

				tk.Grid.columnconfigure(manageuserwin,0,weight=1)

				#FRAME 1
				tk.Grid.rowconfigure(manageuserwin,0,weight=1)
				f1=tk.Frame(manageuserwin)
				f1.grid(row=0,column=0,sticky=tk.NSEW)

				#frame 1 grid
				tk.Grid.columnconfigure(f1,0,weight=1)
				tk.Grid.columnconfigure(f1,1,weight=1)

				tk.Grid.rowconfigure(f1,0,weight=1)
				img6=tk.PhotoImage(file='icons/people.png')
				tk.Label(f1,image=img6).grid(column=0,row=0,sticky=tk.E,padx=10,pady=10)
				himg=tk.Label(f1,text=('Manage the users...'),font=h1fnt)
				himg.grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)
				himg.image=img6
				tk.Label(f1,text=('Connected to database: '+con.database),font=h2fnt,justify=tk.LEFT,fg='green').grid(column=1,row=1,sticky=tk.W,padx=10,pady=10)

				ttk.Separator(f1,orient='horizontal').grid(column=0,row=2,sticky=tk.EW,padx=10,pady=10,columnspan=2)

				#FRAME 2
				tk.Grid.rowconfigure(manageuserwin,1,weight=1)
				f2=tk.Frame(manageuserwin)
				f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

				#frame 2 grid
				tk.Grid.columnconfigure(f2,0,weight=1)
				tk.Grid.columnconfigure(f2,1,weight=1)
				tk.Grid.columnconfigure(f2,2,weight=1)
				tk.Grid.columnconfigure(f2,3,weight=1)

				tk.Label(f2,text='You can:',font=fntit,justify=tk.LEFT).grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

				tk.Grid.rowconfigure(f2,5,weight=1)

				img8=tk.PhotoImage(file='icons/preview.png')
				tbviewbtn=tk.Button(f2,text='view all',image=img8,font=fnt,command=viewuser_all)
				tbviewbtn.grid(column=0,row=5,padx=10,pady=10,sticky=tk.E)
				tbviewbtn.image=img8
				tk.Label(f2,text='View all user details.',font=fnt,fg='blue').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

				img10=tk.PhotoImage(file='icons/searchusr.png')
				viewbtn=tk.Button(f2,text='viewone',image=img10,font=fnt,command=viewuser_single)
				viewbtn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
				viewbtn.imageg=img10
				tk.Label(f2,text='View a single user\'s details.',font=fnt).grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)

				tk.Grid.rowconfigure(f2,6,weight=1)

				img7=tk.PhotoImage(file='icons/adduser.png')
				tbviewbtn=tk.Button(f2,text='add',image=img7,font=fnt,command=register_user)
				tbviewbtn.grid(column=0,row=6,padx=10,pady=10,sticky=tk.E)
				tbviewbtn.image=img7
				tk.Label(f2,text='Add a user.',font=fnt,fg='green').grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

				img11=tk.PhotoImage(file='icons/passwd.png')
				passbtn=tk.Button(f2,text='passwd',image=img11,font=fnt,command=chpasswd_user)
				passbtn.grid(column=2,row=6,padx=10,pady=10,sticky=tk.E)
				passbtn.image=img11
				tk.Label(f2,text='Change the password for a user.',font=fnt).grid(column=3,row=6,padx=10,pady=10,sticky=tk.W)

				tk.Grid.rowconfigure(f2,7,weight=1)
				img12=tk.PhotoImage(file='icons/ban_user.png')
				delbtn=tk.Button(f2,text='del',image=img12,font=fnt,command=deluser)
				delbtn.grid(column=0,row=7,padx=10,pady=10,sticky=tk.E)
				delbtn.image=img12
				tk.Label(f2,text='Delete a user.',font=fnt,fg='red').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)

				tk.Grid.rowconfigure(f2,8,weight=1)
				tk.Message(f2,text='WARNING: This will delete\na user\'s profile\nfrom the system permanently.',width=500,font=fnt,fg='white',bg='red').grid(column=1,row=8,padx=10,pady=10,sticky=tk.NW)

				tk.Grid.rowconfigure(f2,16,weight=1)

				tk.Grid.rowconfigure(f2,17,weight=1)'''				

			def manage_db():	#Manage databases

				# Removes dataframe column output limit
				pd.set_option('display.max_columns', None)

				dbmgr_main_win=tk.Toplevel()
				dbmgr_main_win.title('Database Manager')
				icon=tk.PhotoImage(file='img/icon.png')
				dbmgr_main_win.iconphoto(False,icon)

				cur.execute('show tables')			#creating list of available tables for dropbox
				a=cur.fetchall()
				tables_list=[]
				for i in a:
					tables_list.append(i[0])

				def showtb():	#Show selected table
					if not table.get()=='' and not table.get().isspace():
						if table.get() in tables_list:
							dbwin=tk.Toplevel()
							dbwin.resizable(False,False)
							icon=tk.PhotoImage(file='img/icon.png')
							dbwin.iconphoto(False,icon)
							dbwin.title(table.get()+' table')
							sql=str('desc '+table.get())		#getting headers for table
							cur.execute(sql)
							a=cur.fetchall()
							headers_list=[]
							for x in a:									
								headers_list.append(x[0])
								header=tuple(headers_list)

							sql2=str('select * from '+table.get())			#getting data from table
							cur.execute(sql2)
							data=[header]+cur.fetchall()						#appending header to data
						
							rows=len(data)
							cols=len(data[0])

							for i in range(rows):							#drawing the table in GUI
								for j in range(cols):
									entry = tk.Label(dbwin,borderwidth=1,relief='solid',height=2,font=fnt,padx=10)
									entry.grid(row=i, column=j,padx=2,pady=2,sticky=tk.EW)
									entry.configure(text=data[i][j])
									if i==0:
										entry.configure(fg='red',font=fntit)	#colors and italicises header
						else:
							messagebox.showerror('Error','Table '+table.get()+' does not exist.',parent=dbmgr_main_win)
					else:
						messagebox.showerror('Error','Please choose a table.',parent=dbmgr_main_win)

				def droptb():	#Drop selected table
					if not table.get()=='' and not table.get().isspace():
						if table.get() in tables_list:
							messagebox.showwarning('WARNING','The table chosen will be dropped\nfrom the database permanently.\nContinue?',parent=dbmgr_main_win)
							confirm=messagebox.askyesno('','Do you wish to drop the table \''+table.get()+'\'\nalong with its contents ?',parent=dbmgr_main_win)
							if confirm == True:
								sql=str('drop table '+table.get())
								cur.execute(sql)
								con.commit()
								messagebox.showinfo('','The table \''+table.get()+'\'\nhas been dropped\nfrom the database.',parent=dbmgr_main_win)
							else:
								messagebox.showinfo('','DROP TABLE operation on \''+table.get()+'\' cancelled.\nThe database has not been modified.',parent=dbmgr_main_win)
								pass
						else:
							messagebox.showerror('Error','Table '+table.get()+' does not exist.',parent=dbmgr_main_win)
					else:
						messagebox.showerror('Error','Please choose a table.',parent=dbmgr_main_win)

				def deltb():	#Delete contents of selected table
					if not table.get()=='' and not table.get().isspace():
						if table.get() in tables_list:
							messagebox.showwarning('WARNING','All the contents of the table chosen will be deleted permanently.\nContinue?',parent=dbmgr_main_win)
							confirm=messagebox.askyesno('','Do you wish to delete\nall records from the table \''+table.get()+'\'?',parent=dbmgr_main_win)
							if confirm == True:
								sql=str('delete from '+table.get())
								cur.execute(sql)
								con.commit()
								messagebox.showinfo('','All records in table \''+table.get()+'\'\nhave been permenantly deleted\nfrom the database.',parent=dbmgr_main_win)
							else:
								messagebox.showinfo('','DELETE FROM TABLE operation on \''+table.get()+'\' cancelled.\nThe database has not been modified.',parent=dbmgr_main_win)
								pass
						else:
							messagebox.showerror('Error','Table '+table.get()+' does not exist.',parent=dbmgr_main_win)			
					else:
						messagebox.showerror('Error','Please choose a table.',parent=dbmgr_main_win)

				def exporttb():		#Export selected table to CSV
					if not table.get()=='' and not table.get().isspace():
						if table.get() in tables_list:
							cur.execute('select * from '+table.get())
							data=cur.fetchall()

							sql=str('desc '+table.get())		#Getting description of table structure
							cur.execute(sql)
							desc=cur.fetchall()

							headers_list=[]						#Getting headers from description
							for x in desc:		
								col=x[0]							
								headers_list.append(col)

							df=pd.DataFrame(data,columns=headers_list)		#Conversion of data to Pandas dataframe
							df.set_index(df.columns[0],inplace=True)
							
							def export_to_csv():
								filename_inp=filename.get()
								if not filename_inp=='' and not filename_inp.isspace():
									df.reset_index(inplace=True)
									os.chdir('export')
									df.to_csv(filename_inp,index=False)
									os.chdir('./..')
									messagebox.showinfo('','Table '+table.get()+' exported to '+filename_inp+'.',parent=export_win)
									export_win.destroy()
								else:
									messagebox.showerror('Error','Please enter a filename.',parent=export_win)

							export_win=tk.Toplevel()
							export_win.resizable(False,False)
							export_win.title('Export to CSV')
							icon=tk.PhotoImage(file='img/icon.png')
							export_win.iconphoto(False,icon)
							
							tk.Label(export_win,font=h1fnt,text='Export to CSV file...').grid(row=0,column=0,padx=10,pady=10,sticky=tk.NW)

							Separator(export_win,orient='horizontal').grid(column=0,row=1,sticky=tk.EW,padx=10,pady=10)
							
							tk.Label(export_win,font=('Cascadia Mono',12,'bold italic'),text='Data').grid(row=2,column=0,padx=10,pady=10,sticky=tk.NW)
							
							if df.empty == False:
								txt=str(df)
							else:
								txt='[No data available]'

							tk.Label(export_win,font=fntit,text=txt).grid(row=3,column=0,padx=10,pady=10)

							if df.empty == False:
								shape=('['+str(df.shape[0])+' row(s) x '+str(df.shape[1])+' column(s)]')
								tk.Label(export_win,font=('Cascadia Mono',12,'bold italic'),text=shape).grid(row=4,column=0,padx=10,pady=10)
							
							Separator(export_win,orient='horizontal').grid(column=0,row=6,sticky=tk.EW,padx=10,pady=10)

							tk.Label(export_win,font=fnt,text='Enter the name of the CSV file.\nThe file will be saved to the \'export\' folder.',justify=tk.LEFT).grid(row=9,column=0,padx=10,pady=10,sticky=tk.W)

							filename=tk.Entry(export_win,font=fnt,width=40)
							filename.grid(row=10,column=0,padx=10,pady=10,sticky=tk.W)

							submit=tk.Button(export_win,font=fnt,text='Export',command=export_to_csv)
							submit.grid(row=11,column=0,padx=10,pady=10,sticky=tk.W)

							#Binds Enter key to export function
							export_win.bind('<Return>',lambda event:export_to_csv())
						else:
							messagebox.showerror('Error','Table '+table.get()+' does not exist.',parent=dbmgr_main_win)			
					else:
						messagebox.showerror('Error','Please choose a table.',parent=dbmgr_main_win)

				def help():		#View help page.
					helpwin=tk.Toplevel()
					helpwin.resizable(False,False)
					helpwin.title('Help')
					icon=tk.PhotoImage(file='img/icon.png')
					helpwin.iconphoto(False,icon)

					img14=tk.PhotoImage(file='icons/help.png')
					img=tk.Label(helpwin,image=img14)
					img.grid(column=0,row=0,padx=10,pady=10)
					img.image=img14
					
					tk.Label(helpwin,text='What is the difference between\n\'deleting from\' and \'dropping\' a table?',font=h1fnt,justify=tk.LEFT).grid(row=0,column=1,padx=10,pady=10,sticky=tk.W)
					txt=''''Deleting' from a table performs the SQL DELETE FROM
operation, which (by default, unless a condition is specified with the WHERE clause), 
deletes all records from the table, whilst keeping the table structure intact.

On the other hand, 'dropping' a table performs the SQL DROP TABLE operation, 
which deletes the table structure from the database along with its contents.'''

					a=scrolledtext.ScrolledText(helpwin,wrap=tk.WORD,width=30,height=10,font=fntit)
					a.grid(row=3,column=1,padx=10,pady=10,sticky=tk.EW)
					a.insert(tk.INSERT,txt)
					a.configure(state='disabled')

				menubar=tk.Menu(dbmgr_main_win)

				user=tk.Menu(menubar,tearoff=0)
				menubar.add_cascade(label='Help',menu=user,font=menufnt)

				user.add_command(label='\'Deleting from\' vs \'dropping\' a table',command=help,font=menufnt,underline=0)

				dbmgr_main_win.config(menu=menubar)
					
				tk.Grid.columnconfigure(dbmgr_main_win,0,weight=1)

				#FRAME 1
				tk.Grid.rowconfigure(dbmgr_main_win,0,weight=1)
				f1=tk.Frame(dbmgr_main_win)
				f1.grid(row=0,column=0,sticky=tk.NSEW)

				#frame 1 grid
				tk.Grid.columnconfigure(f1,0,weight=1)
				tk.Grid.columnconfigure(f1,1,weight=1)

				tk.Grid.rowconfigure(f1,0,weight=1)
				
				img6=tk.PhotoImage(file='icons/dataset.png')
				himg=tk.Label(f1,image=img6)
				himg.grid(column=0,row=0,padx=10,pady=10,sticky=tk.E)
				himg.image=img6

				tk.Label(f1,text=('Manage the databases...'),font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)
				tk.Grid.rowconfigure(f1,1,weight=1)
				tk.Label(f1,text=('Connected to database: '+con.database),font=h2fnt,justify=tk.LEFT,fg='green').grid(column=1,row=1,sticky=tk.W,padx=10,pady=1)
				ttk.Separator(f1,orient='horizontal').grid(column=0,row=2,sticky=tk.EW,padx=10,pady=10,columnspan=2)
				#FRAME 2
				tk.Grid.rowconfigure(dbmgr_main_win,1,weight=1)
				f2=tk.Frame(dbmgr_main_win)
				f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

				#frame 2 grid
				tk.Grid.columnconfigure(f2,0,weight=1)
				tk.Grid.columnconfigure(f2,1,weight=1)
				tk.Grid.columnconfigure(f2,2,weight=1)
				tk.Grid.columnconfigure(f2,3,weight=1)

				tk.Label(f2,text='Choose a table.',font=fntit,justify=tk.LEFT).grid(column=1,row=4,sticky=tk.W,padx=10,pady=10)
				img7=tk.PhotoImage(file='icons/table.png')
				h2img=tk.Label(f2,image=img7)
				h2img.grid(column=0,row=4,sticky=tk.E,padx=10,pady=10)
				h2img.image=img7

				tk.Grid.rowconfigure(f2,5,weight=1)
				n=tk.StringVar()
				table=ttk.Combobox(f2,textvariable=n,font=fnt,state='readonly')
				table.grid(row=5,column=1,padx=10,pady=10,sticky=tk.EW)
				table['values']=tables_list

				tk.Label(f2,text='You can:',font=fntit,justify=tk.LEFT).grid(column=1,row=6,sticky=tk.W,padx=10,pady=10)

				tk.Grid.rowconfigure(f2,7,weight=1)
				img8=tk.PhotoImage(file='icons/preview.png')
				tbviewbtn=tk.Button(f2,text='viewtable',image=img8,font=fnt,command=showtb)
				tbviewbtn.grid(column=0,row=7,padx=10,pady=10,sticky=tk.E)
				tbviewbtn.image=img8
				tk.Label(f2,text='View the table.',font=fnt,fg='blue').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)

				tk.Grid.rowconfigure(f2,8,weight=1)
				img9=tk.PhotoImage(file='icons/export.png')
				tbexportbtn=tk.Button(f2,text='export table',image=img9,font=fnt,command=exporttb)
				tbexportbtn.grid(column=0,row=8,padx=10,pady=10,sticky=tk.E)
				tbexportbtn.image=img9
				tk.Label(f2,text='Export the table\nto CSV file.',font=fnt,fg='green',justify=tk.LEFT).grid(column=1,row=8,padx=10,pady=10,sticky=tk.W)

				tk.Grid.rowconfigure(f2,9,weight=1)
				img10=tk.PhotoImage(file='icons/delete.png')
				deltbbtn=tk.Button(f2,text='deltable',image=img10,font=fnt,command=deltb)
				deltbbtn.grid(column=0,row=9,padx=10,pady=10,sticky=tk.E)
				deltbbtn.image=img10
				tk.Label(f2,text='Delete all the contents\nof the table.',font=fnt,justify=tk.LEFT).grid(column=1,row=9,padx=10,pady=10,sticky=tk.W)
				
				tk.Grid.rowconfigure(f2,10,weight=1)

				tk.Message(f2,text='WARNING:\nThis will delete all the contents of the table chosen permanently.',font=fnt,fg='white',bg='orange').grid(column=1,row=10,padx=10,sticky=tk.NW)

				img11=tk.PhotoImage(file='icons/remove.png')
				drptbbtn=tk.Button(f2,text='droptable',image=img11,font=fnt,command=droptb)
				drptbbtn.grid(column=2,row=9,padx=10,pady=10,sticky=tk.E)
				drptbbtn.image=img11
				tk.Label(f2,text='Drop the table.',font=fnt,fg='red').grid(column=3,row=9,padx=10,pady=10,sticky=tk.W)

				tk.Message(f2,text='WARNING:\nThis will drop the table chosen\nand its contents permanently.',font=fnt,fg='white',bg='red').grid(column=3,row=10,padx=10,sticky=tk.NW)

				#Bind Enter to show table function
				dbmgr_main_win.bind('<Return>',lambda event:showtb())
			
			def curadmin_passwd():
				passwd_win=tk.Toplevel()
				passwd_win.resizable(False,False)
				passwd_win.title('Change administrator password')
				icon=tk.PhotoImage(file='img/icon.png')
				passwd_win.iconphoto(False,icon)


				def change_curadmin_passwd():
					if not npass.get()=='' and not npass.get().isspace():
				
						confirm=messagebox.askyesno('','Do you wish to change the administrator password for '+admin_list[emp_uname]+' ?',parent=passwd_win)
						if confirm == True:
							sql="update admin set admin_passwd=%s where admin_uname=%s"
							val=(npass.get(),emp_uname)
							cur.execute(sql,val)
							con.commit()
							messagebox.showinfo('','Administrator password changed for '+admin_list[emp_uname]+'.',parent=passwd_win)
							passwd_win.destroy()
						else:
							messagebox.showinfo('','Administrator password has not been changed.',parent=passwd_win)
					
					else:
						messagebox.showerror('','Please enter a password.',parent=passwd_win)
				
				img14=tk.PhotoImage(file='icons/passwd.png')
				img=tk.Label(passwd_win,image=img14,font=h1fnt)
				img.grid(column=0,row=0,padx=10,pady=10)
				img.image=img14

				tk.Label(passwd_win,text='Changing the administrator\npassword for '+admin_list[emp_uname],font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

				tk.Label(passwd_win,text='New password',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
				npass=tk.Entry(passwd_win,font=fnt,show='*')
				npass.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

				subbtn=tk.Button(passwd_win,text='Make changes',font=fntit,command=change_curadmin_passwd)
				subbtn.grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)	

				passwd_win.bind('<Return>',lambda event:change_curadmin_passwd())
			
			tk.Grid.columnconfigure(root,0,weight=1)

			menubar=tk.Menu(root)

			user_menu=tk.Menu(menubar,tearoff=0)
			menubar.add_cascade(label='User',menu=user_menu,font=menufnt)

			user_menu.add_command(label='Change the administrator password...',command=curadmin_passwd,font=menufnt,underline=0)
			user_menu.add_separator()
			user_menu.add_command(label='Logout',command=logout,font=menufnt,underline=0)
			user_menu.add_command(label='Logout and Exit',command=root.destroy,font=menufnt,underline=11)

			info_menu=tk.Menu(menubar,tearoff=0)
			menubar.add_cascade(label='Info',menu=info_menu,font=menufnt)

			info_menu.add_command(label='About this program...',command=about,font=menufnt,underline=0)
			root.config(menu=menubar)

			#FRAME 1
			tk.Grid.rowconfigure(root,0,weight=1)
			f1=tk.Frame(root,bg='#1b69bc')
			f1.grid(row=0,column=0,sticky=tk.NSEW)

			#frame 1 grid
			tk.Grid.columnconfigure(f1,0,weight=1)

			cur.execute('select admin_uname,admin_name from admin')
			admin_list=dict(cur.fetchall())

			cur.execute('select admin_uname,admin_id from admin')
			uuid_list=dict(cur.fetchall())
			tk.Grid.rowconfigure(f1,0,weight=1)
			tk.Grid.rowconfigure(f1,1,weight=1)
			tk.Grid.rowconfigure(f1,2,weight=1)
			tk.Grid.rowconfigure(f1,3,weight=1)
			
			logo_img=tk.PhotoImage(file='img/logo-150px.png')
			logo=tk.Label(f1,image=logo_img,font=h1fnt,fg='white',bg='#1b69bc')
			logo.grid(column=0,row=0,padx=10,pady=10,sticky=tk.EW)
			logo.image=logo_img
			
			tk.Label(f1,text='Welcome, '+admin_list[emp_uname],font=h1fnt,justify=tk.CENTER,fg='white',bg='#1b69bc').grid(column=0,row=1,padx=10)
			
			tk.Label(f1,text=('User ID: '+uuid_list[emp_uname]),font=h2fnt,fg='black',bg='#00e676').grid(column=0,row=2,padx=10)

			tk.Label(f1,text='Administrators\' Toolbox',font=h2fnt,justify=tk.CENTER,fg='white',bg='#1b69bc').grid(column=0,row=3,padx=10)

			Separator(f1,orient='horizontal').grid(column=0,row=4,sticky=tk.EW,padx=10,pady=10)
			
			#FRAME 2
			tk.Grid.rowconfigure(root,1,weight=1)
			f2=tk.Frame(root)
			f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

			#frame 2 grid
			tk.Grid.columnconfigure(f2,0,weight=1)
			tk.Grid.columnconfigure(f2,1,weight=1)
			tk.Grid.columnconfigure(f2,2,weight=1)
			tk.Grid.columnconfigure(f2,3,weight=1)

			tk.Label(f2,text='You can:',font=fntit).grid(column=1,row=2,sticky=tk.W,padx=10,pady=10)

			tk.Grid.rowconfigure(f2,5,weight=1)
			db_icon=tk.PhotoImage(file='icons/dataset.png')
			db_btn=tk.Button(f2,text='Manage the database',image=db_icon,font=fnt,command=manage_db,width=48,height=48)
			db_btn.grid(column=0,row=5,padx=10,pady=10,sticky=tk.E)
			db_btn.image=db_icon
			tk.Label(f2,text='Manage the databases.',font=fnt,fg='blue').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

			emp_icon=tk.PhotoImage(file='icons/employee.png')
			emp_btn=tk.Button(f2,text='Manage agents',image=emp_icon,font=fnt,command=manage_agents)
			emp_btn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
			emp_btn.image=emp_icon
			tk.Label(f2,text='Manage the agents.',font=fnt,fg='green').grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)

			tk.Grid.rowconfigure(f2,6,weight=1)
			adm_icon=tk.PhotoImage(file='icons/supervisor.png')
			adm_btn=tk.Button(f2,text='Manage administrators',image=adm_icon,font=fnt,command=manage_admin)
			adm_btn.grid(column=0,row=6,padx=10,pady=10,sticky=tk.E)
			adm_btn.image=adm_icon
			tk.Label(f2,text='Manage the administrators.',font=fnt,fg='red').grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

			'''img11=tk.PhotoImage(file='icons/people.png')
			btn4=tk.Button(f2,text='Manage users',image=img11,font=fnt,command=manage_users)
			btn4.grid(column=2,row=6,padx=10,pady=10,sticky=tk.E)
			btn4.image=img11
			tk.Label(f2,text='Manage the users.',font=fnt,fg='purple').grid(column=3,row=6,padx=10,pady=10,sticky=tk.W)'''
			
			tk.Grid.rowconfigure(f2,8,weight=1)

			bkg_icon=tk.PhotoImage(file='icons/booking.png')
			bkg_btn=tk.Button(f2,text='Bookings',image=bkg_icon,font=fnt,command=bookings)
			bkg_btn.grid(column=0,row=8,padx=10,pady=10,sticky=tk.E)
			bkg_btn.image=bkg_icon
			tk.Label(f2,text='Make and manage bookings.',font=fnt).grid(column=1,row=8,padx=10,pady=10,sticky=tk.W)

			pay_icon=tk.PhotoImage(file='icons/make-payment.png')
			pay_btn=tk.Button(f2,text='Payment',image=pay_icon,font=fnt,command=manage_payments)
			pay_btn.grid(column=2,row=8,padx=10,pady=10,sticky=tk.E)
			pay_btn.image=pay_icon
			tk.Label(f2,text='View and manage transactions.',font=fnt).grid(column=3,row=8,padx=10,pady=10,sticky=tk.W)
			
			tk.Grid.rowconfigure(f2,9,weight=1)
			
			root.mainloop()

		def booking_portal():														# Agent booking menu
			#functions
			
			def logout():
				home_page.destroy()
				emp_main()
			
			# Window properties depending on agent or admin
			if emp_type=='Agent':
				home_page=tk.Tk()
				home_page.title('Agent Portal [UNDER DEVELOPMENT]')
			elif emp_type=='Administrator':
				home_page=tk.Toplevel()
				home_page.title('Booking Portal')
			
			icon=tk.PhotoImage(file='img/icon.png')
			home_page.iconphoto(False,icon)

			if emp_type=='Agent':
				try:
					home_page.state('zoomed')
				except:
					w,h=home_page.winfo_screenwidth(),home_page.winfo_screenheight()
					home_page.geometry(str(w)+'x'+str(h))
			
			elif emp_type=='Administrator':
				home_page.geometry('960x540')
			
			if emp_type=='Agent':
				menubar=tk.Menu(home_page)

				user=tk.Menu(menubar,tearoff=0)
				menubar.add_cascade(label='User',menu=user,font=menufnt)
				user.add_command(label='Logout',command=logout,font=menufnt,underline=0)
				user.add_command(label='Logout and exit',command=home_page.destroy,font=menufnt,underline=11)
				home_page.config(menu=menubar)
				
				more=tk.Menu(menubar,tearoff=0)
				menubar.add_cascade(label='Info',menu=more,font=menufnt)
				more.add_command(label='About this program...',command=about,font=menufnt,underline=0)
				home_page.config(menu=menubar)

			tk.Grid.columnconfigure(home_page,0,weight=1)

			#FRAME 1
			tk.Grid.rowconfigure(home_page,0,weight=1)
			f1=tk.Frame(home_page,bg='#1b69bc')
			f1.grid(row=0,column=0,sticky=tk.NSEW)

			tk.Grid.columnconfigure(f1,0,weight=1)

			tk.Grid.rowconfigure(f1,0,weight=1)
			tk.Grid.rowconfigure(f1,1,weight=1)
			tk.Grid.rowconfigure(f1,2,weight=1)
			tk.Grid.rowconfigure(f1,2,weight=1)

			cur.execute('select emp_uname,emp_name from employees')
			emp_list=dict(cur.fetchall())

			cur.execute('select emp_uname,emp_id from employees')
			emp_uuid_list=dict(cur.fetchall())
			
			# Heading title depending on agent or admin
			if emp_type=='Agent':
				tk.Grid.rowconfigure(f1,0,weight=1)
				
				logo_img=tk.PhotoImage(file='img/logo-150px.png')
				logo=tk.Label(f1,image=logo_img,font=h1fnt,fg='white',bg='#1b69bc')
				logo.grid(column=0,row=0,padx=10,pady=10,sticky=tk.EW)
				logo.image=logo_img
				
				txt='Welcome, '+emp_list[emp_uname]
				tk.Label(f1,text=('User ID: '+emp_uuid_list[emp_uname]),font=h2fnt,fg='black',bg='#00e676').grid(column=0,row=2,padx=10)
				tk.Label(f1,text='Agent Portal',fg='white',bg='#1b69bc',font=h2fnt,justify=tk.CENTER).grid(column=0,row=3,padx=10,pady=10)
			elif emp_type=='Administrator':
				txt='Make and manage bookings'
			
			tk.Label(f1,text=txt,fg='white',bg='#1b69bc',font=h1fnt,justify=tk.CENTER).grid(column=0,row=1,padx=10,pady=10)

			Separator(f1,orient='horizontal').grid(column=0,row=4,sticky=tk.EW,padx=10,pady=10)
			#FRAME 2
			tk.Grid.rowconfigure(home_page,1,weight=1)
			f2=tk.Frame(home_page)
			f2.grid(row=1,column=0,sticky=tk.NSEW)

			tk.Grid.columnconfigure(f2,0,weight=1)
			tk.Grid.columnconfigure(f2,1,weight=1)
			tk.Grid.columnconfigure(f2,2,weight=1)
			tk.Grid.columnconfigure(f2,3,weight=1)

			tk.Label(f2,text=('You can:'),font=fntit).grid(column=1,row=2,padx=10,pady=10,sticky=tk.W)

			tk.Grid.rowconfigure(f2,5,weight=1)
			taxi_icon=tk.PhotoImage(file='icons/taxi.png')
			taxi_btn=tk.Button(f2,text='Book taxi',image=taxi_icon,font=fnt,command=taxi_booking)
			taxi_btn.grid(column=0,row=5,padx=10,pady=1,sticky=tk.E)
			taxi_btn.image=taxi_icon
			tk.Label(f2,text='Book a taxi.',font=fnt,bg='yellow').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)
					
			bus_icon=tk.PhotoImage(file='icons/bus.png')
			bus_btn=tk.Button(f2,text='Book Bus',image=bus_icon,command=bus_booking)
			bus_btn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
			bus_btn.image=bus_icon
			tk.Label(f2,text='Book a bus.',font=fnt,fg='blue').grid(column=3,row=5,padx=5,pady=10,sticky=tk.W)

			tk.Label(f2,text=('or:'),font=fntit).grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

			tk.Grid.rowconfigure(f2,7,weight=1)
			
			mag_tbkg_btn=tk.Button(f2,text='Manage taxi bookings',font=fntit,command=manage_taxibkg)
			mag_tbkg_btn.grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)

			if emp_type=='Agent':
				mag_pay_btn=tk.Button(f2,text='Manage payments',font=fntit,command=manage_payments)
				mag_pay_btn.grid(column=2,row=7,padx=10,pady=10,sticky=tk.W)
			
			mag_bbkg_btn=tk.Button(f2,text='Manage bus bookings',font=fntit,command=manage_busbkg)
			mag_bbkg_btn.grid(column=3,row=7,padx=10,pady=10,sticky=tk.W)

			tk.Grid.rowconfigure(f2,10,weight=1)

			if emp_type=='Agent':
				home_page.mainloop()


		# Converts inputs to strings
		emp_uname=emp_uname_inp.get().lower()
		emp_type=emp_type_inp.get()
		emp_passwd=emp_passwd_inp.get()
		
		# Checking for validity in inputs
		if emp_type == 'Agent':	
			cur.execute('select emp_uname,emp_passwd from employees')				# list of agent usernames and passwords
			e=dict(cur.fetchall())

			cur.execute('select emp_uname,emp_name from employees')					# list of agent usernames and names
			f=dict(cur.fetchall())

			if (not emp_uname=='' and not emp_uname.isspace()) and (not emp_passwd=='' and not emp_passwd.isspace()):
				if emp_uname in e.keys():
					if emp_passwd==e[emp_uname]:
						emp_login_win.destroy()
						booking_portal()
					else:
						messagebox.showerror('Error','Invalid password for agent '+f[emp_uname]+'.')
				else:
					messagebox.showerror('Error','Agent '+emp_uname+' does not exist.')
			else:
				messagebox.showerror('Error','Do not leave any fields empty.')
		
		elif emp_type == 'Administrator':
			cur.execute('select admin_uname,admin_passwd from admin')				# list of admin usernames and passwords
			a=dict(cur.fetchall())

			cur.execute('select admin_uname,admin_name from admin')					# list of admin usernames and names
			b=dict(cur.fetchall())

			if (not emp_uname=='' and not emp_uname.isspace()) and (not emp_passwd=='' and not emp_passwd.isspace()):
				if emp_uname in a.keys():
					if emp_passwd==a[emp_uname]:
						emp_login_win.destroy()
						admin_menu()
					else:
						messagebox.showerror('Error','Invalid password for administrator '+b[emp_uname]+'.')
				else:
					messagebox.showerror('Error','Administrator '+emp_uname+' does not exist.')
			else:
				messagebox.showerror('Error','Do not leave any fields empty.')
		
		else:
			messagebox.showerror('Error','Please select login type.')
	
	menubar=tk.Menu(emp_login_win)

	info_menu=tk.Menu(menubar,tearoff=0)
	menubar.add_cascade(label='Info',menu=info_menu,font=menufnt)
	info_menu.add_command(label='About this program...',command=about,font=menufnt,underline=0)
	emp_login_win.config(menu=menubar)
		
	tk.Grid.columnconfigure(emp_login_win,0,weight=1)

	#FRAME 1
	tk.Grid.rowconfigure(emp_login_win,0,weight=1)
	f1=tk.Frame(emp_login_win,bg='#1b69bc')
	f1.grid(row=0,column=0,sticky=tk.NSEW)

	#frame 1 grid
	tk.Grid.columnconfigure(f1,0,weight=1)
	tk.Grid.rowconfigure(f1,0,weight=1)
	tk.Grid.rowconfigure(f1,1,weight=1)
	
	logo_img=tk.PhotoImage(file='img/logo-150px.png')
	logo=tk.Label(f1,image=logo_img,font=h1fnt,fg='white',bg='#1b69bc')
	logo.grid(column=0,row=0,sticky=tk.EW,padx=10,pady=10)
	logo.image=logo_img

	tk.Label(f1,text='Employee login',font=h1fnt,fg='white',bg='#1b69bc').grid(column=0,row=1,padx=10,pady=10,sticky=tk.EW)
	
	ttk.Separator(f1,orient='horizontal').grid(row=2,column=0,sticky=tk.EW,pady=10,columnspan=2)

	#FRAME 2
	tk.Grid.rowconfigure(emp_login_win,1,weight=1)
	f2=tk.Frame(emp_login_win)
	f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

	#frame 2 grid
	tk.Grid.columnconfigure(f2,0,weight=1)
	tk.Grid.columnconfigure(f2,1,weight=1)

	#Login type
	tk.Label(f2,text='Login as',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
	emp_type_inp=tk.StringVar()
	values=('','Agent','Administrator')
	emptype=ttk.OptionMenu(f2,emp_type_inp,*values);emptype.grid(column=1,row=5,sticky=tk.W,padx=10,pady=10)

	#uname
	tk.Label(f2,text='Username',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
	emp_uname_inp=tk.Entry(f2,font=fnt)
	emp_uname_inp.grid(column=1,row=6,sticky=tk.W,padx=10,pady=10)

	#passwd
	tk.Label(f2,text='Password',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
	emp_passwd_inp=tk.Entry(f2,show='*',font=fnt)
	emp_passwd_inp.grid(column=1,row=7,sticky=tk.W,padx=10,pady=10)

	#Login button
	login_icon=tk.PhotoImage(file='icons/login.png')
	loggin_btn=tk.Button(f2,text='Login',image=login_icon,command=on_login)
	loggin_btn.grid(column=1,row=8,padx=10,pady=10,sticky=tk.W)

	emp_login_win.bind('<Return>',lambda event:on_login())

	emp_login_win.mainloop()

init()
