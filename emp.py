#!/bin/python3

def emp_main():
	#import statements

	#Imports libraries
	import mysql.connector as ms
	import tkinter as tk
	from tkinter import ttk
	from tkinter import messagebox
	import platform as pf
	import ctypes
	from tkinter.ttk import Separator

	#Imports other Python scripts
	import manage
	import managebkgs
	import sysinfo
	import bookings
	import init

	#Enables DPI scaling on supported Windows versions
	if pf.system()=='Windows':
		try:
			ctypes.windll.shcore.SetProcessDpiAwareness(True)
		except:
			pass

	#Definitions

	#mysql connection
	con=ms.connect(host='localhost',user='root',password='123456',database='taxi')
	cur=con.cursor()

	init.initdb()
	
	#fonts
	fnt=('IBM Plex Mono',12)
	fntit=('IBM Plex Mono',12,'italic')
	h1fnt=('IBM Plex Sans',24)
	menufnt=('IBM Plex Mono',11)

	#main window
	emplogwin=tk.Tk()
	emplogwin.title('Employee login')

	#maximises window
	try:
		emplogwin.state('zoomed')
	except:
		w,h=emplogwin.winfo_screenwidth(),emplogwin.winfo_screenheight()
		emplogwin.geometry(str(w)+'x'+str(h))

	#functions
	def login():	#action on login

		def admin():	#Admin menu

			root=tk.Tk()
			root.title('Admin menu')

			try:
				root.state('zoomed')
			except:
				w,h=root.winfo_screenwidth(),root.winfo_screenheight()
				root.geometry(str(w)+'x'+str(h))

			def logout():
				root.destroy()
				emp_main()

			def showdb():
				manage.managedb()

			def emp():
				manage.manageemp()

			def bookings():
				empbookings()

			def users():
				manage.manageusers()

			def about_this_program():
				sysinfo.about()

			def admins():
				manage.manageadmin()
			
			def passwd():
				passwd_win=tk.Toplevel()
				passwd_win.resizable(False,False)
				passwd_win.title(' ')

				def change_admin_passwd():
					if not npass.get()=='' and not npass.get().isspace():
				
						confirm=messagebox.askyesno('','Do you wish to change the administrator password for '+a[emp_uname_inp]+' ?',parent=passwd_win)
						if confirm == True:
							sql="update admin set admin_passwd=%s where admin_uname=%s"
							val=(npass.get(),emp_uname_inp)
							cur.execute(sql,val)
							con.commit()
							messagebox.showinfo('','Administrator password changed for '+a[emp_uname_inp]+'.',parent=passwd_win)
							passwd_win.destroy()
						else:
							messagebox.showinfo('','Administrator password has not been changed.',parent=passwd_win)
					
					else:
						messagebox.showerror('','Please enter a password.',parent=passwd_win)
				
				img14=tk.PhotoImage(file='icons/passwd.png')
				img=tk.Label(passwd_win,image=img14,font=h1fnt)
				img.grid(column=0,row=0,padx=10,pady=10)
				img.image=img14

				tk.Label(passwd_win,text='Changing the administrator\npassword for '+a[emp_uname_inp],font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

				tk.Label(passwd_win,text='New password',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
				npass=tk.Entry(passwd_win,font=fnt,show='*')
				npass.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

				subbtn=tk.Button(passwd_win,text='Make changes',font=fntit,command=change_admin_passwd)
				subbtn.grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)	
			
			tk.Grid.columnconfigure(root,0,weight=1)

			menubar=tk.Menu(root)

			user=tk.Menu(menubar,tearoff=0)
			menubar.add_cascade(label='User',menu=user,font=menufnt)

			user.add_command(label='Change the administrator password...',command=passwd,font=menufnt,underline=0)
			user.add_separator()
			user.add_command(label='Logout',command=logout,font=menufnt,underline=0)
			user.add_command(label='Logout and Exit',command=root.destroy,font=menufnt,underline=11)

			more=tk.Menu(menubar,tearoff=0)
			menubar.add_cascade(label='Info',menu=more,font=menufnt)

			more.add_command(label='About this program...',command=about_this_program,font=menufnt,underline=0)
			root.config(menu=menubar)

			#FRAME 1
			tk.Grid.rowconfigure(root,0,weight=1)
			f1=tk.Frame(root,bg='#283593')
			f1.grid(row=0,column=0,sticky=tk.NSEW)

			#frame 1 grid
			tk.Grid.columnconfigure(f1,0,weight=1)

			cur.execute('select admin_uname,admin_name from admin')
			a=dict(cur.fetchall())

			cur.execute('select admin_uname,admin_id from admin')
			uuidlist=dict(cur.fetchall())
			tk.Grid.rowconfigure(f1,0,weight=1)
			tk.Label(f1,text='Welcome, '+a[emp_uname_inp],font=h1fnt,justify=tk.CENTER,fg='white',bg='#283593').grid(column=0,row=0,padx=10,pady=10)
			tk.Label(f1,text=('ID: '+uuidlist[emp_uname_inp]),font=('IBM Plex Sans',12),fg='black',bg='#00e676').grid(column=0,row=1,padx=10)

			Separator(f1,orient='horizontal').grid(column=0,row=2,sticky=tk.EW,padx=10,pady=10)
			
			#FRAME 2
			tk.Grid.rowconfigure(root,1,weight=1)
			f2=tk.Frame(root)
			f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

			#frame 2 grid
			tk.Grid.columnconfigure(f2,0,weight=1)
			tk.Grid.columnconfigure(f2,1,weight=1)
			tk.Grid.columnconfigure(f2,2,weight=1)
			tk.Grid.columnconfigure(f2,3,weight=1)

			tk.Label(f2,text='You can:',font=fntit).grid(column=1,row=2,sticky=tk.W,padx=10,pady=10)

			tk.Grid.rowconfigure(f2,5,weight=1)
			img6=tk.PhotoImage(file='icons/dataset.png')
			btn1=tk.Button(f2,text='View the database',image=img6,font=fnt,command=showdb,width=48,height=48)
			btn1.grid(column=0,row=5,padx=10,pady=10,sticky=tk.E)
			btn1.image=img6
			tk.Label(f2,text='Manage the databases.',font=fnt,fg='blue').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

			img9=tk.PhotoImage(file='icons/employee.png')
			btn2=tk.Button(f2,text='Manage employees',image=img9,font=fnt,command=emp)
			btn2.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
			btn2.image=img9
			tk.Label(f2,text='Manage the employees.',font=fnt,fg='green').grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)

			tk.Grid.rowconfigure(f2,6,weight=1)
			img12=tk.PhotoImage(file='icons/supervisor.png')
			btn5=tk.Button(f2,text='Manage administrators',image=img12,font=fnt,command=admins)
			btn5.grid(column=0,row=6,padx=10,pady=10,sticky=tk.E)
			btn5.image=img12
			tk.Label(f2,text='Manage the administrators.',font=fnt,fg='red').grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

			img11=tk.PhotoImage(file='icons/people.png')
			btn4=tk.Button(f2,text='Manage users',image=img11,font=fnt,command=users)
			btn4.grid(column=2,row=6,padx=10,pady=10,sticky=tk.E)
			btn4.image=img11
			tk.Label(f2,text='Manage the users.',font=fnt,fg='purple').grid(column=3,row=6,padx=10,pady=10,sticky=tk.W)
			
			tk.Grid.rowconfigure(f2,8,weight=1)

			img10=tk.PhotoImage(file='icons/booking.png')
			btn3=tk.Button(f2,text='Bookings',image=img10,font=fnt,command=bookings)
			btn3.grid(column=0,row=8,padx=10,pady=10,sticky=tk.E)
			btn3.image=img10
			tk.Label(f2,text='Make and manage bookings.',font=fnt).grid(column=1,row=8,padx=10,pady=10,sticky=tk.W)

			tk.Grid.rowconfigure(f2,9,weight=1)
			
			root.mainloop()

		def empbookings():		#Agent booking menu

			#functions
			def book_taxi():	#Opens taxi booking window.
				bookings.taxi()

			def book_bus():		#Opens bus booking window
				bookings.bus()
			
			def about_this_program():
				sysinfo.about()

			def logout():
				main_menu.destroy()
				emp_main()

			def managetaxibkgs():
				managebkgs.taxi()
				
			def managebusbkgs():
				managebkgs.bus()

			if emptype_inp=='Agent':
				main_menu=tk.Tk()
			elif emptype_inp=='Administrator':
				main_menu=tk.Toplevel()
			
			main_menu.title('Booking Portal')

			if emptype_inp=='Agent':
				try:
					main_menu.state('zoomed')
				except:
					w,h=main_menu.winfo_screenwidth(),main_menu.winfo_screenheight()
					main_menu.geometry(str(w)+'x'+str(h))
			
			elif emptype_inp=='Administrator':
				main_menu.geometry('960x540')
			
			if emptype_inp=='Agent':
				menubar=tk.Menu(main_menu)

				user=tk.Menu(menubar,tearoff=0)
				menubar.add_cascade(label='User',menu=user,font=menufnt)
				user.add_command(label='Logout',command=logout,font=menufnt,underline=0)
				user.add_command(label='Logout and exit',command=main_menu.destroy,font=menufnt,underline=11)
				main_menu.config(menu=menubar)
				
				more=tk.Menu(menubar,tearoff=0)
				menubar.add_cascade(label='Info',menu=more,font=menufnt)
				more.add_command(label='About this program...',command=about_this_program,font=menufnt,underline=0)
				main_menu.config(menu=menubar)

			tk.Grid.columnconfigure(main_menu,0,weight=1)


			#FRAME 1
			tk.Grid.rowconfigure(main_menu,0,weight=1)
			f1=tk.Frame(main_menu,bg='#283593')
			f1.grid(row=0,column=0,sticky=tk.NSEW)

			tk.Grid.columnconfigure(f1,0,weight=1)

			tk.Grid.rowconfigure(f1,0,weight=1)

			cur.execute('select emp_uname,emp_name from employees')
			b=dict(cur.fetchall())

			cur.execute('select emp_uname,emp_id from employees')
			uuidlist=dict(cur.fetchall())

			if emptype_inp=='Agent':
				txt='Welcome, '+b[emp_uname_inp]
				tk.Label(f1,text=('ID: '+uuidlist[emp_uname_inp]),font=('IBM Plex Sans',12),fg='black',bg='#00e676').grid(column=0,row=1,padx=10)
			elif emptype_inp=='Administrator':
				txt='Make and manage bookings'
			
			tk.Label(f1,text=txt,fg='white',bg='#283593',font=h1fnt,justify=tk.CENTER).grid(column=0,row=0,padx=10,pady=10)

			Separator(f1,orient='horizontal').grid(column=0,row=2,sticky=tk.EW,padx=10,pady=10)
			#FRAME 2
			tk.Grid.rowconfigure(main_menu,1,weight=1)
			f2=tk.Frame(main_menu)
			f2.grid(row=1,column=0,sticky=tk.NSEW)

			tk.Grid.columnconfigure(f2,0,weight=1)
			tk.Grid.columnconfigure(f2,1,weight=1)
			tk.Grid.columnconfigure(f2,2,weight=1)
			tk.Grid.columnconfigure(f2,3,weight=1)

			tk.Label(f2,text=('You can:'),font=fntit).grid(column=1,row=2,padx=10,pady=10,sticky=tk.W)

			tk.Grid.rowconfigure(f2,5,weight=1)
			img6=tk.PhotoImage(file='icons/taxi.png')
			bkgbtn=tk.Button(f2,text='Book taxi',image=img6,font=fnt,command=book_taxi)
			bkgbtn.grid(column=0,row=5,padx=10,pady=1,sticky=tk.E)
			bkgbtn.image=img6
			tk.Label(f2,text='Book a taxi.',font=fnt,bg='yellow').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)
					
			img4=tk.PhotoImage(file='icons/bus.png')
			passbtn=tk.Button(f2,text='Book Bus',image=img4,command=book_bus)
			passbtn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
			passbtn.image=img4
			tk.Label(f2,text='Book a bus.',font=fnt,fg='blue').grid(column=3,row=5,padx=5,pady=10,sticky=tk.W)

			tk.Label(f2,text=('or:'),font=fntit).grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

			tk.Grid.rowconfigure(f2,7,weight=1)
			
			btn5=tk.Button(f2,text='Manage taxi bookings',font=fntit,command=managetaxibkgs)
			btn5.grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)
			
			btn6=tk.Button(f2,text='Manage bus bookings',font=fntit,command=managebusbkgs)
			btn6.grid(column=3,row=7,padx=10,pady=10,sticky=tk.W)

			tk.Grid.rowconfigure(f2,10,weight=1)

			if emptype_inp=='Agent':
				main_menu.mainloop()

		#Converts inputs to strings
		emp_uname_inp=emp_uname.get().lower()
		emptype_inp=n.get()
		emp_passwd_inp=emp_passwd.get()
		
		#Checking for validity in inputs
		if emptype_inp == 'Agent':
			
			cur.execute('select emp_uname,emp_passwd from employees')		#list of employee usernames and passwords
			e=dict(cur.fetchall())

			cur.execute('select emp_uname,emp_name from employees')			#list of employee usernames and names
			f=dict(cur.fetchall())

			if not emp_uname_inp=='' or emp_uname_inp.isspace():
				if emp_uname_inp in e.keys():
					if emp_passwd_inp==e[emp_uname_inp]:
						emplogwin.destroy()
						empbookings()
					else:
						messagebox.showerror('Error','Invalid password for employee '+f[emp_uname_inp]+'.')
				else:
					messagebox.showerror('Error','Employee '+emp_uname_inp+' does not exist.')
			else:
				messagebox.showerror('Error','Do not leave any fields empty.')
		
		elif emptype_inp == 'Administrator':
		
			cur.execute('select admin_uname,admin_passwd from admin')	#list of admin usernames and passwords
			a=dict(cur.fetchall())

			cur.execute('select admin_uname,admin_name from admin')		#list of admin usernames and names
			b=dict(cur.fetchall())

			if not emp_uname_inp=='' or emp_uname_inp.isspace():
				if emp_uname_inp in a.keys():
					if emp_passwd_inp==a[emp_uname_inp]:
						emplogwin.destroy()
						admin()
					else:
						messagebox.showerror('Error','Invalid password for administrator '+b[emp_uname_inp]+'.')
				else:
					messagebox.showerror('Error','Administrator '+emp_uname_inp+' does not exist.')
			else:
				messagebox.showerror('Error','Do not leave any fields empty.')
		else:
			messagebox.showerror('Error','Please select login type.')
	
	def about_this_program():
		sysinfo.about()

	menubar=tk.Menu(emplogwin)

	more=tk.Menu(menubar,tearoff=0)
	menubar.add_cascade(label='Info',menu=more,font=menufnt)
	more.add_command(label='About this program...',command=about_this_program,font=menufnt,underline=0)
	emplogwin.config(menu=menubar)
		
	tk.Grid.columnconfigure(emplogwin,0,weight=1)

	#FRAME 1
	tk.Grid.rowconfigure(emplogwin,0,weight=1)
	f1=tk.Frame(emplogwin,bg='#283593')
	f1.grid(row=0,column=0,sticky=tk.NSEW)

	#frame 1 grid
	tk.Grid.columnconfigure(f1,0,weight=1)

	tk.Grid.rowconfigure(f1,0,weight=1)
	tk.Label(f1,text='Employee login',font=h1fnt,justify=tk.CENTER,fg='white',bg='#283593').grid(column=0,row=0)
	ttk.Separator(f1,orient='horizontal').grid(row=1,column=0,sticky=tk.EW,padx=10,pady=10)

	#FRAME 2
	tk.Grid.rowconfigure(emplogwin,1,weight=1)
	f2=tk.Frame(emplogwin)
	f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

	#frame 2 grid
	tk.Grid.columnconfigure(f2,0,weight=1)
	tk.Grid.columnconfigure(f2,1,weight=1)

	#Login type
	tk.Label(f2,text='Login as',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
	n=tk.StringVar()
	values=('','Agent','Administrator')
	emptype=ttk.OptionMenu(f2,n,*values);emptype.grid(column=1,row=5,sticky=tk.W,padx=10,pady=10)

	#uname
	tk.Label(f2,text='Username',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
	emp_uname=tk.Entry(f2,font=fnt)
	emp_uname.grid(column=1,row=6,sticky=tk.W,padx=10,pady=10)

	#passwd
	tk.Label(f2,text='Password',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
	emp_passwd=tk.Entry(f2,show='*',font=fnt)
	emp_passwd.grid(column=1,row=7,sticky=tk.W,padx=10,pady=10)

	#Login button
	img1=tk.PhotoImage(file='icons/login.png')
	logsubmit=tk.Button(f2,text='Login',image=img1,command=login)
	logsubmit.grid(column=1,row=8,padx=10,pady=10,sticky=tk.W)

	emplogwin.bind('<Return>',lambda event:login())

	emplogwin.mainloop()

emp_main()