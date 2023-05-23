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
	
	'''
	img9=tk.PhotoImage(file='monoico/icon-714.png')
	btn1=tk.Button(f2,text='exit',image=img9,font=fnt,command=home)
	btn1.grid(column=0,row=16,padx=10,pady=10,sticky=tk.E)
	btn1.image=img9

	tk.Label(f2,text='Return home.',font=fnt).grid(column=1,row=16,padx=10,pady=10,sticky=tk.W)
	'''