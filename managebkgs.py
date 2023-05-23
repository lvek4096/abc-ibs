def bus():
	import mysql.connector as ms
	import tkinter as tk
	import platform as pf
	import ctypes
	from tkinter import ttk
	from tkinter import messagebox

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

	managebusbkgs=tk.Toplevel()
	managebusbkgs.title('Bus Bookings Manager')
	#w,h=manageempwin.winfo_screenwidth(),manageempwin.winfo_screenheight()
	#manageempwin.geometry(str(w)+'x'+str(h))

	def viewall():
		viewall_win=tk.Toplevel()
		viewall_win.title('All bus bookings')
		viewall_win.resizable(False,False)
		
		header=('Booking ID','Timestamp','Number of Passengers','Origin','Destination','Date','Time','Bus Type')

		sql2=str('select * from bus_bkgs')			#getting data from table
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
		def getbusbkginfo():
			cur.execute('select bkgid from bus_bkgs')
			a=cur.fetchall()
			for i in a:
				b.append(str(i[0]))
			
			if not bkgid.get()=='' and not bkgid.get().isspace():
				if bkgid.get() in b:
					sql='select * from bus_bkgs where bkgid=%s'
					val=(bkgid.get(),)
					cur.execute(sql,val)
					c=cur.fetchall()
					bkg_id=c[0][0]
					bkg_ts=c[0][1]
					bkg_passno=c[0][2]
					bkg_org=c[0][3]
					bkg_dest=c[0][4]
					bkg_date=c[0][5]
					bkg_time=c[0][6]
					bkg_type=c[0][7]
					
					e=[('Booking ID',bkg_id),('Timestamp',bkg_ts),('Number of passengers',bkg_passno),('Origin',bkg_org),('Destination',bkg_dest),('Date',bkg_date),('Time',bkg_time),('Bus Type',bkg_type)]
					
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
					messagebox.showerror('Error','Booking \''+bkgid.get()+'\' does not exist.',parent=viewone_win)
			else:
				messagebox.showerror('Error','Please enter the booking.',parent=viewone_win)
		viewone_win=tk.Toplevel()
		viewone_win.title(' ')
		viewone_win.resizable(False,False)
		
		frame1=tk.Frame(viewone_win)
		frame1.grid(row=0,column=0,padx=10,pady=10,sticky=tk.EW)

		frame2=tk.Frame(viewone_win)
		frame2.grid(row=2,column=0,padx=10,pady=10,sticky=tk.EW)

		frame3=tk.Frame(viewone_win)
		frame3.grid(row=1,column=0,padx=10,pady=10,sticky=tk.W)

		cur.execute('select bkgid from bus_bkgs')
		a=cur.fetchall()
		b=[]
		for i in a:
			b.append(i[0])

		img14=tk.PhotoImage(file='icons/searchusr.png')
		img=tk.Label(frame1,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(frame1,font=h1fnt,text='View bus booking details').grid(row=0,column=1,padx=10,pady=10,sticky=tk.W)

		tk.Label(frame1,font=fnt,text='Enter booking ID.').grid(row=4,column=1,padx=10,pady=10,sticky=tk.W)
		n=tk.StringVar()
		bkgid=ttk.Combobox(frame1,textvariable=n,font=fnt)
		bkgid.grid(row=5,column=1,padx=10,pady=10,sticky=tk.EW)
		bkgid['values']=b
		
		#img11=tk.PhotoImage(file='monoico/icon-582.png')
		submit=tk.Button(frame1,font=fntit,text='Submit',command=getbusbkginfo)
		submit.grid(row=5,column=2,padx=10,pady=10)
		#submit.image=img11
		viewone_win.bind('<Return>',lambda event:getbusbkginfo())

	def delone():
		delone_win=tk.Toplevel()
		delone_win.resizable(False,False)
		delone_win.title(' ')
		#cur.execute('select admin_uname,admin_name from admin')
		#a=cur.fetchall()
		#b=dict(a)
		def deletebkg():
			if not bkgid.get()=='' and not bkgid.get().isspace():
				if bkgid.get() in c:
					messagebox.showwarning('','This operation will delete\nthe booking selected permanently.\nContinue?',parent=delone_win)
					confirm=messagebox.askyesno('','Do you wish to delete the booking '+bkgid.get()+'?',parent=delone_win)
					if confirm == True:
						sql='delete from bus_bkgs where bkgid =%s'
						val=(bkgid.get(),)
						cur.execute(sql,val)
						con.commit()
						messagebox.showinfo('','Booking '+bkgid.get()+' deleted.',parent=delone_win)
						delone_win.destroy()
					else:
						messagebox.showinfo('','Booking '+bkgid.get()+' not deleted.\nThe database has not been modified.',parent=delone_win)
				else:
					messagebox.showerror('Error','Bookinge \''+bkgid.get()+'\' does not exist.',parent=delone_win)
			else:
				messagebox.showerror('','Please enter the booking ID.',parent=delone_win)
			
		img14=tk.PhotoImage(file='icons/delete_bkgs.png')
		img=tk.Label(delone_win,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(delone_win,text='Delete a bus booking',font=h1fnt).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

		cur.execute('select bkgid from bus_bkgs')
		d=cur.fetchall()
		c=[]
		for i in d:
			c.append(str(i[0]))

		tk.Label(delone_win,text='Select a booking.',font=fntit).grid(column=1,row=4,padx=10,pady=10,sticky=tk.W)

		n=tk.StringVar()
		bkgid=ttk.Combobox(delone_win,textvariable=n,font=fnt,width=19)
		bkgid.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
		bkgid['values']=c

		#img13=tk.PhotoImage(file='monoico/icon-694.png')
		delbtn=tk.Button(delone_win,text='Delete',font=fntit,command=deletebkg,fg='red')
		#delbtn.image=img13
		delbtn.grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)
		delone_win.bind('<Return>',lambda event:deletebkg())

	tk.Grid.columnconfigure(managebusbkgs,0,weight=1)

	#FRAME 1
	tk.Grid.rowconfigure(managebusbkgs,0,weight=1)
	f1=tk.Frame(managebusbkgs)
	f1.grid(row=0,column=0,sticky=tk.NSEW)

	#frame 1 grid
	tk.Grid.columnconfigure(f1,0,weight=1)
	tk.Grid.columnconfigure(f1,1,weight=1)

	tk.Grid.rowconfigure(f1,0,weight=1)
	img6=tk.PhotoImage(file='icons/bus.png')
	himg=tk.Label(f1,image=img6)
	himg.grid(column=0,row=0,sticky=tk.E,padx=10,pady=10)
	himg.image=img6
	tk.Label(f1,text=('Manage the bus booking...'),font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)
	#tk.Grid.rowconfigure(f1,1,weight=1)
	tk.Label(f1,text=('Connected to database: '+con.database),font=('IBM Plex Sans',12),justify=tk.LEFT,fg='green').grid(column=1,row=1,sticky=tk.W,padx=10,pady=10)
	ttk.Separator(f1,orient='horizontal').grid(column=0,row=2,sticky=tk.EW,padx=10,pady=10,columnspan=2)
	#FRAME 2
	tk.Grid.rowconfigure(managebusbkgs,1,weight=1)
	f2=tk.Frame(managebusbkgs)
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
	tk.Label(f2,text='View all booking details.',font=fnt,fg='blue').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

	img10=tk.PhotoImage(file='icons/search_bkgs.png')
	viewbtn=tk.Button(f2,text='viewone',image=img10,font=fnt,command=viewone)
	viewbtn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
	viewbtn.image=img10
	tk.Label(f2,text='View a single booking details.',font=fnt).grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)

	tk.Grid.rowconfigure(f2,7,weight=1)
	img12=tk.PhotoImage(file='icons/delete_bkgs.png')
	delbtn=tk.Button(f2,text='del',image=img12,font=fnt,command=delone)
	delbtn.grid(column=0,row=7,padx=10,pady=10,sticky=tk.E)
	delbtn.image=img12
	tk.Label(f2,text='Delete a booking.',font=fnt,fg='red').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)
	tk.Grid.rowconfigure(f2,8,weight=1)
	tk.Message(f2,text='WARNING: This will delete\nthe booking selected\nfrom the system permanently.',width=500,font=fnt,fg='white',bg='red').grid(column=1,row=8,padx=10,pady=10,sticky=tk.NW)

	#tk.Label(f2,text='or:',font=fntit,justify=tk.LEFT).grid(column=1,row=15,sticky=tk.W,padx=10,pady=10)

	tk.Grid.rowconfigure(f2,16,weight=1)

def taxi():
	import mysql.connector as ms
	import tkinter as tk
	import platform as pf
	import ctypes
	from tkinter import ttk
	from tkinter import messagebox
	
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

	managetaxibkgs=tk.Toplevel()
	managetaxibkgs.title('Taxi Bookings Manager')
	#w,h=manageempwin.winfo_screenwidth(),manageempwin.winfo_screenheight()
	#manageempwin.geometry(str(w)+'x'+str(h))

	def viewall():
		viewall_win=tk.Toplevel()
		viewall_win.title('All taxi bookings')
		viewall_win.resizable(False,False)
		
		header=('Booking ID','Timestamp','Origin','Destination','Date','Time','Taxi Type')

		sql2=str('select * from taxi_bkgs')			#getting data from table
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
		def gettaxibkginfo():
			cur.execute('select bkgid from taxi_bkgs')
			a=cur.fetchall()
			for i in a:
				b.append(str(i[0]))
			
			if not bkgid.get()=='' and not bkgid.get().isspace():
				if bkgid.get() in b:
					sql='select * from taxi_bkgs where bkgid=%s'
					val=(bkgid.get(),)
					cur.execute(sql,val)
					c=cur.fetchall()
					bkg_id=c[0][0]
					bkg_ts=c[0][1]
					bkg_org=c[0][2]
					bkg_dest=c[0][3]
					bkg_date=c[0][4]
					bkg_time=c[0][5]
					bkg_type=c[0][6]
					
					e=[('Booking ID',bkg_id),('Timestamp',bkg_ts),('Origin',bkg_org),('Destination',bkg_dest),('Date',bkg_date),('Time',bkg_time),('Taxi Type',bkg_type)]
					
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
					messagebox.showerror('Error','Booking \''+bkgid.get()+'\' does not exist.',parent=viewone_win)
			else:
				messagebox.showerror('Error','Please enter the booking.',parent=viewone_win)
		viewone_win=tk.Toplevel()
		viewone_win.title(' ')
		viewone_win.resizable(False,False)
		
		frame1=tk.Frame(viewone_win)
		frame1.grid(row=0,column=0,padx=10,pady=10,sticky=tk.EW)

		frame2=tk.Frame(viewone_win)
		frame2.grid(row=2,column=0,padx=10,pady=10,sticky=tk.EW)

		frame3=tk.Frame(viewone_win)
		frame3.grid(row=1,column=0,padx=10,pady=10,sticky=tk.W)

		cur.execute('select bkgid from taxi_bkgs')
		a=cur.fetchall()
		b=[]
		for i in a:
			b.append(i[0])

		img14=tk.PhotoImage(file='icons/searchusr.png')
		img=tk.Label(frame1,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(frame1,font=h1fnt,text='View taxi booking details').grid(row=0,column=1,padx=10,pady=10,sticky=tk.W)

		tk.Label(frame1,font=fnt,text='Enter booking ID.').grid(row=4,column=1,padx=10,pady=10,sticky=tk.W)
		n=tk.StringVar()
		bkgid=ttk.Combobox(frame1,textvariable=n,font=fnt)
		bkgid.grid(row=5,column=1,padx=10,pady=10,sticky=tk.EW)
		bkgid['values']=b
		
		#img11=tk.PhotoImage(file='monoico/icon-582.png')
		submit=tk.Button(frame1,font=fntit,text='Submit',command=gettaxibkginfo)
		submit.grid(row=5,column=2,padx=10,pady=10)
		#submit.image=img11
		viewone_win.bind('<Return>',lambda event:gettaxibkginfo())

	def delone():
		delone_win=tk.Toplevel()
		delone_win.resizable(False,False)
		delone_win.title(' ')
		#cur.execute('select admin_uname,admin_name from admin')
		#a=cur.fetchall()
		#b=dict(a)
		def deletebkg():
			if not bkgid.get()=='' and not bkgid.get().isspace():
				if bkgid.get() in c:
					messagebox.showwarning('','This operation will delete\nthe booking selected permanently.\nContinue?',parent=delone_win)
					confirm=messagebox.askyesno('','Do you wish to delete the booking '+bkgid.get()+'?',parent=delone_win)
					if confirm == True:
						sql='delete from taxi_bkgs where bkgid =%s'
						val=(bkgid.get(),)
						cur.execute(sql,val)
						con.commit()
						messagebox.showinfo('','Booking '+bkgid.get()+' deleted.',parent=delone_win)
						delone_win.destroy()
					else:
						messagebox.showinfo('','Booking '+bkgid.get()+' not deleted.\nThe database has not been modified.',parent=delone_win)
				else:
					messagebox.showerror('Error','Bookinge \''+bkgid.get()+'\' does not exist.',parent=delone_win)
			else:
				messagebox.showerror('','Please enter the booking ID.',parent=delone_win)
			
		img14=tk.PhotoImage(file='icons/delete_bkgs.png')
		img=tk.Label(delone_win,image=img14,font=h1fnt)
		img.grid(column=0,row=0,padx=10,pady=10)
		img.image=img14

		tk.Label(delone_win,text='Delete a taxi booking',font=h1fnt).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

		cur.execute('select bkgid from taxi_bkgs')
		d=cur.fetchall()
		c=[]
		for i in d:
			c.append(str(i[0]))

		tk.Label(delone_win,text='Select a booking.',font=fntit).grid(column=1,row=4,padx=10,pady=10,sticky=tk.W)

		n=tk.StringVar()
		bkgid=ttk.Combobox(delone_win,textvariable=n,font=fnt,width=19)
		bkgid.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
		bkgid['values']=c

		#img13=tk.PhotoImage(file='monoico/icon-694.png')
		delbtn=tk.Button(delone_win,text='Delete',font=fntit,command=deletebkg,fg='red')
		#delbtn.image=img13
		delbtn.grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)
		delone_win.bind('<Return>',lambda event:deletebkg())

	tk.Grid.columnconfigure(managetaxibkgs,0,weight=1)

	#FRAME 1
	tk.Grid.rowconfigure(managetaxibkgs,0,weight=1)
	f1=tk.Frame(managetaxibkgs)
	f1.grid(row=0,column=0,sticky=tk.NSEW)

	#frame 1 grid
	tk.Grid.columnconfigure(f1,0,weight=1)
	tk.Grid.columnconfigure(f1,1,weight=1)

	tk.Grid.rowconfigure(f1,0,weight=1)
	img6=tk.PhotoImage(file='icons/taxi.png')
	himg=tk.Label(f1,image=img6)
	himg.grid(column=0,row=0,sticky=tk.E,padx=10,pady=10)
	himg.image=img6
	tk.Label(f1,text=('Manage the taxi booking...'),font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)
	#tk.Grid.rowconfigure(f1,1,weight=1)
	tk.Label(f1,text=('Connected to database: '+con.database),font=('IBM Plex Sans',12),justify=tk.LEFT,fg='green').grid(column=1,row=1,sticky=tk.W,padx=10,pady=10)
	ttk.Separator(f1,orient='horizontal').grid(column=0,row=2,sticky=tk.EW,padx=10,pady=10,columnspan=2)
	#FRAME 2
	tk.Grid.rowconfigure(managetaxibkgs,1,weight=1)
	f2=tk.Frame(managetaxibkgs)
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
	tk.Label(f2,text='View all booking details.',font=fnt,fg='blue').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

	img10=tk.PhotoImage(file='icons/search_bkgs.png')
	viewbtn=tk.Button(f2,text='viewone',image=img10,font=fnt,command=viewone)
	viewbtn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
	viewbtn.image=img10
	tk.Label(f2,text='View a single booking details.',font=fnt).grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)

	tk.Grid.rowconfigure(f2,7,weight=1)
	img12=tk.PhotoImage(file='icons/delete_bkgs.png')
	delbtn=tk.Button(f2,text='del',image=img12,font=fnt,command=delone)
	delbtn.grid(column=0,row=7,padx=10,pady=10,sticky=tk.E)
	delbtn.image=img12
	tk.Label(f2,text='Delete a booking.',font=fnt,fg='red').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)
	tk.Grid.rowconfigure(f2,8,weight=1)
	tk.Message(f2,text='WARNING: This will delete\nthe booking selected\nfrom the system permanently.',width=500,font=fnt,fg='white',bg='red').grid(column=1,row=8,padx=10,pady=10,sticky=tk.NW)

	#tk.Label(f2,text='or:',font=fntit,justify=tk.LEFT).grid(column=1,row=15,sticky=tk.W,padx=10,pady=10)

	tk.Grid.rowconfigure(f2,16,weight=1)
	
	managetaxibkgs.mainloop()