import tkinter as tk
import random as rd
import mysql.connector as ms
import platform as pf
from tkinter import messagebox
import os

import home as hm

#mysql connection
con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
cur=con.cursor()

#init GUI
logwin=tk.Tk()
logwin.title('')
fnt=('IBM Plex Mono',12)
fntit=('IBM Plex Mono',12,'italic')
h1fnt=('IBM Plex Sans',24)
w,h=logwin.winfo_screenwidth(),logwin.winfo_screenheight()
logwin.geometry(str(w)+'x'+str(h))

#login
def login():
	uname_inp=login_uname.get()
	passwd_inp=login_passwd.get()
	cur.execute('select uname,passwd from users')
	op=dict(cur.fetchall())

	cur.execute('select uname,fname from users')
	fnamelist=dict(cur.fetchall())

	if uname_inp not in op.keys():
		messagebox.showerror('Error','Username \''+uname_inp+'\' does not exist.')
	else:
		if not passwd_inp == op[uname_inp]:
			messagebox.showerror('Error','Invalid password entered for '+fnamelist[uname_inp]+'.')
		else:
			logwin.destroy()
			hm.main()

def register():
	uuid='U'+str(rd.randint(1000,9999))
	
	def reguser():
		
		#status=tk.Label(regwin,font=fnt);status.grid(column=1,row=7,padx=10,pady=10)
		
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

						messagebox.showinfo('','The new user '+reg_fname_inp+'\nhas been successfully registered.',parent=regwin)

					else:
						messagebox.showerror('Error','Invalid phone number entered.',parent=regwin)
				else:
					messagebox.showerror('Error','Invalid electronic mail ID entered.',parent=regwin)		
			else:

				messagebox.showerror('Error','Username '+reg_uname_inp+'\nalready exists.',parent=regwin)
		else:
			messagebox.showerror('Error','Please do not leave any fields blank.',parent=regwin)
	
	regwin=tk.Toplevel()
	regwin.title('Register')
	regwin.resizable(False, False)

	tk.Label(regwin,text='Register',font=h1fnt).grid(column=0,row=0,padx=10,pady=10,columnspan=2,sticky=tk.EW)
	
	tk.Label(regwin,text='ID',font=fnt).grid(column=0,row=3,sticky=tk.E,padx=10,pady=10)
	tk.Label(regwin,text=uuid,font=fnt).grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)
	
	tk.Label(regwin,text='1. Personal info',font=fntit).grid(column=0,row=5,sticky=tk.W,padx=10,pady=10)

	tk.Label(regwin,text='Name',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
	reg_fname=tk.Entry(regwin,font=fnt)
	reg_fname.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

	tk.Label(regwin,text='Electronic mail ID',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
	reg_email=tk.Entry(regwin,font=fnt)
	reg_email.grid(column=1,row=7,sticky=tk.EW,padx=10,pady=10)

	tk.Label(regwin,text='Phone number',font=fnt).grid(column=0,row=8,sticky=tk.E,padx=10,pady=10)
	reg_num=tk.Entry(regwin,font=fnt)
	reg_num.grid(column=1,row=8,sticky=tk.EW,padx=10,pady=10)

	tk.Label(regwin,text='2. Login info',font=fntit).grid(column=0,row=10,sticky=tk.W,padx=10,pady=10)

	tk.Label(regwin,text='Username',font=fnt).grid(column=0,row=11,sticky=tk.E,padx=10,pady=10)
	reg_uname=tk.Entry(regwin,font=fnt)
	reg_uname.grid(column=1,row=11,sticky=tk.EW,padx=10,pady=10)

	tk.Label(regwin,text='Password',font=fnt).grid(column=0,row=12,sticky=tk.E,padx=10,pady=10)
	reg_passwd=tk.Entry(regwin,show='*',font=fnt)
	reg_passwd.grid(column=1,row=12,sticky=tk.EW,padx=10,pady=10)

	regsubimg=tk.PhotoImage(file='monoico/icon-67.png')	
	regsubmit=tk.Button(regwin,image=regsubimg,command=reguser)
	regsubmit.grid(column=1,row=14,padx=10,pady=10,sticky=tk.W)
	regsubmit.image=regsubimg
	
	regcloseimg=tk.PhotoImage(file='monoico/icon-66.png')
	regclose=tk.Button(regwin,text='Close',image=regcloseimg,command=regwin.destroy)
	regclose.grid(column=0,row=15,sticky=tk.SW,padx=10,pady=10)
	regclose.image=regcloseimg

def changepass():
	logwin.destroy()
	os.system('python3 manageusr.py')

#Window
tk.Grid.columnconfigure(logwin,0,weight=1)

#FRAME 1
tk.Grid.rowconfigure(logwin,0,weight=1)
f1=tk.Frame(logwin)
f1.grid(row=0,column=0,sticky=tk.NSEW)

#frame 1 grid
tk.Grid.columnconfigure(f1,0,weight=1)

tk.Grid.rowconfigure(f1,0,weight=1)
tk.Label(f1,text='Login',font=h1fnt).grid(column=0,row=0)

#FRAME 2
tk.Grid.rowconfigure(logwin,1,weight=1)
f2=tk.Frame(logwin)
f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

#frame 2 grid
tk.Grid.columnconfigure(f2,0,weight=1)
tk.Grid.columnconfigure(f2,1,weight=1)

#tk.Grid.rowconfigure(f2,3,weight=1)
tk.Label(f2,text='Username',font=fnt).grid(column=0,row=3,padx=10,pady=10,sticky=tk.E)
login_uname=tk.Entry(f2,font=fnt)
login_uname.grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

#tk.Grid.rowconfigure(f2,4,weight=1)
tk.Label(f2,text='Password',font=fnt).grid(column=0,row=4,padx=10,pady=10,sticky=tk.E)
login_passwd=tk.Entry(f2,show='*',font=fnt)
login_passwd.grid(column=1,row=4,sticky=tk.W,padx=10,pady=10)

#tk.Grid.rowconfigure(f2,10,weight=2)
img1=tk.PhotoImage(file='monoico/icon-669.png')
logsubmit=tk.Button(f2,text='Login...',image=img1,command=login)
logsubmit.grid(column=1,row=10,padx=10,pady=10,sticky=tk.W)

tk.Grid.rowconfigure(f2,12,weight=2)
img2=tk.PhotoImage(file='monoico/icon-67.png')
reg=tk.Button(f2,text='Register',image=img2,command=register)
reg.grid(column=1,row=12,padx=10,pady=10,sticky=tk.W)

#tk.Grid.rowconfigure(f2,11,weight=2)
manage=tk.Button(f2,text='Change password...',font=fntit,command=changepass)
manage.grid(column=1,row=11,padx=10,pady=10,columnspan=2,sticky=tk.W)

logwin.mainloop()
