def main():
	import mysql.connector as ms
	import tkinter as tk
	import os
	from tkinter import ttk
	from tkinter import messagebox
	import random as rd

	con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
	cur=con.cursor()

	fnt=('IBM Plex Mono',12)
	fntit=('IBM Plex Mono',12,'italic')
	h1fnt=('IBM Plex Sans',24)

	manageempwin=tk.Toplevel()
	manageempwin.title('Manage employees')
	w,h=manageempwin.winfo_screenwidth(),manageempwin.winfo_screenheight()
	manageempwin.geometry(str(w)+'x'+str(h))

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

		img14=tk.PhotoImage(file='monoico/icon-716.png')
		img=tk.Label(frame1,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(frame1,font=h1fnt,text='View employee details').grid(row=0,column=1,padx=10,pady=10,sticky=tk.W)

		tk.Label(frame1,font=fnt,text='Enter username of employee.').grid(row=4,column=1,padx=10,pady=10,sticky=tk.W)
		n=tk.StringVar()
		uname=ttk.Combobox(frame1,textvariable=n,font=fnt)
		uname.grid(row=5,column=1,padx=10,pady=10,sticky=tk.EW)
		uname['values']=b
		
		img11=tk.PhotoImage(file='monoico/icon-582.png')
		submit=tk.Button(frame1,font=fnt,image=img11,command=getempinfo)
		submit.grid(row=5,column=2,padx=10,pady=10)
		submit.image=img11

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
					else:
						messagebox.showinfo('','Employee '+b[uname.get()]+' not deleted.\nThe database has not been modified.',parent=delone_win)
				else:
					messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=delone_win)
			else:
				messagebox.showerror('','Please enter the employee username.',parent=delone_win)
		
		
			img14=tk.PhotoImage(file='monoico/icon-79.png')
		
		img14=tk.PhotoImage(file='monoico/icon-76.png')
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

		img13=tk.PhotoImage(file='monoico/icon-694.png')
		delbtn=tk.Button(delone_win,text='del',image=img13,font=fnt,command=deleteemp)
		delbtn.image=img13
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
					else:
						messagebox.showinfo('','Password for '+b[uname.get()]+' has not been changed..\nThe databasehas not\nbeen modified.',parent=passwd_win)
				else:
					messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=passwd_win)
			else:
				messagebox.showerror('','Do not leave any fields blank.',parent=passwd_win)
		
		img14=tk.PhotoImage(file='monoico/icon-79.png')
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

		img13=tk.PhotoImage(file='monoico/icon-694.png')
		subbtn=tk.Button(passwd_win,text='submit',image=img13,font=fnt,command=chpasswd)
		subbtn.image=img13
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
				else:
					messagebox.showerror('Error','Username \''+uname_inp+'\'\nalready exists.',parent=add_win)
			else:
				messagebox.showerror('Error','Do not leave any fields blank.',parent=add_win)
		
		id='E'+str(rd.randint(1000,9999))

		img14=tk.PhotoImage(file='monoico/icon-67.png')
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

		subimg=tk.PhotoImage(file='monoico/icon-308.png')
		subbtn=tk.Button(add_win,font=fnt,text='Submit',image=subimg,command=add_emp)
		subbtn.grid(column=1,row=12,padx=10,pady=10,sticky=tk.W)
		subbtn.image=subimg

		exitimg=tk.PhotoImage(file='monoico/icon-66.png')
		exitbtn=tk.Button(add_win,font=fnt,text='Exit',image=exitimg,command=add_win.destroy)
		exitbtn.grid(column=0,row=15,padx=10,pady=10,sticky=tk.SW)
		exitbtn.image=exitimg

	tk.Grid.columnconfigure(manageempwin,0,weight=1)

	#FRAME 1
	tk.Grid.rowconfigure(manageempwin,0,weight=1)
	f1=tk.Frame(manageempwin)
	f1.grid(row=0,column=0,sticky=tk.NSEW)

	#frame 1 grid
	tk.Grid.columnconfigure(f1,0,weight=1)
	tk.Grid.columnconfigure(f1,1,weight=1)

	tk.Grid.rowconfigure(f1,0,weight=1)
	img6=tk.PhotoImage(file='monoico/icon-306.png')
	tk.Label(f1,image=img6).grid(column=0,row=0,sticky=tk.E,padx=10,pady=10)
	tk.Label(f1,text=('Manage the employees...'),font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)
	#tk.Grid.rowconfigure(f1,1,weight=1)
	tk.Label(f1,text=('Connected to database: '+con.database),font=('IBM Plex Sans',12),justify=tk.LEFT,fg='green').grid(column=1,row=1,sticky=tk.W,padx=10,pady=10)

	#FRAME 2
	tk.Grid.rowconfigure(manageempwin,1,weight=1)
	f2=tk.Frame(manageempwin)
	f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

	#frame 2 grid
	tk.Grid.columnconfigure(f2,0,weight=1)
	tk.Grid.columnconfigure(f2,1,weight=1)
	tk.Grid.columnconfigure(f2,2,weight=1)
	tk.Grid.columnconfigure(f2,3,weight=1)

	tk.Grid.rowconfigure(f2,3,weight=1)
	tk.Label(f2,text='You can:',font=fntit,justify=tk.LEFT).grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

	#tk.Grid.rowconfigure(f2,5,weight=1)
	img8=tk.PhotoImage(file='monoico/icon-675.png')
	tbviewbtn=tk.Button(f2,text='view all',image=img8,font=fnt,command=viewall)
	tbviewbtn.grid(column=0,row=5,padx=10,pady=10,sticky=tk.E)
	tk.Label(f2,text='View all employee details.',font=fnt,fg='blue').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

	img10=tk.PhotoImage(file='monoico/icon-716.png')
	viewbtn=tk.Button(f2,text='viewone',image=img10,font=fnt,command=viewone)
	viewbtn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
	tk.Label(f2,text='View a single employee\'s details.',font=fnt).grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)

	#tk.Grid.rowconfigure(f2,6,weight=1)
	img7=tk.PhotoImage(file='monoico/icon-67.png')
	tbviewbtn=tk.Button(f2,text='add',image=img7,font=fnt,command=add)
	tbviewbtn.grid(column=0,row=6,padx=10,pady=10,sticky=tk.E)
	tk.Label(f2,text='Register an employee.',font=fnt,fg='green').grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

	img11=tk.PhotoImage(file='monoico/icon-79.png')
	passbtn=tk.Button(f2,text='passwd',image=img11,font=fnt,command=passwd)
	passbtn.grid(column=2,row=6,padx=10,pady=10,sticky=tk.E)
	tk.Label(f2,text='Change the password for an employee.',font=fnt).grid(column=3,row=6,padx=10,pady=10,sticky=tk.W)

	#tk.Grid.rowconfigure(f2,7,weight=1)
	img12=tk.PhotoImage(file='monoico/icon-76.png')
	delbtn=tk.Button(f2,text='del',image=img12,font=fnt,command=delone)
	delbtn.grid(column=0,row=7,padx=10,pady=10,sticky=tk.E)
	tk.Label(f2,text='Delete an employee.',font=fnt,fg='red').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)
	#tk.Grid.rowconfigure(f2,8,weight=1)
	tk.Message(f2,text='WARNING: This will delete\nan employee\'s profile\nfrom the system permanently.',width=500,font=fnt,fg='white',bg='red').grid(column=1,row=8,padx=10,pady=10,sticky=tk.NW)

	def home():
		manageempwin.destroy()
		os.system('python3 admin.py')
	tk.Grid.rowconfigure(f2,15,weight=1)
	tk.Label(f2,text='or:',font=fntit,justify=tk.LEFT).grid(column=1,row=15,sticky=tk.W,padx=10,pady=10)

	tk.Grid.rowconfigure(f2,16,weight=1)
	img9=tk.PhotoImage(file='monoico/icon-714.png')
	bkgbtn=tk.Button(f2,text='exit',image=img9,font=fnt,command=home)
	bkgbtn.grid(column=0,row=16,padx=10,pady=10,sticky=tk.E)
	tk.Label(f2,text='Return home.',font=fnt).grid(column=1,row=16,padx=10,pady=10,sticky=tk.W)
