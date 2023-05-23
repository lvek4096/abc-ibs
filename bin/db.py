def main():
	import mysql.connector as ms
	import tkinter as tk
	import os
	from tkinter import ttk
	from tkinter import messagebox
	from tkinter import scrolledtext

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
	'''
	def home():
		dbmainwin.destroy()
		os.system('python3 admin.py')
	tk.Grid.rowconfigure(f2,15,weight=1)
	
	tk.Label(f2,text='or',font=fntit,justify=tk.LEFT).grid(column=1,row=15,sticky=tk.W,padx=10,pady=10)

	tk.Grid.rowconfigure(f2,16,weight=1)
	img9=tk.PhotoImage(file='monoico/icon-714.png')
	btn1=tk.Button(f2,text='exit',image=img9,font=fnt,command=home)
	btn1.grid(column=0,row=16,padx=10,pady=10,sticky=tk.E)
	btn1.image=img9
	tk.Label(f2,text='Return home.',font=fnt).grid(column=1,row=16,padx=10,pady=10,sticky=tk.W)

	img12=tk.PhotoImage(file='monoico/icon-595.png')
	helpbtn=tk.Button(f2,text='help',image=img12,font=fnt,command=help)
	helpbtn.grid(column=2,row=16,padx=10,pady=10,sticky=tk.E)
	helpbtn.image=img12
	tk.Label(f2,text='Know the difference\nbetween DELETE FROM and DROP.',font=fnt,justify=tk.LEFT).grid(column=3,row=16,padx=10,pady=10,sticky=tk.W)
	'''