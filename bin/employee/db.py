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

dbmainwin=tk.Tk()
dbmainwin.title('Database')
dbmainwin.resizable(False,False)

def showtb():

	if not table.get()=='' and not table.get().isspace():
		dbwin=tk.Toplevel()
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

cur.execute('show tables')			#creating list of available tables for dropbox
a=cur.fetchall()
#print(a)
b=[]
for i in a:
	b.append(i[0])

def droptb():
	if not table.get()=='' and not table.get().isspace():
		messagebox.showwarning('WARNING','The table chosen will be dropped\nfrom the database permanently.\nContinue?')
		confirm=messagebox.askyesno('','Do you wish to drop the table \''+table.get()+'\'\nalong with its contents?')
		if confirm == True:
			sql=str('drop table '+table.get())
			cur.execute(sql)
			con.commit()
			messagebox.showinfo('','The table \''+table.get()+'\'\nhas been dropped\nfrom the database.')
		else:
			messagebox.showinfo('','DROP TABLE operation on \''+table.get()+'\' cancelled.\nThe database has not been modified.')
			pass
	else:
		messagebox.showerror('Error','Please choose a table.',parent=dbmainwin)

def deltb():
	if not table.get()=='' and not table.get().isspace():
		messagebox.showwarning('WARNING','All the contents of the table chosen will be deleted permanently.\nContinue?')
		confirm=messagebox.askyesno('','Do you wish to delete\nall records from the table \''+table.get()+'\'\n?')
		if confirm == True:
			sql=str('delete from '+table.get())
			cur.execute(sql)
			con.commit()
			messagebox.showinfo('','All records in table \''+table.get()+'\'\nhave been permenantly deleted\nfrom the database.')
		else:
			messagebox.showinfo('','DELETE FROM TABLE operation on \''+table.get()+'\' cancelled.\nThe database has not been modified.')
			pass
	else:
		messagebox.showerror('Error','Please choose a table.',parent=dbmainwin)

img6=tk.PhotoImage(file='monoico/icon-829.png')
tk.Label(dbmainwin,image=img6).grid(column=0,row=0,padx=10,pady=10)
tk.Label(dbmainwin,text=('View database'),font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)

tk.Label(dbmainwin,text=('Connected to database: '+con.database),font=('IBM Plex Sans',12),justify=tk.LEFT,fg='green').grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

tk.Label(dbmainwin,text='Choose a table.',font=fntit,justify=tk.LEFT).grid(column=1,row=4,sticky=tk.W,padx=10,pady=10)
img7=tk.PhotoImage(file='monoico/icon-830.png')
tk.Label(dbmainwin,image=img7).grid(column=0,row=4,sticky=tk.E,padx=10,pady=10)
n=tk.StringVar()
table=ttk.Combobox(dbmainwin,textvariable=n,font=fnt)
table.grid(row=5,column=1,padx=10,pady=10,sticky=tk.EW)
table['values']=b

tk.Label(dbmainwin,text='You can:',font=fntit,justify=tk.LEFT).grid(column=1,row=6,sticky=tk.W,padx=10,pady=10)

img8=tk.PhotoImage(file='monoico/icon-758.png')
tbviewbtn=tk.Button(dbmainwin,text='viewtable',image=img8,font=fnt,command=showtb)
tbviewbtn.grid(column=0,row=7,padx=10,pady=10)
tk.Label(dbmainwin,text='View the table.',font=fnt,fg='blue').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)

img10=tk.PhotoImage(file='monoico/icon-321.png')
deltbbtn=tk.Button(dbmainwin,text='deltable',image=img10,font=fnt,command=deltb)
deltbbtn.grid(column=0,row=8,padx=10,pady=10)
tk.Label(dbmainwin,text='Delete all the contents\nof the table.',font=fnt,justify=tk.LEFT).grid(column=1,row=8,padx=10,pady=10,sticky=tk.W)
tk.Message(dbmainwin,text='WARNING:\nThis will delete all the contents of the table chosen permanently.',font=fnt,fg='white',bg='orange').grid(column=1,row=9,padx=10,sticky=tk.W)

img11=tk.PhotoImage(file='monoico/icon-598.png')
deltbbtn=tk.Button(dbmainwin,text='droptable',image=img11,font=fnt,command=droptb)
deltbbtn.grid(column=2,row=8,padx=10,pady=10)
tk.Label(dbmainwin,text='Drop the table.',font=fnt,fg='red').grid(column=3,row=8,padx=10,pady=10,sticky=tk.W)
tk.Message(dbmainwin,text='WARNING:\nThis will drop the table chosen\nand its contents permanently.',font=fnt,fg='white',bg='red').grid(column=3,row=9,padx=10,sticky=tk.W)

def home():
	dbmainwin.destroy()
	os.system('python3 admin.py')

tk.Label(dbmainwin,text='or',font=fntit,justify=tk.LEFT).grid(column=1,row=15,sticky=tk.W,padx=10,pady=10)

img9=tk.PhotoImage(file='monoico/icon-714.png')
bkgbtn=tk.Button(dbmainwin,text='exit',image=img9,font=fnt,command=home)
bkgbtn.grid(column=0,row=16,padx=10,pady=10)
tk.Label(dbmainwin,text='Return home.',font=fnt).grid(column=1,row=16,padx=10,pady=10,sticky=tk.W)

def help():
	helpwin=tk.Toplevel()
	helpwin.resizable(False,False)
	helpwin.title('')

	img14=tk.PhotoImage(file='monoico/icon-595.png')
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

img12=tk.PhotoImage(file='monoico/icon-595.png')
bkgbtn=tk.Button(dbmainwin,text='help',image=img12,font=fnt,command=help)
bkgbtn.grid(column=2,row=16,padx=10,pady=10)
tk.Label(dbmainwin,text='Know the difference\nbetween DELETE FROM and DROP.',font=fnt,justify=tk.LEFT).grid(column=3,row=16,padx=10,pady=10,sticky=tk.W)

dbmainwin.mainloop()