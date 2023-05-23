import mysql.connector as ms
import tkinter as tk
import os
from tkinter import ttk
from tkinter import messagebox

#mysql connection
con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
cur=con.cursor()

fnt=('IBM Plex Mono',12)
fntit=('IBM Plex Mono',12,'italic')
h1fnt=('IBM Plex Sans',24)

emplogwin=tk.Tk()
emplogwin.title('Login for employees')
w,h=emplogwin.winfo_screenwidth(),emplogwin.winfo_screenheight()
emplogwin.geometry(str(w)+'x'+str(h))

def login():
	emp_uname_inp=emp_uname.get().lower()
	emptype_inp=n.get()
	emp_passwd_inp=emp_passwd.get()
	
	if emptype_inp == 'Agent':
		
		cur.execute('select emp_uname,emp_passwd from employees')
		e=dict(cur.fetchall())

		cur.execute('select emp_uname,emp_name from employees')
		f=dict(cur.fetchall())
		if not emp_uname_inp=='' or emp_uname_inp.isspace():
			if emp_uname_inp in e.keys():
				if emp_passwd_inp==e[emp_uname_inp]:
					emplogwin.destroy()
					os.system('python3 empbkgs.py')
				else:
					messagebox.showerror('Error','Invalid password for\nemployee '+f[emp_uname_inp]+'.')
			else:
				messagebox.showerror('Error','Employee '+emp_uname_inp+' does not exist.')
		else:
			messagebox.showerror('Error','Do not leave any fields empty.')
	elif emptype_inp == 'Administrator':
	
		cur.execute('select admin_uname,admin_passwd from admin')
		a=dict(cur.fetchall())
		if emp_uname_inp in a.keys():
			if emp_passwd_inp==a[emp_uname_inp]:
				emplogwin.destroy()
				os.system('python3 admin.py')
			else:
				messagebox.showerror('Error','Invalid password for\nadministrator '+emp_uname_inp+'.')
		else:
			messagebox.showerror('Error','Administrator '+emp_uname_inp+' does not exist.')
	else:
		messagebox.showerror('Error','Please select login type.')
#Window
tk.Grid.columnconfigure(emplogwin,0,weight=1)

#FRAME 1
tk.Grid.rowconfigure(emplogwin,0,weight=1)
f1=tk.Frame(emplogwin)
f1.grid(row=0,column=0,sticky=tk.NSEW)

#frame 1 grid
tk.Grid.columnconfigure(f1,0,weight=1)

tk.Grid.rowconfigure(f1,0,weight=1)
tk.Label(f1,text='Login for employees',font=h1fnt,justify=tk.CENTER).grid(column=0,row=0)

#FRAME 2
tk.Grid.rowconfigure(emplogwin,1,weight=1)
f2=tk.Frame(emplogwin)
f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

#frame 2 grid
tk.Grid.columnconfigure(f2,0,weight=1)
tk.Grid.columnconfigure(f2,1,weight=1)

tk.Label(f2,text='Login as',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
n=tk.StringVar()
values=('','Agent','Administrator')
emptype=ttk.OptionMenu(f2,n,*values);emptype.grid(column=1,row=5,sticky=tk.W,padx=10,pady=10)

tk.Label(f2,text='Username',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
emp_uname=tk.Entry(f2,font=fnt)
emp_uname.grid(column=1,row=6,sticky=tk.W,padx=10,pady=10)

tk.Label(f2,text='Password',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
emp_passwd=tk.Entry(f2,show='*',font=fnt)
emp_passwd.grid(column=1,row=7,sticky=tk.W,padx=10,pady=10)

img1=tk.PhotoImage(file='monoico/icon-669.png')
logsubmit=tk.Button(f2,text='Login',image=img1,command=login)
logsubmit.grid(column=1,row=8,padx=10,pady=10,sticky=tk.W)

tk.Grid.rowconfigure(f2,9,weight=2)
img2=tk.PhotoImage(file='monoico/icon-66.png')
logsubmit=tk.Button(f2,text='Exit',image=img2,command=emplogwin.destroy)
logsubmit.grid(column=1,row=9,padx=10,pady=10,sticky=tk.W)

emplogwin.mainloop()
