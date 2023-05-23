import tkinter as tk
import random as rd
import mysql.connector as ms
import platform as pf
from tkinter import messagebox
import os

build='30'

uuid='U'+str(rd.randint(1000,9999))

#MySQL
con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
cur=con.cursor()

#GUI
logwin=tk.Tk()
logwin.title('Register')
fnt=('IBM Plex Mono',12)
fntit=('IBM Plex Mono',12,'italic')
h1fnt=('IBM Plex Sans',24)


def login():
	uname_inp=uname.get()
	passwd_inp=passwd.get()
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


def regpop():
	def register():
		reg_uname_inp=reg_uname.get().lower()
		reg_passwd_inp=reg_passwd.get()

		l2=[uuid,reg_uname_inp,reg_passwd_inp]

		regsql='insert into users values(%s,%s,%s)'
		regval=(uuid,reg_uname_inp,reg_passwd_inp)

		cur.execute(regsql,regval)
		con.commit()
		
		tk.Label(regwin,text='Registration success.',font=fnt).grid(column=1,row=7)
		tk.Label(regwin,text=str(l2),font=fnt).grid(column=1,row=8)

	regwin=tk.Toplevel()
	regwin.title('Register')
	tk.Label(regwin,text='Register',font=h1fnt).grid(column=1,row=0)
	
	tk.Label(regwin,text='ID',font=fnt).grid(column=0,row=3)
	tk.Label(regwin,text=uuid,font=fnt).grid(column=1,row=3)
	
	tk.Label(regwin,text='Username',font=fnt).grid(column=0,row=4)
	reg_uname=tk.Entry(regwin,font=fnt);reg_uname.grid(column=1,row=4)

	tk.Label(regwin,text='Password',font=fnt).grid(column=0,row=5)
	reg_passwd=tk.Entry(regwin,show='*',font=fnt);reg_passwd.grid(column=1,row=5)

	regsubimg=tk.PhotoImage(file='ico/emblem-default.png')	
	regsub=tk.Button(regwin,image=regsubimg,command=register);regsub.grid(column=1,row=6)
	regsub.image=regsubimg
	
	regcloseimg=tk.PhotoImage(file='ico/emblem-unreadable.png')
	regclose=tk.Button(regwin,text='Close',image=regcloseimg,command=regwin.destroy);regclose.grid(column=2,row=9)
	regclose.image=regcloseimg

	tk.Label(regwin,text=('Build '+build+' on\n'+pf.system()+' '+pf.release()),font=fntit).grid(column=0,row=12)
	
	


#Window
tk.Label(logwin,text='Login',font=h1fnt).grid(column=1,row=0)

tk.Label(logwin,text='Username',font=fnt).grid(column=0,row=3)
uname=tk.Entry(logwin,font=fnt);uname.grid(column=1,row=3)

tk.Label(logwin,text='Password',font=fnt).grid(column=0,row=4)
passwd=tk.Entry(logwin,show='*',font=fnt);passwd.grid(column=1,row=4)

subimg=tk.PhotoImage(file='ico/emblem-personal.png')
submit=tk.Button(logwin,text='Check',image=subimg,command=login);submit.grid(column=1,row=5)
submit.image=subimg
#tk.Label(logwin,text='Click to register ->',font=fnt).grid(column=1,row=8)

regimg=tk.PhotoImage(file='ico/emblem-list-add.png')
regbtn=tk.Button(logwin,text='Register',image=regimg,command=regpop);regbtn.grid(column=2,row=8)
regbtnimage=regimg

tk.Label(logwin,text=('Build '+build+' on\n'+pf.system()+' '+pf.release()),font=fntit).grid(column=0,row=12)
logwin.mainloop()
