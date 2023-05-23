import mysql.connector as ms
import tkinter as tk
import os
from tkinter import ttk
from tkinter import messagebox

#mysql connection
con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
cur=con.cursor()
cur.execute('create table if not exists employees(emp_id varchar(10) primary key,emp_name varchar(50),emp_uname varchar(50),emp_passwd varchar(50))')
cur.execute('create table if not exists admin(admin_id varchar(10) primary key,admin_name varchar(50),admin_uname varchar(50),admin_passwd varchar(50))')
con.commit()
fnt=('IBM Plex Mono',12)
fntit=('IBM Plex Mono',12,'italic')
h1fnt=('IBM Plex Sans',24)

emplogwin=tk.Tk()
emplogwin.title('Login for employees')
emplogwin.resizable(False,False)

def login():
	emp_uname_inp=emp_uname.get().lower()
	emptype_inp=emptype.get()
	emp_passwd_inp=emp_passwd.get()

	if emptype_inp == 'Driver':
		cur.execute('select emp_uname,emp_passwd from employees')
		e=dict(cur.fetchall())
		if emp_uname_inp in e.keys():
			if emp_passwd_inp==e[emp_uname_inp]:
				emplogwin.destroy()
				os.system('xeyes -render &')
			else:
				messagebox.showerror('Error','Invalid password for\ndriver '+emp_uname_inp+'.')
		else:
			messagebox.showerror('Error','Driver '+emp_uname_inp+' does not exist.')
	elif emptype_inp == 'Administrator':
		cur.execute('select admin_uname,admin_passwd from admin')
		a=dict(cur.fetchall())
		if emp_uname_inp in a.keys():
			if emp_passwd_inp==a[emp_uname_inp]:
				messagebox.showinfo('','Welcome '+emp_uname_inp+'.')
			else:
				messagebox.showerror('Error','Invalid password for\nadministrator '+emp_uname_inp+'.')
		else:
			messagebox.showerror('Error','Administrator '+emp_uname_inp+' does not exist.')

tk.Label(emplogwin,text='Login for employees',font=h1fnt).grid(column=1,row=0)

tk.Label(emplogwin,text='Login as',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
n=tk.StringVar()
#tk.Label(emplogwin,text='Bus Type',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
emptype=ttk.Combobox(emplogwin,textvariable=n,font=fnt,width=19);emptype.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
emptype['values']=('Driver','Administrator')
emptype.current(0)

tk.Label(emplogwin,text='Username',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
emp_uname=tk.Entry(emplogwin,font=fnt)
emp_uname.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

tk.Label(emplogwin,text='Password',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
emp_passwd=tk.Entry(emplogwin,show='*',font=fnt)
emp_passwd.grid(column=1,row=7,sticky=tk.EW,padx=10,pady=10)

img1=tk.PhotoImage(file='monoico/icon-669.png')
logsubmit=tk.Button(emplogwin,text='Login',image=img1,command=login)
logsubmit.grid(column=1,row=8,padx=10,pady=10)
#tk.Label(emplogwin,text='Click to register ->',font=fnt).grid(column=1,row=8)

img3=tk.PhotoImage(file='monoico/icon-722.png')

emplogwin.mainloop()