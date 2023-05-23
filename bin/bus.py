#import statements
import mysql.connector as ms
import random as rd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

#definitions
id=rd.randint(10000,99999)	#random number for ID
locations='ABCDEFGHIJKLMNOPQRSTUVWXYZ'	#defines locations
#ctype=['Standard','Premium','Express']	#defines coach type
build='35'	#Program build

#mysql connection
con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
cur=con.cursor()
#print('Connected to database.')

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
#window.geometry('640x480')
window.resizable(False, False)
def submit():	#Backend - takes inputs, sends to MySQL db
	#Converts inputs to variables
	start_inp=start.get().upper()
	end_inp=end.get().upper()
	date_inp=date.get()
	time_inp=time.get()
	bustype_inp=n.get()

	#confirm=tk.Message(window,text='',width=500,font=fnt)
	#confirm.grid(column=1,row=11)

	l1=[id,start_inp,end_inp,date_inp,time_inp,bustype_inp]

	if (not start_inp=='' and not start_inp.isspace()) and (not end_inp=='' and not end_inp.isspace()) and (not date_inp=='' and not date_inp.isspace()) and (not time_inp=='' and not time_inp.isspace()):
		if start_inp in locations and end_inp in locations:

			#Sends inputs to MySQL db
			sql='insert into bus_bkgs values (%s,%s,%s,%s,%s,%s)'
			val=(id,start_inp,end_inp,date_inp,time_inp,bustype_inp)
			cur.execute(sql,val)
			con.commit()

			#data=[];data.append(l1)
			#df=pd.DataFrame(data,columns=['ID','From','To','Date','Time'])
	
			#Shows confirmation on GUI Window
			#confirm.configure(text=('Booking\n'+str(l1)+'\nentered successfully'))
			messagebox.showinfo('','The booking \n'+str(l1)+'\nwas made successfully.')
		else:
			#confirm.configure(text=('Invalid origin or destination entered.'))
			messagebox.showerror('Error','Invalid origin or destination entered.')
	else:
		messagebox.showerror('Error','Do not leave any fields blank.')
#Window
tk.Label(window,text='BUS BOOKING',font=h1fnt,bg='yellow').grid(column=1,row=0,padx=10,pady=10)
#tk.Label(window,text='This is pre-release software.\nBugs may exist and features may not be complete.\nUse at your own risk.',font=fnt).grid(column=1,row=1)

#Input fields
tk.Label(text='ID',font=fnt).grid(column=0,row=3,sticky=tk.E,padx=10,pady=10)
bkgid=tk.Label(window,text=id,font=fnt)
bkgid.grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

tk.Label(window,text='From',font=fnt).grid(column=0,row=4,sticky=tk.E,padx=10,pady=10)
start=tk.Entry(window,font=fnt)
start.grid(column=1,row=4,sticky=tk.EW,padx=10,pady=10)

tk.Label(window,text='To',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
end=tk.Entry(window,font=fnt)
end.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)

tk.Label(window,text='Date',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
date=tk.Entry(window,font=fnt)
date.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)
tk.Label(window,text='[YYYY-MM-DD]',font=fnt).grid(column=2,row=6,padx=10,pady=10)

tk.Label(window,text='Time',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
time=tk.Entry(window,font=fnt)
time.grid(column=1,row=7,sticky=tk.EW,padx=10,pady=10)
tk.Label(window,text='[HH:MM]',font=fnt).grid(column=2,row=7,padx=10,pady=10)

n=tk.StringVar()
tk.Label(window,text='Bus Type',font=fnt).grid(column=0,row=8,sticky=tk.E,padx=10,pady=10)
bustype=ttk.Combobox(window,textvariable=n,font=fnt,width=19);bustype.grid(column=1,row=8,sticky=tk.EW,padx=10,pady=10)
bustype['values']=('Standart','Express','Premium')
bustype.current(0)
#buttons

subimg=tk.PhotoImage(file='monoico/icon-511.png')
btn=tk.Button(window,font=fnt,text='Submit',image=subimg,command=submit);btn.grid(column=1,row=9,padx=10,pady=10)
btn.image=subimg

#abtimg=tk.PhotoImage(file='ico/dialog-information.png')
#btn2=tk.Button(window,font=fnt,text='About this program...',image=abtimg,command=aboutprg);btn2.grid(column=2,row=11)
#btn2.img=abtimg

def close():
	window.destroy()
	os.system('python3 home.py')

clsimg=tk.PhotoImage(file='monoico/icon-269.png')
btn3=tk.Button(window,font=fnt,image=clsimg,command=close);btn3.grid(column=0,row=11,padx=10,pady=10,sticky=tk.SW)
btn3.img=clsimg


#Version on system
#tk.Label(window,text=('Build '+build+' on\n'+pf.system()+' '+pf.release()),font=fntit).grid(column=0,row=13)
window.mainloop()
