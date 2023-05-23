#import statements
import mysql.connector as ms
import random as rd
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
import os
import datetime as dt

#definitions
id=rd.randint(10000,99999)	#random number for ID
locations=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']	#defines locations
ctype=['','Standard','Express','Premium']	#defines coach type
build='35'	#Program build

#mysql connection
con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
cur=con.cursor()

if con.is_connected()==True:
	dbstatus='Connected to database.'
else:
	dbstatus='Not connected to database.'
#GUI
window=tk.Tk()
#fonts for GUI
fnt=('IBM Plex Mono',12)
fntit=('IBM Plex Mono',12,'italic')
h1fnt=('IBM Plex Sans',24)
#Main Window parameters
window.title('Bus Booking')
window.resizable(False, False)

def payment():
	
	def submit():
		
		sql='insert into bus_bkgs values (%s,%s,%s,%s,%s,%s,%s)'
		val=(id,passno,start_inp,end_inp,date_inp,time_inp,bustype_inp)
		cur.execute(sql,val)
		con.commit()

		submit_message=tk.Toplevel()
		submit_message.resizable(False,False)
		submit_message.title(' ')

		tk.Label(submit_message,text='The booking has been\nsuccessfully made.',font=h1fnt,justify=tk.LEFT).grid(row=0,column=0,sticky=tk.W,padx=10,pady=10)
		
		booking_summary=scrolledtext.ScrolledText(submit_message,font=fnt,width=30,height=8)
		booking_summary.grid(column=0,row=3,sticky=tk.EW,padx=10,pady=10,columnspan=2)
		
		text2='Booking\n-------\n\nBooking ID: '+str(id)+'\nFrom: '+o+'\nTo: '+d+'\nType: '+n.get()+'\nNumber of passengers: '+str(passno)+'\n\nTotal fare: $'+str(total_fare)+'\n\nPayment\n-------\n\n'+'Payment ID: '+payment_id+'\nPaid by: '+m.get()+'\nCardholder name: '+card_name.get()+'\nCard number: XXXX-XXXX-XXXX-'+card_no.get()[-4:]+'\nAmount paid: $'+str(total_fare)+'\n\n------------------'+'\nPAYMENT SUCCESSFUL'+'\n------------------'
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
			window.destroy()
			os.system('python3 home.py')

		btn2=tk.Button(submit_message,text='Return home',font=fnt,command=exit,fg='red',justify=tk.CENTER)
		btn2.grid(row=8,column=0,padx=10,pady=10)

	start_inp=start.get().upper()
	end_inp=end.get().upper()
	date_inp=date.get()
	time_inp=time.get()
	bustype_inp=n.get()
	passno=q.get()

	if (not start_inp=='' and not start_inp.isspace()) and (not end_inp=='' and not end_inp.isspace()) and (not date_inp=='' and not date_inp.isspace()) and (not time_inp=='' and not time_inp.isspace()) and (not bustype_inp=='' and not bustype_inp.isspace()):
		if start_inp in locations and end_inp in locations:
			if not start_inp == end_inp:
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

						x=dt.datetime.now()
						cmonth=x.month
						cyear=x.year

						def pay():
							sql=('insert into payment_details values(%s,%s,%s,%s,%s,%s,%s,%s,%s)')
							val=(payment_id,id,total_fare,paytype_inp,cardno_inp,cardname_inp,cvv_inp,expmonth_inp,expyear_inp)
							cur.execute(sql,val)
							con.commit()
							#messagebox.showinfo('','Payment successfully made.\nPayment reference: '+payment_id,parent=pay_win)
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

					img1=tk.PhotoImage(file='monoico/icon-394.png')
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

					text='Booking ID: '+str(id)+'\nFrom: '+o+'\nTo: '+d+'\nType: '+n.get()+'\n\nRate: $'+str(rate)+' per km\nDistance: '+str(distance)+' km\nNumber of passengers: '+str(passno)+'\n\nTotal fare: $'+str(total_fare)
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
					pay_type.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)

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

					tk.Label(f4,text='Make payment',font=fnt).grid(column=0,row=10,sticky=tk.E,padx=10,pady=10)
					subimg=tk.PhotoImage(file='monoico/icon-394.png')
					btn=tk.Button(f4,font=fnt,text='Pay',image=subimg,command=make_payment);btn.grid(column=1,row=10,padx=10,pady=10,sticky=tk.W)
					btn.image=subimg

					clsimg=tk.PhotoImage(file='monoico/icon-66.png')
					btn3=tk.Button(f4,font=fnt,image=clsimg,command=close)
					btn3.grid(column=0,row=16,padx=10,pady=10,sticky=tk.SW)
					btn3.img=clsimg

					tk.Label(f4,text='Return to previous page',font=fnt).grid(column=0,row=15,sticky=tk.E,padx=10,pady=10)
					retimg=tk.PhotoImage(file='monoico/icon-95.png')
					btn4=tk.Button(f4,font=fnt,image=retimg,command=pay_win.destroy)
					btn4.grid(column=1,row=15,padx=10,pady=10,sticky=tk.SW)
					btn4.img=retimg

			else:
				messagebox.showerror('Error','The origin and destination are the same.',parent=window)
		else:
			messagebox.showerror('Error','Invalid origin or destination.',parent=window)
	else:
		messagebox.showerror('Error','Please do not leave any fields blank.',parent=window)

f1=tk.Frame(window)
f1.grid(row=0,column=0)

tk.Label(f1,text='BUS BOOKING',font=h1fnt,fg='blue').grid(column=1,row=0,padx=10,pady=10)

f2=tk.Frame(window)
f2.grid(row=1,column=0)

#Input fields
tk.Label(f2,text='ID',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
bkgid=tk.Label(f2,text=id,font=fnt)
bkgid.grid(column=1,row=5,sticky=tk.W,padx=10,pady=10)

tk.Label(f2,text='No of passengers',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
q=tk.IntVar()
pass_no=tk.Scale(f2,from_=1,to=100,orient='horizontal',variable=q,font=fnt)
pass_no.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

n=tk.StringVar()
tk.Label(f2,text='Bus Type',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
bustype=ttk.OptionMenu(f2,n,*ctype)
bustype.grid(column=1,row=7,sticky=tk.EW,padx=10,pady=10)

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

tk.Label(f2,text='Submit and\nproceed to payment',font=fnt,justify=tk.RIGHT).grid(column=0,row=15,sticky=tk.E,padx=10,pady=10)
subimg=tk.PhotoImage(file='monoico/icon-334.png')
btn=tk.Button(f2,font=fnt,text='Continue to Payment',image=subimg,command=payment)
btn.grid(column=1,row=15,padx=10,pady=10,sticky=tk.W)
btn.image=subimg


def close():
	window.destroy()
	os.system('python3 home.py')	

clsimg=tk.PhotoImage(file='monoico/icon-269.png')
btn3=tk.Button(f2,font=fnt,image=clsimg,command=close)
btn3.grid(column=0,row=16,padx=10,pady=10,sticky=tk.SW)
btn3.img=clsimg


window.mainloop()
