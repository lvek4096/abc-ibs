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

manageuserwin=tk.Tk()
manageuserwin.title('Manage users')
w,h=manageuserwin.winfo_screenwidth(),manageuserwin.winfo_screenheight()
manageuserwin.geometry(str(w)+'x'+str(h))

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
	def getempinfo():
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

	img14=tk.PhotoImage(file='monoico/icon-716.png')
	img=tk.Label(frame1,image=img14,font=h1fnt)
	img.grid(column=0,row=0,padx=10,pady=10)
	img.image=img14

	tk.Label(frame1,font=h1fnt,text='View user details').grid(row=0,column=1,padx=10,pady=10,sticky=tk.W)

	tk.Label(frame1,font=fnt,text='Enter username.').grid(row=4,column=1,padx=10,pady=10,sticky=tk.W)
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

	def deleteemp():
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
				else:
					messagebox.showinfo('','User '+uname.get()+' not deleted.\nThe database has not been modified.',parent=delone_win)
			else:
				messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=delone_win)
		else:
			messagebox.showerror('','Please enter the username.',parent=delone_win)
	
	
		img14=tk.PhotoImage(file='monoico/icon-79.png')
	
	img14=tk.PhotoImage(file='monoico/icon-76.png')
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

	img13=tk.PhotoImage(file='monoico/icon-694.png')
	delbtn=tk.Button(delone_win,text='del',image=img13,font=fnt,command=deleteemp)
	delbtn.image=img13
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
				else:
					messagebox.showinfo('','Password for '+uname.get()+' has not been changed..\nThe databasehas not\nbeen modified.',parent=passwd_win)
			else:
				messagebox.showerror('Error','Username \''+uname.get()+'\' does not exist.',parent=passwd_win)
		else:
			messagebox.showerror('','Do not leave any fields blank.',parent=passwd_win)
	
	img14=tk.PhotoImage(file='monoico/icon-79.png')
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

	img13=tk.PhotoImage(file='monoico/icon-694.png')
	subbtn=tk.Button(passwd_win,text='submit',image=img13,font=fnt,command=chpasswd)
	subbtn.image=img13
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

	regsubimg=tk.PhotoImage(file='monoico/icon-67.png')	
	regsubmit=tk.Button(regwin,image=regsubimg,command=reguser)
	regsubmit.grid(column=1,row=14,padx=10,pady=10,sticky=tk.W)
	regsubmit.image=regsubimg
	
	regcloseimg=tk.PhotoImage(file='monoico/icon-66.png')
	regclose=tk.Button(regwin,text='Close',image=regcloseimg,command=regwin.destroy)
	regclose.grid(column=0,row=15,sticky=tk.SW,padx=10,pady=10)
	regclose.image=regcloseimg

tk.Grid.columnconfigure(manageuserwin,0,weight=1)

#FRAME 1
tk.Grid.rowconfigure(manageuserwin,0,weight=1)
f1=tk.Frame(manageuserwin)
f1.grid(row=0,column=0,sticky=tk.NSEW)

#frame 1 grid
tk.Grid.columnconfigure(f1,0,weight=1)
tk.Grid.columnconfigure(f1,1,weight=1)

tk.Grid.rowconfigure(f1,0,weight=1)
img6=tk.PhotoImage(file='monoico/icon-675.png')
tk.Label(f1,image=img6).grid(column=0,row=0,sticky=tk.E,padx=10,pady=10)
tk.Label(f1,text=('Manage the users...'),font=h1fnt).grid(column=1,row=0,sticky=tk.W,padx=10,pady=10)
#tk.Grid.rowconfigure(f1,1,weight=1)
tk.Label(f1,text=('Connected to database: '+con.database),font=('IBM Plex Sans',12),justify=tk.LEFT,fg='green').grid(column=1,row=1,sticky=tk.W,padx=10,pady=10)

#FRAME 2
tk.Grid.rowconfigure(manageuserwin,1,weight=1)
f2=tk.Frame(manageuserwin)
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
tk.Label(f2,text='View all user details.',font=fnt,fg='blue').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

img10=tk.PhotoImage(file='monoico/icon-716.png')
viewbtn=tk.Button(f2,text='viewone',image=img10,font=fnt,command=viewone)
viewbtn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
tk.Label(f2,text='View a single user\'s details.',font=fnt).grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)

#tk.Grid.rowconfigure(f2,6,weight=1)
img7=tk.PhotoImage(file='monoico/icon-67.png')
tbviewbtn=tk.Button(f2,text='add',image=img7,font=fnt,command=register)
tbviewbtn.grid(column=0,row=6,padx=10,pady=10,sticky=tk.E)
tk.Label(f2,text='Add a user.',font=fnt,fg='green').grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

img11=tk.PhotoImage(file='monoico/icon-79.png')
passbtn=tk.Button(f2,text='passwd',image=img11,font=fnt,command=passwd)
passbtn.grid(column=2,row=6,padx=10,pady=10,sticky=tk.E)
tk.Label(f2,text='Change the password for a user.',font=fnt).grid(column=3,row=6,padx=10,pady=10,sticky=tk.W)

#tk.Grid.rowconfigure(f2,7,weight=1)
img12=tk.PhotoImage(file='monoico/icon-76.png')
delbtn=tk.Button(f2,text='del',image=img12,font=fnt,command=delone)
delbtn.grid(column=0,row=7,padx=10,pady=10,sticky=tk.E)
tk.Label(f2,text='Delete a user.',font=fnt,fg='red').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)
#tk.Grid.rowconfigure(f2,8,weight=1)
tk.Message(f2,text='WARNING: This will delete\na user\'s profile\nfrom the system permanently.',width=500,font=fnt,fg='white',bg='red').grid(column=1,row=8,padx=10,pady=10,sticky=tk.NW)

def home():
	manageuserwin.destroy()
	os.system('python3 admin.py')
tk.Grid.rowconfigure(f2,15,weight=1)
tk.Label(f2,text='or:',font=fntit,justify=tk.LEFT).grid(column=1,row=15,sticky=tk.W,padx=10,pady=10)

tk.Grid.rowconfigure(f2,16,weight=1)
img9=tk.PhotoImage(file='monoico/icon-714.png')
bkgbtn=tk.Button(f2,text='exit',image=img9,font=fnt,command=home)
bkgbtn.grid(column=0,row=16,padx=10,pady=10,sticky=tk.E)
tk.Label(f2,text='Return home.',font=fnt).grid(column=1,row=16,padx=10,pady=10,sticky=tk.W)


manageuserwin.mainloop()