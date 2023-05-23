def manage_admin():	#Manage admins
	import mysql.connector as ms
	import tkinter as tk
	import platform as pf
	import ctypes
	from tkinter import ttk
	from tkinter import messagebox
	import random as rd
	
	#Enables DPI scaling on supported versions of Windows
	if pf.system()=='Windows':
		try:
			ctypes.windll.shcore.SetProcessDpiAwareness(True)
		except:
			pass
	
	#MySQL connection
	con=ms.connect(host='localhost',user='root',password='123456',database='taxi')
	cur=con.cursor()

	#Fonts
	fnt=('IBM Plex Mono',12)
	fntit=('IBM Plex Mono',12,'italic')
	h1fnt=('IBM Plex Sans',24)

	#Creating Toplevel window
	manageadminwin=tk.Toplevel()
	manageadminwin.title('Administrator Manager')

	def viewall():	#Show all Administrators
		viewall_win=tk.Toplevel()
		viewall_win.title('All administrators')
		viewall_win.resizable(False,False)
		
		header=('Admin ID','Admin Username','Admin Name','Admin Password')

		sql2=str('select * from admin')			#getting data from table
		cur.execute(sql2)
		data=[header]+cur.fetchall()						#appending header to data
		
		rows=len(data)
		cols=len(data[0])

		for i in range(rows):							#drawing the table in GUI
			for j in range(cols):
				entry = tk.Label(viewall_win,borderwidth=1,relief='solid',padx=10,height=2,font=fnt)
				entry.grid(row=i, column=j,padx=2,pady=2,sticky=tk.EW)
				entry.configure(text=data[i][j])
				if i==0:
					entry.configure(fg='red',font=fntit)	#colors and italicises header

	def viewone():	#View details of administrator
		def getadmninfo():	#Gets data from DB

			if not uname.get()=='' and not uname.get().isspace():
				if uname.get() in admin_list:
					sql='select * from admin where admin_uname=%s'
					val=(uname.get(),)
					cur.execute(sql,val)
					c=cur.fetchall()
					admin_id=c[0][0]
					admin_uname=c[0][1]
					admin_name=c[0][2]
					admin_passwd=c[0][3]
					
					data=[('Administrator ID',admin_id),('Administrator Username',admin_uname),('Administrator Full Name',admin_name),('Administrator Password',admin_passwd)]
					
					rows=len(data)
					cols=len(data[0])
					tk.Label(frame3,font=fntit,text='Data').grid(row=0,column=0,sticky=tk.W)
					for i in range(rows):							#drawing the table in GUI
						for j in range(cols):
							entry = tk.Label(frame2,borderwidth=1,relief='solid',padx=10,width=30,height=2,font=fnt)
							entry.grid(row=i,column=j,padx=2,pady=2,sticky=tk.EW)
							entry.configure(text=data[i][j])
							if j==0:
								entry.configure(fg='red',font=fntit) #colors and italicises header
				else:
					messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=viewone_win)
			else:
				messagebox.showerror('Error','Please enter the administrator username.',parent=viewone_win)
		
		#Creating Toplevel window
		viewone_win=tk.Toplevel()
		viewone_win.title('View admin details')
		viewone_win.resizable(False,False)
		
		#Dividing window into frames
		frame1=tk.Frame(viewone_win)
		frame1.grid(row=0,column=0,padx=10,pady=10,sticky=tk.EW)

		frame2=tk.Frame(viewone_win)
		frame2.grid(row=2,column=0,padx=10,pady=10,sticky=tk.EW)

		frame3=tk.Frame(viewone_win)
		frame3.grid(row=1,column=0,padx=10,pady=10,sticky=tk.W)

		#Creates list of admins for dropdown
		cur.execute('select admin_uname from admin')
		a=cur.fetchall()
		admin_list=[]
		for i in a:
			admin_list.append(i[0])

		img14=tk.PhotoImage(file='icons/searchusr.png')
		img=tk.Label(frame1,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(frame1,font=h1fnt,text='View administrator details').grid(row=0,column=1,padx=10,pady=10,sticky=tk.W)

		tk.Label(frame1,font=fnt,text='Enter username of administrator.').grid(row=4,column=1,padx=10,pady=10,sticky=tk.W)
		n=tk.StringVar()
		uname=ttk.Combobox(frame1,textvariable=n,font=fnt)
		uname.grid(row=5,column=1,padx=10,pady=10,sticky=tk.EW)
		uname['values']=admin_list
		
		submit=tk.Button(frame1,font=fntit,text='Submit',command=getadmninfo)
		submit.grid(row=5,column=2,padx=10,pady=10)
		
		#Binds Enter key to submit function
		viewone_win.bind('<Return>',lambda event:getadmninfo())

	def delone():	#Deletes an administrator.
		
		delone_win=tk.Toplevel()
		delone_win.resizable(False,False)
		delone_win.title('Delete adminstrator')
		
		#Creates list of admins and respective full names.
		cur.execute('select admin_uname,admin_name from admin')
		a=cur.fetchall()
		admin_namelist=dict(a)

		def delete_admin():		#Delets from DB.
			if not uname.get()=='' and not uname.get().isspace():
				if uname.get() in admin_list:
					messagebox.showwarning('','This operation will delete\nthe username of the administrator permanently.\nContinue?',parent=delone_win)
					confirm=messagebox.askyesno('','Do you wish to delete the administrator '+admin_namelist[uname.get()]+'?',parent=delone_win)
					if confirm == True:
						sql='delete from admin where admin_uname =%s'
						val=(uname.get(),)
						cur.execute(sql,val)
						con.commit()
						messagebox.showinfo('','Administrator '+admin_namelist[uname.get()]+' deleted.',parent=delone_win)
						delone_win.destroy()
					else:
						messagebox.showinfo('','Administrator '+admin_namelist[uname.get()]+' not deleted.\nThe database has not been modified.',parent=delone_win)
				else:
					messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=delone_win)
			else:
				messagebox.showerror('','Please enter the administrator username.',parent=delone_win)
		
		img14=tk.PhotoImage(file='icons/ban_user.png')
		img=tk.Label(delone_win,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(delone_win,text='Delete an administrator...',font=h1fnt).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

		cur.execute('select admin_uname from admin')
		d=cur.fetchall()
		admin_list=[]
		for i in d:
			admin_list.append(i[0])

		tk.Label(delone_win,text='Select an administrator.',font=fntit).grid(column=1,row=4,padx=10,pady=10,sticky=tk.W)

		n=tk.StringVar()
		uname=ttk.Combobox(delone_win,textvariable=n,font=fnt,width=19)
		uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
		uname['values']=admin_list

		delbtn=tk.Button(delone_win,text='Delete',font=fntit,command=delete_admin,fg='red')
		delbtn.grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

		#Binds Enter key to submit function.
		delone_win.bind('<Return>',lambda event:delete_admin())

	def passwd():	#Change password for administrator currently logged in
		
		passwd_win=tk.Toplevel()
		passwd_win.resizable(False,False)
		passwd_win.title('Change password for administrator')

		cur.execute('select admin_uname,admin_name from admin')
		a=cur.fetchall()
		admin_namelist=dict(a)

		def change_admin_passwd():	#Changes admin password in DB
			if (not uname.get()=='' and not uname.get().isspace()) and (not npass.get()=='' and not npass.get().isspace()):
				if uname.get() in admin_list:
		
					confirm=messagebox.askyesno('','Do you wish to change the password of '+admin_namelist[uname.get()]+'?',parent=passwd_win)
					if confirm == True:
						sql='update admin set admin_passwd=%s where admin_uname=%s'
						val=(npass.get(),uname.get())
						cur.execute(sql,val)
						con.commit()
						messagebox.showinfo('','Password for '+admin_namelist[uname.get()]+'\nchanged.',parent=passwd_win)
						passwd_win.destroy()
					else:
						messagebox.showinfo('','Password for '+admin_namelist[uname.get()]+' has not been changed..\nThe databasehas not\nbeen modified.',parent=passwd_win)
				else:
					messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=passwd_win)
			else:
				messagebox.showerror('','Do not leave any fields blank.',parent=passwd_win)
		
		img14=tk.PhotoImage(file='icons/passwd.png')
		img=tk.Label(passwd_win,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(passwd_win,text='Change password\nfor administrator...',font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

		cur.execute('select admin_uname from admin')
		d=cur.fetchall()
		admin_list=[]
		for i in d:
			admin_list.append(i[0])

		n=tk.StringVar()
		tk.Label(passwd_win,text='Username',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
		uname=ttk.Combobox(passwd_win,textvariable=n,font=fnt,width=19)
		uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
		uname['values']=admin_list
		uname.current(0)

		tk.Label(passwd_win,text='New password',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
		npass=tk.Entry(passwd_win,font=fnt,show='*')
		npass.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

		subbtn=tk.Button(passwd_win,text='Make changes',font=fntit,command=change_admin_passwd)
		subbtn.grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)
		passwd_win.bind('<Return>',lambda event:change_admin_passwd())

	def add():	#Register a new administrator.
		
		add_win=tk.Toplevel()
		add_win.resizable(False,False)
		add_win.title('Add administrator')

		def add_admin():	#Adds admin in DB
			uname_inp=uname.get().lower()
			fname_inp=fname.get()
			passwd_inp=passwd.get()

			cur.execute('select admin_uname from admin')
			a=cur.fetchall()
			admin_list=[]
			for i in a:
				admin_list.append(i[0])

			if (not uname_inp=='' and not uname_inp.isspace()) and (not fname_inp=='' and not fname_inp.isspace()) and (not passwd_inp=='' and not passwd_inp.isspace()):
				if uname_inp not in admin_list:
					sql='insert into admin values (%s,%s,%s,%s)'
					val=(id,uname_inp,fname_inp,passwd_inp)
					cur.execute(sql,val)
					con.commit()
					messagebox.showinfo('','Administrator '+fname_inp+' registered successfully.',parent=add_win)
					add_win.destroy()
				else:
					messagebox.showerror('Error','Username \''+uname_inp+'\'\nalready exists.',parent=add_win)			
			else:
				messagebox.showerror('Error','Please do not leave any fields blank.',parent=add_win)
		
		id='A'+str(rd.randint(1000,9999))

		img14=tk.PhotoImage(file='icons/adduser.png')
		img=tk.Label(add_win,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(add_win,text='Register administrator...',font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)

		tk.Label(add_win,text='UID',font=fnt).grid(column=0,row=3,sticky=tk.E,padx=10,pady=10)
		bkgid=tk.Label(add_win,text=id,font=fnt)
		bkgid.grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

		#Input fields
		tk.Label(add_win,text='Full Name',font=fnt).grid(column=0,row=4,sticky=tk.E,padx=10,pady=10)
		fname=tk.Entry(add_win,font=fnt)
		fname.grid(column=1,row=4,sticky=tk.EW,padx=10,pady=10)

		tk.Label(add_win,text='Username',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
		uname=tk.Entry(add_win,font=fnt)
		uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)

		tk.Label(add_win,text='Password',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
		passwd=tk.Entry(add_win,font=fnt,show='*')
		passwd.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

		subbtn=tk.Button(add_win,font=fntit,text='Register',command=add_admin)
		subbtn.grid(column=1,row=12,padx=10,pady=10,sticky=tk.W)

		#Binds Enter to submit function.
		add_win.bind('<Return>',lambda event:add_admin())

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

	tk.Grid.rowconfigure(f2,16,weight=1)

def manage_agents():	#Manage agents (employees)
	import mysql.connector as ms
	import tkinter as tk
	import platform as pf
	import ctypes
	from tkinter import ttk
	from tkinter import messagebox
	import random as rd

	#Enables DPI scaling on supported versions of Windows
	if pf.system()=='Windows':
		try:
			ctypes.windll.shcore.SetProcessDpiAwareness(True)
		except:
			pass
	
	#MySQL connection
	con=ms.connect(host='localhost',user='root',password='123456',database='taxi')
	cur=con.cursor()

	#Fonts for GUI
	fnt=('IBM Plex Mono',12)
	fntit=('IBM Plex Mono',12,'italic')
	h1fnt=('IBM Plex Sans',24)

	#Creating Toplevel window
	manage_agentwin=tk.Toplevel()
	manage_agentwin.title('Agent Manager')

	def viewall():	#View all Agent

		viewall_win=tk.Toplevel()
		viewall_win.title('All Agents')
		viewall_win.resizable(False,False)
		
		#Headers for table
		header=('Agent ID','Agent Username','Agent Name','Agent Password')

		sql2=str('select * from employees')			
		cur.execute(sql2)
		data=[header]+cur.fetchall()						#appending header to data
		
		rows=len(data)
		cols=len(data[0])

		for i in range(rows):							#drawing the table in GUI
			for j in range(cols):
				entry = tk.Label(viewall_win,borderwidth=1,relief='solid',padx=10,height=2,font=fnt)
				entry.grid(row=i, column=j,padx=2,pady=2,sticky=tk.EW)
				entry.configure(text=data[i][j])
				if i==0:
					entry.configure(fg='red',font=fntit)	#colors and italicises header

	def viewone():	#Show an agent's info
		def getagentinfo():	#Gets data from DB

			if not uname.get()=='' and not uname.get().isspace():
				if uname.get() in agent_list:
					sql='select * from employees where emp_uname=%s'
					val=(uname.get(),)
					cur.execute(sql,val)
					c=cur.fetchall()
					agent_id=c[0][0]
					agent_uname=c[0][1]
					agent_name=c[0][2]
					agent_passwd=c[0][3]
					
					e=[('Agent ID',agent_id),('Agent Username',agent_uname),('Agent Full Name',agent_name),('Agent Password',agent_passwd)]
					
					
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
				messagebox.showerror('Error','Please enter the agent username.',parent=viewone_win)
		viewone_win=tk.Toplevel()
		viewone_win.title('View agent details')
		viewone_win.resizable(False,False)
		
		frame1=tk.Frame(viewone_win)
		frame1.grid(row=0,column=0,padx=10,pady=10,sticky=tk.EW)

		frame2=tk.Frame(viewone_win)
		frame2.grid(row=2,column=0,padx=10,pady=10,sticky=tk.EW)

		frame3=tk.Frame(viewone_win)
		frame3.grid(row=1,column=0,padx=10,pady=10,sticky=tk.W)

		#Creating list of agent
		cur.execute('select emp_uname from employees')
		a=cur.fetchall()
		agent_list=[]
		for i in a:
			agent_list.append(i[0])

		img14=tk.PhotoImage(file='icons/searchusr.png')
		img=tk.Label(frame1,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(frame1,font=h1fnt,text='View agent details').grid(row=0,column=1,padx=10,pady=10,sticky=tk.W)

		tk.Label(frame1,font=fnt,text='Enter username of agent.').grid(row=4,column=1,padx=10,pady=10,sticky=tk.W)
		n=tk.StringVar()
		uname=ttk.Combobox(frame1,textvariable=n,font=fnt)
		uname.grid(row=5,column=1,padx=10,pady=10,sticky=tk.EW)
		uname['values']=agent_list
		
		submit=tk.Button(frame1,font=fntit,text='Submit',command=getagentinfo)
		submit.grid(row=5,column=2,padx=10,pady=10)

		#Binds Enter to submit function.
		viewone_win.bind('<Return>',lambda event:getagentinfo())

	def delone():	#Delete an agent
		delone_win=tk.Toplevel()
		delone_win.resizable(False,False)
		delone_win.title('Delete agent')
		cur.execute('select emp_uname,emp_name from employees')
		a=cur.fetchall()
		agent_namelist=dict(a)
		def delete_agent():	#Delete agent from db
			if not uname.get()=='' and not uname.get().isspace():
				if uname.get() in agent_list:
					messagebox.showwarning('','This operation will delete\nthe profile of the agent permanently.\nContinue?',parent=delone_win)
					confirm=messagebox.askyesno('','Do you wish to delete the agent '+agent_namelist[uname.get()]+'?',parent=delone_win)
					if confirm == True:
						sql='delete from employees where emp_uname =%s'
						val=(uname.get(),)
						cur.execute(sql,val)
						con.commit()
						messagebox.showinfo('','Agent '+agent_namelist[uname.get()]+' deleted.',parent=delone_win)
						delone_win.destroy()
					else:
						messagebox.showinfo('','Agent '+agent_namelist[uname.get()]+' not deleted.\nThe database has not been modified.',parent=delone_win)
				else:
					messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=delone_win)
			else:
				messagebox.showerror('','Please enter the agent username.',parent=delone_win)
		
		img14=tk.PhotoImage(file='icons/ban_user.png')
		img=tk.Label(delone_win,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(delone_win,text='Delete an agent...',font=h1fnt).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

		cur.execute('select emp_uname from employees')
		d=cur.fetchall()
		agent_list=[]
		for i in d:
			agent_list.append(i[0])

		tk.Label(delone_win,text='Select an agent.',font=fntit).grid(column=1,row=4,padx=10,pady=10,sticky=tk.W)

		n=tk.StringVar()
		uname=ttk.Combobox(delone_win,textvariable=n,font=fnt,width=19)
		uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
		uname['values']=agent_list

		delbtn=tk.Button(delone_win,text='Delete',font=fntit,command=delete_agent,fg='red')
		delbtn.grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)
		delone_win.bind('<Return>',lambda event:delete_agent())

	def passwd():	#Change password for agent
		passwd_win=tk.Toplevel()
		passwd_win.resizable(False,False)
		passwd_win.title('Change password for employee')

		cur.execute('select emp_uname,emp_name from employees')
		a=cur.fetchall()
		agent_namelist=dict(a)
		def change_emp_passwd():	#Changes agent passwd in DB
			if (not uname.get()=='' and not uname.get().isspace()) and (not npass.get()=='' and not npass.get().isspace()):
				if uname.get() in agent_list:
		
					confirm=messagebox.askyesno('','Do you wish to change the password of '+agent_namelist[uname.get()]+'?',parent=passwd_win)
					if confirm == True:
						sql='update employees set emp_passwd=%s where emp_uname=%s'
						val=(npass.get(),uname.get())
						cur.execute(sql,val)
						con.commit()
						messagebox.showinfo('','Password for '+agent_namelist[uname.get()]+'\nchanged.',parent=passwd_win)
						passwd_win.destroy()
					else:
						messagebox.showinfo('','Password for '+agent_namelist[uname.get()]+' has not been changed..\nThe databasehas not\nbeen modified.',parent=passwd_win)
				else:
					messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=passwd_win)
			else:
				messagebox.showerror('','Do not leave any fields blank.',parent=passwd_win)
		
		img14=tk.PhotoImage(file='icons/passwd.png')
		img=tk.Label(passwd_win,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(passwd_win,text='Change password\nfor agent...',font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

		cur.execute('select emp_uname from employees')
		d=cur.fetchall()
		agent_list=[]
		for i in d:
			agent_list.append(i[0])

		n=tk.StringVar()
		tk.Label(passwd_win,text='Username',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
		uname=ttk.Combobox(passwd_win,textvariable=n,font=fnt,width=19)
		uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
		uname['values']=agent_list
		uname.current(0)

		tk.Label(passwd_win,text='New password',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
		npass=tk.Entry(passwd_win,font=fnt,show='*')
		npass.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

		subbtn=tk.Button(passwd_win,text='Make changes',font=fntit,command=change_emp_passwd)
		subbtn.grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)
		passwd_win.bind('<Return>',lambda event:change_emp_passwd())

	def add():	#Add an agent.
		add_win=tk.Toplevel()
		add_win.resizable(False,False)
		add_win.title('Add agent')

		def add_agent():	#Adds agent to DB.
			uname_inp=uname.get().lower()
			fname_inp=fname.get()
			passwd_inp=passwd.get()
			
			#Creates list of employees
			cur.execute('select emp_uname from employees')
			a=cur.fetchall()
			agent_list=[]
			for i in a:
				agent_list.append(i[0])

			if (not uname_inp=='' and not uname_inp.isspace()) and (not fname_inp=='' and not fname_inp.isspace()) and (not passwd_inp=='' and not passwd_inp.isspace()):
				if uname_inp not in agent_list:
					sql='insert into employees values (%s,%s,%s,%s)'
					val=(id,uname_inp,fname_inp,passwd_inp)
					cur.execute(sql,val)
					con.commit()
					messagebox.showinfo('','Agent '+fname_inp+' registered successfully.',parent=add_win)
					add_win.destroy()
				else:
					messagebox.showerror('Error','Username \''+uname_inp+'\'\nalready exists.',parent=add_win)
			else:
				messagebox.showerror('Error','Please do not leave any fields blank.',parent=add_win)
		
		id='E'+str(rd.randint(1000,9999))

		img14=tk.PhotoImage(file='icons/adduser.png')
		img=tk.Label(add_win,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(add_win,text='Register agent...',font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)

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

		subbtn=tk.Button(add_win,font=fntit,text='Register',command=add_agent)
		subbtn.grid(column=1,row=12,padx=10,pady=10,sticky=tk.W)

		add_win.bind('<Return>',lambda event:add_agent())


	tk.Grid.columnconfigure(manage_agentwin,0,weight=1)

	#FRAME 1
	tk.Grid.rowconfigure(manage_agentwin,0,weight=1)
	f1=tk.Frame(manage_agentwin)
	f1.grid(row=0,column=0,sticky=tk.NSEW)

	#frame 1 grid
	tk.Grid.columnconfigure(f1,0,weight=1)
	tk.Grid.columnconfigure(f1,1,weight=1)

	tk.Grid.rowconfigure(f1,0,weight=1)
	img6=tk.PhotoImage(file='icons/employee.png')
	himg=tk.Label(f1,image=img6)
	himg.grid(column=0,row=0,sticky=tk.E,padx=10,pady=10)
	himg.image=img6
	tk.Label(f1,text=('Manage the agents...'),font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)

	tk.Label(f1,text=('Connected to database: '+con.database),font=('IBM Plex Sans',12),justify=tk.LEFT,fg='green').grid(column=1,row=1,sticky=tk.W,padx=10,pady=10)
	ttk.Separator(f1,orient='horizontal').grid(column=0,row=2,sticky=tk.EW,padx=10,pady=10,columnspan=2)
	#FRAME 2
	tk.Grid.rowconfigure(manage_agentwin,1,weight=1)
	f2=tk.Frame(manage_agentwin)
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
	tk.Label(f2,text='View all agent details.',font=fnt,fg='blue').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

	img10=tk.PhotoImage(file='icons/searchusr.png')
	viewbtn=tk.Button(f2,text='viewone',image=img10,font=fnt,command=viewone)
	viewbtn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
	viewbtn.image=img10
	tk.Label(f2,text='View a single agent\'s details.',font=fnt).grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)

	tk.Grid.rowconfigure(f2,6,weight=1)
	img7=tk.PhotoImage(file='icons/adduser.png')
	tbviewbtn=tk.Button(f2,text='add',image=img7,font=fnt,command=add)
	tbviewbtn.grid(column=0,row=6,padx=10,pady=10,sticky=tk.E)
	tbviewbtn.image=img7
	tk.Label(f2,text='Register an agent.',font=fnt,fg='green').grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

	img11=tk.PhotoImage(file='icons/passwd.png')
	passbtn=tk.Button(f2,text='passwd',image=img11,font=fnt,command=passwd)
	passbtn.grid(column=2,row=6,padx=10,pady=10,sticky=tk.E)
	passbtn.image=img11
	tk.Label(f2,text='Change the password for an agent.',font=fnt).grid(column=3,row=6,padx=10,pady=10,sticky=tk.W)

	tk.Grid.rowconfigure(f2,7,weight=1)
	img12=tk.PhotoImage(file='icons/deluser.png')
	delbtn=tk.Button(f2,text='del',image=img12,font=fnt,command=delone)
	delbtn.grid(column=0,row=7,padx=10,pady=10,sticky=tk.E)
	delbtn.image=img12
	tk.Label(f2,text='Delete an agent.',font=fnt,fg='red').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)
	tk.Grid.rowconfigure(f2,8,weight=1)
	tk.Message(f2,text='WARNING: This will delete\nan agent\'s profile\nfrom the system permanently.',width=500,font=fnt,fg='white',bg='red').grid(column=1,row=8,padx=10,pady=10,sticky=tk.NW)

	tk.Grid.rowconfigure(f2,16,weight=1)
	
def manage_users():	#Manage users
	import mysql.connector as ms
	import tkinter as tk
	import platform as pf
	import ctypes
	from tkinter import ttk
	from tkinter import messagebox
	import random as rd

	#Enables DPI scaling on supported versions of Windows
	if pf.system()=='Windows':
		try:
			ctypes.windll.shcore.SetProcessDpiAwareness(True)
		except:
			pass

	con=ms.connect(host='localhost',user='root',password='123456',database='taxi')
	cur=con.cursor()

	fnt=('IBM Plex Mono',12)
	fntit=('IBM Plex Mono',12,'italic')
	h1fnt=('IBM Plex Sans',24)

	manageuserwin=tk.Toplevel()
	manageuserwin.title('User Manager')


	def viewall():		#View all users
		viewall_win=tk.Toplevel()
		viewall_win.title('All users')
		viewall_win.resizable(False,False)
		
		header=('User ID','Full Name','Electronic Mail','Number','Username','Password')

		sql2=str('select * from users')	

		cur.execute(sql2)
		data=[header]+cur.fetchall()						#appending header to data
		
		rows=len(data)
		cols=len(data[0])

		for i in range(rows):							#drawing the table in GUI
			for j in range(cols):
				entry = tk.Label(viewall_win,borderwidth=1,relief='solid',padx=10,height=2,font=fnt)
				entry.grid(row=i,column=j,padx=2,pady=2,sticky=tk.EW)
				entry.configure(text=data[i][j])
				if i==0:
					entry.configure(fg='red',font=fntit)	#colors and italicises header

	def viewone():	#view single user

		def getuserinfo():	#gets user info from DB

			if not uname.get()=='' and not uname.get().isspace():
				if uname.get() in user_list:
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
					
					data=[('User ID',user_id),('Full Name',user_fname),('Electronic Mail',user_email),('Phone Number',user_num),('Username',user_uname),('Password',user_passwd)]
					
					rows=len(data)
					cols=len(data[0])
					tk.Label(frame3,font=fntit,text='Data').grid(row=0,column=0,sticky=tk.W)
					for i in range(rows):							#drawing the table in GUI
						for j in range(cols):
							entry = tk.Label(frame2,borderwidth=1,relief='solid',padx=10,height=2,width=25,font=fnt)
							entry.grid(row=i,column=j,padx=2,pady=2,sticky=tk.EW)
							entry.configure(text=data[i][j])
							if j==0:
								entry.configure(fg='red',font=fntit,width=15) #colors and italicises header
				else:
					messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=viewone_win)
			else:
				messagebox.showerror('Error','Please enter the username.',parent=viewone_win)
		
		viewone_win=tk.Toplevel()
		viewone_win.title('View user details')
		viewone_win.resizable(False,False)
		
		frame1=tk.Frame(viewone_win)
		frame1.grid(row=0,column=0,padx=10,pady=10,sticky=tk.EW)

		frame2=tk.Frame(viewone_win)
		frame2.grid(row=2,column=0,padx=10,pady=10,sticky=tk.EW)

		frame3=tk.Frame(viewone_win)
		frame3.grid(row=1,column=0,padx=10,pady=10,sticky=tk.W)

		cur.execute('select uname from users')
		a=cur.fetchall()
		user_list=[]
		for i in a:
			user_list.append(i[0])

		img14=tk.PhotoImage(file='icons/searchusr.png')
		img=tk.Label(frame1,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(frame1,font=h1fnt,text='View user details').grid(row=0,column=1,padx=10,pady=10,sticky=tk.W)

		tk.Label(frame1,font=fnt,text='Enter username.').grid(row=4,column=1,padx=10,pady=10,sticky=tk.W)
		n=tk.StringVar()
		uname=ttk.Combobox(frame1,textvariable=n,font=fnt)
		uname.grid(row=5,column=1,padx=10,pady=10,sticky=tk.EW)
		uname['values']=user_list
		
		submit=tk.Button(frame1,font=fntit,text='Submit',command=getuserinfo)
		submit.grid(row=5,column=2,padx=10,pady=10)
		
		#Binds Enter to submit function.
		viewone_win.bind('<Return>',lambda event:getuserinfo())

	def delone():	#delete user
		delone_win=tk.Toplevel()
		delone_win.resizable(False,False)
		delone_win.title('Delete user')

		def delete_user(): #deletes user from DB.
			
			if not uname.get()=='' and not uname.get().isspace():
				if uname.get() in users_list:
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
		users_list=[]
		for i in d:
			users_list.append(i[0])

		tk.Label(delone_win,text='Select a user.',font=fntit).grid(column=1,row=4,padx=10,pady=10,sticky=tk.W)

		n=tk.StringVar()
		uname=ttk.Combobox(delone_win,textvariable=n,font=fnt,width=19)
		uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
		uname['values']=users_list

		delbtn=tk.Button(delone_win,text='Delete',font=fntit,command=delete_user,fg='red')
		delbtn.grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)
		delone_win.bind('<Return>',lambda event:delete_user())

	def passwd():	#changes password for user
		passwd_win=tk.Toplevel()
		passwd_win.resizable(False,False)
		passwd_win.title('Change password for user')

		def ch_user_passwd():	#changes password in db
			if (not uname.get()=='' and not uname.get().isspace()) and (not npass.get()=='' and not npass.get().isspace()):
				if uname.get() in users_list:
		
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
		users_list=[]
		for i in d:
			users_list.append(i[0])

		n=tk.StringVar()
		tk.Label(passwd_win,text='Username',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
		uname=ttk.Combobox(passwd_win,textvariable=n,font=fnt,width=19)
		uname.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
		uname['values']=users_list
		uname.current(0)

		tk.Label(passwd_win,text='New password',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
		npass=tk.Entry(passwd_win,font=fnt,show='*')
		npass.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

		subbtn=tk.Button(passwd_win,text='Make changes',font=fntit,command=ch_user_passwd)
		subbtn.grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)
		passwd_win.bind('<Return>',lambda event:ch_user_passwd())

	def register():	#adds user
		uuid='U'+str(rd.randint(10000,99999))
		
		def reguser():	#adds user to db
			
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
		regwin.title('Add user')
		regwin.resizable(False, False)

		img15=tk.PhotoImage(file='icons/adduser.png')
		img=tk.Label(regwin,image=img15,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10,sticky=tk.E)
		img.image=img15

		tk.Label(regwin,text='Add user...',font=h1fnt).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)
		
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

		regsubmit=tk.Button(regwin,text='Register',command=reguser,font=fntit)
		regsubmit.grid(column=1,row=14,padx=10,pady=10,sticky=tk.W)
		regwin.bind('<Return>',lambda event:reguser())

	
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

	img8=tk.PhotoImage(file='icons/preview.png')
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

	tk.Grid.rowconfigure(f2,16,weight=1)

	tk.Grid.rowconfigure(f2,17,weight=1)

def manage_db():		#Manage db
	import mysql.connector as ms
	import tkinter as tk
	import platform as pf
	import ctypes
	import pandas as pd
	from tkinter import ttk
	import os
	from tkinter import messagebox
	from tkinter import scrolledtext

	#Enables DPI scaling on supported versions of Windows
	if pf.system()=='Windows':
		try:
			ctypes.windll.shcore.SetProcessDpiAwareness(True)
		except:
			pass

	#mysql connection
	con=ms.connect(host='localhost',user='root',password='123456',database='taxi')
	cur=con.cursor()

	fnt=('IBM Plex Mono',12)
	fntit=('IBM Plex Mono',12,'italic')
	h1fnt=('IBM Plex Sans',24)
	menufnt=('IBM Plex Mono',11)

	dbmainwin=tk.Toplevel()
	dbmainwin.title('Database Manager')

	cur.execute('show tables')			#creating list of available tables for dropbox
	a=cur.fetchall()
	tables_list=[]
	for i in a:
		tables_list.append(i[0])

	def showtb():	#Show selected table
		if not table.get()=='' and not table.get().isspace():
			if table.get() in tables_list:
				dbwin=tk.Toplevel()
				dbwin.resizable(False,False)
				dbwin.title(table.get()+' table')
				sql=str('show columns from '+table.get())		#getting headers for table
				cur.execute(sql)
				a=cur.fetchall()
				headers_list=[]
				for x in a:									
					headers_list.append(x[0])
					header=tuple(headers_list)

				sql2=str('select * from '+table.get())			#getting data from table
				cur.execute(sql2)
				data=[header]+cur.fetchall()						#appending header to data
			
				rows=len(data)
				cols=len(data[0])

				for i in range(rows):							#drawing the table in GUI
					for j in range(cols):
						entry = tk.Label(dbwin,borderwidth=1,relief='solid',height=2,font=fnt,padx=10)
						entry.grid(row=i, column=j,padx=2,pady=2,sticky=tk.EW)
						entry.configure(text=data[i][j])
						if i==0:
							entry.configure(fg='red',font=fntit)	#colors and italicises header
			else:
				messagebox.showerror('Error','Table '+table.get()+' does not exist.',parent=dbmainwin)
		else:
			messagebox.showerror('Error','Please choose a table.',parent=dbmainwin)

	def droptb():	#Drop selected tablr
		if not table.get()=='' and not table.get().isspace():
			if table.get() in tables_list:
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
				messagebox.showerror('Error','Table '+table.get()+' does not exist.',parent=dbmainwin)
		else:
			messagebox.showerror('Error','Please choose a table.',parent=dbmainwin)

	def deltb():	#Delete contents of selected tables
		if not table.get()=='' and not table.get().isspace():
			if table.get() in tables_list:
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
				messagebox.showerror('Error','Table '+table.get()+' does not exist.',parent=dbmainwin)			
		else:
			messagebox.showerror('Error','Please choose a table.',parent=dbmainwin)

	def exporttb():		#Export selected table to CSV
		if not table.get()=='' and not table.get().isspace():
			if table.get() in tables_list:
				df=pd.read_sql('select * from '+table.get(),con)
				df.set_index(df.columns[0],inplace=True)
				
				def export_to_csv():
					path_input=path.get()
					if not path_input=='' and not path_input.isspace():
						df.reset_index(inplace=True)
						os.chdir('export')
						df.to_csv(path_input,index=False)
						os.chdir('./..')
						messagebox.showinfo('','Table '+table.get()+' exported to '+path_input+'.',parent=export_win)
						export_win.destroy()
					else:
						messagebox.showerror('Error','Please enter a filename.',parent=export_win)

				export_win=tk.Toplevel()
				export_win.resizable(False,False)
				export_win.title('Export to CSV')
				
				tk.Label(export_win,font=h1fnt,text='Export to CSV file...').grid(row=0,column=0,padx=10,pady=10,sticky=tk.NW)
				
				tk.Label(export_win,font=('IBM Plex Mono',12,'bold italic'),text='Data',justify=tk.LEFT).grid(row=1,column=0,padx=10,pady=10,sticky=tk.W)
				
				tk.Label(export_win,font=fnt,text='Enter the name of the\nCSV file.\nThe file will be saved to the\n\'export\' folder.',justify=tk.LEFT).grid(row=3,column=0,padx=10,pady=10,sticky=tk.W)

				path=tk.Entry(export_win,font=fnt)
				path.grid(row=5,column=0,padx=10,pady=10,sticky=tk.EW)

				submit=tk.Button(export_win,font=fnt,text='Export',command=export_to_csv)
				submit.grid(row=6,column=0,padx=10,pady=10)

				#Binds Enter key to export function
				export_win.bind('<Return>',lambda event:export_to_csv())
			else:
				messagebox.showerror('Error','Table '+table.get()+' does not exist.',parent=dbmainwin)			
		else:
			messagebox.showerror('Error','Please choose a table.',parent=dbmainwin)

	def help():		#View help page.
		helpwin=tk.Toplevel()
		helpwin.resizable(False,False)
		helpwin.title('Help')

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

	tk.Label(f2,text='Choose a table.',font=fntit,justify=tk.LEFT).grid(column=1,row=4,sticky=tk.W,padx=10,pady=10)
	img7=tk.PhotoImage(file='icons/table.png')
	h2img=tk.Label(f2,image=img7)
	h2img.grid(column=0,row=4,sticky=tk.E,padx=10,pady=10)
	h2img.image=img7

	tk.Grid.rowconfigure(f2,5,weight=1)
	n=tk.StringVar()
	table=ttk.Combobox(f2,textvariable=n,font=fnt,state='readonly')
	table.grid(row=5,column=1,padx=10,pady=10,sticky=tk.EW)
	table['values']=tables_list

	tk.Label(f2,text='You can:',font=fntit,justify=tk.LEFT).grid(column=1,row=6,sticky=tk.W,padx=10,pady=10)

	tk.Grid.rowconfigure(f2,7,weight=1)
	img8=tk.PhotoImage(file='icons/preview.png')
	tbviewbtn=tk.Button(f2,text='viewtable',image=img8,font=fnt,command=showtb)
	tbviewbtn.grid(column=0,row=7,padx=10,pady=10,sticky=tk.E)
	tbviewbtn.image=img8
	tk.Label(f2,text='View the table.',font=fnt,fg='blue').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)

	tk.Grid.rowconfigure(f2,8,weight=1)
	img9=tk.PhotoImage(file='icons/export.png')
	tbexportbtn=tk.Button(f2,text='export table',image=img9,font=fnt,command=exporttb)
	tbexportbtn.grid(column=0,row=8,padx=10,pady=10,sticky=tk.E)
	tbexportbtn.image=img9
	tk.Label(f2,text='Export the table\nto CSV file.',font=fnt,fg='green',justify=tk.LEFT).grid(column=1,row=8,padx=10,pady=10,sticky=tk.W)

	tk.Grid.rowconfigure(f2,9,weight=1)
	img10=tk.PhotoImage(file='icons/delete.png')
	deltbbtn=tk.Button(f2,text='deltable',image=img10,font=fnt,command=deltb)
	deltbbtn.grid(column=0,row=9,padx=10,pady=10,sticky=tk.E)
	deltbbtn.image=img10
	tk.Label(f2,text='Delete all the contents\nof the table.',font=fnt,justify=tk.LEFT).grid(column=1,row=9,padx=10,pady=10,sticky=tk.W)
	
	tk.Grid.rowconfigure(f2,10,weight=1)

	tk.Message(f2,text='WARNING:\nThis will delete all the contents of the table chosen permanently.',font=fnt,fg='white',bg='orange').grid(column=1,row=10,padx=10,sticky=tk.NW)

	img11=tk.PhotoImage(file='icons/remove.png')
	drptbbtn=tk.Button(f2,text='droptable',image=img11,font=fnt,command=droptb)
	drptbbtn.grid(column=2,row=9,padx=10,pady=10,sticky=tk.E)
	drptbbtn.image=img11
	tk.Label(f2,text='Drop the table.',font=fnt,fg='red').grid(column=3,row=9,padx=10,pady=10,sticky=tk.W)

	tk.Message(f2,text='WARNING:\nThis will drop the table chosen\nand its contents permanently.',font=fnt,fg='white',bg='red').grid(column=3,row=10,padx=10,sticky=tk.NW)

	#Bind Enter to show table function
	dbmainwin.bind('<Return>',lambda event:showtb())