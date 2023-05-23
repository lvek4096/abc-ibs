def bus():
	#import statements
	import mysql.connector as ms
	import random as rd
	import tkinter as tk
	from tkinter import ttk
	from tkinter import scrolledtext
	from tkinter.ttk import Separator
	from tkinter import messagebox
	from datetime import datetime,timedelta
	import platform as pf
	import ctypes

	if pf.system()=='Windows':
		ctypes.windll.shcore.SetProcessDpiAwareness(True)

	#definitions
	id=rd.randint(10000,99999)	#random number for ID
	locations=['Blackcastle','Westerwitch','Ironlyn','Wellsummer','Meadowynne','Aldcourt','Butterhaven','Winterglass','Northcrest','Mallowdell']	#defines locations
	ctype=['','Standard','Express','Premium']	#defines coach type


	#mysql connection
	con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
	cur=con.cursor()

	if con.is_connected()==True:
		dbstatus='Connected to database.'
	else:
		dbstatus='Not connected to database.'
	

	#GUI
	window=tk.Toplevel()
	#fonts for GUI
	fnt=('IBM Plex Mono',12)
	fntit=('IBM Plex Mono',12,'italic')
	h1fnt=('IBM Plex Sans',24)
	#Main Window parameters
	window.title('Bus Booking')
	window.resizable(False, False)

	def payment():
		
		def submit():
			#timestamp to mark bookings
			t=datetime.now()
			today=t.strftime('%Y-%m-%d %H:%M:%S')	#Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM
		
			sql='insert into bus_bkgs values (%s,%s,%s,%s,%s,%s,%s,%s)'
			val=(id,today,passno,start_inp,end_inp,date_inp,time_inp,bustype_inp)
			cur.execute(sql,val)
			con.commit()

			submit_message=tk.Toplevel()
			submit_message.resizable(False,False)
			submit_message.title(' ')

			tk.Label(submit_message,text='The booking has been\nsuccessfully made.',font=h1fnt,justify=tk.LEFT).grid(row=0,column=0,sticky=tk.W,padx=10,pady=10)
			
			booking_summary=scrolledtext.ScrolledText(submit_message,font=fnt,width=30,height=8)
			booking_summary.grid(column=0,row=3,sticky=tk.EW,padx=10,pady=10,columnspan=2)
			
			text2='Booking\n-------\n\nBooking ID: '+str(id)+'\nBooking Timestamp: \n'+today+'\n\nFrom: '+o+'\nTo: '+d+'\nType: '+n.get()+'\n\nDate: '+date_inp+'\nTime: '+time_inp+'\n\nNumber of passengers: '+str(passno)+'\n\nTotal fare: $'+str(total_fare)+'\n\nPayment\n-------\n\n'+'Payment ID: '+payment_id+'\nPaid by: '+m.get()+'\nCardholder name: '+card_name.get()+'\nCard number: XXXX-XXXX-XXXX-'+card_no.get()[-4:]+'\nAmount paid: $'+str(total_fare)+'\n\n------------------'+'\nPAYMENT SUCCESSFUL'+'\n------------------'
			booking_summary.insert(tk.INSERT,text2)
			booking_summary.configure(state='disabled')
			
			def clipboard():
				submit_message.clipboard_clear()
				submit_message.clipboard_append(text2)
				btn1.configure(fg='green',text='Copied!')
			
			btn1=tk.Button(submit_message,text='Copy to clipboard',font=fnt,command=clipboard,justify=tk.CENTER)
			btn1.grid(row=5,column=0,padx=10,pady=10)
			
			tk.Label(submit_message,text='The e-receipt will also be sent to\nyour registered electronic mail\naddress.',font=fnt,justify=tk.LEFT).grid(row=6,column=0,padx=10,pady=10,sticky=tk.W)
			
			def exit():
				submit_message.destroy()
				pay_win.destroy()
				window.destroy()

			btn2=tk.Button(submit_message,text='OK',font=fnt,command=exit,justify=tk.CENTER)
			btn2.grid(row=8,column=0,padx=10,pady=10)

		start_inp=start.get().capitalize()
		end_inp=end.get().capitalize()
		date_inp=date.get()
		time_inp=time.get()
		bustype_inp=n.get()
		passno=q.get()

		format='%Y-%m-%d %H:%M'	#datetime format
		current_ts=datetime.now()+timedelta(minutes=45)	#timestamp for reference - 45 min from current time

		ts_str=current_ts.strftime(format)	#Converts datetime to string in specific time format (YYYY-MM-DD HH:MM; MySQL datetime format)

		ts=datetime.strptime(ts_str,format)		#Converts string back to datetime object for comparision


		y=date_inp+' '+time_inp

		
		d_res=True
		try:
			d_res=bool(datetime.strptime(y,format))
		except ValueError:
			d_res=False

		if d_res==True:
			x=datetime.strptime(y,format)

			if x >= ts:
				isNotPast=True
			else:
				isNotPast=False

			if x <= ts+timedelta(days=1096):			# 3-year limit on dates entered
				isNotDistFuture=True
			else:
				isNotDistFuture=False

		if (not start_inp=='' and not start_inp.isspace()) and (not end_inp=='' and not end_inp.isspace()) and (not date_inp=='' and not date_inp.isspace()) and (not time_inp=='' and not time_inp.isspace()) and (not bustype_inp=='' and not bustype_inp.isspace()):
			if start_inp in locations and end_inp in locations:
				if not start_inp == end_inp:
					if d_res==True:
						if isNotPast==True and isNotDistFuture==True:
							pay_win=tk.Toplevel()
							pay_win.title('')
							pay_win.resizable(False,False)

							def make_payment():
								paytype_inp=m.get()
								cardno_inp=card_no.get()
								cardname_inp=card_name.get()
								expyear_inp=exp_year.get()
								expmonth_inp=exp_month.get()
								cvv_inp=cvv_no.get()

								x=datetime.now()
								cmonth=x.month
								cyear=x.year

								def pay():

									#timestamp to mark bookings
									t=datetime.now()
									today=t.strftime('%Y-%m-%d %H:%M:%S')	#Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM
									
									sql=('insert into payment_details values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
									val=(payment_id,today,id,total_fare,paytype_inp,cardno_inp,cardname_inp,cvv_inp,expmonth_inp,expyear_inp)
									cur.execute(sql,val)
									con.commit()
								
									submit()

								
									

								if (not paytype_inp=='' and not paytype_inp.isspace()) and (not cardno_inp=='' and not cardno_inp.isspace()) and (not cardname_inp=='' and not cardname_inp.isspace()) and (not expyear_inp=='' and not expyear_inp.isspace()) and (not expmonth_inp=='' and not expmonth_inp.isspace()) and (not cvv_inp=='' and not cvv_inp.isspace()):
									if len(cardno_inp) == 16:
										if len(expyear_inp) == 4 and int(expyear_inp) >= cyear:
											if int(expyear_inp) == cyear:
												if (len(expmonth_inp) == 2) and (int(expmonth_inp)>= 1 and int(expmonth_inp) <= 12) and (int(expmonth_inp) > cmonth):
													if len(cvv_inp)==3:
														pay()
													else:
														messagebox.showerror('Error','CVV must be a 3-digit number.',parent=pay_win)
												else:
													messagebox.showerror('Error','Expiry month must be a valid number.',parent=pay_win)
											elif int(expyear_inp) > cyear:							
												if (len(expmonth_inp) == 2) and (int(expmonth_inp)>= 1 and int(expmonth_inp) <= 12):
													if len(cvv_inp)==3:
														pay()
													else:
														messagebox.showerror('Error','CVV must be a 3-digit number.',parent=pay_win)
												else:
													messagebox.showerror('Error','Expiry month must be a valid number.',parent=pay_win)
											else:
												pass
										else:
											messagebox.showerror('Error','Expiry year must be a valid number.',parent=pay_win)
									else:
										messagebox.showerror('Error','Credit card must be a 16-digit number.',parent=pay_win)
								else:
									messagebox.showerror('Error','Please enter all required\npayment details.',parent=pay_win)

							f3=tk.Frame(pay_win)
							f3.grid(row=0,column=0)

							img1=tk.PhotoImage(file='icons/make-payment.png')
							img=tk.Label(f3,image=img1,font=h1fnt)
							img.grid(column=0,row=0,padx=10,pady=10)
							img.image=img1

							tk.Label(f3,text='Payment',font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

							f4=tk.Frame(pay_win)
							f4.grid(row=1,column=0)

							payment_summary=scrolledtext.ScrolledText(f4,font=fnt,width=25,height=5)
							payment_summary.grid(column=1,row=3,sticky=tk.EW,padx=10,pady=10)
		
							if n.get()=='Standard':
								rate=5
							elif n.get()=='Express':
								rate=10
							elif n.get()=='Premium':
								rate=15

							o=start.get()
							d=end.get()
							distance=abs((locations.index(d))-(locations.index(o)))*4	#distance between locations - 4 km.
							total_fare=(rate*distance)*passno

							text='Booking ID: '+str(id)+'\nFrom: '+o+'\nTo: '+d+'\nType: '+n.get()+'\n\nDate: '+date_inp+'\nTime: '+time_inp+'\n\nRate: $'+str(rate)+' per km\nDistance: '+str(distance)+' km\nNumber of passengers: '+str(passno)+'\n\nTotal fare: $'+str(total_fare)
							payment_summary.insert(tk.INSERT,text)
							payment_summary.configure(state='disabled')


							tk.Label(f4,text='Payment ID',font=fnt).grid(column=0,row=4,sticky=tk.E,padx=10,pady=10)
							payment_id='P'+str(rd.randint(1000,9999))
							payid=tk.Label(f4,text=payment_id,font=fnt)
							payid.grid(column=1,row=4,sticky=tk.W,padx=10,pady=10)

							m=tk.StringVar()
							tk.Label(f4,text='Pay by',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
							card=('','Debit card','Credit card')
							pay_type=ttk.OptionMenu(f4,m,*card)
							pay_type.grid(column=1,row=5,sticky=tk.W,padx=10,pady=10)

							tk.Label(f4,text='Card number',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
							card_no=tk.Entry(f4,font=fnt)
							card_no.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

							tk.Label(f4,text='Cardholder name',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
							card_name=tk.Entry(f4,font=fnt)
							card_name.grid(column=1,row=7,sticky=tk.EW,padx=10,pady=10)

							tk.Label(f4,text='Expiry Year and Month',font=fnt).grid(column=0,row=8,sticky=tk.E,padx=10,pady=10)
							exp_year=tk.Entry(f4,font=fnt,width=10)
							exp_year.grid(column=1,row=8,sticky=tk.EW,padx=10,pady=10)

							tk.Label(f4,text='/',font=fnt).grid(column=2,row=8,sticky=tk.EW,padx=10,pady=10)
							exp_month=tk.Entry(f4,font=fnt,width=10)
							exp_month.grid(column=3,row=8,sticky=tk.W,padx=10,pady=10)

							tk.Label(f4,text='CVV number',font=fnt).grid(column=0,row=9,sticky=tk.E,padx=10,pady=10)
							cvv_no=tk.Entry(f4,font=fnt)
							cvv_no.grid(column=1,row=9,sticky=tk.EW,padx=10,pady=10)

							#tk.Label(f4,text='Make payment',font=fnt).grid(column=0,row=10,sticky=tk.E,padx=10,pady=10)
							#subimg=tk.PhotoImage(file='monoico/icon-394.png')
							btn=tk.Button(f4,font=fntit,text='Pay',command=make_payment,fg='green');btn.grid(column=1,row=10,padx=10,pady=10,sticky=tk.W)
							#btn.image=subimg

							#tk.Label(f4,text='Return to previous page',font=fnt).grid(column=0,row=15,sticky=tk.E,padx=10,pady=10)
							retimg=tk.PhotoImage(file='icons/return.png')
							btn4=tk.Button(f4,font=fnt,image=retimg,command=pay_win.destroy)
							btn4.grid(column=0,row=15,padx=10,pady=10,sticky=tk.SW)
							btn4.img=retimg

						else:
							messagebox.showerror('Error','Invalid timing entered.',parent=window)
					else:
						messagebox.showerror('Error','Invalid date or time format entered.',parent=window)
				else:
					messagebox.showerror('Error','The origin and destination are the same.',parent=window)
			else:
				messagebox.showerror('Error','Invalid origin or destination.',parent=window)
		else:
			messagebox.showerror('Error','Please do not leave any fields blank.',parent=window)

	f1=tk.Frame(window)
	f1.grid(row=0,column=0)

	tk.Label(f1,text='BUS BOOKING',font=h1fnt,fg='blue').grid(column=1,row=0,padx=10,pady=10)
	#Separator(f1,orient='horizontal').grid(row=1,column=1,sticky=tk.EW)

	f2=tk.Frame(window)
	f2.grid(row=1,column=0)

	#Input fields
	tk.Label(f2,text='ID',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
	bkgid=tk.Label(f2,text=id,font=fnt)
	bkgid.grid(column=1,row=5,sticky=tk.W,padx=10,pady=10)

	tk.Label(f2,text='Number of passengers',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
	q=tk.IntVar()
	pass_no=tk.Scale(f2,from_=1,to=100,orient='horizontal',variable=q,font=fnt)
	pass_no.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

	n=tk.StringVar()
	tk.Label(f2,text='Bus Type',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
	bustype=ttk.OptionMenu(f2,n,*ctype)
	bustype.grid(column=1,row=7,sticky=tk.W,padx=10,pady=10)

	tk.Label(f2,text='From',font=fnt).grid(column=0,row=8,sticky=tk.E,padx=10,pady=10)
	l=tk.StringVar()
	start=ttk.Combobox(f2,textvariable=l,font=fnt,width=19)
	start.grid(column=1,row=8,sticky=tk.EW,padx=10,pady=10)
	start['values']=locations

	tk.Label(f2,text='To',font=fnt).grid(column=0,row=9,sticky=tk.E,padx=10,pady=10)
	m=tk.StringVar()
	end=ttk.Combobox(f2,textvariable=m,font=fnt,width=19)
	end.grid(column=1,row=9,sticky=tk.EW,padx=10,pady=10)
	end['values']=locations

	tk.Label(f2,text='Date',font=fnt).grid(column=0,row=10,sticky=tk.E,padx=10,pady=10)
	date=tk.Entry(f2,font=fnt)
	date.grid(column=1,row=10,sticky=tk.EW,padx=10,pady=10)
	tk.Label(f2,text='[YYYY-MM-DD]',font=fnt).grid(column=2,row=10,padx=10,pady=10)

	tk.Label(f2,text='Time',font=fnt).grid(column=0,row=11,sticky=tk.E,padx=10,pady=10)
	time=tk.Entry(f2,font=fnt)
	time.grid(column=1,row=11,sticky=tk.EW,padx=10,pady=10)
	tk.Label(f2,text='[HH:MM]',font=fnt).grid(column=2,row=11,padx=10,pady=10)

	Separator(f2,orient='horizontal').grid(row=14,column=0,columnspan=3,sticky=tk.EW)

	tk.Label(f2,text='Proceed to checkout',font=fnt,justify=tk.RIGHT).grid(column=0,row=15,sticky=tk.E,padx=10,pady=10)
	subimg=tk.PhotoImage(file='icons/checkout.png')
	btn=tk.Button(f2,font=fnt,text='Continue to Payment',image=subimg,command=payment)
	btn.grid(column=1,row=15,padx=10,pady=10,sticky=tk.W)
	btn.image=subimg

def taxi():
	#import statements
	import mysql.connector as ms
	import random as rd
	from tkinter.ttk import Separator
	import tkinter as tk
	from tkinter import ttk
	from tkinter import scrolledtext
	from tkinter import messagebox
	from datetime import datetime,timedelta
	import ctypes
	import platform as pf

	if pf.system()=='Windows':
		ctypes.windll.shcore.SetProcessDpiAwareness(True)

	#definitions
	id=rd.randint(10000,99999)	#random number for ID
	locations=['Blackcastle','Westerwitch','Ironlyn','Wellsummer','Meadowynne','Aldcourt','Butterhaven','Winterglass','Northcrest','Mallowdell']	#defines locations
	ctype=['','Standard','XL','Luxury']	#defines coach type

	#timestamp to mark bookings
	t=datetime.now()
	today=t.strftime('%Y-%m-%d %H:%M:%S')	#Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM

	#mysql connection
	con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
	cur=con.cursor()
	

	#GUI
	window=tk.Toplevel()
	#fonts for GUI
	fnt=('IBM Plex Mono',12)
	fntit=('IBM Plex Mono',12,'italic')
	h1fnt=('IBM Plex Sans',24)
	#Main Window parameters
	window.title('Taxi Booking')
	window.resizable(False, False)

	def payment():
		
		def submit():

			#timestamp to mark bookings
			t=datetime.now()
			today=t.strftime('%Y-%m-%d %H:%M:%S')	#Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM

			
			sql='insert into taxi_bkgs values (%s,%s,%s,%s,%s,%s,%s)'
			val=(id,today,start_inp,end_inp,date_inp,time_inp,taxitype_inp)
			cur.execute(sql,val)
			con.commit()

			submit_message=tk.Toplevel()
			submit_message.resizable(False,False)
			submit_message.title(' ')

			tk.Label(submit_message,text='The booking has been\nsuccessfully made.',font=h1fnt,justify=tk.LEFT).grid(row=0,column=0,sticky=tk.W,padx=10,pady=10)
			
			booking_summary=scrolledtext.ScrolledText(submit_message,font=fnt,width=30,height=8)
			booking_summary.grid(column=0,row=3,sticky=tk.EW,padx=10,pady=10,columnspan=2)
			
			text2='Booking\n-------\n\nBooking ID: '+str(id)+'\nBooking Timestamp: \n'+today+'\n\nFrom: '+o+'\nTo: '+d+'\nType: '+n.get()+'\n\nDate: '+date_inp+'\nTime: '+time_inp+'\n\nTotal fare: $'+str(total_fare)+'\n\nPayment\n-------\n\n'+'Payment ID: '+payment_id+'\nPaid by: '+m.get()+'\nCardholder name: '+card_name.get()+'\nCard number: XXXX-XXXX-XXXX-'+card_no.get()[-4:]+'\nAmount paid: $'+str(total_fare)+'\n\n------------------'+'\nPAYMENT SUCCESSFUL'+'\n------------------'
			booking_summary.insert(tk.INSERT,text2)
			booking_summary.configure(state='disabled')
			
			def clipboard():
				submit_message.clipboard_clear()
				submit_message.clipboard_append(text2)
				btn1.configure(fg='green',text='Copied!')
			
			btn1=tk.Button(submit_message,text='Copy to clipboard',font=fnt,command=clipboard,justify=tk.CENTER)
			btn1.grid(row=5,column=0,padx=10,pady=10)
			
			tk.Label(submit_message,text='The e-receipt will also be sent to\nyour registered electronic mail\naddress.',font=fnt,justify=tk.LEFT).grid(row=6,column=0,padx=10,pady=10,sticky=tk.W)
			
			def exit():
				submit_message.destroy()
				pay_win.destroy()
				window.destroy()

			btn2=tk.Button(submit_message,text='OK',font=fnt,command=exit,justify=tk.CENTER)
			btn2.grid(row=8,column=0,padx=10,pady=10)

		if 'Today' in p.get():
			bkgdate=a.strftime('%Y-%m-%d')
		elif 'Tomorrow' in p.get():
			bkgdate=b.strftime('%Y-%m-%d')
		else:
			messagebox.showerror('Error','Please select date.',parent=window)


		start_inp=start.get().capitalize()
		end_inp=end.get().capitalize()
		date_inp=bkgdate
		time_inp=time.get()
		taxitype_inp=n.get()

		format='%Y-%m-%d %H:%M'	#datetime format
		current_ts=datetime.now()+timedelta(minutes=10)	#timestamp for reference - 45 min from current time

		ts_str=current_ts.strftime(format)	#Converts datetime to string in specific time format (YYYY-MM-DD HH:MM; MySQL datetime format)

		ts=datetime.strptime(ts_str,format)		#Converts string back to datetime object for comparision


		y=date_inp+' '+time_inp

		
		d_res=True
		try:
			d_res=bool(datetime.strptime(y,format))
		except ValueError:
			d_res=False

		if d_res==True:
			x=datetime.strptime(y,format)

			if x >= ts:
				isNotPast=True
			else:
				isNotPast=False

			if x <= ts+timedelta(days=2):
				isNotDistFuture=True
			else:
				isNotDistFuture=False

		if (not start_inp=='' and not start_inp.isspace()) and (not end_inp=='' and not end_inp.isspace()) and (not date_inp=='' and not date_inp.isspace()) and (not time_inp=='' and not time_inp.isspace()) and (not taxitype_inp=='' and not taxitype_inp.isspace()):
			if start_inp in locations and end_inp in locations:
				if not start_inp == end_inp:
					if d_res==True:
						if isNotPast==True and isNotDistFuture==True:
							pay_win=tk.Toplevel()
							pay_win.title('')
							pay_win.resizable(False,False)

							def make_payment():
								paytype_inp=m.get()
								cardno_inp=card_no.get()
								cardname_inp=card_name.get()
								expyear_inp=exp_year.get()
								expmonth_inp=exp_month.get()
								cvv_inp=cvv_no.get()

								x=datetime.now()
								cmonth=x.month
								cyear=x.year

								def pay():

									#timestamp to mark bookings
									t=datetime.now()
									today=t.strftime('%Y-%m-%d %H:%M:%S')	#Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM

									sql=('insert into payment_details values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
									val=(payment_id,today,id,total_fare,paytype_inp,cardno_inp,cardname_inp,cvv_inp,expmonth_inp,expyear_inp)
									cur.execute(sql,val)
									con.commit()
								
									submit()

								if (not paytype_inp=='' and not paytype_inp.isspace()) and (not cardno_inp=='' and not cardno_inp.isspace()) and (not cardname_inp=='' and not cardname_inp.isspace()) and (not expyear_inp=='' and not expyear_inp.isspace()) and (not expmonth_inp=='' and not expmonth_inp.isspace()) and (not cvv_inp=='' and not cvv_inp.isspace()):
									if len(cardno_inp) == 16:
										if len(expyear_inp) == 4 and int(expyear_inp) >= cyear:
											if int(expyear_inp) == cyear:
												if (len(expmonth_inp) == 2) and (int(expmonth_inp)>= 1 and int(expmonth_inp) <= 12) and (int(expmonth_inp) > cmonth):
													if len(cvv_inp)==3:
														pay()
													else:
														messagebox.showerror('Error','CVV must be a 3-digit number.',parent=pay_win)
												else:
													messagebox.showerror('Error','Expiry month must be a valid number.',parent=pay_win)
											elif int(expyear_inp) > cyear:							
												if (len(expmonth_inp) == 2) and (int(expmonth_inp)>= 1 and int(expmonth_inp) <= 12):
													if len(cvv_inp)==3:
														pay()
													else:
														messagebox.showerror('Error','CVV must be a 3-digit number.',parent=pay_win)
												else:
													messagebox.showerror('Error','Expiry month must be a valid number.',parent=pay_win)
											else:
												pass
										else:
											messagebox.showerror('Error','Expiry year must be a valid number.',parent=pay_win)
									else:
										messagebox.showerror('Error','Credit card must be a 16-digit number.',parent=pay_win)
								else:
									messagebox.showerror('Error','Please enter all required\npayment details.',parent=pay_win)

							f3=tk.Frame(pay_win)
							f3.grid(row=0,column=0)

							img1=tk.PhotoImage(file='icons/make-payment.png')
							img=tk.Label(f3,image=img1,font=h1fnt)
							img.grid(column=0,row=0,padx=10,pady=10)
							img.image=img1

							tk.Label(f3,text='Payment',font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

							f4=tk.Frame(pay_win)
							f4.grid(row=1,column=0)

							payment_summary=scrolledtext.ScrolledText(f4,font=fnt,width=25,height=5)
							payment_summary.grid(column=1,row=3,sticky=tk.EW,padx=10,pady=10)
		
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

							o=start.get()
							d=end.get()
							distance=abs((locations.index(d))-(locations.index(o)))*4	#distance between locations - 4 km.
							if distance > 5:
								total_fare=(base_rate+(rate*(distance-5)))
							else:
								total_fare=(base_rate+0)

							text='Booking ID: '+str(id)+'\nFrom: '+o+'\nTo: '+d+'\nType: '+n.get()+'\n\nDate: '+date_inp+'\nTime: '+time_inp+'\n\nBase rate: $'+str(base_rate)+' for first 5 km\n$'+str(rate)+' per additional km\nDistance: '+str(distance)+' km'+'\n\nTotal fare: $'+str(total_fare)
							payment_summary.insert(tk.INSERT,text)
							payment_summary.configure(state='disabled')


							tk.Label(f4,text='Payment ID',font=fnt).grid(column=0,row=4,sticky=tk.E,padx=10,pady=10)
							payment_id='P'+str(rd.randint(1000,9999))
							payid=tk.Label(f4,text=payment_id,font=fnt)
							payid.grid(column=1,row=4,sticky=tk.W,padx=10,pady=10)

							m=tk.StringVar()
							tk.Label(f4,text='Pay by',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
							card=('','Debit card','Credit card')
							pay_type=ttk.OptionMenu(f4,m,*card)
							pay_type.grid(column=1,row=5,sticky=tk.W,padx=10,pady=10)

							tk.Label(f4,text='Card number',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
							card_no=tk.Entry(f4,font=fnt)
							card_no.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

							tk.Label(f4,text='Cardholder name',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
							card_name=tk.Entry(f4,font=fnt)
							card_name.grid(column=1,row=7,sticky=tk.EW,padx=10,pady=10)

							tk.Label(f4,text='Expiry Year and Month',font=fnt).grid(column=0,row=8,sticky=tk.E,padx=10,pady=10)
							exp_year=tk.Entry(f4,font=fnt,width=10)
							exp_year.grid(column=1,row=8,sticky=tk.EW,padx=10,pady=10)

							tk.Label(f4,text='/',font=fnt).grid(column=2,row=8,sticky=tk.EW,padx=10,pady=10)
							exp_month=tk.Entry(f4,font=fnt,width=10)
							exp_month.grid(column=3,row=8,sticky=tk.W,padx=10,pady=10)

							tk.Label(f4,text='CVV number',font=fnt).grid(column=0,row=9,sticky=tk.E,padx=10,pady=10)
							cvv_no=tk.Entry(f4,font=fnt)
							cvv_no.grid(column=1,row=9,sticky=tk.EW,padx=10,pady=10)

							#tk.Label(f4,text='Make payment',font=fnt).grid(column=0,row=10,sticky=tk.E,padx=10,pady=10)
							#subimg=tk.PhotoImage(file='monoico/icon-394.png')
							btn=tk.Button(f4,font=fntit,text='Pay',command=make_payment,fg='green');btn.grid(column=1,row=10,padx=10,pady=10,sticky=tk.W)
							#btn.image=subimg

							#tk.Label(f4,text='Return to previous page',font=fnt).grid(column=0,row=15,sticky=tk.E,padx=10,pady=10)
							retimg=tk.PhotoImage(file='icons/return.png')
							btn4=tk.Button(f4,font=fnt,image=retimg,command=pay_win.destroy)
							btn4.grid(column=0,row=15,padx=10,pady=10,sticky=tk.SW)
							btn4.img=retimg

						else:
							messagebox.showerror('Error','Invalid timing entered.',parent=window)
					else:
						messagebox.showerror('Error','Invalid time format entered.',parent=window)
				else:
					messagebox.showerror('Error','The origin and destination are the same.',parent=window)
			else:
				messagebox.showerror('Error','Invalid origin or destination.',parent=window)
		else:
			messagebox.showerror('Error','Please do not leave any fields blank.',parent=window)

	f1=tk.Frame(window)
	f1.grid(row=0,column=0)

	tk.Label(f1,text='TAXI BOOKING',font=h1fnt,bg='yellow').grid(column=1,row=0,padx=10,pady=10)

	#Separator(f1,orient='horizontal').grid(row=1,column=1,sticky=tk.EW)

	f2=tk.Frame(window)
	f2.grid(row=1,column=0)

	#Input fields
	tk.Label(f2,text='ID',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
	bkgid=tk.Label(f2,text=id,font=fnt)
	bkgid.grid(column=1,row=5,sticky=tk.W,padx=10,pady=10)

	n=tk.StringVar()
	tk.Label(f2,text='Taxi Type',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
	taxitype=ttk.OptionMenu(f2,n,*ctype)
	taxitype.grid(column=1,row=7,sticky=tk.W,padx=10,pady=10)

	tk.Label(f2,text='From',font=fnt).grid(column=0,row=8,sticky=tk.E,padx=10,pady=10)
	l=tk.StringVar()
	start=ttk.Combobox(f2,textvariable=l,font=fnt,width=19)
	start.grid(column=1,row=8,sticky=tk.EW,padx=10,pady=10)
	start['values']=locations

	tk.Label(f2,text='To',font=fnt).grid(column=0,row=9,sticky=tk.E,padx=10,pady=10)
	m=tk.StringVar()
	end=ttk.Combobox(f2,textvariable=m,font=fnt,width=19)
	end.grid(column=1,row=9,sticky=tk.EW,padx=10,pady=10)
	end['values']=locations

	'''
	tk.Label(f2,text='Date',font=fnt).grid(column=0,row=10,sticky=tk.E,padx=10,pady=10)
	date=tk.Entry(f2,font=fnt)
	date.grid(column=1,row=10,sticky=tk.EW,padx=10,pady=10)
	tk.Label(f2,text='[YYYY-MM-DD]',font=fnt).grid(column=2,row=10,padx=10,pady=10)
	'''

	a=(t+timedelta(minutes=10))
	b=(t+timedelta(days=1,minutes=10))
	datetype=('','Today '+a.strftime('%Y-%m-%d'),'Tomorrow '+b.strftime('%Y-%m-%d'))

	p=tk.StringVar()
	tk.Label(f2,text='Date',font=fnt).grid(column=0,row=10,sticky=tk.E,padx=10,pady=10)
	date=ttk.OptionMenu(f2,p,*datetype)
	date.grid(column=1,row=10,sticky=tk.W,padx=10,pady=10)

	tk.Label(f2,text='Time',font=fnt).grid(column=0,row=11,sticky=tk.E,padx=10,pady=10)
	time=tk.Entry(f2,font=fnt)
	time.grid(column=1,row=11,sticky=tk.EW,padx=10,pady=10)
	tk.Label(f2,text='[HH:MM]',font=fnt).grid(column=2,row=11,padx=10,pady=10)

	Separator(f2,orient='horizontal').grid(row=14,column=0,columnspan=3,sticky=tk.EW)

	tk.Label(f2,text='Proceed to checkout',font=fnt,justify=tk.RIGHT).grid(column=0,row=15,sticky=tk.E,padx=10,pady=10)
	subimg=tk.PhotoImage(file='icons/checkout.png')
	btn=tk.Button(f2,font=fnt,text='Continue to Payment',image=subimg,command=payment)
	btn.grid(column=1,row=15,padx=10,pady=10,sticky=tk.W)
	btn.image=subimg