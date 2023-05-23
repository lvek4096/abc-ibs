import mysql.connector as ms
import tkinter as tk
import os
from tkinter import messagebox

#mysql connection
con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
cur=con.cursor()

fnt=('IBM Plex Mono',12)
fntit=('IBM Plex Mono',12,'italic')
h1fnt=('IBM Plex Sans',24)

root=tk.Tk()
root.title('Admin menu')
root.resizable(False,False)

def logout():
	root.destroy()
	os.system('python3 emplogin.py')

def db():
	root.destroy()
	os.system('python3 db.py')

def emp():
	root.destroy()
	os.system('python3 manageemp.py')

def bookings():
	root.destroy()
	os.system('python3 adminbkgs.py')

def users():
	root.destroy()
	os.system('python3 manageusers.py')


tk.Label(root,text='Welcome',font=h1fnt).grid(column=1,row=0,padx=10,pady=10)
tk.Label(root,text='You can:',font=fntit).grid(column=1,row=2,sticky=tk.W,padx=10)
		
img6=tk.PhotoImage(file='monoico/icon-829.png')
bkgbtn=tk.Button(root,text='View the database',image=img6,font=fnt,command=db)
bkgbtn.grid(column=0,row=5,padx=10,pady=10)
tk.Label(root,text='View databases',font=fnt,fg='blue').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

img9=tk.PhotoImage(file='monoico/icon-306.png')
bkgbtn=tk.Button(root,text='Manage employees',image=img9,font=fnt,command=emp)
bkgbtn.grid(column=2,row=5,padx=10,pady=10)
tk.Label(root,text='Manage employees',font=fnt,fg='green').grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)

img10=tk.PhotoImage(file='monoico/icon-13.png')
bkgbtn=tk.Button(root,text='Bookings',image=img10,font=fnt,command=bookings)
bkgbtn.grid(column=0,row=6,padx=10,pady=10)
tk.Label(root,text='Make bookings',font=fnt).grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

img11=tk.PhotoImage(file='monoico/icon-675.png')
bkgbtn=tk.Button(root,text='Manage users',image=img11,font=fnt,command=users)
bkgbtn.grid(column=2,row=6,padx=10,pady=10)
tk.Label(root,text='Manage users',font=fnt).grid(column=3,row=6,padx=10,pady=10,sticky=tk.W)

tk.Label(root,text='or:',font=fntit).grid(column=1,row=9,padx=10,sticky=tk.W)

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

	tk.Label(passwd_win,text='Change the\nadministrator password',font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

	tk.Label(passwd_win,text='New password',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
	npass=tk.Entry(passwd_win,font=fnt,show='*')
	npass.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

	img13=tk.PhotoImage(file='monoico/icon-694.png')
	subbtn=tk.Button(passwd_win,text='submit',image=img13,font=fnt,command=chpasswd)
	subbtn.image=img13
	subbtn.grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)

img12=tk.PhotoImage(file='monoico/icon-79.png')
bkgbtn=tk.Button(root,text='root password',image=img12,font=fnt,command=chrootpasswd)
bkgbtn.grid(column=0,row=10,padx=10,pady=10)
tk.Label(root,text='Change the\nadministrator password',font=fnt,justify=tk.LEFT).grid(column=1,row=10,padx=10,pady=10,sticky=tk.W)

img7=tk.PhotoImage(file='monoico/icon-670.png')
bkgbtn=tk.Button(root,text='Logout',image=img7,font=fnt,command=logout)
bkgbtn.grid(column=0,row=11,padx=10,pady=10)
tk.Label(root,text='Logout',font=fnt).grid(column=1,row=11,padx=10,pady=10,sticky=tk.W)

img8=tk.PhotoImage(file='monoico/icon-66.png')
bkgbtn=tk.Button(root,text='Exit',image=img8,font=fnt,command=root.destroy)
bkgbtn.grid(column=2,row=11,padx=10,pady=10)
tk.Label(root,text='Logout and exit',font=fnt,fg='red').grid(column=3,row=11,padx=10,pady=10,sticky=tk.W)
root.mainloop()