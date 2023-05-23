def manageadmin():	#Manage admins
	import mysql.connector as ms
	import tkinter as tk
	import platform as pf
	import ctypes
	from tkinter import ttk
	from tkinter import messagebox
	import random as rd
	
	try:
		ctypes.windll.shcore.SetProcessDpiAwareness(True)
	except:
		pass

	con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
	cur=con.cursor()

	fnt=('IBM Plex Mono',12)
	fntit=('IBM Plex Mono',12,'italic')
	h1fnt=('IBM Plex Sans',24)

	manageadminwin=tk.Toplevel()
	manageadminwin.title('Administrator Manager')
	#w,h=manageempwin.winfo_screenwidth(),manageempwin.winfo_screenheight()
	#manageempwin.geometry(str(w)+'x'+str(h))

	def viewall():
		viewall_win=tk.Toplevel()
		viewall_win.title('All administrators')
		viewall_win.resizable(False,False)
		
		header=('Admin ID','Admin Username','Admin Name','Admin Password')

		sql2=str('select * from admin')			#getting data from table
		#print(sql2)
		cur.execute(sql2)
		e=[header]+cur.fetchall()						#appending header to data
		#print(e)
		
		rows=len(e)
		cols=len(e[0])

		for i in range(rows):							#drawing the table in GUI
			for j in range(cols):
				entry = tk.Label(viewall_win,borderwidth=1,relief='solid',padx=10,height=2,font=fnt)
				entry.grid(row=i, column=j,padx=2,pady=2,sticky=tk.EW)
				entry.configure(text=e[i][j])
				if i==0:
					entry.configure(fg='red',font=fntit)	#colors and italicises header

	def viewone():
		def getadmninfo():
			cur.execute('select admin_uname from admin')
			a=cur.fetchall()
			b=[]
			for i in a:
				b.append(i[0])
			if not uname.get()=='' and not uname.get().isspace():
				if uname.get() in b:
					sql='select * from admin where admin_uname=%s'
					val=(uname.get(),)
					cur.execute(sql,val)
					c=cur.fetchall()
					admin_id=c[0][0]
					admin_uname=c[0][1]
					admin_name=c[0][2]
					admin_passwd=c[0][3]
					
					e=[('Administrator ID',admin_id),('Administrator Username',admin_uname),('Administrator Full Name',admin_name),('Administrator Password',admin_passwd)]
					
					#details.configure(text=txt)
					#details.grid(row=7,column=0,sticky=tk.EW)
					
					rows=len(e)
					cols=len(e[0])
					tk.Label(frame3,font=fntit,text='Data').grid(row=0,column=0,sticky=tk.W)
					for i in range(rows):							#drawing the table in GUI
						for j in range(cols):
							entry = tk.Label(frame2,borderwidth=1,relief='solid',padx=10,width=30,height=2,font=fnt)
							entry.grid(row=i,column=j,padx=2,pady=2,sticky=tk.EW)
							entry.configure(text=e[i][j])
							if j==0:
								entry.configure(fg='red',font=fntit) #colors and italicises header
				else:
					messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=viewone_win)
			else:
				messagebox.showerror('Error','Please enter the administrator username.',parent=viewone_win)
		viewone_win=tk.Toplevel()
		viewone_win.title('')
		viewone_win.resizable(False,False)
		
		frame1=tk.Frame(viewone_win)
		frame1.grid(row=0,column=0,padx=10,pady=10,sticky=tk.EW)

		frame2=tk.Frame(viewone_win)
		frame2.grid(row=2,column=0,padx=10,pady=10,sticky=tk.EW)

		frame3=tk.Frame(viewone_win)
		frame3.grid(row=1,column=0,padx=10,pady=10,sticky=tk.W)

		cur.execute('select admin_uname from admin')
		a=cur.fetchall()
		b=[]
		for i in a:
			b.append(i[0])

		img14=tk.PhotoImage(file='icons/searchusr.png')
		img=tk.Label(frame1,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(frame1,font=h1fnt,text='View administrator details').grid(row=0,column=1,padx=10,pady=10,sticky=tk.W)

		tk.Label(frame1,font=fnt,text='Enter username of administrator.').grid(row=4,column=1,padx=10,pady=10,sticky=tk.W)
		n=tk.StringVar()
		uname=ttk.Combobox(frame1,textvariable=n,font=fnt)
		uname.grid(row=5,column=1,padx=10,pady=10,sticky=tk.EW)
		uname['values']=b
		
		#img11=tk.PhotoImage(file='monoico/icon-582.png')
		submit=tk.Button(frame1,font=fntit,text='Submit',command=getadmninfo)
		submit.grid(row=5,column=2,padx=10,pady=10)
		#submit.image=img11

	def delone():
		delone_win=tk.Toplevel()
		delone_win.resizable(False,False)
		delone_win.title('')
		cur.execute('select admin_uname,admin_name from admin')
		a=cur.fetchall()
		b=dict(a)
		def deleteadmin():
			if not uname.get()=='' and not uname.get().isspace():
				if uname.get() in c:
					messagebox.showwarning('','This operation will delete\nthe username of the administrator permanently.\nContinue?',parent=delone_win)
					confirm=messagebox.askyesno('','Do you wish to delete the administrator '+b[uname.get()]+'?',parent=delone_win)
					if confirm == True:
						sql='delete from admin where admin_uname =%s'
						val=(uname.get(),)
						cur.execute(sql,val)
						con.commit()
						messagebox.showinfo('','Administrator '+b[uname.get()]+' deleted.',parent=delone_win)
						delone_win.destroy()
					else:
						messagebox.showinfo('','Administrator '+b[uname.get()]+' not deleted.\nThe database has not been modified.',parent=delone_win)
				else:
					messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=delone_win)
			else:
				messagebox.showerror('','Please enter the administrator username.',parent=delone_win)
		
		
		
		img14=tk.PhotoImage(file='icons/ban_user.png')
		img=tk.Label(delone_win,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(delone_win,text='Delete an administrator',font=h1fnt).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

		cur.execute('select admin_uname from admin')
		d=cur.fetchall()
		c=[]
		for i in d:
			c.append(i[0])

		tk.Label(delone_win,text='Select an administrator.',font=fntit).grid(column=1,row=4,padx=10,pady=10,sticky=tk.W)

		n=tk.StringVar()
		uname=ttk.Combobox(delone_win,textvariable=n,font=fnt,width=19)
		uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
		uname['values']=c

		#img13=tk.PhotoImage(file='monoico/icon-694.png')
		delbtn=tk.Button(delone_win,text='Delete',font=fntit,command=deleteadmin,fg='red')
		#delbtn.image=img13
		delbtn.grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

	def passwd():
		passwd_win=tk.Toplevel()
		passwd_win.resizable(False,False)
		passwd_win.title('')

		cur.execute('select admin_uname,admin_name from admin')
		a=cur.fetchall()
		b=dict(a)
		def chpasswd():
			if (not uname.get()=='' and not uname.get().isspace()) and (not npass.get()=='' and not npass.get().isspace()):
				if uname.get() in c:
		
					confirm=messagebox.askyesno('','Do you wish to change the password of '+b[uname.get()]+'?',parent=passwd_win)
					if confirm == True:
						sql='update admin set admin_passwd=%s where admin_uname=%s'
						val=(npass.get(),uname.get())
						cur.execute(sql,val)
						con.commit()
						messagebox.showinfo('','Password for '+b[uname.get()]+'\nchanged.',parent=passwd_win)
						passwd_win.destroy()
					else:
						messagebox.showinfo('','Password for '+b[uname.get()]+' has not been changed..\nThe databasehas not\nbeen modified.',parent=passwd_win)
				else:
					messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=passwd_win)
			else:
				messagebox.showerror('','Do not leave any fields blank.',parent=passwd_win)
		
		img14=tk.PhotoImage(file='icons/passwd.png')
		img=tk.Label(passwd_win,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(passwd_win,text='Change password\nfor administrator',font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

		cur.execute('select admin_uname from admin')
		d=cur.fetchall()
		c=[]
		for i in d:
			c.append(i[0])

		n=tk.StringVar()
		tk.Label(passwd_win,text='Username',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
		uname=ttk.Combobox(passwd_win,textvariable=n,font=fnt,width=19)
		uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
		uname['values']=c
		uname.current(0)

		tk.Label(passwd_win,text='New password',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
		npass=tk.Entry(passwd_win,font=fnt,show='*')
		npass.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

		#img13=tk.PhotoImage(file='monoico/icon-694.png')
		subbtn=tk.Button(passwd_win,text='Make changes',font=fntit,command=chpasswd)
		#subbtn.image=img13
		subbtn.grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)

	def add():
		add_win=tk.Toplevel()
		add_win.resizable(False,False)
		add_win.title('')

		def add_admin():
			uname_inp=uname.get().lower()
			fname_inp=fname.get()
			passwd_inp=passwd.get()

			cur.execute('select admin_uname from admin')
			a=cur.fetchall()
			b=[]
			for i in a:
				b.append(i[0])

			#l1=[id,uname_inp,fname_inp,passwd_inp]
			if (not uname_inp=='' and not uname_inp.isspace()) and (not fname_inp=='' and not fname_inp.isspace()) and (not passwd_inp=='' and not passwd_inp.isspace()):
				if uname_inp not in b:
					#Sends inputs to MySQL db
					sql='insert into admin values (%s,%s,%s,%s)'
					val=(id,uname_inp,fname_inp,passwd_inp)
					cur.execute(sql,val)
					con.commit()
					messagebox.showinfo('','Administrator '+fname_inp+' registered successfully.',parent=add_win)
					add_win.destroy()
				else:
					messagebox.showerror('Error','Username \''+uname_inp+'\'\nalready exists.',parent=add_win)
			else:
				messagebox.showerror('Error','Do not leave any fields blank.',parent=add_win)
		
		id='A'+str(rd.randint(1000,9999))

		img14=tk.PhotoImage(file='icons/adduser.png')
		img=tk.Label(add_win,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(add_win,text='Register administrator',font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)

		tk.Label(add_win,text='UID',font=fnt).grid(column=0,row=3,sticky=tk.E,padx=10,pady=10)
		bkgid=tk.Label(add_win,text=id,font=fnt)
		bkgid.grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

		tk.Label(add_win,text='Full Name',font=fnt).grid(column=0,row=4,sticky=tk.E,padx=10,pady=10)
		fname=tk.Entry(add_win,font=fnt)
		fname.grid(column=1,row=4,sticky=tk.EW,padx=10,pady=10)

		tk.Label(add_win,text='Username',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
		uname=tk.Entry(add_win,font=fnt)
		uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)

		tk.Label(add_win,text='Password',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
		passwd=tk.Entry(add_win,font=fnt,show='*')
		passwd.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

		#subimg=tk.PhotoImage(file='monoico/icon-308.png')
		subbtn=tk.Button(add_win,font=fntit,text='Register',command=add_admin)
		subbtn.grid(column=1,row=12,padx=10,pady=10,sticky=tk.W)
		#subbtn.image=subimg

		'''
		exitimg=tk.PhotoImage(file='monoico/icon-66.png')
		exitbtn=tk.Button(add_win,font=fnt,text='Exit',image=exitimg,command=add_win.destroy)
		exitbtn.grid(column=0,row=15,padx=10,pady=10,sticky=tk.SW)
		exitbtn.image=exitimg
		'''

	tk.Grid.columnconfigure(manageadminwin,0,weight=1)

	#FRAME 1
	tk.Grid.rowconfigure(manageadminwin,0,weight=1)
	f1=tk.Frame(manageadminwin)
	f1.grid(row=0,column=0,sticky=tk.NSEW)

	#frame 1 grid
	tk.Grid.columnconfigure(f1,0,weight=1)
	tk.Grid.columnconfigure(f1,1,weight=1)

	tk.Grid.rowconfigure(f1,0,weight=1)
	img6=tk.PhotoImage(file='icons/supervisor.png')
	himg=tk.Label(f1,image=img6)
	himg.grid(column=0,row=0,sticky=tk.E,padx=10,pady=10)
	himg.image=img6
	tk.Label(f1,text=('Manage the administrators...'),font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)
	#tk.Grid.rowconfigure(f1,1,weight=1)
	tk.Label(f1,text=('Connected to database: '+con.database),font=('IBM Plex Sans',12),justify=tk.LEFT,fg='green').grid(column=1,row=1,sticky=tk.W,padx=10,pady=10)
	ttk.Separator(f1,orient='horizontal').grid(column=0,row=2,sticky=tk.EW,padx=10,pady=10,columnspan=2)
	#FRAME 2
	tk.Grid.rowconfigure(manageadminwin,1,weight=1)
	f2=tk.Frame(manageadminwin)
	f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

	#frame 2 grid
	tk.Grid.columnconfigure(f2,0,weight=1)
	tk.Grid.columnconfigure(f2,1,weight=1)
	tk.Grid.columnconfigure(f2,2,weight=1)
	tk.Grid.columnconfigure(f2,3,weight=1)

	tk.Label(f2,text='You can:',font=fntit,justify=tk.LEFT).grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

	tk.Grid.rowconfigure(f2,5,weight=1)
	img8=tk.PhotoImage(file='icons/preview.png')
	tbviewbtn=tk.Button(f2,text='view all',image=img8,font=fnt,command=viewall)
	tbviewbtn.grid(column=0,row=5,padx=10,pady=10,sticky=tk.E)
	tbviewbtn.image=img8
	tk.Label(f2,text='View all administrator details.',font=fnt,fg='blue').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

	img10=tk.PhotoImage(file='icons/searchusr.png')
	viewbtn=tk.Button(f2,text='viewone',image=img10,font=fnt,command=viewone)
	viewbtn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
	viewbtn.image=img10
	tk.Label(f2,text='View a single admin\'s details.',font=fnt).grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)

	tk.Grid.rowconfigure(f2,6,weight=1)
	img7=tk.PhotoImage(file='icons/adduser.png')
	tbviewbtn=tk.Button(f2,text='add',image=img7,font=fnt,command=add)
	tbviewbtn.grid(column=0,row=6,padx=10,pady=10,sticky=tk.E)
	tbviewbtn.image=img7
	tk.Label(f2,text='Register an administrator.',font=fnt,fg='green').grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

	img11=tk.PhotoImage(file='icons/passwd.png')
	passbtn=tk.Button(f2,text='passwd',image=img11,font=fnt,command=passwd)
	passbtn.grid(column=2,row=6,padx=10,pady=10,sticky=tk.E)
	passbtn.image=img11
	tk.Label(f2,text='Change the password for an administrator.',font=fnt).grid(column=3,row=6,padx=10,pady=10,sticky=tk.W)

	tk.Grid.rowconfigure(f2,7,weight=1)
	img12=tk.PhotoImage(file='icons/deluser.png')
	delbtn=tk.Button(f2,text='del',image=img12,font=fnt,command=delone)
	delbtn.grid(column=0,row=7,padx=10,pady=10,sticky=tk.E)
	delbtn.image=img12
	tk.Label(f2,text='Delete an administrator.',font=fnt,fg='red').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)
	tk.Grid.rowconfigure(f2,8,weight=1)
	tk.Message(f2,text='WARNING: This will delete\nan admin\'s profile\nfrom the system permanently.',width=500,font=fnt,fg='white',bg='red').grid(column=1,row=8,padx=10,pady=10,sticky=tk.NW)

	#tk.Label(f2,text='or:',font=fntit,justify=tk.LEFT).grid(column=1,row=15,sticky=tk.W,padx=10,pady=10)

	tk.Grid.rowconfigure(f2,16,weight=1)

def manageemp():	#Manage agents (employees)
	import mysql.connector as ms
	import tkinter as tk
	import platform as pf
	import ctypes
	from tkinter import ttk
	from tkinter import messagebox
	import random as rd

	try:
		ctypes.windll.shcore.SetProcessDpiAwareness(True)
	except:
		pass

	con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
	cur=con.cursor()

	fnt=('IBM Plex Mono',12)
	fntit=('IBM Plex Mono',12,'italic')
	h1fnt=('IBM Plex Sans',24)

	manageempwin=tk.Toplevel()
	manageempwin.title('Employee Manager')
	#w,h=manageempwin.winfo_screenwidth(),manageempwin.winfo_screenheight()
	#manageempwin.geometry(str(w)+'x'+str(h))

	def viewall():
		viewall_win=tk.Toplevel()
		viewall_win.title('All employees')
		viewall_win.resizable(False,False)
		
		header=('Employee ID','Employee Username','Employee Name','Employee Password')

		sql2=str('select * from employees')			#getting data from table
		#print(sql2)
		cur.execute(sql2)
		e=[header]+cur.fetchall()						#appending header to data
		#print(e)
		
		rows=len(e)
		cols=len(e[0])

		for i in range(rows):							#drawing the table in GUI
			for j in range(cols):
				entry = tk.Label(viewall_win,borderwidth=1,relief='solid',padx=10,height=2,font=fnt)
				entry.grid(row=i, column=j,padx=2,pady=2,sticky=tk.EW)
				entry.configure(text=e[i][j])
				if i==0:
					entry.configure(fg='red',font=fntit)	#colors and italicises header

	def viewone():
		def getempinfo():
			cur.execute('select emp_uname from employees')
			a=cur.fetchall()
			b=[]
			for i in a:
				b.append(i[0])
			if not uname.get()=='' and not uname.get().isspace():
				if uname.get() in b:
					sql='select * from employees where emp_uname=%s'
					val=(uname.get(),)
					cur.execute(sql,val)
					c=cur.fetchall()
					emp_id=c[0][0]
					emp_uname=c[0][1]
					emp_name=c[0][2]
					emp_passwd=c[0][3]
					
					e=[('Employee ID',emp_id),('Employee Username',emp_uname),('Employee Full Name',emp_name),('Employee Password',emp_passwd)]
					
					#details.configure(text=txt)
					#details.grid(row=7,column=0,sticky=tk.EW)
					
					rows=len(e)
					cols=len(e[0])
					tk.Label(frame3,font=fntit,text='Data').grid(row=0,column=0,sticky=tk.W)
					for i in range(rows):							#drawing the table in GUI
						for j in range(cols):
							entry = tk.Label(frame2,borderwidth=1,relief='solid',padx=10,width=30,height=2,font=fnt)
							entry.grid(row=i,column=j,padx=2,pady=2,sticky=tk.EW)
							entry.configure(text=e[i][j])
							if j==0:
								entry.configure(fg='red',font=fntit,width=20) #colors and italicises header
				else:
					messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=viewone_win)
			else:
				messagebox.showerror('Error','Please enter the employee username.',parent=viewone_win)
		viewone_win=tk.Toplevel()
		viewone_win.title('')
		viewone_win.resizable(False,False)
		
		frame1=tk.Frame(viewone_win)
		frame1.grid(row=0,column=0,padx=10,pady=10,sticky=tk.EW)

		frame2=tk.Frame(viewone_win)
		frame2.grid(row=2,column=0,padx=10,pady=10,sticky=tk.EW)

		frame3=tk.Frame(viewone_win)
		frame3.grid(row=1,column=0,padx=10,pady=10,sticky=tk.W)

		cur.execute('select emp_uname from employees')
		a=cur.fetchall()
		b=[]
		for i in a:
			b.append(i[0])

		img14=tk.PhotoImage(file='icons/searchusr.png')
		img=tk.Label(frame1,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(frame1,font=h1fnt,text='View employee details').grid(row=0,column=1,padx=10,pady=10,sticky=tk.W)

		tk.Label(frame1,font=fnt,text='Enter username of employee.').grid(row=4,column=1,padx=10,pady=10,sticky=tk.W)
		n=tk.StringVar()
		uname=ttk.Combobox(frame1,textvariable=n,font=fnt)
		uname.grid(row=5,column=1,padx=10,pady=10,sticky=tk.EW)
		uname['values']=b
		
		#img11=tk.PhotoImage(file='monoico/icon-582.png')
		submit=tk.Button(frame1,font=fntit,text='Submit',command=getempinfo)
		submit.grid(row=5,column=2,padx=10,pady=10)
		#submit.image=img11

	def delone():
		delone_win=tk.Toplevel()
		delone_win.resizable(False,False)
		delone_win.title('')
		cur.execute('select emp_uname,emp_name from employees')
		a=cur.fetchall()
		b=dict(a)
		def deleteemp():
			if not uname.get()=='' and not uname.get().isspace():
				if uname.get() in c:
					messagebox.showwarning('','This operation will delete\nthe username of the employee permanently.\nContinue?',parent=delone_win)
					confirm=messagebox.askyesno('','Do you wish to delete the employee '+b[uname.get()]+'?',parent=delone_win)
					if confirm == True:
						sql='delete from employees where emp_uname =%s'
						val=(uname.get(),)
						cur.execute(sql,val)
						con.commit()
						messagebox.showinfo('','Employee '+b[uname.get()]+' deleted.',parent=delone_win)
						delone_win.destroy()
					else:
						messagebox.showinfo('','Employee '+b[uname.get()]+' not deleted.\nThe database has not been modified.',parent=delone_win)
				else:
					messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=delone_win)
			else:
				messagebox.showerror('','Please enter the employee username.',parent=delone_win)
		
		
		
		img14=tk.PhotoImage(file='icons/ban_user.png')
		img=tk.Label(delone_win,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(delone_win,text='Delete an employee',font=h1fnt).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

		cur.execute('select emp_uname from employees')
		d=cur.fetchall()
		c=[]
		for i in d:
			c.append(i[0])

		tk.Label(delone_win,text='Select an employee.',font=fntit).grid(column=1,row=4,padx=10,pady=10,sticky=tk.W)

		n=tk.StringVar()
		uname=ttk.Combobox(delone_win,textvariable=n,font=fnt,width=19)
		uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
		uname['values']=c

		#img13=tk.PhotoImage(file='monoico/icon-694.png')
		delbtn=tk.Button(delone_win,text='Delete',font=fntit,command=deleteemp,fg='red')
		#delbtn.image=img13
		delbtn.grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

	def passwd():
		passwd_win=tk.Toplevel()
		passwd_win.resizable(False,False)
		passwd_win.title('')

		cur.execute('select emp_uname,emp_name from employees')
		a=cur.fetchall()
		b=dict(a)
		def chpasswd():
			if (not uname.get()=='' and not uname.get().isspace()) and (not npass.get()=='' and not npass.get().isspace()):
				if uname.get() in c:
		
					confirm=messagebox.askyesno('','Do you wish to change the password of '+b[uname.get()]+'?',parent=passwd_win)
					if confirm == True:
						sql='update employees set emp_passwd=%s where emp_uname=%s'
						val=(npass.get(),uname.get())
						cur.execute(sql,val)
						con.commit()
						messagebox.showinfo('','Password for '+b[uname.get()]+'\nchanged.',parent=passwd_win)
						passwd_win.destroy()
					else:
						messagebox.showinfo('','Password for '+b[uname.get()]+' has not been changed..\nThe databasehas not\nbeen modified.',parent=passwd_win)
				else:
					messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=passwd_win)
			else:
				messagebox.showerror('','Do not leave any fields blank.',parent=passwd_win)
		
		img14=tk.PhotoImage(file='icons/passwd.png')
		img=tk.Label(passwd_win,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(passwd_win,text='Change password\nfor employee',font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

		cur.execute('select emp_uname from employees')
		d=cur.fetchall()
		c=[]
		for i in d:
			c.append(i[0])

		n=tk.StringVar()
		tk.Label(passwd_win,text='Username',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
		uname=ttk.Combobox(passwd_win,textvariable=n,font=fnt,width=19)
		uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
		uname['values']=c
		uname.current(0)

		tk.Label(passwd_win,text='New password',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
		npass=tk.Entry(passwd_win,font=fnt,show='*')
		npass.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

		#img13=tk.PhotoImage(file='monoico/icon-694.png')
		subbtn=tk.Button(passwd_win,text='Make changes',font=fntit,command=chpasswd)
		#subbtn.image=img13
		subbtn.grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)

	def add():
		add_win=tk.Toplevel()
		add_win.resizable(False,False)
		add_win.title('')

		def add_emp():
			uname_inp=uname.get().lower()
			fname_inp=fname.get()
			passwd_inp=passwd.get()

			cur.execute('select emp_uname from employees')
			a=cur.fetchall()
			b=[]
			for i in a:
				b.append(i[0])

			#l1=[id,uname_inp,fname_inp,passwd_inp]
			if (not uname_inp=='' and not uname_inp.isspace()) and (not fname_inp=='' and not fname_inp.isspace()) and (not passwd_inp=='' and not passwd_inp.isspace()):
				if uname_inp not in b:
					#Sends inputs to MySQL db
					sql='insert into employees values (%s,%s,%s,%s)'
					val=(id,uname_inp,fname_inp,passwd_inp)
					cur.execute(sql,val)
					con.commit()
					messagebox.showinfo('','Employee '+fname_inp+' registered successfully.',parent=add_win)
					add_win.destroy()
				else:
					messagebox.showerror('Error','Username \''+uname_inp+'\'\nalready exists.',parent=add_win)
			else:
				messagebox.showerror('Error','Do not leave any fields blank.',parent=add_win)
		
		id='E'+str(rd.randint(1000,9999))

		img14=tk.PhotoImage(file='icons/adduser.png')
		img=tk.Label(add_win,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(add_win,text='Register employee',font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)

		tk.Label(add_win,text='UID',font=fnt).grid(column=0,row=3,sticky=tk.E,padx=10,pady=10)
		bkgid=tk.Label(add_win,text=id,font=fnt)
		bkgid.grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

		tk.Label(add_win,text='Full Name',font=fnt).grid(column=0,row=4,sticky=tk.E,padx=10,pady=10)
		fname=tk.Entry(add_win,font=fnt)
		fname.grid(column=1,row=4,sticky=tk.EW,padx=10,pady=10)

		tk.Label(add_win,text='Username',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
		uname=tk.Entry(add_win,font=fnt)
		uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)

		tk.Label(add_win,text='Password',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
		passwd=tk.Entry(add_win,font=fnt,show='*')
		passwd.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

		#subimg=tk.PhotoImage(file='monoico/icon-308.png')
		subbtn=tk.Button(add_win,font=fntit,text='Register',command=add_emp)
		subbtn.grid(column=1,row=12,padx=10,pady=10,sticky=tk.W)
		#subbtn.image=subimg

		'''
		exitimg=tk.PhotoImage(file='monoico/icon-66.png')
		exitbtn=tk.Button(add_win,font=fnt,text='Exit',image=exitimg,command=add_win.destroy)
		exitbtn.grid(column=0,row=15,padx=10,pady=10,sticky=tk.SW)
		exitbtn.image=exitimg
		'''


	tk.Grid.columnconfigure(manageempwin,0,weight=1)

	#FRAME 1
	tk.Grid.rowconfigure(manageempwin,0,weight=1)
	f1=tk.Frame(manageempwin)
	f1.grid(row=0,column=0,sticky=tk.NSEW)

	#frame 1 grid
	tk.Grid.columnconfigure(f1,0,weight=1)
	tk.Grid.columnconfigure(f1,1,weight=1)

	tk.Grid.rowconfigure(f1,0,weight=1)
	img6=tk.PhotoImage(file='icons/employee.png')
	himg=tk.Label(f1,image=img6)
	himg.grid(column=0,row=0,sticky=tk.E,padx=10,pady=10)
	himg.image=img6
	tk.Label(f1,text=('Manage the employees...'),font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)
	#tk.Grid.rowconfigure(f1,1,weight=1)
	tk.Label(f1,text=('Connected to database: '+con.database),font=('IBM Plex Sans',12),justify=tk.LEFT,fg='green').grid(column=1,row=1,sticky=tk.W,padx=10,pady=10)
	ttk.Separator(f1,orient='horizontal').grid(column=0,row=2,sticky=tk.EW,padx=10,pady=10,columnspan=2)
	#FRAME 2
	tk.Grid.rowconfigure(manageempwin,1,weight=1)
	f2=tk.Frame(manageempwin)
	f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

	#frame 2 grid
	tk.Grid.columnconfigure(f2,0,weight=1)
	tk.Grid.columnconfigure(f2,1,weight=1)
	tk.Grid.columnconfigure(f2,2,weight=1)
	tk.Grid.columnconfigure(f2,3,weight=1)

	tk.Label(f2,text='You can:',font=fntit,justify=tk.LEFT).grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

	tk.Grid.rowconfigure(f2,5,weight=1)
	img8=tk.PhotoImage(file='icons/preview.png')
	tbviewbtn=tk.Button(f2,text='view all',image=img8,font=fnt,command=viewall)
	tbviewbtn.grid(column=0,row=5,padx=10,pady=10,sticky=tk.E)
	tbviewbtn.image=img8
	tk.Label(f2,text='View all employee details.',font=fnt,fg='blue').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

	img10=tk.PhotoImage(file='icons/searchusr.png')
	viewbtn=tk.Button(f2,text='viewone',image=img10,font=fnt,command=viewone)
	viewbtn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
	viewbtn.image=img10
	tk.Label(f2,text='View a single employee\'s details.',font=fnt).grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)

	tk.Grid.rowconfigure(f2,6,weight=1)
	img7=tk.PhotoImage(file='icons/adduser.png')
	tbviewbtn=tk.Button(f2,text='add',image=img7,font=fnt,command=add)
	tbviewbtn.grid(column=0,row=6,padx=10,pady=10,sticky=tk.E)
	tbviewbtn.image=img7
	tk.Label(f2,text='Register an employee.',font=fnt,fg='green').grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

	img11=tk.PhotoImage(file='icons/passwd.png')
	passbtn=tk.Button(f2,text='passwd',image=img11,font=fnt,command=passwd)
	passbtn.grid(column=2,row=6,padx=10,pady=10,sticky=tk.E)
	passbtn.image=img11
	tk.Label(f2,text='Change the password for an employee.',font=fnt).grid(column=3,row=6,padx=10,pady=10,sticky=tk.W)

	tk.Grid.rowconfigure(f2,7,weight=1)
	img12=tk.PhotoImage(file='icons/deluser.png')
	delbtn=tk.Button(f2,text='del',image=img12,font=fnt,command=delone)
	delbtn.grid(column=0,row=7,padx=10,pady=10,sticky=tk.E)
	delbtn.image=img12
	tk.Label(f2,text='Delete an employee.',font=fnt,fg='red').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)
	tk.Grid.rowconfigure(f2,8,weight=1)
	tk.Message(f2,text='WARNING: This will delete\nan employee\'s profile\nfrom the system permanently.',width=500,font=fnt,fg='white',bg='red').grid(column=1,row=8,padx=10,pady=10,sticky=tk.NW)

	#tk.Label(f2,text='or:',font=fntit,justify=tk.LEFT).grid(column=1,row=15,sticky=tk.W,padx=10,pady=10)

	tk.Grid.rowconfigure(f2,16,weight=1)
	
def manageusers():	#Manage users
	import mysql.connector as ms
	import tkinter as tk
	import platform as pf
	import ctypes
	from tkinter import ttk
	from tkinter import messagebox
	import random as rd

	try:
		ctypes.windll.shcore.SetProcessDpiAwareness(True)
	except:
		pass

	con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
	cur=con.cursor()

	fnt=('IBM Plex Mono',12)
	fntit=('IBM Plex Mono',12,'italic')
	h1fnt=('IBM Plex Sans',24)

	manageuserwin=tk.Toplevel()
	manageuserwin.title('User Manager')
	#w,h=manageuserwin.winfo_screenwidth(),manageuserwin.winfo_screenheight()
	#manageuserwin.geometry(str(w)+'x'+str(h))

	def viewall():
		viewall_win=tk.Toplevel()
		viewall_win.title('All users')
		viewall_win.resizable(False,False)
		
		header=('User ID','Full Name','Electronic Mail','Number','Username','Password')

		sql2=str('select * from users')			#getting data from table
		#print(sql2)
		cur.execute(sql2)
		e=[header]+cur.fetchall()						#appending header to data
		#print(e)
		
		rows=len(e)
		cols=len(e[0])

		for i in range(rows):							#drawing the table in GUI
			for j in range(cols):
				entry = tk.Label(viewall_win,borderwidth=1,relief='solid',padx=10,height=2,font=fnt)
				entry.grid(row=i,column=j,padx=2,pady=2,sticky=tk.EW)
				entry.configure(text=e[i][j])
				if i==0:
					entry.configure(fg='red',font=fntit)	#colors and italicises header

	def viewone():
		def getuserinfo():
			cur.execute('select uname from users')
			a=cur.fetchall()
			b=[]
			for i in a:
				b.append(i[0])
			if not uname.get()=='' and not uname.get().isspace():
				if uname.get() in b:
					sql='select * from users where uname=%s'
					val=(uname.get(),)
					cur.execute(sql,val)
					c=cur.fetchall()
					user_id=c[0][0]
					user_fname=c[0][1]
					user_email=c[0][2]
					user_num=c[0][3]
					user_uname=c[0][4]
					user_passwd=c[0][5]
					
					e=[('User ID',user_id),('Full Name',user_fname),('Electronic Mail',user_email),('Phone Number',user_num),('Username',user_uname),('Password',user_passwd)]
					
					#details.configure(text=txt)
					#details.grid(row=7,column=0,sticky=tk.EW)
					
					rows=len(e)
					cols=len(e[0])
					tk.Label(frame3,font=fntit,text='Data').grid(row=0,column=0,sticky=tk.W)
					for i in range(rows):							#drawing the table in GUI
						for j in range(cols):
							entry = tk.Label(frame2,borderwidth=1,relief='solid',padx=10,height=2,width=25,font=fnt)
							entry.grid(row=i,column=j,padx=2,pady=2,sticky=tk.EW)
							entry.configure(text=e[i][j])
							if j==0:
								entry.configure(fg='red',font=fntit,width=15) #colors and italicises header
				else:
					messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=viewone_win)
			else:
				messagebox.showerror('Error','Please enter the username.',parent=viewone_win)
		viewone_win=tk.Toplevel()
		viewone_win.title('')
		viewone_win.resizable(False,False)
		
		frame1=tk.Frame(viewone_win)
		frame1.grid(row=0,column=0,padx=10,pady=10,sticky=tk.EW)

		frame2=tk.Frame(viewone_win)
		frame2.grid(row=2,column=0,padx=10,pady=10,sticky=tk.EW)

		frame3=tk.Frame(viewone_win)
		frame3.grid(row=1,column=0,padx=10,pady=10,sticky=tk.W)

		cur.execute('select uname from users')
		a=cur.fetchall()
		b=[]
		for i in a:
			b.append(i[0])

		img14=tk.PhotoImage(file='icons/searchusr.png')
		img=tk.Label(frame1,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(frame1,font=h1fnt,text='View user details').grid(row=0,column=1,padx=10,pady=10,sticky=tk.W)

		tk.Label(frame1,font=fnt,text='Enter username.').grid(row=4,column=1,padx=10,pady=10,sticky=tk.W)
		n=tk.StringVar()
		uname=ttk.Combobox(frame1,textvariable=n,font=fnt)
		uname.grid(row=5,column=1,padx=10,pady=10,sticky=tk.EW)
		uname['values']=b
		
		#img11=tk.PhotoImage(file='monoico/icon-582.png')
		submit=tk.Button(frame1,font=fntit,text='Submit',command=getuserinfo)
		submit.grid(row=5,column=2,padx=10,pady=10)
		#submit.image=img11

	def delone():
		delone_win=tk.Toplevel()
		delone_win.resizable(False,False)
		delone_win.title('')

		def deleteuser():
			#cur.execute('select uname,fname from users')
			#a=dict(cur.fetchall())
			
			if not uname.get()=='' and not uname.get().isspace():
				if uname.get() in c:
					messagebox.showwarning('','This operation will delete\nthe user permanently.\nContinue?',parent=delone_win)
					confirm=messagebox.askyesno('','Do you wish to delete the user '+uname.get()+'?',parent=delone_win)
					if confirm == True:
						sql='delete from users where uname =%s'
						val=(uname.get(),)
						cur.execute(sql,val)
						con.commit()
						messagebox.showinfo('','User '+uname.get()+' deleted.',parent=delone_win)
						delone_win.destroy()
					else:
						messagebox.showinfo('','User '+uname.get()+' not deleted.\nThe database has not been modified.',parent=delone_win)
				else:
					messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=delone_win)
			else:
				messagebox.showerror('','Please enter the username.',parent=delone_win)
		
		
		img14=tk.PhotoImage(file='icons/ban_user.png')
		img=tk.Label(delone_win,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(delone_win,text='Delete a user.',font=h1fnt).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

		cur.execute('select uname from users')
		d=cur.fetchall()
		c=[]
		for i in d:
			c.append(i[0])

		tk.Label(delone_win,text='Select a user.',font=fntit).grid(column=1,row=4,padx=10,pady=10,sticky=tk.W)

		n=tk.StringVar()
		uname=ttk.Combobox(delone_win,textvariable=n,font=fnt,width=19)
		uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
		uname['values']=c

		#img13=tk.PhotoImage(file='monoico/icon-694.png')
		delbtn=tk.Button(delone_win,text='Delete',font=fntit,command=deleteuser,fg='red')
		#delbtn.image=img13
		delbtn.grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

	def passwd():
		passwd_win=tk.Toplevel()
		passwd_win.resizable(False,False)
		passwd_win.title('')

		def chpasswd():
			if (not uname.get()=='' and not uname.get().isspace()) and (not npass.get()=='' and not npass.get().isspace()):
				if uname.get() in c:
		
					confirm=messagebox.askyesno('','Do you wish to change the password of '+uname.get()+'?',parent=passwd_win)
					if confirm == True:
						sql='update users set passwd=%s where uname=%s'
						val=(npass.get(),uname.get())
						cur.execute(sql,val)
						con.commit()
						messagebox.showinfo('','Password for '+uname.get()+'\nchanged.',parent=passwd_win)
						passwd_win.destroy()
					else:
						messagebox.showinfo('','Password for '+uname.get()+' has not been changed..\nThe databasehas not\nbeen modified.',parent=passwd_win)
				else:
					messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=passwd_win)
			else:
				messagebox.showerror('','Do not leave any fields blank.',parent=passwd_win)
		
		img14=tk.PhotoImage(file='icons/passwd.png')
		img=tk.Label(passwd_win,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(passwd_win,text='Change password\nfor user',font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

		cur.execute('select uname from users')
		d=cur.fetchall()
		c=[]
		for i in d:
			c.append(i[0])

		n=tk.StringVar()
		tk.Label(passwd_win,text='Username',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
		uname=ttk.Combobox(passwd_win,textvariable=n,font=fnt,width=19)
		uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
		uname['values']=c
		uname.current(0)

		tk.Label(passwd_win,text='New password',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
		npass=tk.Entry(passwd_win,font=fnt,show='*')
		npass.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

		#img13=tk.PhotoImage(file='monoico/icon-694.png')
		subbtn=tk.Button(passwd_win,text='Make changes',font=fntit,command=chpasswd)
		#subbtn.image=img13
		subbtn.grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)

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

							messagebox.showinfo('','The new user '+reg_uname_inp+'\nhas been successfully registered.',parent=regwin)
							regwin.destroy()
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

		#regsubimg=tk.PhotoImage(file='monoico/icon-67.png')	
		regsubmit=tk.Button(regwin,text='Register',command=reguser,font=fntit)
		regsubmit.grid(column=1,row=14,padx=10,pady=10,sticky=tk.W)
		#regsubmit.image=regsubimg

	
	tk.Grid.columnconfigure(manageuserwin,0,weight=1)

	#FRAME 1
	tk.Grid.rowconfigure(manageuserwin,0,weight=1)
	f1=tk.Frame(manageuserwin)
	f1.grid(row=0,column=0,sticky=tk.NSEW)

	#frame 1 grid
	tk.Grid.columnconfigure(f1,0,weight=1)
	tk.Grid.columnconfigure(f1,1,weight=1)

	tk.Grid.rowconfigure(f1,0,weight=1)
	img6=tk.PhotoImage(file='icons/people.png')
	tk.Label(f1,image=img6).grid(column=0,row=0,sticky=tk.E,padx=10,pady=10)
	himg=tk.Label(f1,text=('Manage the users...'),font=h1fnt)
	himg.grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)
	himg.image=img6
	tk.Label(f1,text=('Connected to database: '+con.database),font=('IBM Plex Sans',12),justify=tk.LEFT,fg='green').grid(column=1,row=1,sticky=tk.W,padx=10,pady=10)

	ttk.Separator(f1,orient='horizontal').grid(column=0,row=2,sticky=tk.EW,padx=10,pady=10,columnspan=2)

	#FRAME 2
	tk.Grid.rowconfigure(manageuserwin,1,weight=1)
	f2=tk.Frame(manageuserwin)
	f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

	#frame 2 grid
	tk.Grid.columnconfigure(f2,0,weight=1)
	tk.Grid.columnconfigure(f2,1,weight=1)
	tk.Grid.columnconfigure(f2,2,weight=1)
	tk.Grid.columnconfigure(f2,3,weight=1)

	tk.Label(f2,text='You can:',font=fntit,justify=tk.LEFT).grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

	tk.Grid.rowconfigure(f2,5,weight=1)

	img8=tk.PhotoImage(file='icons/people.png')
	tbviewbtn=tk.Button(f2,text='view all',image=img8,font=fnt,command=viewall)
	tbviewbtn.grid(column=0,row=5,padx=10,pady=10,sticky=tk.E)
	tbviewbtn.image=img8
	tk.Label(f2,text='View all user details.',font=fnt,fg='blue').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

	img10=tk.PhotoImage(file='icons/searchusr.png')
	viewbtn=tk.Button(f2,text='viewone',image=img10,font=fnt,command=viewone)
	viewbtn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
	viewbtn.imageg=img10
	tk.Label(f2,text='View a single user\'s details.',font=fnt).grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)

	tk.Grid.rowconfigure(f2,6,weight=1)

	img7=tk.PhotoImage(file='icons/adduser.png')
	tbviewbtn=tk.Button(f2,text='add',image=img7,font=fnt,command=register)
	tbviewbtn.grid(column=0,row=6,padx=10,pady=10,sticky=tk.E)
	tbviewbtn.image=img7
	tk.Label(f2,text='Add a user.',font=fnt,fg='green').grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

	img11=tk.PhotoImage(file='icons/passwd.png')
	passbtn=tk.Button(f2,text='passwd',image=img11,font=fnt,command=passwd)
	passbtn.grid(column=2,row=6,padx=10,pady=10,sticky=tk.E)
	passbtn.image=img11
	tk.Label(f2,text='Change the password for a user.',font=fnt).grid(column=3,row=6,padx=10,pady=10,sticky=tk.W)

	tk.Grid.rowconfigure(f2,7,weight=1)
	img12=tk.PhotoImage(file='icons/ban_user.png')
	delbtn=tk.Button(f2,text='del',image=img12,font=fnt,command=delone)
	delbtn.grid(column=0,row=7,padx=10,pady=10,sticky=tk.E)
	delbtn.image=img12
	tk.Label(f2,text='Delete a user.',font=fnt,fg='red').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)

	tk.Grid.rowconfigure(f2,8,weight=1)
	tk.Message(f2,text='WARNING: This will delete\na user\'s profile\nfrom the system permanently.',width=500,font=fnt,fg='white',bg='red').grid(column=1,row=8,padx=10,pady=10,sticky=tk.NW)

	#tk.Label(f2,text='or:',font=fntit,justify=tk.LEFT).grid(column=1,row=15,sticky=tk.W,padx=10,pady=10)

	tk.Grid.rowconfigure(f2,16,weight=1)

	tk.Grid.rowconfigure(f2,17,weight=1)

def managedb():		#Manage db
	import mysql.connector as ms
	import tkinter as tk
	import platform as pf
	import ctypes
	from tkinter import ttk
	from tkinter import messagebox
	from tkinter import scrolledtext

	try:
		ctypes.windll.shcore.SetProcessDpiAwareness(True)
	except:
		pass

	#mysql connection
	con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
	cur=con.cursor()

	fnt=('IBM Plex Mono',12)
	fntit=('IBM Plex Mono',12,'italic')
	h1fnt=('IBM Plex Sans',24)
	menufnt=('IBM Plex Mono',11)

	dbmainwin=tk.Toplevel()
	dbmainwin.title('Database Manager')
	#w,h=dbmainwin.winfo_screenwidth(),dbmainwin.winfo_screenheight()
	#dbmainwin.geometry(str(w)+'x'+str(h))

	cur.execute('show tables')			#creating list of available tables for dropbox
	a=cur.fetchall()
	#print(a)
	b=[]
	for i in a:
		b.append(i[0])

	def showtb():

		if not table.get()=='' and not table.get().isspace():
			dbwin=tk.Toplevel()
			dbwin.resizable(False,False)
			dbwin.title(table.get()+' table')
			sql=str('show columns from '+table.get())		#getting headers for table
			#print(sql)
			cur.execute(sql)
			a=cur.fetchall()
			b=[]
			for x in a:									
				b.append(x[0])
				header=tuple(b)

			sql2=str('select * from '+table.get())			#getting data from table
			#print(sql2)
			cur.execute(sql2)
			e=[header]+cur.fetchall()						#appending header to data
			#print(e)
		
			rows=len(e)
			cols=len(e[0])

			for i in range(rows):							#drawing the table in GUI
				for j in range(cols):
					entry = tk.Label(dbwin,borderwidth=1,relief='solid',height=2,font=fnt,padx=10)
					entry.grid(row=i, column=j,padx=2,pady=2,sticky=tk.EW)
					entry.configure(text=e[i][j])
					if i==0:
						entry.configure(fg='red',font=fntit)	#colors and italicises header
		else:
			messagebox.showerror('Error','Please choose a table.',parent=dbmainwin)

	def droptb():
		if not table.get()=='' and not table.get().isspace():
			messagebox.showwarning('WARNING','The table chosen will be dropped\nfrom the database permanently.\nContinue?',parent=dbmainwin)
			confirm=messagebox.askyesno('','Do you wish to drop the table \''+table.get()+'\'\nalong with its contents ?',parent=dbmainwin)
			if confirm == True:
				sql=str('drop table '+table.get())
				cur.execute(sql)
				con.commit()
				messagebox.showinfo('','The table \''+table.get()+'\'\nhas been dropped\nfrom the database.',parent=dbmainwin)
			else:
				messagebox.showinfo('','DROP TABLE operation on \''+table.get()+'\' cancelled.\nThe database has not been modified.',parent=dbmainwin)
				pass
		else:
			messagebox.showerror('Error','Please choose a table.',parent=dbmainwin)

	def deltb():
		if not table.get()=='' and not table.get().isspace():
			messagebox.showwarning('WARNING','All the contents of the table chosen will be deleted permanently.\nContinue?',parent=dbmainwin)
			confirm=messagebox.askyesno('','Do you wish to delete\nall records from the table \''+table.get()+'\'?',parent=dbmainwin)
			if confirm == True:
				sql=str('delete from '+table.get())
				cur.execute(sql)
				con.commit()
				messagebox.showinfo('','All records in table \''+table.get()+'\'\nhave been permenantly deleted\nfrom the database.',parent=dbmainwin)
			else:
				messagebox.showinfo('','DELETE FROM TABLE operation on \''+table.get()+'\' cancelled.\nThe database has not been modified.',parent=dbmainwin)
				pass
		else:
			messagebox.showerror('Error','Please choose a table.',parent=dbmainwin)

	def help():
		helpwin=tk.Toplevel()
		helpwin.resizable(False,False)
		helpwin.title('')

		img14=tk.PhotoImage(file='icons/help.png')
		img=tk.Label(helpwin,image=img14)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14
		
		tk.Label(helpwin,text='What is the difference between\n\'deleting from\' and \'dropping\' a table?',font=h1fnt,justify=tk.LEFT).grid(row=0,column=1,padx=10,pady=10,sticky=tk.W)
		txt=''''Deleting' from a table performs the SQL DELETE FROM
operation, which, by default, deletes all records
from the table, whilst keeping the table structure
intact.

On the other hand, 'dropping' a table performs the
SQL DROP TABLE deletes the table structure from the
database along with its contents.'''

		a=scrolledtext.ScrolledText(helpwin,wrap=tk.WORD,width=30,height=10,font=fnt)
		a.grid(row=3,column=1,padx=10,pady=10,sticky=tk.EW)
		a.insert(tk.INSERT,txt)
		a.configure(state='disabled')

	menubar=tk.Menu(dbmainwin)

	user=tk.Menu(menubar,tearoff=0)
	menubar.add_cascade(label='Help',menu=user,font=menufnt)

	user.add_command(label='DELETE FROM vs DROP table',command=help,font=menufnt,underline=0)

	dbmainwin.config(menu=menubar)
		
	tk.Grid.columnconfigure(dbmainwin,0,weight=1)

	#FRAME 1
	tk.Grid.rowconfigure(dbmainwin,0,weight=1)
	f1=tk.Frame(dbmainwin)
	f1.grid(row=0,column=0,sticky=tk.NSEW)

	#frame 1 grid
	tk.Grid.columnconfigure(f1,0,weight=1)
	tk.Grid.columnconfigure(f1,1,weight=1)

	tk.Grid.rowconfigure(f1,0,weight=1)
	
	img6=tk.PhotoImage(file='icons/dataset.png')
	himg=tk.Label(f1,image=img6)
	himg.grid(column=0,row=0,padx=10,pady=10,sticky=tk.E)
	himg.image=img6

	tk.Label(f1,text=('Manage the databases...'),font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)
	tk.Grid.rowconfigure(f1,1,weight=1)
	tk.Label(f1,text=('Connected to database: '+con.database),font=('IBM Plex Sans',12),justify=tk.LEFT,fg='green').grid(column=1,row=1,sticky=tk.W,padx=10,pady=1)
	ttk.Separator(f1,orient='horizontal').grid(column=0,row=2,sticky=tk.EW,padx=10,pady=10,columnspan=2)
	#FRAME 2
	tk.Grid.rowconfigure(dbmainwin,1,weight=1)
	f2=tk.Frame(dbmainwin)
	f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

	#frame 2 grid
	tk.Grid.columnconfigure(f2,0,weight=1)
	tk.Grid.columnconfigure(f2,1,weight=1)
	tk.Grid.columnconfigure(f2,2,weight=1)
	tk.Grid.columnconfigure(f2,3,weight=1)

	#tk.Grid.rowconfigure(f2,4,weight=1)
	tk.Label(f2,text='Choose a table.',font=fntit,justify=tk.LEFT).grid(column=1,row=4,sticky=tk.W,padx=10,pady=10)
	img7=tk.PhotoImage(file='icons/table.png')
	h2img=tk.Label(f2,image=img7)
	h2img.grid(column=0,row=4,sticky=tk.E,padx=10,pady=10)
	h2img.image=img7

	tk.Grid.rowconfigure(f2,5,weight=1)
	n=tk.StringVar()
	table=ttk.Combobox(f2,textvariable=n,font=fnt)
	table.grid(row=5,column=1,padx=10,pady=10,sticky=tk.EW)
	table['values']=b

	tk.Label(f2,text='You can:',font=fntit,justify=tk.LEFT).grid(column=1,row=6,sticky=tk.W,padx=10,pady=10)

	tk.Grid.rowconfigure(f2,7,weight=1)
	img8=tk.PhotoImage(file='icons/preview.png')
	tbviewbtn=tk.Button(f2,text='viewtable',image=img8,font=fnt,command=showtb)
	tbviewbtn.grid(column=0,row=7,padx=10,pady=10,sticky=tk.E)
	tbviewbtn.image=img8
	tk.Label(f2,text='View the table.',font=fnt,fg='blue').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)

	tk.Grid.rowconfigure(f2,8,weight=1)
	img10=tk.PhotoImage(file='icons/delete.png')
	deltbbtn=tk.Button(f2,text='deltable',image=img10,font=fnt,command=deltb)
	deltbbtn.grid(column=0,row=8,padx=10,pady=10,sticky=tk.E)
	deltbbtn.image=img10
	tk.Label(f2,text='Delete all the contents\nof the table.',font=fnt,justify=tk.LEFT).grid(column=1,row=8,padx=10,pady=10,sticky=tk.W)
	tk.Grid.rowconfigure(f2,9,weight=1)
	tk.Message(f2,text='WARNING:\nThis will delete all the contents of the table chosen permanently.',font=fnt,fg='white',bg='orange').grid(column=1,row=9,padx=10,sticky=tk.NW)

	img11=tk.PhotoImage(file='icons/remove.png')
	drptbbtn=tk.Button(f2,text='droptable',image=img11,font=fnt,command=droptb)
	drptbbtn.grid(column=2,row=8,padx=10,pady=10,sticky=tk.E)
	drptbbtn.image=img11
	tk.Label(f2,text='Drop the table.',font=fnt,fg='red').grid(column=3,row=8,padx=10,pady=10,sticky=tk.W)
	tk.Message(f2,text='WARNING:\nThis will drop the table chosen\nand its contents permanently.',font=fnt,fg='white',bg='red').grid(column=3,row=9,padx=10,sticky=tk.NW)