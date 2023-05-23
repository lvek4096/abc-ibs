#Modules for GUI

import tkinter as tk
from tkinter.ttk import Separator
from tkinter import messagebox

#Module for DBMS connectivity
import mysql.connector as ms

#Other modules
import random as rd
import platform as pf
import ctypes
import os

#Imports other Python scripts
import init
import sysinfo
import bookings

init.initdb()

#Mysql connection
try:
	con=ms.connect(host='192.168.0.175',user='dbms',password='123456',database='taxi')
except:
	con=ms.connect(host='localhost',user='root',password='123456',database='taxi')

cur=con.cursor()

#Initialise the UI

welcome=tk.Tk()
welcome.title('Welcome to ABC Lines')

fnt=('Cascadia Mono',12)
fntit=('Cascadia Mono',12,'italic')
h1fnt=('Segoe UI Variable Display Semibold',24)
h2fnt=('Segoe UI Variable Text',12)
menufnt=('Cascadia Mono',11)

if pf.system()=='Windows':
	try:
		ctypes.windll.shcore.SetProcessDpiAwareness(True)
	except:
		pass
try:
	welcome.state('zoomed')
except:		
	w,h=welcome.winfo_screenwidth(),welcome.winfo_screenheight()
	welcome.geometry(str(w)+'x'+str(h))
icon=tk.PhotoImage(file='img/icon.png')
welcome.iconphoto(False,icon)

tk.Grid.columnconfigure(welcome,0,weight=1)

# definitions
def main_login():		#make bookings
	welcome.destroy()
		
	#init GUI
	logwin=tk.Tk()
	logwin.title('Make bookings')

	icon=tk.PhotoImage(file='img/icon.png')
	logwin.iconphoto(False,icon)

	#Maximises windows
	try:
		logwin.state('zoomed')
	except:		
		w,h=logwin.winfo_screenwidth(),logwin.winfo_screenheight()
		logwin.geometry(str(w)+'x'+str(h))

	#login
	def onlogin():
		#Main menu
		def main():
			#functions
			def book_taxi():	#Opens taxi booking window.
				bookings.taxi()

			def book_bus():		#Opens bus booking window
				bookings.bus()

			def about_this_program():
				sysinfo.about()

			def logout():	#Logs out and returns to the start page.
				main_menu.destroy()
				os.system('python3 start.py')

			main_menu=tk.Tk()
			main_menu.title('Main Menu')
			icon=tk.PhotoImage(file='img/icon.png')
			main_menu.iconphoto(False,icon)
			try:
				main_menu.state('zoomed')
			except:
				w,h=main_menu.winfo_screenwidth(),main_menu.winfo_screenheight()
				main_menu.geometry(str(w)+'x'+str(h))

			menubar=tk.Menu(main_menu)

			more=tk.Menu(menubar,tearoff=0)
			menubar.add_cascade(label='Info',menu=more,font=menufnt)
			more.add_command(label='About this program...',command=about_this_program,font=menufnt,underline=0)
			main_menu.config(menu=menubar)

			tk.Grid.columnconfigure(main_menu,0,weight=1)

			#FRAME 1
			tk.Grid.rowconfigure(main_menu,0,weight=1)
			f1=tk.Frame(main_menu,bg='#283593')
			f1.grid(row=0,column=0,sticky=tk.NSEW)

			#frame 1 grid
			tk.Grid.columnconfigure(f1,0,weight=1)

			cur.execute('select uname,fname from users')
			a=dict(cur.fetchall())
			cur.execute('select uname,uuid from users')
			uuidlist=dict(cur.fetchall())

			tk.Grid.rowconfigure(f1,0,weight=1)
			tk.Grid.rowconfigure(f1,1,weight=1)
			tk.Grid.rowconfigure(f1,2,weight=1)

			logo_img=tk.PhotoImage(file='img/logo.png')
			logo=tk.Label(f1,image=logo_img,fg='white',bg='#283593')
			logo.grid(column=0,row=0,padx=10,pady=10,sticky=tk.EW)
			logo.image=logo_img

			tk.Label(f1,text='Welcome, '+a[uname_inp],font=h1fnt,fg='white',bg='#283593').grid(column=0,row=1)
			tk.Label(f1,text=('ID: '+uuidlist[uname_inp]),font=h2fnt,fg='black',bg='#00e676').grid(column=0,row=2,padx=10)
			
			
			Separator(f1,orient='horizontal').grid(column=0,row=3,sticky=tk.EW,padx=10,pady=10)

			#FRAME 2
			tk.Grid.rowconfigure(main_menu,1,weight=1)
			f2=tk.Frame(main_menu)
			f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

			#frame 2 grid
			tk.Grid.columnconfigure(f2,0,weight=1)
			tk.Grid.columnconfigure(f2,1,weight=1)
			tk.Grid.columnconfigure(f2,2,weight=1)
			tk.Grid.columnconfigure(f2,3,weight=1)


			tk.Label(f2,text=('You can:'),font=fntit).grid(column=1,row=2,padx=10,pady=10,sticky=tk.W)

			tk.Grid.rowconfigure(f2,5,weight=1)
			#Book Taxi
			img6=tk.PhotoImage(file='icons/taxi.png')
			bkgbtn=tk.Button(f2,text='Book taxi',image=img6,font=fnt,command=book_taxi)
			bkgbtn.grid(column=0,row=5,padx=10,pady=10,sticky=tk.E)
			tk.Label(f2,text='Book a taxi.',font=fnt,bg='yellow').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

			#Book Bus
			img4=tk.PhotoImage(file='icons/bus.png')
			passbtn=tk.Button(f2,text='Book Bus',image=img4,command=book_bus)
			passbtn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
			tk.Label(f2,text='Book a bus.',font=fnt,fg='blue').grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)


			tk.Label(f2,text=('or:'),font=fntit).grid(column=1,row=9,padx=10,sticky=tk.W)

			tk.Grid.rowconfigure(f2,11,weight=1)
			#Logout
			img7=tk.PhotoImage(file='icons/logout.png')
			logoutbtn=tk.Button(f2,text='Logout',font=fnt,image=img7,command=logout)
			logoutbtn.grid(column=0,row=11,padx=10,pady=10,sticky=tk.E)
			tk.Label(f2,text='Logout',font=fnt).grid(column=1,row=11,padx=10,pady=10,sticky=tk.W)


			#Logout and Exit
			img8=tk.PhotoImage(file='icons/close.png')
			exitbtn=tk.Button(f2,text='Logout and exit',font=fnt,image=img8,command=main_menu.destroy)
			exitbtn.grid(column=2,row=11,padx=10,pady=10,sticky=tk.E)
			tk.Label(f2,text='Logout and exit',font=fnt,fg='red').grid(column=3,row=11,padx=10,pady=10,sticky=tk.W)

			tk.Grid.rowconfigure(f2,12,weight=1)
			main_menu.mainloop()

		uname_inp=login_uname.get()
		passwd_inp=login_passwd.get()
		cur.execute('select uname,passwd from users')
		op=dict(cur.fetchall())

		cur.execute('select uname,fname from users')
		fnamelist=dict(cur.fetchall())

		if (not uname_inp=='' and not uname_inp.isspace()) and (not passwd_inp=='' and not passwd_inp.isspace()):
			if uname_inp not in op.keys():
				messagebox.showerror('Error','Username \''+uname_inp+'\' does not exist.')
			else:
				if not passwd_inp == op[uname_inp]:
					messagebox.showerror('Error','Invalid password entered for '+fnamelist[uname_inp]+'.')
				else:
					logwin.destroy()
					main()
		else:
			messagebox.showerror('Error','Please do not leave any fields blank.')

	#Register user
	def register():
		uuid='U'+str(rd.randint(10000,99999))
		#Adds user to DB
		def reguser():
			
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

							messagebox.showinfo('','The new user '+reg_fname_inp+'\nhas been successfully registered.',parent=logwin)
							logwin.destroy()
						else:
							messagebox.showerror('Error','Invalid phone number entered.',parent=logwin)
					else:
						messagebox.showerror('Error','Invalid electronic mail ID entered.',parent=logwin)		
				else:
					messagebox.showerror('Error','Username '+reg_uname_inp+'\nalready exists.',parent=logwin)
				
			else:
				messagebox.showerror('Error','Please do not leave any fields blank.',parent=logwin)
		
		logwin=tk.Toplevel()
		logwin.title('Register')
		logwin.resizable(False, False)
		icon=tk.PhotoImage(file='img/icon.png')
		logwin.iconphoto(False,icon)

		tk.Label(logwin,text='Register',font=h1fnt).grid(column=0,row=0,padx=10,pady=10,columnspan=2,sticky=tk.EW)
		
		tk.Label(logwin,text='ID',font=fnt).grid(column=0,row=3,sticky=tk.E,padx=10,pady=10)
		tk.Label(logwin,text=uuid,font=fnt).grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)
		
		tk.Label(logwin,text='1. Personal info',font=fntit).grid(column=0,row=5,sticky=tk.W,padx=10,pady=10)

		tk.Label(logwin,text='Name',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
		reg_fname=tk.Entry(logwin,font=fnt)
		reg_fname.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)

		tk.Label(logwin,text='Electronic mail ID',font=fnt).grid(column=0,row=7,sticky=tk.E,padx=10,pady=10)
		reg_email=tk.Entry(logwin,font=fnt)
		reg_email.grid(column=1,row=7,sticky=tk.EW,padx=10,pady=10)

		tk.Label(logwin,text='Phone number',font=fnt).grid(column=0,row=8,sticky=tk.E,padx=10,pady=10)
		reg_num=tk.Entry(logwin,font=fnt)
		reg_num.grid(column=1,row=8,sticky=tk.EW,padx=10,pady=10)

		tk.Label(logwin,text='2. Login info',font=fntit).grid(column=0,row=10,sticky=tk.W,padx=10,pady=10)

		tk.Label(logwin,text='Username',font=fnt).grid(column=0,row=11,sticky=tk.E,padx=10,pady=10)
		reg_uname=tk.Entry(logwin,font=fnt)
		reg_uname.grid(column=1,row=11,sticky=tk.EW,padx=10,pady=10)

		tk.Label(logwin,text='Password',font=fnt).grid(column=0,row=12,sticky=tk.E,padx=10,pady=10)
		reg_passwd=tk.Entry(logwin,show='*',font=fnt)
		reg_passwd.grid(column=1,row=12,sticky=tk.EW,padx=10,pady=10)

		regsubmit=tk.Button(logwin,text='Register',command=reguser,font=fntit)
		regsubmit.grid(column=1,row=14,padx=10,pady=10,sticky=tk.W)
		logwin.bind('<Return>',lambda event:reguser())
	#Opens manage profile window
	def manage_profile():
		logwin.destroy()
		manage_user_profile()

	#Window
	tk.Grid.columnconfigure(logwin,0,weight=1)

	#FRAME 1
	tk.Grid.rowconfigure(logwin,0,weight=1)
	f1=tk.Frame(logwin,bg='#283593')
	f1.grid(row=0,column=0,sticky=tk.NSEW)

	#frame 1 grid
	tk.Grid.columnconfigure(f1,0,weight=1)

	tk.Grid.rowconfigure(f1,0,weight=1)
	tk.Label(f1,text='Login',font=h1fnt,fg='white',bg='#283593').grid(column=0,row=0)
	Separator(f1,orient='horizontal').grid(row=1,column=0,sticky=tk.EW,padx=10,pady=10)

	#FRAME 2
	tk.Grid.rowconfigure(logwin,1,weight=1)
	f2=tk.Frame(logwin)
	f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

	#frame 2 grid
	tk.Grid.columnconfigure(f2,0,weight=1)
	tk.Grid.columnconfigure(f2,1,weight=1)

	tk.Label(f2,text='Username',font=fnt).grid(column=0,row=3,padx=10,pady=10,sticky=tk.E)
	login_uname=tk.Entry(f2,font=fnt)
	login_uname.grid(column=1,row=3,sticky=tk.W,padx=10,pady=10)

	tk.Label(f2,text='Password',font=fnt).grid(column=0,row=4,padx=10,pady=10,sticky=tk.E)
	login_passwd=tk.Entry(f2,show='*',font=fnt)
	login_passwd.grid(column=1,row=4,sticky=tk.W,padx=10,pady=10)

	img1=tk.PhotoImage(file='icons/login.png')
	logsubmit=tk.Button(f2,text='Login...',image=img1,command=onlogin)
	logsubmit.grid(column=1,row=10,padx=10,pady=10,sticky=tk.W)

	tk.Grid.rowconfigure(f2,12,weight=2)
	tk.Label(f2,text='New here?\nClick here to register.',font=fntit,justify=tk.RIGHT,fg='#283593').grid(column=0,row=12,padx=10,pady=10,sticky=tk.E)
	img2=tk.PhotoImage(file='icons/adduser.png')
	reg=tk.Button(f2,text='Register',image=img2,command=register)
	reg.grid(column=1,row=12,padx=10,pady=10,sticky=tk.W)

	manage=tk.Button(f2,text='Manage your profile...',font=fntit,command=manage_profile)
	manage.grid(column=1,row=11,padx=10,pady=10,columnspan=2,sticky=tk.W)

	logwin.bind('<Return>',lambda event:onlogin())
	logwin.mainloop()

def manage_user_profile():		#manages profile
	welcome.destroy()

	#init GUI
	logwin=tk.Tk()
	logwin.title('Manage profile')
	icon=tk.PhotoImage(file='img/icon.png')
	logwin.iconphoto(False,icon)


	try:
		logwin.state('zoomed')
	except:
		w,h=logwin.winfo_screenwidth(),logwin.winfo_screenheight()
		logwin.geometry(str(w)+'x'+str(h))


	def bookings_login():
		logwin.destroy()
		main_login()
	
	def onlogin():
		def manage(): #Manage user window

			def delete():	#Delete function
				cur.execute('select uname,fname from users')
				a=cur.fetchall()
				user_namelist=dict(a)				
				def deluser():	#Delete user from DB
					cur.execute('select uname,passwd from users')
					b=cur.fetchall()
					upass=dict(b)
					p=del_passwd.get()
					
					if not p=='' and not p.isspace():
						if p == upass[uname_inp]:
							confirm=messagebox.askyesno('','Really delete your user profile?',parent=delwin)
							if confirm==True:
								sql="delete from users where uname =%s"
								val=(uname_inp,)
								cur.execute(sql,val)
								con.commit()
								messagebox.showinfo('','User '+user_namelist[uname_inp]+' deleted.\nYou will be returned to the start page.',parent=delwin)
								delwin.destroy()
								manage_userswin.destroy()
								os.system('python3 start.py')
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

				tk.Label(delwin,text='Please enter the password.',font=fnt).grid(column=0,row=4,sticky=tk.W,padx=10,pady=10)
				del_passwd=tk.Entry(delwin,show='*',font=fnt);del_passwd.grid(column=0,row=5,sticky=tk.EW,padx=10,pady=10)

				delsubmit=tk.Button(delwin,text='Delete User',command=deluser,font=fntit,fg='red');delsubmit.grid(column=0,row=6,padx=10,pady=10)
				delwin.bind('<Return>',lambda event:deluser())
				
			def passwd():	#Change password function
				def chpasswd():		#Changes passwd in DB.
					cur.execute('select uname,passwd from users')
					b=cur.fetchall()
					upass=dict(b)
					op=old_pass.get()
					np=new_pass.get()
					if (not np=='' and not np.isspace()) and (not op=='' and not op.isspace()):
						if op == upass[uname_inp]:
							confirm=messagebox.askyesno('','Really change your password?',parent=passwin)
							if confirm==True:
								sql="update users set passwd=%s where uname=%s"
								val=(np,uname_inp)
								cur.execute(sql,val)
								con.commit()
								messagebox.showinfo('','Password updated.',parent=passwin)
								passwin.destroy()
							else:
								pass
						else:
							messagebox.showerror('Error','Invalid old password entered.',parent=passwin)
					else:
						messagebox.showerror('Error','Please do not leave any fields blank.',parent=passwin)

				passwin=tk.Toplevel()
				passwin.title('Change Password')
				passwin.resizable(False,False)
				icon=tk.PhotoImage(file='img/icon.png')
				passwin.iconphoto(False,icon)


				tk.Label(passwin,text='Changing password for '+fnamelist[uname_inp],font=(h1fnt,18)).grid(column=1,row=0,padx=10,pady=10)

				tk.Label(passwin,text='Current Password',font=fnt).grid(column=0,row=5,sticky=tk.E,padx=10,pady=10)
				old_pass=tk.Entry(passwin,show='*',font=fnt);old_pass.grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)
				
				tk.Label(passwin,text='New Password',font=fnt).grid(column=0,row=6,sticky=tk.E,padx=10,pady=10)
				new_pass=tk.Entry(passwin,show='*',font=fnt);new_pass.grid(column=1,row=6,sticky=tk.EW,padx=10,pady=10)
				
				passsubmit=tk.Button(passwin,text='Change password',command=chpasswd,font=fntit)
				passsubmit.grid(column=1,row=10,padx=10,pady=10,sticky=tk.W)
				passwin.bind('<Return>',lambda event:chpasswd())
				
			def logout():	#Logs out
				manage_userswin.destroy()
				os.system('python3 start.py')
			
			def info():		#Changes personal information.
				chinfo_home=tk.Toplevel()
				chinfo_home.resizable(False,False)
				chinfo_home.title('Change personal information')
				icon=tk.PhotoImage(file='img/icon.png')
				chinfo_home.iconphoto(False,icon)

				tk.Label(chinfo_home,text=('Change your\npersonal information'),font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,sticky=tk.W)
				
				def name():		#Change full (display) name

					def chname():		#Changes full name in DB
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
					chinfo_name.title('Change display name...')
					icon=tk.PhotoImage(file='img/icon.png')
					chinfo_name.iconphoto(False,icon)

					tk.Label(chinfo_name,text=('Change your display (full) name'),font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,sticky=tk.W)
					
					tk.Label(chinfo_name,text='Current name',font=fnt).grid(row=5,column=0,sticky=tk.E,padx=10,pady=10)
					tk.Label(chinfo_name,text=fnamelist[uname_inp],font=fnt).grid(row=5,column=1,sticky=tk.W,padx=10,pady=10)

					tk.Label(chinfo_name,text='New name',font=fnt).grid(row=6,column=0,sticky=tk.E,padx=10,pady=10)
					en1=tk.Entry(chinfo_name,font=fnt)
					en1.grid(row=6,column=1,sticky=tk.W,padx=10,pady=10)

					btn3=tk.Button(chinfo_name,text='Make changes',font=fntit,command=chname)
					btn3.grid(row=10,column=1,padx=10,pady=10,sticky=tk.W)

					#Binds Enter key to submit function
					chinfo_name.bind('<Return>',lambda event:chname())

				def contacts():		#Change contact info
					def chcontacts():	#Changes email or phone number in DB
						new_email=en2.get()
						new_num=en3.get()
					
						def changes_confirmed():
							# tk.Label(chinfo_contacts,text='Please log out for\nany changes to take effect.',font=fnt,justify=tk.LEFT).grid(row=10,column=1,sticky=tk.W,padx=10,pady=10)
							chinfo_contacts.destroy()
							
						if (not new_num=='' and not new_num.isspace()) or (not new_email=='' and not new_email.isspace()):
							if new_num=='' or new_num.isspace():
								if '@' in new_email and '.' in new_email:
									sql='update users set email=%s where uname like %s' 
									val=(new_email,uname_inp)
									cur.execute(sql,val)
									con.commit()
									messagebox.showinfo('','Electronic mail address changed successfully to '+new_email+'.',parent=chinfo_contacts)
									changes_confirmed()							
								else:
									messagebox.showerror('Error','Invalid electronic mail entered.',parent=chinfo_contacts)
							elif new_email=='' or new_email.isspace():
								if len(new_num)==10:
									sql='update users set num=%s where uname like %s' 
									val=(new_num,uname_inp)
									cur.execute(sql,val)
									con.commit()
									messagebox.showinfo('','Phone number changed successfully to '+new_num+'.',parent=chinfo_contacts)
									changes_confirmed()						
								else:
									messagebox.showerror('Error','Invalid phone number entered.',parent=chinfo_contacts)
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
									messagebox.showinfo('','Electronic mail address and phone number changed successfully to '+new_email+' and '+new_num+', respectively.',parent=chinfo_contacts)
									changes_confirmed()							
								else:
									messagebox.showerror('Error','Invalid electronic mail or phone number entered.',parent=chinfo_contacts)
						else:
							messagebox.showerror('Error','Please fill at least one field.',parent=chinfo_contacts)

					cur.execute('select uname,email from users')
					a=dict(cur.fetchall())

					cur.execute('select uname,num from users')
					b=dict(cur.fetchall())

					chinfo_contacts=tk.Toplevel()
					chinfo_contacts.resizable(False,False)
					icon=tk.PhotoImage(file='img/icon.png')
					chinfo_contacts.iconphoto(False,icon)

					chinfo_contacts.title('Change contact details...')
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

					btn3=tk.Button(chinfo_contacts,text='Make changes',font=fntit,command=chcontacts)
					btn3.grid(row=15,column=1,padx=10,pady=10,sticky=tk.W)

					#Binds Enter key to submit function
					chinfo_contacts.bind('<Return>',lambda event:chcontacts())

				img1=tk.PhotoImage(file='icons/user.png')
				btn1=tk.Button(chinfo_home,text='Name',image=img1,command=name)
				btn1.image=img1
				btn1.grid(column=0,row=3,padx=10,pady=10,sticky=tk.E)
				tk.Label(chinfo_home,text='Change your display (full) name',font=fnt,justify=tk.LEFT).grid(column=1,row=3,padx=10,pady=10,sticky=tk.W)

				img2=tk.PhotoImage(file='icons/contacts-2.png')
				btn2=tk.Button(chinfo_home,text='Contact',image=img2,command=contacts)
				btn2.image=img2
				btn2.grid(column=0,row=6,padx=10,pady=10,sticky=tk.E)
				tk.Label(chinfo_home,text='Change your contact details',font=fnt).grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

			def about_this_program():	#About this program
				sysinfo.about()

			cur.execute('select uname,uuid from users')
			uuidlist=dict(cur.fetchall())
			cur.execute('select uname,fname from users')
			fnamelist=dict(cur.fetchall())
			
			logwin.destroy()

			manage_userswin=tk.Tk()
			manage_userswin.title('Manage profile')
			icon=tk.PhotoImage(file='img/icon.png')
			manage_userswin.iconphoto(False,icon)

			try:
				manage_userswin.state('zoomed')
			except:
				w,h=manage_userswin.winfo_screenwidth(),manage_userswin.winfo_screenheight()
				manage_userswin.geometry(str(w)+'x'+str(h))
			
			#Menubar
			menubar=tk.Menu(manage_userswin)
			more=tk.Menu(menubar,tearoff=0)
			menubar.add_cascade(label='Info',menu=more,font=menufnt)
			more.add_command(label='About this program...',command=about_this_program,font=menufnt,underline=0)
			manage_userswin.config(menu=menubar)

			tk.Grid.columnconfigure(manage_userswin,0,weight=1)
			
			#FRAME 1
			tk.Grid.rowconfigure(manage_userswin,0,weight=1)
			f1=tk.Frame(manage_userswin,bg='#283593')
			f1.grid(row=0,column=0,sticky=tk.NSEW)

			#frame 1 grid
			tk.Grid.columnconfigure(f1,0,weight=1)
			
			tk.Grid.rowconfigure(f1,0,weight=1)
			tk.Grid.rowconfigure(f1,1,weight=1)
			tk.Grid.rowconfigure(f1,2,weight=1)
			tk.Grid.rowconfigure(f1,3,weight=1)

			logo_img=tk.PhotoImage(file='img/logo.png')
			logo=tk.Label(f1,image=logo_img,fg='white',bg='#283593')
			logo.grid(column=0,row=0,padx=10,pady=10,sticky=tk.EW)
			logo.image=logo_img

			tk.Label(f1,text=('Welcome, '+fnamelist[uname_inp]),font=h1fnt,fg='white',bg='#283593').grid(column=0,row=1,padx=10,sticky=tk.EW)
			tk.Label(f1,text=('ID: '+uuidlist[uname_inp]),font=h2fnt,fg='black',bg='#00e676').grid(column=0,row=2,padx=10)
			tk.Label(f1,text=('Manage your profile'),font=h2fnt,fg='white',bg='#283593').grid(column=0,row=3,padx=10,sticky=tk.EW)
			
			Separator(f1,orient='horizontal').grid(column=0,row=4,sticky=tk.EW,padx=10,pady=10,columnspan=2)
			#FRAME 2
			tk.Grid.rowconfigure(manage_userswin,1,weight=1)
			f2=tk.Frame(manage_userswin)
			f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

			#frame 2 grid
			tk.Grid.columnconfigure(f2,0,weight=1)
			tk.Grid.columnconfigure(f2,1,weight=1)
			tk.Grid.columnconfigure(f2,2,weight=1)
			tk.Grid.columnconfigure(f2,3,weight=1)

			tk.Label(f2,text=('You can:'),font=fntit).grid(column=1,row=2,padx=10,pady=10,sticky=tk.W)
			
			tk.Grid.rowconfigure(f2,5,weight=1)
			img4=tk.PhotoImage(file='icons/passwd.png')
			passbtn=tk.Button(f2,text='Change Password',image=img4,command=passwd)
			passbtn.grid(column=0,row=5,padx=10,pady=10,sticky=tk.E)
			tk.Label(f2,text='Change your password.',font=fnt).grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

			img9=tk.PhotoImage(file='icons/user.png')
			delusrbtn=tk.Button(f2,text='Manage Personal Info',image=img9,command=info)
			delusrbtn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
			tk.Label(f2,text='Change your personal information.',font=fnt,fg='green').grid(column=3,row=5,padx=10,pady=10,sticky=tk.W)

			tk.Grid.rowconfigure(f2,6,weight=1)
			img3=tk.PhotoImage(file='icons/ban_user.png')
			delusrbtn=tk.Button(f2,text='Remove User',image=img3,command=delete)
			delusrbtn.grid(column=0,row=6,padx=10,pady=10,sticky=tk.E)
			tk.Label(f2,text='Delete your profile.',font=fnt,fg='red').grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)
			
			tk.Label(f2,text=('or:'),font=fntit).grid(column=1,row=9,padx=10,sticky=tk.W)

			tk.Grid.rowconfigure(f2,11,weight=1)
			img7=tk.PhotoImage(file='icons/logout.png')
			logoutbtn=tk.Button(f2,text='Logout',font=fnt,image=img7,command=logout)
			logoutbtn.grid(column=0,row=11,padx=10,pady=10,sticky=tk.E)
			tk.Label(f2,text='Logout',font=fnt).grid(column=1,row=11,padx=10,pady=10,sticky=tk.W)

			img8=tk.PhotoImage(file='icons/close.png')
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

		if (not uname_inp=='' and not uname_inp.isspace()) and (not passwd_inp=='' and not passwd_inp.isspace()):
			if uname_inp not in op.keys():
				messagebox.showerror('Error','Username \''+uname_inp+'\' does not exist.')
			else:
				if not passwd_inp == op[uname_inp]:
					messagebox.showerror('Error','Invalid password entered for '+fnamelist[uname_inp]+'.')
				else:
					manage()
		else:
			messagebox.showerror('Error','Please do not leave any fields blank.')

	tk.Grid.columnconfigure(logwin,0,weight=1)

	#FRAME 3
	tk.Grid.rowconfigure(logwin,0,weight=1)
	f3=tk.Frame(logwin,bg='#283593')
	f3.grid(row=0,column=0,sticky=tk.NSEW)

	#frame 3 grid
	tk.Grid.columnconfigure(f3,0,weight=1)

	tk.Grid.rowconfigure(f3,0,weight=1)
	tk.Label(logwin,text='Login',font=h1fnt,fg='white',bg='#283593').grid(column=0,row=0)
	Separator(f3,orient='horizontal').grid(row=1,column=0,sticky=tk.EW,padx=10,pady=10)

	#FRAME 4
	tk.Grid.rowconfigure(logwin,1,weight=1)
	f4=tk.Frame(logwin)
	f4.grid(row=1,column=0,sticky=tk.NSEW,padx=10,pady=10)

	#frame 4 grid
	tk.Grid.columnconfigure(f4,0,weight=1)
	tk.Grid.columnconfigure(f4,1,weight=1)

	tk.Label(f4,text='Username',font=fnt).grid(column=0,row=3,padx=10,pady=10,sticky=tk.E)
	login_uname=tk.Entry(f4,font=fnt)
	login_uname.grid(column=1,row=3,padx=10,pady=10,sticky=tk.W)

	tk.Label(f4,text='Password',font=fnt).grid(column=0,row=4,padx=10,pady=10,sticky=tk.E)
	login_passwd=tk.Entry(f4,show='*',font=fnt)
	login_passwd.grid(column=1,row=4,padx=10,pady=10,sticky=tk.W)

	img1=tk.PhotoImage(file='icons/login.png')
	logsubmit=tk.Button(f4,text='Login...',image=img1,command=onlogin)
	logsubmit.grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

	tk.Grid.rowconfigure(f4,6,weight=1)
	tk.Label(f4,text='Want to make bookings?\nClick here to continue.',font=fntit,justify=tk.RIGHT,bg='#00e676').grid(column=0,row=6,padx=10,pady=10,sticky=tk.E)
	img6=tk.PhotoImage(file='icons/booking.png')
	bkgbtn=tk.Button(f4,text='Booking',image=img6,font=fnt,command=bookings_login)
	bkgbtn.grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

	#Binds enter key to login function
	logwin.bind('<Return>',lambda event:onlogin())
	logwin.mainloop()

def about_this_program():
	sysinfo.about()

menubar=tk.Menu(welcome)

more=tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label='Info',menu=more,font=menufnt)
more.add_command(label='About this program...',command=about_this_program,font=menufnt,underline=0)
welcome.config(menu=menubar)

tk.Grid.columnconfigure(welcome,0,weight=1)

#FRAME 1
tk.Grid.rowconfigure(welcome,0,weight=1)
f1=tk.Frame(welcome,bg='#283593')
f1.grid(row=0,column=0,sticky=tk.NSEW)

#frame 1 grid
tk.Grid.columnconfigure(f1,0,weight=1)
tk.Grid.rowconfigure(f1,0,weight=1)

logo_img=tk.PhotoImage(file='img/logo.png')
logo=tk.Label(f1,image=logo_img,font=h1fnt,fg='white',bg='#283593')
logo.grid(column=0,row=0,padx=10,pady=10,sticky=tk.EW)
logo.image=logo_img

Separator(f1,orient='horizontal').grid(column=0,row=1,sticky=tk.EW,padx=10,pady=10,columnspan=2)

#FRAME 2
tk.Grid.rowconfigure(welcome,1,weight=1)

f2=tk.Frame(welcome)
f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

#frame 2 grid
tk.Grid.columnconfigure(f2,0,weight=1)
tk.Grid.columnconfigure(f2,1,weight=1)

#Bookings
tk.Grid.rowconfigure(f2,5,weight=1)
img6=tk.PhotoImage(file='icons/booking.png')
bkgbtn=tk.Button(f2,text='Booking',image=img6,font=fnt,command=main_login)
bkgbtn.grid(column=0,row=5,padx=10,pady=10,sticky=tk.E)
tk.Label(f2,text='Make a booking...',font=fnt,bg='#00e676').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

#Manage Profile
tk.Grid.rowconfigure(f2,6,weight=1)	
img4=tk.PhotoImage(file='icons/manage_accts.png')
passbtn=tk.Button(f2,text='Profile',image=img4,command=manage_user_profile)
passbtn.grid(column=0,row=6,padx=10,pady=10,sticky=tk.E)
tk.Label(f2,text='Manage user profile...',font=fnt).grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

#Exit
tk.Grid.rowconfigure(f2,7,weight=1)	
img5=tk.PhotoImage(file='icons/close.png')
passbtn=tk.Button(f2,text='Exit',image=img5,command=welcome.destroy)
passbtn.grid(column=0,row=7,padx=10,pady=10,sticky=tk.E)
tk.Label(f2,text='Exit',font=fnt,fg='red').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)

tk.Grid.rowconfigure(f2,8,weight=1)	

welcome.mainloop()