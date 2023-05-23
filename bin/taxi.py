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
ttype=['','Standart','XL','Luxury']	#defines coach type
build='35'	#Program build

#mysql connection
con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
cur=con.cursor()

if con.is_connected()==True:
	dbstatus='Connected to database.'
else:
	dbstatus='Not connected to database.'

#main window
window=tk.Tk()

#fonts for GUI
fnt=('IBM Plex Mono',12)
fntit=('IBM Plex Mono',12,'italic')
h1fnt=('IBM Plex Sans',24)

window.title('Taxi Booking')
window.resizable(False, False)

def payment():	#Payment function
	def submit():	
		#Converts inputs to variables

		l1=[id,start_inp,end_inp,taxitype_inp]


		#Sends inputs to MySQL db
		sql='insert into taxi_bkgs values (%s,%s,%s,%s)'
		val=(id,start_inp,end_inp,taxitype_inp)
		cur.execute(sql,val)
		con.commit()

		messagebox.showinfo('','The booking \n'+str(l1)+'\nwas made successfully.',parent=pay_win)

	
	start_inp=start.get().upper()
	end_inp=end.get().upper()
	taxitype_inp=n.get()

	if (not start_inp=='' and not start_inp.isspace()) and (not end_inp=='' and not end_inp.isspace()) and (not taxitype_inp=='' and not taxitype_inp.isspace()):
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

					if (not paytype_inp=='' and not paytype_inp.isspace()) and (not cardno_inp=='' and not cardno_inp.isspace()) and (not cardname_inp=='' and not cardname_inp.isspace()) and (not expyear_inp=='' and not expyear_inp.isspace()) and (not expmonth_inp=='' and not expmonth_inp.isspace()) and (not cvv_inp=='' and not cvv_inp.isspace()):
						if len(cardno_inp) == 16:
							if len(expyear_inp) == 4 and int(expyear_inp) >= cyear:
								if len(expmonth_inp) == 2 and (int(expmonth_inp)>= 1 and int(expmonth_inp) <= 12) and int(expmonth_inp) > cmonth:
									if len(cvv_inp)==3:
										sql=('insert into payment_details values(%s,%s,%s,%s,%s,%s,%s,%s,%s)')
										val=(payment_id,id,total_fare,paytype_inp,cardno_inp,cardname_inp,cvv_inp,expmonth_inp,expyear_inp)
										cur.execute(sql,val)
										con.commit()
										messagebox.showinfo('','Payment successfully made.\nPayment reference: '+payment_id,parent=pay_win)
										submit()
									else:
										messagebox.showerror('Error','CVV must be a 3-digit number.',parent=pay_win)
								else:
									messagebox.showerror('Error','Expiry month must be a valid number.',parent=pay_win)
							else:
								messagebox.showerror('Error','Expiry year must be a valid number.',parent=pay_win)
						else:
							messagebox.showerror('Error','Credit card must be a 16-digit number.',parent=pay_win)
					else:
						messagebox.showerror('Error','Please enter all required\npayment details.',parent=pay_win)

				img1=tk.PhotoImage(file='monoico/icon-394.png')
				img=tk.Label(pay_win,image=img1,font=h1fnt)
				img.grid(column=0,row=0,padx=10,pady=10)
				img.image=img1

				tk.Label(pay_win,text='Payment',font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

				payment_summary=scrolledtext.ScrolledText(pay_win,font=fnt,width=30,height=6)
				payment_summary.grid(column=1,row=3,sticky=tk.EW,padx=10,pady=10)

				if n.get()=='Standart':
					base_rate=15
				elif n.get()=='XL':
					base_rate=25
				elif n.get()=='Luxury':
					base_rate=40
				
				if n.get()=='Standart':
					rate=3
				elif n.get()=='XL':
					rate=5
				elif n.get()=='Luxury':
					rate=10

				o=start.get()
				d=end.get()
				distance=abs((locations.index(d))-(locations.index(o)))*4		#distance between locations - 4 km.
				total_fare=(base_rate+(rate*(distance-5)))

				text='Type: '+n.get()+'\nFrom: '+o+'\nTo: '+d+'\nBase Rate for first 5 km: $'+str(base_rate)+'\nRate: $'+str(rate)+' per km\nDistance: '+str(distance)+' km\nTotal fare: $'+str(total_fare)
				payment_summary.insert(tk.INSERT,text)
				payment_summary.configure(state='disabled')


				tk.Label(pay_win,text='Payment ID',font=fnt).grid(column=0,row=4,sticky=tk.E,padx=10,pady=10)
				payment_id='P'+str(rd.randint(1000,9999))
				payid=tk.Label(pay_win,text=payment_id,font=fnt)
				payid.grid(column=1,row=4,sticky=tk.W,padx=10,pady=10)

				m=tk.StringVar()
				tk.Label(pay_win,text='Pay by',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
				card=('','Debit card','Credit card')
				pay_type=ttk.OptionMenu(pay_win,m,*card)
				pay_type.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)

				tk.Label(pay_win,text='Card number',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
				card_no=tk.Entry(pay_win,font=fnt)
				card_no.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

				tk.Label(pay_win,text='Cardholder name',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
				card_name=tk.Entry(pay_win,font=fnt)
				card_name.grid(column=1,row=7,sticky=tk.EW,padx=10,pady=10)

				tk.Label(pay_win,text='Expiry Year and Month',font=fnt).grid(column=0,row=8,sticky=tk.E,padx=10,pady=10)
				exp_year=tk.Entry(pay_win,font=fnt,width=10)
				exp_year.grid(column=1,row=8,sticky=tk.EW,padx=10,pady=10)

				tk.Label(pay_win,text='/',font=fnt).grid(column=2,row=8,sticky=tk.EW,padx=10,pady=10)
				exp_month=tk.Entry(pay_win,font=fnt,width=10)
				exp_month.grid(column=3,row=8,sticky=tk.W,padx=10,pady=10)

				tk.Label(pay_win,text='CVV number',font=fnt).grid(column=0,row=9,sticky=tk.E,padx=10,pady=10)
				cvv_no=tk.Entry(pay_win,font=fnt)
				cvv_no.grid(column=1,row=9,sticky=tk.EW,padx=10,pady=10)

				tk.Label(pay_win,text='Make payment',font=fnt).grid(column=0,row=10,sticky=tk.E,padx=10,pady=10)
				subimg=tk.PhotoImage(file='monoico/icon-134.png')
				btn=tk.Button(pay_win,font=fnt,text='Pay',image=subimg,command=make_payment);btn.grid(column=1,row=10,padx=10,pady=10,sticky=tk.W)
				btn.image=subimg

				clsimg=tk.PhotoImage(file='monoico/icon-66.png')
				btn3=tk.Button(pay_win,font=fnt,image=clsimg,command=close)
				btn3.grid(column=0,row=16,padx=10,pady=10,sticky=tk.SW)
				btn3.img=clsimg

				tk.Label(pay_win,text='Return to previous page',font=fnt).grid(column=0,row=15,sticky=tk.E,padx=10,pady=10)
				retimg=tk.PhotoImage(file='monoico/icon-95.png')
				btn4=tk.Button(pay_win,font=fnt,image=retimg,command=pay_win.destroy)
				btn4.grid(column=1,row=15,padx=10,pady=10,sticky=tk.SW)
				btn4.img=retimg
			else:
				messagebox.showerror('Error','The origin and destination are the same.',parent=window)
		else:
			messagebox.showerror('Error','Invalid origin or destination.',parent=window)
	else:
		messagebox.showerror('Error','Please do not leave any fields blank.',parent=window)

tk.Label(window,text='TAXI BOOKING',font=h1fnt,fg='blue').grid(column=1,row=0,padx=10,pady=10)

#Input fields
tk.Label(window,text='ID',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
bkgid=tk.Label(window,text=id,font=fnt)
bkgid.grid(column=1,row=5,sticky=tk.W,padx=10,pady=10)

n=tk.StringVar()
tk.Label(window,text='Taxi Type',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
taxitype=ttk.OptionMenu(window,n,*ttype)
taxitype.grid(column=1,row=7,sticky=tk.EW,padx=10,pady=10)

tk.Label(window,text='From',font=fnt).grid(column=0,row=8,sticky=tk.E,padx=10,pady=10)
l=tk.StringVar()
start=ttk.Combobox(window,textvariable=l,font=fnt,width=19)
start.grid(column=1,row=8,sticky=tk.EW,padx=10,pady=10)
start['values']=locations

tk.Label(window,text='To',font=fnt).grid(column=0,row=9,sticky=tk.E,padx=10,pady=10)
m=tk.StringVar()
end=ttk.Combobox(window,textvariable=m,font=fnt,width=19)
end.grid(column=1,row=9,sticky=tk.EW,padx=10,pady=10)
end['values']=locations

tk.Label(window,text='Submit and\nproceed to payment',font=fnt,justify=tk.RIGHT).grid(column=0,row=15,sticky=tk.E,padx=10,pady=10)
subimg=tk.PhotoImage(file='monoico/icon-334.png')
btn=tk.Button(window,font=fnt,text='Continue to Payment',image=subimg,command=payment)
btn.grid(column=1,row=15,padx=10,pady=10,sticky=tk.W)
btn.image=subimg


def close():
	window.destroy()
	os.system('python3 home.py')

clsimg=tk.PhotoImage(file='monoico/icon-269.png')
btn3=tk.Button(window,font=fnt,image=clsimg,command=close)
btn3.grid(column=0,row=16,padx=10,pady=10,sticky=tk.SW)
btn3.img=clsimg


window.mainloop()
