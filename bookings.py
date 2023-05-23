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

	#Enables DPI scaling on supported Windows versions
	if pf.system()=='Windows':
		try:
			ctypes.windll.shcore.SetProcessDpiAwareness(True)
		except:
			pass

	#definitions

	id='B'+str(rd.randint(10000,99999))	#random number for ID
	locations=['Blackcastle','Westerwitch','Ironlyn','Wellsummer','Meadowynne','Aldcourt','Butterhaven','Winterglass','Northcrest','Mallowdell']	#defines locations
	ctype=['','Standard','Express','Premium']	#defines coach type

	#mysql connection
	con=ms.connect(host='localhost',user='root',password='123456',database='taxi')
	cur=con.cursor()

	#GUI
	window=tk.Toplevel()
	#fonts for GUI
	fnt=('Consolas',12)
	fntit=('Consolas',12,'italic')
	h1fnt=('Segoe UI',24)
	#Main Window parameters
	window.title('Bus Booking')
	window.resizable(False, False)

	def payment():	#Payment window

		#Taking of inputs
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


		y=date_inp+' '+time_inp		#Combines date and time inputs into correct format for comparision purpose

		
		d_res=True	
		try:
			d_res=bool(datetime.strptime(y,format))  #Is date and time inputted in format?
		except ValueError:		
			d_res=False

		if d_res==True:		
			x=datetime.strptime(y,format)	#Converts input to datetime for comparision

			if x >= ts:		#Is y not before minimum 45min from now?
				isNotPast=True
			else:
				isNotPast=False

			if x <= ts+timedelta(days=1096):		# 3-year limit on dates entered
				isNotDistFuture=True
			else:
				isNotDistFuture=False

		#Checking of inputs before proceeding to payment
		if (not start_inp=='' and not start_inp.isspace()) and (not end_inp=='' and not end_inp.isspace()) and (not date_inp=='' and not date_inp.isspace()) and (not time_inp=='' and not time_inp.isspace()) and (not bustype_inp=='' and not bustype_inp.isspace()):
			if start_inp in locations and end_inp in locations:
				if not start_inp == end_inp:
					if d_res==True and len(date_inp)==10 and len(time_inp)==5: 
						if isNotPast==True and isNotDistFuture==True:
							pay_win=tk.Toplevel()
							pay_win.title('Payment Gateway')
							pay_win.resizable(False,False)

							def make_payment():		#Payment function

								#Takes inputs of payment details
								paytype_inp=m.get()
								cardno_inp=card_no.get()
								cardname_inp=card_name.get()
								expyear_inp=exp_year.get()
								expmonth_inp=exp_month.get()
								cvv_inp=cvv_no.get()
								
								#Gets current month and year for expiry date checking
								x=datetime.now()
								cmonth=x.month
								cyear=x.year

								def pay():
									def submit():	#Adds booking to DB
										#timestamp to mark bookings
										t=datetime.now()
										today=t.strftime('%Y-%m-%d %H:%M:%S')	#Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM
									
										sql='insert into bus_bkgs values (%s,%s,%s,%s,%s,%s,%s,%s)'
										val=(id,today,passno,start_inp,end_inp,date_inp,time_inp,bustype_inp)
										cur.execute(sql,val)
										con.commit()

										#Confirmation message
										submit_message=tk.Toplevel()
										submit_message.resizable(False,False)
										submit_message.title('Booking successful')

										tk.Label(submit_message,text='The booking has been\nsuccessfully made.',font=h1fnt,justify=tk.LEFT).grid(row=0,column=0,sticky=tk.W,padx=10,pady=10)

										cardtype=''
										if cardno_inp[0] == '3':
											cardtype='AMEX'
										elif cardno_inp[0] == '4':
											cardtype='VISA'
										elif cardno_inp[0] == '5':
											cardtype='MASTER'
										elif cardno_inp[0] == '6':
											cardtype='DISCOVER'

										booking_summary=scrolledtext.ScrolledText(submit_message,font=fnt,width=30,height=8)
										booking_summary.grid(column=0,row=3,sticky=tk.EW,padx=10,pady=10,columnspan=2)

										text2='Bus Booking\n-----------\n\nBooking ID: '+id+'\nBooking Timestamp: \n'+today+'\n\nFrom: '+o+'\nTo: '+d+'\nType: '+n.get()+'\n\nDate: '+date_inp+'\nTime: '+time_inp+'\n\nNumber of passengers: '+str(passno)+'\n\nTotal fare: $'+str(total_fare)+'\n\nPayment\n-------\n\n'+'Payment ID: '+payment_id+'\nPaid by: '+m.get()+'\nCardholder name: '+card_name.get()+'\nCard number: XXXX-XXXX-XXXX-'+card_no.get()[-4:]+'\nCard type: '+cardtype+'\nAmount paid: $'+str(total_fare)+'\n\n------------------'+'\nPAYMENT SUCCESSFUL'+'\n------------------'
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
										submit_message.bind('<Return>',lambda event:exit())		

									#timestamp to mark bookings
									t=datetime.now()
									today=t.strftime('%Y-%m-%d %H:%M:%S')	#Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM
									
									sql=('insert into payment_details values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
									val=(payment_id,today,id,total_fare,paytype_inp,cardno_inp,cardname_inp,cvv_inp,expmonth_inp,expyear_inp)
									cur.execute(sql,val)
									con.commit()
								
									submit()

								
									
								#Payment details input checking
								if (not paytype_inp=='' and not paytype_inp.isspace()) and (not cardno_inp=='' and not cardno_inp.isspace()) and (not cardname_inp=='' and not cardname_inp.isspace()) and (not expyear_inp=='' and not expyear_inp.isspace()) and (not expmonth_inp=='' and not expmonth_inp.isspace()) and (not cvv_inp=='' and not cvv_inp.isspace()):
									if len(cardno_inp) == 16 and cardno_inp[0] in '3456':
										if len(expyear_inp) == 4 and int(expyear_inp) >= cyear:
											if int(expyear_inp) == cyear:
												if (len(expmonth_inp) == 2) and (int(expmonth_inp)>= 1 and int(expmonth_inp) <= 12) and (int(expmonth_inp) > cmonth):
													if len(cvv_inp)==3:
														pay()
													else:
														messagebox.showerror('Error','CVV must be a 3-digit number.',parent=pay_win)
												else:
													messagebox.showerror('Error','Invalid expiry month.',parent=pay_win)
											elif int(expyear_inp) > cyear:							
												if (len(expmonth_inp) == 2) and (int(expmonth_inp)>= 1 and int(expmonth_inp) <= 12):
													if len(cvv_inp)==3:
														pay()
													else:
														messagebox.showerror('Error','CVV must be a 3-digit number.',parent=pay_win)
												else:
													messagebox.showerror('Error','Invalid expiry month.',parent=pay_win)
											else:
												pass
										else:
											messagebox.showerror('Error','Invalid expiry year.',parent=pay_win)
									else:
										messagebox.showerror('Error','Invalid card number.',parent=pay_win)
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
							payment_summary.grid(column=1,row=2,sticky=tk.EW,padx=10,pady=10)
		
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

							text='Booking ID: '+id+'\nFrom: '+o+'\nTo: '+d+'\nType: '+n.get()+'\n\nDate: '+date_inp+'\nTime: '+time_inp+'\n\nRate: $'+str(rate)+' per km\nDistance: '+str(distance)+' km\nNumber of passengers: '+str(passno)+'\n\nTotal fare: $'+str(total_fare)
							payment_summary.insert(tk.INSERT,text)
							payment_summary.configure(state='disabled')

							tk.Label(f4,text='Payment ID',font=fnt).grid(column=0,row=3,sticky=tk.E,padx=10,pady=10)
							payment_id='P'+str(rd.randint(10000,99999))
							payid=tk.Label(f4,text=payment_id,font=fnt)
							payid.grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

							m=tk.StringVar()
							tk.Label(f4,text='Pay by',font=fnt).grid(column=0,row=4,sticky=tk.E,padx=10,pady=10)
							card=('','Debit card','Credit card')
							pay_type=ttk.OptionMenu(f4,m,*card)
							pay_type.grid(column=1,row=4,sticky=tk.W,padx=10,pady=10)

							tk.Label(f4,text='Accepted cards',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
							
							img2=tk.PhotoImage(file='img/cards.png')
							card_image=tk.Label(f4,image=img2,font=fnt)
							card_image.grid(column=1,row=5,sticky=tk.W,padx=10,pady=10)
							card_image.image=img2

							tk.Label(f4,text='Card number',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
							card_no=tk.Entry(f4,font=fnt)
							card_no.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

							tk.Label(f4,text='Cardholder name',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
							card_name=tk.Entry(f4,font=fnt)
							card_name.grid(column=1,row=7,sticky=tk.EW,padx=10,pady=10)

							tk.Label(f4,text='Expiry Year and Month\n[YYYY-MM]',font=fnt,justify=tk.RIGHT).grid(column=0,row=8,sticky=tk.E,padx=10,pady=10)
							exp_year=tk.Entry(f4,font=fnt,width=10)
							exp_year.grid(column=1,row=8,sticky=tk.EW,padx=10,pady=10)

							tk.Label(f4,text='-',font=fnt).grid(column=2,row=8,sticky=tk.EW,padx=10,pady=10)
							exp_month=tk.Entry(f4,font=fnt,width=10)
							exp_month.grid(column=3,row=8,sticky=tk.W,padx=10,pady=10)

							tk.Label(f4,text='CVV number',font=fnt).grid(column=0,row=9,sticky=tk.E,padx=10,pady=10)
							cvv_no=tk.Entry(f4,font=fnt)
							cvv_no.grid(column=1,row=9,sticky=tk.EW,padx=10,pady=10)

							btn=tk.Button(f4,font=fntit,text='Pay',command=make_payment,fg='green');btn.grid(column=1,row=10,padx=10,pady=10,sticky=tk.W)
							
							retimg=tk.PhotoImage(file='icons/return.png')
							btn4=tk.Button(f4,font=fnt,image=retimg,command=pay_win.destroy)
							btn4.grid(column=0,row=15,padx=10,pady=10,sticky=tk.SW)
							btn4.img=retimg

							pay_win.bind('<Return>',lambda event:make_payment())

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
	#FRAME 1
	f1=tk.Frame(window)
	f1.grid(row=0,column=0)

	tk.Label(f1,text='BUS BOOKING',font=h1fnt,fg='blue').grid(column=1,row=0,padx=10,pady=10)

	#FRAME 2
	f2=tk.Frame(window)
	f2.grid(row=1,column=0)

	#Booking ID
	tk.Label(f2,text='ID',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
	bkgid=tk.Label(f2,text=id,font=fnt)
	bkgid.grid(column=1,row=5,sticky=tk.W,padx=10,pady=10)

	#Input fields
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
	start=ttk.Combobox(f2,textvariable=l,font=fnt,width=19,state='readonly')
	start.grid(column=1,row=8,sticky=tk.EW,padx=10,pady=10)
	start['values']=locations

	tk.Label(f2,text='To',font=fnt).grid(column=0,row=9,sticky=tk.E,padx=10,pady=10)
	m=tk.StringVar()
	end=ttk.Combobox(f2,textvariable=m,font=fnt,width=19,state='readonly')
	end.grid(column=1,row=9,sticky=tk.EW,padx=10,pady=10)
	end['values']=locations

	tk.Label(f2,text='Date',font=fnt).grid(column=0,row=10,sticky=tk.E,padx=10,pady=10)
	date=tk.Entry(f2,font=fnt)
	date.grid(column=1,row=10,sticky=tk.EW,padx=10,pady=10)
	tk.Label(f2,text='[YYYY-MM-DD]',font=fnt).grid(column=2,row=10,padx=10,pady=10)

	tk.Label(f2,text='Time',font=fnt).grid(column=0,row=11,sticky=tk.E,padx=10,pady=10)
	time=tk.Entry(f2,font=fnt)
	time.grid(column=1,row=11,sticky=tk.EW,padx=10,pady=10)
	tk.Label(f2,text='24h [HH:MM]',font=fnt).grid(column=2,row=11,padx=10,pady=10)

	Separator(f2,orient='horizontal').grid(row=14,column=0,columnspan=3,sticky=tk.EW)

	tk.Label(f2,text='Proceed to checkout',font=fnt,justify=tk.RIGHT).grid(column=0,row=15,sticky=tk.E,padx=10,pady=10)
	subimg=tk.PhotoImage(file='icons/checkout.png')
	btn=tk.Button(f2,font=fnt,text='Continue to Payment',image=subimg,command=payment)
	btn.grid(column=1,row=15,padx=10,pady=10,sticky=tk.W)
	btn.image=subimg

	#Binds enter key to submit function
	window.bind('<Return>',lambda event:payment())

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

	#Enables DPI scaling on supported Windows versions
	if pf.system()=='Windows':
		try:
			ctypes.windll.shcore.SetProcessDpiAwareness(True)
		except:
			pass

	#definitions
	id='T'+str(rd.randint(10000,99999))	#random number for ID
	locations=['Blackcastle','Westerwitch','Ironlyn','Wellsummer','Meadowynne','Aldcourt','Butterhaven','Winterglass','Northcrest','Mallowdell']	#defines locations
	ctype=['','Standard','XL','Luxury']	#defines coach type

	#timestamp to mark bookings
	t=datetime.now()

	#mysql connection
	con=ms.connect(host='localhost',user='root',password='123456',database='taxi')
	cur=con.cursor()
	

	#GUI
	window=tk.Toplevel()
	#fonts for GUI
	fnt=('Consolas',12)
	fntit=('Consolas',12,'italic')
	h1fnt=('Segoe UI',24)
	#Main Window parameters
	window.title('Taxi Booking')
	window.resizable(False, False)

	def payment():	#Payment function
		
		bkgdate=''
		if 'Today' in p.get():
			bkgdate=a.strftime('%Y-%m-%d')
		elif 'Tomorrow' in p.get():
			bkgdate=b.strftime('%Y-%m-%d')
		else:
			pass


		start_inp=start.get().capitalize()
		end_inp=end.get().capitalize()
		date_inp=bkgdate
		time_inp=time.get()
		taxitype_inp=n.get()

		format='%Y-%m-%d %H:%M'	#datetime format
		current_ts=datetime.now()+timedelta(minutes=10)	#timestamp for reference - 10 min from current time

		ts_str=current_ts.strftime(format)	#Converts datetime to string in specific time format (YYYY-MM-DD HH:MM; MySQL datetime format)

		ts=datetime.strptime(ts_str,format)		#Converts string back to datetime object for comparision


		y=date_inp+' '+time_inp

		
		d_res=True
		try:
			d_res=bool(datetime.strptime(y,format))		#Is date and time inputted in correct format?
		except ValueError:
			d_res=False

		if d_res==True:
			x=datetime.strptime(y,format)		#Converts inputs to datetime format

			if x >= ts:							#Is input in the past?
				isNotPast=True
			else:
				isNotPast=False

			if x <= ts+timedelta(days=2):		#Is input greater than 2 days?
				isNotDistFuture=True
			else:
				isNotDistFuture=False

		if (not start_inp=='' and not start_inp.isspace()) and (not end_inp=='' and not end_inp.isspace()) and (not date_inp=='' and not date_inp.isspace()) and (not time_inp=='' and not time_inp.isspace()) and (not taxitype_inp=='' and not taxitype_inp.isspace()):
			if start_inp in locations and end_inp in locations:
				if not start_inp == end_inp:
					if d_res==True and len(date_inp)==10 and len(time_inp)==5:
						if isNotPast==True and isNotDistFuture==True:
							pay_win=tk.Toplevel()
							pay_win.title('Payment Gateway')
							pay_win.resizable(False,False)

							def make_payment():		#Payment window
								paytype_inp=m.get()
								cardno_inp=card_no.get()
								cardname_inp=card_name.get()
								expyear_inp=exp_year.get()
								expmonth_inp=exp_month.get()
								cvv_inp=cvv_no.get()

								x=datetime.now()
								cmonth=x.month
								cyear=x.year

								def pay():		#Makes payment

									def submit():		#Adds booking to DB

										#timestamp to mark bookings
										t=datetime.now()
										today=t.strftime('%Y-%m-%d %H:%M:%S')	#Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM

										
										sql='insert into taxi_bkgs values (%s,%s,%s,%s,%s,%s,%s)'
										val=(id,today,start_inp,end_inp,date_inp,time_inp,taxitype_inp)
										cur.execute(sql,val)
										con.commit()

										submit_message=tk.Toplevel()
										submit_message.resizable(False,False)
										submit_message.title('Booking successful')

										tk.Label(submit_message,text='The booking has been\nsuccessfully made.',font=h1fnt,justify=tk.LEFT).grid(row=0,column=0,sticky=tk.W,padx=10,pady=10)
										
										if cardno_inp[0] == '3':
											cardtype='AMEX'
										elif cardno_inp[0] == '4':
											cardtype='VISA'
										elif cardno_inp[0] == '5':
											cardtype='MASTER'
										elif cardno_inp[0] == '6':
											cardtype='DISCOVER'

										booking_summary=scrolledtext.ScrolledText(submit_message,font=fnt,width=30,height=8)
										booking_summary.grid(column=0,row=3,sticky=tk.EW,padx=10,pady=10,columnspan=2)

										text2='Taxi Booking\n------------\n\nBooking ID: '+id+'\nBooking Timestamp: \n'+today+'\n\nFrom: '+o+'\nTo: '+d+'\nType: '+n.get()+'\n\nDate: '+date_inp+'\nTime: '+time_inp+'\n\nTotal fare: $'+str(total_fare)+'\n\nPayment\n-------\n\n'+'Payment ID: '+payment_id+'\nPaid by: '+m.get()+'\nCardholder name: '+card_name.get()+'\nCard number: XXXX-XXXX-XXXX-'+card_no.get()[-4:]+'\nCard type: '+cardtype+'\nAmount paid: $'+str(total_fare)+'\n\n------------------'+'\nPAYMENT SUCCESSFUL'+'\n------------------'
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
										submit_message.bind('<Return>',lambda event:exit())


									#timestamp to mark bookings
									t=datetime.now()
									today=t.strftime('%Y-%m-%d %H:%M:%S')	#Converts ts to string in MySQL datetime format for insertion into db - YYYY-MM-DD HH:MM

									sql=('insert into payment_details values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
									val=(payment_id,today,id,total_fare,paytype_inp,cardno_inp,cardname_inp,cvv_inp,expmonth_inp,expyear_inp)
									cur.execute(sql,val)
									con.commit()
								
									submit()

								if (not paytype_inp=='' and not paytype_inp.isspace()) and (not cardno_inp=='' and not cardno_inp.isspace()) and (not cardname_inp=='' and not cardname_inp.isspace()) and (not expyear_inp=='' and not expyear_inp.isspace()) and (not expmonth_inp=='' and not expmonth_inp.isspace()) and (not cvv_inp=='' and not cvv_inp.isspace()):
									if len(cardno_inp) == 16 and cardno_inp[0] in '3456':
										if len(expyear_inp) == 4 and int(expyear_inp) >= cyear:
											if int(expyear_inp) == cyear:
												if (len(expmonth_inp) == 2) and (int(expmonth_inp)>= 1 and int(expmonth_inp) <= 12) and (int(expmonth_inp) > cmonth):
													if len(cvv_inp)==3:
														pay()
													else:
														messagebox.showerror('Error','CVV must be a 3-digit number.',parent=pay_win)
												else:
													messagebox.showerror('Error','Invalid expiry month.',parent=pay_win)
											elif int(expyear_inp) > cyear:							
												if (len(expmonth_inp) == 2) and (int(expmonth_inp)>= 1 and int(expmonth_inp) <= 12):
													if len(cvv_inp)==3:
														pay()
													else:
														messagebox.showerror('Error','CVV must be a 3-digit number.',parent=pay_win)
												else:
													messagebox.showerror('Error','Invalid expiry month..',parent=pay_win)
											else:
												pass
										else:
											messagebox.showerror('Error','Invalid expiry year.',parent=pay_win)
									else:
										messagebox.showerror('Error','Invalid card number.',parent=pay_win)
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
							payment_summary.grid(column=1,row=2,sticky=tk.EW,padx=10,pady=10)
		
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

							text='Booking ID: '+id+'\nFrom: '+o+'\nTo: '+d+'\nType: '+n.get()+'\n\nDate: '+date_inp+'\nTime: '+time_inp+'\n\nBase rate: $'+str(base_rate)+' for first 5 km\n$'+str(rate)+' per additional km\nDistance: '+str(distance)+' km'+'\n\nTotal fare: $'+str(total_fare)
							payment_summary.insert(tk.INSERT,text)
							payment_summary.configure(state='disabled')


							tk.Label(f4,text='Payment ID',font=fnt).grid(column=0,row=3,sticky=tk.E,padx=10,pady=10)
							payment_id='P'+str(rd.randint(10000,99999))
							payid=tk.Label(f4,text=payment_id,font=fnt)
							payid.grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

							m=tk.StringVar()
							tk.Label(f4,text='Pay by',font=fnt).grid(column=0,row=4,sticky=tk.E,padx=10,pady=10)
							card=('','Debit card','Credit card')
							pay_type=ttk.OptionMenu(f4,m,*card)
							pay_type.grid(column=1,row=4,sticky=tk.W,padx=10,pady=10)
							
							tk.Label(f4,text='Accepted cards',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
							
							img2=tk.PhotoImage(file='img/cards.png')
							card_image=tk.Label(f4,image=img2,font=fnt)
							card_image.grid(column=1,row=5,sticky=tk.W,padx=10,pady=10)
							card_image.image=img2

							tk.Label(f4,text='Card number',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
							card_no=tk.Entry(f4,font=fnt)
							card_no.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

							tk.Label(f4,text='Cardholder name',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
							card_name=tk.Entry(f4,font=fnt)
							card_name.grid(column=1,row=7,sticky=tk.EW,padx=10,pady=10)

							tk.Label(f4,text='Expiry Year and Month\n[YYYY-MM]',font=fnt,justify=tk.RIGHT).grid(column=0,row=8,sticky=tk.E,padx=10,pady=10)
							exp_year=tk.Entry(f4,font=fnt,width=10)
							exp_year.grid(column=1,row=8,sticky=tk.EW,padx=10,pady=10)

							tk.Label(f4,text='-',font=fnt).grid(column=2,row=8,sticky=tk.EW,padx=10,pady=10)
							exp_month=tk.Entry(f4,font=fnt,width=10)
							exp_month.grid(column=3,row=8,sticky=tk.W,padx=10,pady=10)

							tk.Label(f4,text='CVV number',font=fnt).grid(column=0,row=9,sticky=tk.E,padx=10,pady=10)
							cvv_no=tk.Entry(f4,font=fnt)
							cvv_no.grid(column=1,row=9,sticky=tk.EW,padx=10,pady=10)

							btn=tk.Button(f4,font=fntit,text='Pay',command=make_payment,fg='green');btn.grid(column=1,row=10,padx=10,pady=10,sticky=tk.W)

							retimg=tk.PhotoImage(file='icons/return.png')
							btn4=tk.Button(f4,font=fnt,image=retimg,command=pay_win.destroy)
							btn4.grid(column=0,row=15,padx=10,pady=10,sticky=tk.SW)
							btn4.img=retimg

							pay_win.bind('<Return>',lambda event:make_payment())

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
	
	#FRAME 1
	f1=tk.Frame(window)
	f1.grid(row=0,column=0)

	tk.Label(f1,text='TAXI BOOKING',font=h1fnt,bg='yellow').grid(column=1,row=0,padx=10,pady=10)

	
	#FRAME 2
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
	start=ttk.Combobox(f2,textvariable=l,font=fnt,width=19,state='readonly')
	start.grid(column=1,row=8,sticky=tk.EW,padx=10,pady=10)
	start['values']=locations

	tk.Label(f2,text='To',font=fnt).grid(column=0,row=9,sticky=tk.E,padx=10,pady=10)
	m=tk.StringVar()
	end=ttk.Combobox(f2,textvariable=m,font=fnt,width=19,state='readonly')
	end.grid(column=1,row=9,sticky=tk.EW,padx=10,pady=10)
	end['values']=locations

	a=(t+timedelta(minutes=10))		#today
	b=(t+timedelta(days=1,minutes=10))		#tomorrow
	datetype=('','Today '+a.strftime('%Y-%m-%d'),'Tomorrow '+b.strftime('%Y-%m-%d'))

	p=tk.StringVar()
	tk.Label(f2,text='Date',font=fnt).grid(column=0,row=10,sticky=tk.E,padx=10,pady=10)
	date=ttk.OptionMenu(f2,p,*datetype)
	date.grid(column=1,row=10,sticky=tk.W,padx=10,pady=10)

	tk.Label(f2,text='Time',font=fnt).grid(column=0,row=11,sticky=tk.E,padx=10,pady=10)
	time=tk.Entry(f2,font=fnt)
	time.grid(column=1,row=11,sticky=tk.EW,padx=10,pady=10)
	tk.Label(f2,text='24h [HH:MM]',font=fnt).grid(column=2,row=11,padx=10,pady=10)

	Separator(f2,orient='horizontal').grid(row=14,column=0,columnspan=3,sticky=tk.EW)

	tk.Label(f2,text='Proceed to checkout',font=fnt,justify=tk.RIGHT).grid(column=0,row=15,sticky=tk.E,padx=10,pady=10)
	subimg=tk.PhotoImage(file='icons/checkout.png')
	btn=tk.Button(f2,font=fnt,text='Continue to Payment',image=subimg,command=payment)
	btn.grid(column=1,row=15,padx=10,pady=10,sticky=tk.W)
	btn.image=subimg

	window.bind('<Return>',lambda event:payment())