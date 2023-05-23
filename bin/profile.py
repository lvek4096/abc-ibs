import tkinter as tk
from tkinter import messagebox
import mysql.connector as ms
from tkinter import messagebox
import os
import home


con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
cur=con.cursor()

#init GUI
logwin=tk.Tk()
logwin.title('Manage your profile...')
w,h=logwin.winfo_screenwidth(),logwin.winfo_screenheight()
logwin.geometry(str(w)+'x'+str(h))
fnt=('IBM Plex Mono',12)
fntit=('IBM Plex Mono',12,'italic')
h1fnt=('IBM Plex Sans',24)

def main_login():
	logwin.destroy()
	os.system('python3 userlogin.py')


def onlogin():
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

			tk.Label(passwin,text='Changing password for '+fnamelist[uname_inp],font=('IBM Plex Sans',18)).grid(column=1,row=0,padx=10,pady=10)

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
			home.main()

		def logout():
			manage_userswin.destroy()
			os.system('python3 start.py')
		
		def info():
			chinfo_home=tk.Toplevel()
			chinfo_home.resizable(False,False)
			chinfo_home.title('')
			tk.Label(chinfo_home,text=('Change your\npersonal information'),font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,sticky=tk.W)
			
			def name():

				def chname():
					new_name=en1.get()

					if not new_name=='' and not new_name.isspace():
						sql="update users set fname=%s where uname like %s"
						val=(new_name,uname_inp)

						cur.execute(sql,val)
						con.commit()

						messagebox.showinfo('','Name successfully changed from '+fnamelist[uname_inp]+' to '+new_name+'.\nPlease log out for any changes to take effect.',parent=chinfo_name)
						tk.Label(chinfo_name,text='Please log out for\nany changes to take effect.',font=fnt,justify=tk.LEFT).grid(row=8,column=1,sticky=tk.W,padx=10,pady=10)
						chinfo_name.destroy()
					else:
						messagebox.showerror('','No new name has been specified.',parent=chinfo_name)
				chinfo_name=tk.Toplevel()
				chinfo_name.resizable(False,False)
				chinfo_name.title('')
				tk.Label(chinfo_name,text=('Change your display name'),font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,sticky=tk.W)
				#tk.Label(chinfo_name,text=(''),font=fnt,justify=tk.LEFT).grid(column=1,row=1,padx=10,sticky=tk.W)
				
				tk.Label(chinfo_name,text='Current name',font=fnt).grid(row=5,column=0,sticky=tk.E,padx=10,pady=10)
				tk.Label(chinfo_name,text=fnamelist[uname_inp],font=fnt).grid(row=5,column=1,sticky=tk.W,padx=10,pady=10)

				tk.Label(chinfo_name,text='New name',font=fnt).grid(row=6,column=0,sticky=tk.E,padx=10,pady=10)
				en1=tk.Entry(chinfo_name,font=fnt)
				en1.grid(row=6,column=1,sticky=tk.W,padx=10,pady=10)

				img10=tk.PhotoImage(file='monoico/icon-134.png')
				btn3=tk.Button(chinfo_name,image=img10,command=chname)
				btn3.image=img10
				btn3.grid(row=10,column=1,padx=10,pady=10,sticky=tk.W)
			
			def contacts():
				def chcontacts():
					new_email=en2.get()
					new_num=en3.get()
				
					def conf():
						tk.Label(chinfo_contacts,text='Please log out for\nany changes to take effect.',font=fnt,justify=tk.LEFT).grid(row=10,column=1,sticky=tk.W,padx=10,pady=10)
						chinfo_contacts.destroy()
						
					if (not new_num=='' and not new_num.isspace()) or (not new_email=='' and not new_email.isspace()):
						if new_num=='' or new_num.isspace():
							if '@' in new_email and '.' in new_email:
								sql='update users set email=%s where uname like %s' 
								val=(new_email,uname_inp)
								cur.execute(sql,val)
								con.commit()
								messagebox.showinfo('','Electronic mail address changed successfully to '+new_email+'.\nPlease log out for any changes to take effect.',parent=chinfo_contacts)
								conf()							
							else:
								messagebox.showerror('Error','Invalid electronic mail entered',parent=chinfo_contacts)
						elif new_email=='' or new_email.isspace():
							if len(new_num)==10:
								sql='update users set num=%s where uname like %s' 
								val=(new_num,uname_inp)
								cur.execute(sql,val)
								con.commit()
								messagebox.showinfo('','Phone number changed successfully to '+new_num+'.\nPlease log out for any changes to take effect.',parent=chinfo_contacts)
								conf()						
							else:
								messagebox.showerror('Error','Invalid phone number entered',parent=chinfo_contacts)
						elif (not new_num=='' and not new_num.isspace()) and (not new_email=='' and not new_email.isspace()):
							if ('@' in new_email and '.' in new_email) and (len(new_num)==10):
								sql='update users set email=%s where uname like %s' 
								val=(new_email,uname_inp)
								cur.execute(sql,val)
								con.commit()

								sql='update users set num=%s where uname like %s' 
								val=(new_num,uname_inp)
								cur.execute(sql,val)
								con.commit()
								messagebox.showinfo('','Electronic mail address and phone number changed successfully to '+new_email+' and '+new_num+', respectively.\nPlease log out for any changes to take effect.',parent=chinfo_contacts)
								conf()							
							else:
								messagebox.showerror('Error','Invalid electronic mail or phone number entered',parent=chinfo_contacts)
					else:
						messagebox.showerror('Error','Please fill at least one field.',parent=chinfo_contacts)

				cur.execute('select uname,email from users')
				a=dict(cur.fetchall())

				cur.execute('select uname,num from users')
				b=dict(cur.fetchall())

				chinfo_contacts=tk.Toplevel()
				chinfo_contacts.resizable(False,False)
				chinfo_contacts.title('')
				tk.Label(chinfo_contacts,text=('Change your contact details'),font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,sticky=tk.W)
				tk.Label(chinfo_contacts,text='If you do not wish to change a\nparticular contact, then leave the\ncorresponding field blank.',font=fnt,justify=tk.LEFT).grid(row=2,column=1,sticky=tk.W,padx=10,pady=10)
				tk.Label(chinfo_contacts,text='Current\nelectronic mail address',font=fnt,justify=tk.RIGHT).grid(row=5,column=0,sticky=tk.E,padx=10,pady=10)
				tk.Label(chinfo_contacts,text=a[uname_inp],font=fnt).grid(row=5,column=1,sticky=tk.W,padx=10,pady=10)

				tk.Label(chinfo_contacts,text='New\nelectronic mail address',font=fnt,justify=tk.RIGHT).grid(row=6,column=0,sticky=tk.E,padx=10,pady=10)
				en2=tk.Entry(chinfo_contacts,font=fnt)
				en2.grid(row=6,column=1,sticky=tk.EW,padx=10,pady=10)

				tk.Label(chinfo_contacts,text='Current phone number',font=fnt).grid(row=7,column=0,sticky=tk.E,padx=10,pady=10)
				tk.Label(chinfo_contacts,text=b[uname_inp],font=fnt).grid(row=7,column=1,sticky=tk.W,padx=10,pady=10)

				tk.Label(chinfo_contacts,text='New phone number',font=fnt).grid(row=8,column=0,sticky=tk.E,padx=10,pady=10)
				en3=tk.Entry(chinfo_contacts,font=fnt)
				en3.grid(row=8,column=1,sticky=tk.EW,padx=10,pady=10)

				img10=tk.PhotoImage(file='monoico/icon-134.png')
				btn3=tk.Button(chinfo_contacts,image=img10,command=chcontacts)
				btn3.image=img10
				btn3.grid(row=15,column=1,padx=10,pady=10,sticky=tk.W)

			img1=tk.PhotoImage(file='monoico/icon-302.png')
			btn1=tk.Button(chinfo_home,text='Name',image=img1,command=name)
			btn1.image=img1
			btn1.grid(column=0,row=3,padx=10,pady=10,sticky=tk.E)
			tk.Label(chinfo_home,text='Change your display name',font=fnt,justify=tk.LEFT).grid(column=1,row=3,padx=10,pady=10,sticky=tk.W)

			img2=tk.PhotoImage(file='monoico/icon-666.png')
			btn2=tk.Button(chinfo_home,text='Contact',image=img2,command=contacts)
			btn2.image=img2
			btn2.grid(column=0,row=6,padx=10,pady=10,sticky=tk.E)
			tk.Label(chinfo_home,text='Change your contact details',font=fnt).grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

		cur.execute('select uname,uuid from users')
		uuidlist=dict(cur.fetchall())
		cur.execute('select uname,fname from users')
		fnamelist=dict(cur.fetchall())
		
		logwin.destroy()

		manage_userswin=tk.Tk()
		manage_userswin.title('Manage your profile')
		w,h=manage_userswin.winfo_screenwidth(),manage_userswin.winfo_screenheight()
		manage_userswin.geometry(str(w)+'x'+str(h))
		
		tk.Grid.columnconfigure(manage_userswin,0,weight=1)
		
		#FRAME 1
		tk.Grid.rowconfigure(manage_userswin,0,weight=1)
		f1=tk.Frame(manage_userswin)
		f1.grid(row=0,column=0,sticky=tk.NSEW)

		#frame 1 grid
		tk.Grid.columnconfigure(f1,0,weight=1)
		
		tk.Grid.rowconfigure(f1,0,weight=1)
		tk.Label(f1,text=('Welcome, '+fnamelist[uname_inp]),font=h1fnt).grid(column=0,row=0,padx=10,sticky=tk.EW)
		tk.Label(f1,text=('ID: '+uuidlist[uname_inp]),font=('IBM Plex Sans',12)).grid(column=0,row=1,padx=10,sticky=tk.EW)

		#FRAME 2
		tk.Grid.rowconfigure(manage_userswin,1,weight=1)
		f2=tk.Frame(manage_userswin)
		f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

		#frame 2 grid
		tk.Grid.columnconfigure(f2,0,weight=1)
		tk.Grid.columnconfigure(f2,1,weight=1)
		tk.Grid.columnconfigure(f2,2,weight=1)
		tk.Grid.columnconfigure(f2,3,weight=1)

		tk.Grid.rowconfigure(f2,2,weight=1)
		tk.Label(f2,text=('You can:'),font=fntit).grid(column=1,row=2,padx=10,pady=10,sticky=tk.W)
		
		img4=tk.PhotoImage(file='monoico/icon-79.png')
		passbtn=tk.Button(f2,text='Change Password',image=img4,command=passwd)
		passbtn.grid(column=0,row=5,padx=10,pady=10,sticky=tk.E)
		tk.Label(f2,text='Change your password.',font=fnt).grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

		img9=tk.PhotoImage(file='monoico/icon-86.png')
		delusrbtn=tk.Button(f2,text='Manage Personal Info',image=img9,command=info)
		delusrbtn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
		tk.Label(f2,text='Change your personal information.',font=fnt,justify=tk.LEFT).grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)

		img3=tk.PhotoImage(file='monoico/icon-722.png')
		delusrbtn=tk.Button(f2,text='Remove User',image=img3,command=delete)
		delusrbtn.grid(column=0,row=6,padx=10,pady=10,sticky=tk.E)
		tk.Label(f2,text='Delete your profile.',font=fnt,fg='red').grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)
		
		tk.Grid.rowconfigure(f2,9,weight=1)
		tk.Label(f2,text=('or:'),font=fntit).grid(column=1,row=9,padx=10,sticky=tk.W)

		img7=tk.PhotoImage(file='monoico/icon-670.png')
		logoutbtn=tk.Button(f2,text='Logout',font=fnt,image=img7,command=logout)
		logoutbtn.grid(column=0,row=11,padx=10,pady=10,sticky=tk.E)
		tk.Label(f2,text='Logout',font=fnt).grid(column=1,row=11,padx=10,pady=10,sticky=tk.W)

		img8=tk.PhotoImage(file='monoico/icon-66.png')
		exitbtn=tk.Button(f2,text='Logout and exit',font=fnt,image=img8,command=manage_userswin.destroy)
		exitbtn.grid(column=2,row=11,padx=10,pady=10,sticky=tk.E)
		tk.Label(f2,text='Logout and exit',font=fnt,fg='red').grid(column=3,row=11,padx=10,pady=10,sticky=tk.W)
		
		manage_userswin.mainloop()

	uname_inp=login_uname.get()
	passwd_inp=login_passwd.get()
	cur.execute('select uname,passwd from users')
	op=dict(cur.fetchall())

	cur.execute('select uname,fname from users')
	fnamelist=dict(cur.fetchall())

	if uname_inp not in op.keys():
		messagebox.showerror('Error','Username \''+uname_inp+'\' does not exist.')
	else:
		if not passwd_inp == op[uname_inp]:
			messagebox.showerror('Error','Invalid password entered for '+fnamelist[uname_inp]+'.')
		else:
			manage()

tk.Grid.columnconfigure(logwin,0,weight=1)

#FRAME 3
tk.Grid.rowconfigure(logwin,0,weight=1)
f3=tk.Frame(logwin)
f3.grid(row=0,column=0,sticky=tk.NSEW)

#frame 3 grid
tk.Grid.columnconfigure(f3,0,weight=1)

tk.Grid.rowconfigure(f3,0,weight=1)
tk.Label(logwin,text='Login',font=h1fnt).grid(column=0,row=0)

#FRAME 4
tk.Grid.rowconfigure(logwin,1,weight=1)
f4=tk.Frame(logwin)
f4.grid(row=1,column=0,sticky=tk.NSEW,padx=10,pady=10)

#frame 4 grid
tk.Grid.columnconfigure(f4,0,weight=1)
tk.Grid.columnconfigure(f4,1,weight=1)

#tk.Grid.rowconfigure(f4,3,weight=1)
tk.Label(f4,text='Username',font=fnt).grid(column=0,row=3,padx=10,pady=10,sticky=tk.E)
login_uname=tk.Entry(f4,font=fnt)
login_uname.grid(column=1,row=3,padx=10,pady=10,sticky=tk.W)

#tk.Grid.rowconfigure(f4,4,weight=1)
tk.Label(f4,text='Password',font=fnt,justify=tk.CENTER).grid(column=0,row=4,padx=10,pady=10,sticky=tk.E)
login_passwd=tk.Entry(f4,show='*',font=fnt)
login_passwd.grid(column=1,row=4,padx=10,pady=10,sticky=tk.W)

#tk.Grid.rowconfigure(f4,5,weight=1)
img1=tk.PhotoImage(file='monoico/icon-669.png')
logsubmit=tk.Button(f4,text='Login...',image=img1,command=onlogin)
logsubmit.grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

tk.Grid.rowconfigure(f4,6,weight=1)
reg=tk.Button(f4,text='Login or register...',font=fntit,command=main_login)
reg.grid(column=1,row=6,padx=10,pady=1,sticky=tk.W)

logwin.mainloop()