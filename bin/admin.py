def main():
	import mysql.connector as ms
	import tkinter as tk
	import os
	from tkinter import messagebox

	import db
	import manageemp
	import manageusers
	import empbkgs
	
	#mysql connection
	con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
	cur=con.cursor()

	fnt=('IBM Plex Mono',12)
	fntit=('IBM Plex Mono',12,'italic')
	h1fnt=('IBM Plex Sans',24)

	root=tk.Tk()
	root.title('Admin menu')
	w,h=root.winfo_screenwidth(),root.winfo_screenheight()
	root.geometry(str(w)+'x'+str(h))

	def logout():
		root.destroy()
		os.system('python3 emplogin.py')

	def showdb():
		db.main()

	def emp():
		manageemp.main()

	def bookings():
		root.destroy()
		empbkgs.main()

	def users():
		manageusers.main()

	tk.Grid.columnconfigure(root,0,weight=1)

	#cur.execute('select emp_uname,emp_name from employees')
	#a=dict(cur.fetchall())

	#FRAME 1
	tk.Grid.rowconfigure(root,0,weight=1)
	f1=tk.Frame(root)
	f1.grid(row=0,column=0,sticky=tk.NSEW)

	#frame 1 grid
	tk.Grid.columnconfigure(f1,0,weight=1)

	tk.Grid.rowconfigure(f1,0,weight=1)
	tk.Label(f1,text='Welcome',font=h1fnt,justify=tk.CENTER).grid(column=0,row=0,padx=10,pady=10)

	#FRAME 2
	tk.Grid.rowconfigure(root,1,weight=1)
	f2=tk.Frame(root)
	f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

	#frame 2 grid
	tk.Grid.columnconfigure(f2,0,weight=1)
	tk.Grid.columnconfigure(f2,1,weight=1)
	tk.Grid.columnconfigure(f2,2,weight=1)
	tk.Grid.columnconfigure(f2,3,weight=1)

	tk.Grid.rowconfigure(f2,2,weight=1)
	tk.Label(f2,text='You can:',font=fntit).grid(column=1,row=2,sticky=tk.W,padx=10)

	#tk.Grid.rowconfigure(f2,5,weight=1)
	img6=tk.PhotoImage(file='monoico/icon-829.png')
	bkgbtn=tk.Button(f2,text='View the database',image=img6,font=fnt,command=showdb,width=48,height=48)
	bkgbtn.grid(column=0,row=5,padx=10,pady=10,sticky=tk.E)
	tk.Label(f2,text='Manage the databases.',font=fnt,fg='blue').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

	img9=tk.PhotoImage(file='monoico/icon-306.png')
	bkgbtn=tk.Button(f2,text='Manage employees',image=img9,font=fnt,command=emp)
	bkgbtn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
	tk.Label(f2,text='Manage the employees.',font=fnt,fg='green').grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)

	#tk.Grid.rowconfigure(f2,6,weight=1)
	img10=tk.PhotoImage(file='monoico/icon-13.png')
	bkgbtn=tk.Button(f2,text='Bookings',image=img10,font=fnt,command=bookings)
	bkgbtn.grid(column=0,row=6,padx=10,pady=10,sticky=tk.E)
	tk.Label(f2,text='Make bookings.',font=fnt).grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

	img11=tk.PhotoImage(file='monoico/icon-675.png')
	bkgbtn=tk.Button(f2,text='Manage users',image=img11,font=fnt,command=users)
	bkgbtn.grid(column=2,row=6,padx=10,pady=10,sticky=tk.E)
	tk.Label(f2,text='Manage the users.',font=fnt).grid(column=3,row=6,padx=10,pady=10,sticky=tk.W)

	tk.Grid.rowconfigure(f2,9,weight=1)
	tk.Label(f2,text='or:',font=fntit).grid(column=1,row=9,padx=10,sticky=tk.W)

	def chrootpasswd():
		passwd_win=tk.Toplevel()
		passwd_win.resizable(False,False)
		passwd_win.title('')

		def chpasswd():
			if not npass.get()=='' and not npass.get().isspace():
		
				confirm=messagebox.askyesno('','Do you wish to change the administrator password ?',parent=passwd_win)
				if confirm == True:
					sql="update admin set admin_passwd=%s where admin_uname='root'"
					val=(npass.get(),)
					cur.execute(sql,val)
					con.commit()
					messagebox.showinfo('','Administrator password changed.',parent=passwd_win)
				else:
					messagebox.showinfo('','Administrator password has not been changed',parent=passwd_win)
			
			else:
				messagebox.showerror('','Please enter a password.',parent=passwd_win)
		
		img14=tk.PhotoImage(file='monoico/icon-79.png')
		img=tk.Label(passwd_win,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(passwd_win,text='Change the administrator\npassword...',font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

		tk.Label(passwd_win,text='New password',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
		npass=tk.Entry(passwd_win,font=fnt,show='*')
		npass.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

		img13=tk.PhotoImage(file='monoico/icon-694.png')
		subbtn=tk.Button(passwd_win,text='submit',image=img13,font=fnt,command=chpasswd)
		subbtn.image=img13
		subbtn.grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)

	#tk.Grid.rowconfigure(f2,10,weight=1)
	img12=tk.PhotoImage(file='monoico/icon-79.png')
	bkgbtn=tk.Button(f2,text='root password',image=img12,font=fnt,command=chrootpasswd)
	bkgbtn.grid(column=0,row=10,padx=10,pady=10,sticky=tk.E)
	tk.Label(f2,text='Change the\nadministrator password.',font=fnt,justify=tk.LEFT).grid(column=1,row=10,padx=10,pady=10,sticky=tk.W)

	tk.Grid.rowconfigure(f2,11,weight=1)
	img7=tk.PhotoImage(file='monoico/icon-670.png')
	bkgbtn=tk.Button(f2,text='Logout.',image=img7,font=fnt,command=logout)
	bkgbtn.grid(column=0,row=11,padx=10,pady=10,sticky=tk.E)
	tk.Label(f2,text='Logout',font=fnt).grid(column=1,row=11,padx=10,pady=10,sticky=tk.W)

	img8=tk.PhotoImage(file='monoico/icon-66.png')
	bkgbtn=tk.Button(f2,text='Exit',image=img8,font=fnt,command=root.destroy)
	bkgbtn.grid(column=2,row=11,padx=10,pady=10,sticky=tk.E)
	tk.Label(f2,text='Logout and exit.',font=fnt,fg='red').grid(column=3,row=11,padx=10,pady=10,sticky=tk.W)
	root.mainloop()