from curses.ascii import isspace
import tkinter as tk
import mysql.connector as ms

from tkinter import messagebox
import os

con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
cur=con.cursor()

#init GUI
logwin=tk.Tk()
logwin.title('Manage your profile...')
fnt=('IBM Plex Mono',12)
fntit=('IBM Plex Mono',12,'italic')
h1fnt=('IBM Plex Sans',24)
logwin.resizable(False, False)

def main_login():
	logwin.destroy()
	os.system('python3 login.py')

def login():
	def manage():
		def delete():
			def deluser():
				cur.execute('select uname,passwd from users')
				b=cur.fetchall()
				upass=dict(b)
				p=del_passwd.get()
				if not p=='' and not p.isspace():
					if p == upass[uname_inp]:
						confirm=messagebox.askyesno('','Really delete your user profile?',parent=delwin)
						if confirm==True:
							messagebox.showinfo('','Username '+uname_inp+' deleted.',parent=delwin)
							sql="delete from users where uname =%s"
							val=(uname_inp,)
							cur.execute(sql,val)
							con.commit()
						else:
							pass
					else:
						messagebox.showerror('Error','Invalid password entered.',parent=delwin)
				else:
					messagebox.showerror('Error','Please enter a password.',parent=delwin)
			
			delwin=tk.Toplevel()
			delwin.title('Delete User')
			delwin.resizable(False,False)
			tk.Label(delwin,text='Delete User',font=h1fnt).grid(column=0,row=0,padx=10,pady=10)
			#tk.Label(delwin,text='Enter the username which you wish to delete',font=fnt).grid(column=0,row=1,padx=10,pady=10)

			tk.Label(delwin,text='Please enter your password.',font=fnt).grid(column=0,row=4,sticky=tk.W,padx=10,pady=10)
			del_passwd=tk.Entry(delwin,show='*',font=fnt);del_passwd.grid(column=0,row=5,sticky=tk.EW,padx=10,pady=10)

			delsubimg=tk.PhotoImage(file='monoico/icon-722.png')
			delsubmit=tk.Button(delwin,image=delsubimg,command=deluser);delsubmit.grid(column=0,row=6,padx=10,pady=10)
			delsubmit.image=delsubimg
	
			delcloseimg=tk.PhotoImage(file='monoico/icon-66.png')
			delclose=tk.Button(delwin,text='Close',image=delcloseimg,command=delwin.destroy)
			delclose.grid(column=0,row=9,sticky=tk.SW,padx=10,pady=10)
			delclose.image=delcloseimg
			delwin.mainloop()

		def passwd():
			def changepass():
				cur.execute('select uname,passwd from users')
				b=cur.fetchall()
				upass=dict(b)
				op=old_pass.get()
				np=new_pass.get()
				if not np=='' and not np.isspace():
					if op == upass[uname_inp]:
						confirm=messagebox.askyesno('','Really change your password?',parent=passwin)
						if confirm==True:
							sql="update users set passwd=%s where uname=%s"
							val=(np,uname_inp)
							cur.execute(sql,val)
							con.commit()
							messagebox.showinfo('','Password updated.',parent=passwin)
						else:
							pass
					else:
						messagebox.showerror('Error','Invalid password entered.',parent=passwin)
				else:
					messagebox.showerror('Error','Please enter the new password.',parent=passwin)

			passwin=tk.Toplevel()
			passwin.title('Change Password')
			passwin.resizable(False,False)

			tk.Label(passwin,text='Changing password for '+uname_inp,font=('IBM Plex Sans',18)).grid(column=1,row=0,padx=10,pady=10)

			tk.Label(passwin,text='Current Password',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
			old_pass=tk.Entry(passwin,show='*',font=fnt);old_pass.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
			
			tk.Label(passwin,text='New Password',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
			new_pass=tk.Entry(passwin,show='*',font=fnt);new_pass.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)
			
			passsubimg=tk.PhotoImage(file='monoico/icon-86.png')
			passsubmit=tk.Button(passwin,image=passsubimg,command=changepass);passsubmit.grid(column=1,row=10,padx=10,pady=10,sticky=tk.W)
			
			delcloseimg=tk.PhotoImage(file='monoico/icon-66.png')
			delclose=tk.Button(passwin,text='Close',image=delcloseimg,command=passwin.destroy)
			delclose.grid(column=0,row=10,sticky=tk.SW,padx=10,pady=10)
			delclose.image=delcloseimg

			passwin.mainloop()

		def booking():
			manage_userswin.destroy()
			os.system('python3 home.py')

		def logout():
			manage_userswin.destroy()
			os.system('python3 start.py')
		cur.execute('select uname,uuid from users')
		uuidlist=dict(cur.fetchall())

		logwin.destroy()
		manage_userswin=tk.Tk()
		manage_userswin.title('Manage User')
		manage_userswin.resizable(False, False)
		tk.Label(manage_userswin,text=('Welcome, '+uname_inp),font=h1fnt).grid(column=1,row=0)
		tk.Label(manage_userswin,text=('ID: '+uuidlist[uname_inp]),font=('IBM Plex Sans',12)).grid(column=1,row=1)

		tk.Label(manage_userswin,text=('You can:'),font=fntit).grid(column=1,row=2)
		tk.Label(manage_userswin,text=('or:'),font=fntit).grid(column=3,row=2)
		
		img6=tk.PhotoImage(file='monoico/icon-693.png')
		bkgbtn=tk.Button(manage_userswin,text='Make a booking',image=img6,font=fnt,command=booking)
		bkgbtn.grid(column=2,row=5,padx=10,pady=10)
		tk.Label(manage_userswin,text='Make a booking',font=fnt,fg='green').grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)
		
		img4=tk.PhotoImage(file='monoico/icon-79.png')
		passbtn=tk.Button(manage_userswin,text='Change Password',image=img4,command=passwd)
		passbtn.grid(column=0,row=5,padx=10,pady=10)
		tk.Label(manage_userswin,text='Change your password',font=fnt).grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

		img3=tk.PhotoImage(file='monoico/icon-722.png')
		delusrbtn=tk.Button(manage_userswin,text='Remove User',image=img3,command=delete)
		delusrbtn.grid(column=0,row=6,padx=10,pady=10)
		tk.Label(manage_userswin,text='Delete your profile',font=fnt,fg='red').grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)
		
		img7=tk.PhotoImage(file='monoico/icon-670.png')
		logoutbtn=tk.Button(manage_userswin,text='Logout',font=fnt,image=img7,command=logout)
		logoutbtn.grid(column=2,row=6,padx=10,pady=10)
		tk.Label(manage_userswin,text='Logout',font=fnt).grid(column=3,row=6,padx=10,pady=10,sticky=tk.W)

		img8=tk.PhotoImage(file='monoico/icon-66.png')
		exitbtn=tk.Button(manage_userswin,text='Logout and exit',font=fnt,image=img8,command=manage_userswin.destroy)
		exitbtn.grid(column=2,row=7,padx=10,pady=10)
		tk.Label(manage_userswin,text='Logout and exit',font=fnt,fg='red').grid(column=3,row=7,padx=10,pady=10,sticky=tk.W)
		
		manage_userswin.mainloop()

	uname_inp=login_uname.get()
	passwd_inp=login_passwd.get()
	cur.execute('select uname,passwd from users')
	op=dict(cur.fetchall())

	if uname_inp not in op.keys():
		messagebox.showerror('Error','Username '+uname_inp+' does not exist.')
	else:
		if not passwd_inp == op[uname_inp]:
			messagebox.showerror('Error','Invalid password entered for '+uname_inp+'.')
		else:
			manage()

tk.Label(logwin,text='Login',font=h1fnt).grid(column=1,row=0)

tk.Label(logwin,text='Username',font=fnt).grid(column=0,row=3,sticky=tk.E,padx=10,pady=10)
login_uname=tk.Entry(logwin,font=fnt)
login_uname.grid(column=1,row=3,sticky=tk.EW,padx=10,pady=10)

tk.Label(logwin,text='Password',font=fnt).grid(column=0,row=4,sticky=tk.E,padx=10,pady=10)
login_passwd=tk.Entry(logwin,show='*',font=fnt)
login_passwd.grid(column=1,row=4,sticky=tk.EW,padx=10,pady=10)

img1=tk.PhotoImage(file='monoico/icon-669.png')
logsubmit=tk.Button(logwin,text='Login...',image=img1,command=login)
logsubmit.grid(column=1,row=5,padx=10,pady=10)
#tk.Label(logwin,text='Click to register ->',font=fnt).grid(column=1,row=8)

'''
img2=tk.PhotoImage(file='monoico/icon-67.png')
reg=tk.Button(logwin,text='Register',image=img2)
reg.grid(column=1,row=8,padx=10,pady=10)

img3=tk.PhotoImage(file='monoico/icon-722.png')
delusrbtn=tk.Button(logwin,text='Remove User',image=img3)
delusrbtn.grid(column=0,row=8,padx=10,pady=10)
'''

#img1=tk.PhotoImage(file='monoico/icon-669.png')
reg=tk.Button(logwin,text='Login or register...',font=fntit,command=main_login)
reg.grid(column=1,row=6,padx=10,pady=10)

#tk.Label(logwin,text=('Build '+build+' on\n'+pf.system()+' '+pf.release()),font=fntit).grid(column=0,row=12)
logwin.mainloop()