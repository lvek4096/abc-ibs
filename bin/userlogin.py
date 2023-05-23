import tkinter as tk
import random as rd
import mysql.connector as ms
import platform as pf
from tkinter import messagebox
import os

#mysql connection
con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
cur=con.cursor()

#init GUI
logwin=tk.Tk()
logwin.title('Login')
fnt=('IBM Plex Mono',12)
fntit=('IBM Plex Mono',12,'italic')
h1fnt=('IBM Plex Sans',24)
logwin.resizable(False, False)

#login
def login():
	uname_inp=login_uname.get()
	passwd_inp=login_passwd.get()
	cur.execute('select uname,passwd from users')
	op=dict(cur.fetchall())

	if uname_inp not in op.keys():
		messagebox.showerror('Error','Username '+uname_inp+' does not exist.')
	else:
		if not passwd_inp == op[uname_inp]:
			messagebox.showerror('Error','Invalid password entered for '+uname_inp+'.')
		else:
			logwin.destroy()
			os.system('python3 home.py')

def register():
	uuid='U'+str(rd.randint(1000,9999))
	
	def reguser():
		
		#status=tk.Label(regwin,font=fnt);status.grid(column=1,row=7,padx=10,pady=10)
		reg_uname_inp=reg_uname.get().lower()
		reg_passwd_inp=reg_passwd.get()

		cur.execute('select uname from users')
		users=cur.fetchall()

		b=(reg_uname_inp,)
		if not reg_uname_inp.isspace()==True and not reg_uname_inp=='':		#checks if uname is not empty or contains spaces
			if b not in users:
				if not reg_passwd_inp.isspace()==True and not reg_passwd_inp=='':		#checks if uname is not empty or contains spaces
					regsql='insert into users values(%s,%s,%s)'
					regval=(uuid,reg_uname_inp,reg_passwd_inp)

					cur.execute(regsql,regval)
					con.commit()

					messagebox.showinfo('','The new user '+reg_uname_inp+'\nhas been successfully registered.',parent=regwin)
					#status.configure(text=' ')
					#status.configure(text='Registration success.')
				else:
					messagebox.showerror('Error','Please enter a password.',parent=regwin)
			else:
				#status.configure(text=' ')
				messagebox.showerror('Error','Username '+reg_uname_inp+'\nalready exists.',parent=regwin)
		else:
			messagebox.showerror('Error','Please enter a username.',parent=regwin)
	
	regwin=tk.Toplevel()
	regwin.title('Register')
	regwin.resizable(False, False)

	tk.Label(regwin,text='Register',font=h1fnt).grid(column=1,row=0)
	
	tk.Label(regwin,text='ID',font=fnt).grid(column=0,row=3,sticky=tk.E,padx=10,pady=10)
	tk.Label(regwin,text=uuid,font=fnt).grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)
	
	tk.Label(regwin,text='Username',font=fnt).grid(column=0,row=4,sticky=tk.E,padx=10,pady=10)
	reg_uname=tk.Entry(regwin,font=fnt);reg_uname.grid(column=1,row=4,sticky=tk.EW,padx=10,pady=10)

	tk.Label(regwin,text='Password',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
	reg_passwd=tk.Entry(regwin,show='*',font=fnt);reg_passwd.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)

	regsubimg=tk.PhotoImage(file='monoico/icon-67.png')	
	regsubmit=tk.Button(regwin,image=regsubimg,command=reguser);regsubmit.grid(column=1,row=6,padx=10,pady=10)
	regsubmit.image=regsubimg
	
	regcloseimg=tk.PhotoImage(file='monoico/icon-66.png')
	regclose=tk.Button(regwin,text='Close',image=regcloseimg,command=regwin.destroy);regclose.grid(column=0,row=9,sticky=tk.SW,padx=10,pady=10)
	regclose.image=regcloseimg

def changepass():
	logwin.destroy()
	os.system('python3 users.py')

#Window
tk.Label(logwin,text='Login',font=h1fnt).grid(column=1,row=0)

tk.Label(logwin,text='Username',font=fnt).grid(column=0,row=3,sticky=tk.E,padx=10,pady=10)
login_uname=tk.Entry(logwin,font=fnt)
login_uname.grid(column=1,row=3,sticky=tk.EW,padx=10,pady=10)

tk.Label(logwin,text='Password',font=fnt).grid(column=0,row=4,sticky=tk.E,padx=10,pady=10)
login_passwd=tk.Entry(logwin,show='*',font=fnt)
login_passwd.grid(column=1,row=4,sticky=tk.EW,padx=10,pady=10)

img1=tk.PhotoImage(file='monoico/icon-669.png')
logsubmit=tk.Button(logwin,text='Login...',image=img1,command=login)
logsubmit.grid(column=1,row=5,padx=10,pady=10)
#tk.Label(logwin,text='Click to register ->',font=fnt).grid(column=1,row=8)

img2=tk.PhotoImage(file='monoico/icon-67.png')
reg=tk.Button(logwin,text='Register',image=img2,command=register)
reg.grid(column=1,row=8,padx=10,pady=10)

manage=tk.Button(logwin,text='Change password...',font=fntit,command=changepass)
manage.grid(column=1,row=10,padx=10,pady=10)

#tk.Label(logwin,text=('Build '+build+' on\n'+pf.system()+' '+pf.release()),font=fntit).grid(column=0,row=12)
logwin.mainloop()
