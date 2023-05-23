#!/bin/python3

#import statements
#Imports libraries
import tkinter as tk
import mysql.connector as ms
from tkinter.ttk import Separator
import ctypes
import platform as pf

#Imports other Python scripts
import user
import init
import sysinfo

#definitions

#Font
fnt=('IBM Plex Mono',12,'bold italic')
fntit=('IBM Plex Mono',12,'italic')
h1fnt=('IBM Plex Sans',24)
hfnt=('IBM Plex Sans',36,'bold')
menufnt=('IBM Plex Mono',11)

#MySQL connection

con=ms.connect(host='localhost',user='root',password='123456')
cur=con.cursor()

#Initalises database
init.initdb()

#functions	
def make_booking():		#to make booking
	welcome.destroy()
	user.bookings()

def manage_user():		#to manage user
	welcome.destroy()
	user.manage_user_profile()

def about_this_program():
	sysinfo.about()

#Enables DPI scaling on supported Windows versions
if pf.system()=='Windows':
	try:
		ctypes.windll.shcore.SetProcessDpiAwareness(True)
	except:
		pass
	
#main window
welcome=tk.Tk()
welcome.title('Start Page')

#maximises window
try:
	welcome.state('zoomed')
except:
	w,h=welcome.winfo_screenwidth(),welcome.winfo_screenheight()
	welcome.geometry(str(w)+'x'+str(h))

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
logo=tk.Label(f1,image=logo_img,font=hfnt,fg='white',bg='#283593')
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
bkgbtn=tk.Button(f2,text='Booking',image=img6,font=fnt,command=make_booking)
bkgbtn.grid(column=0,row=5,padx=10,pady=10,sticky=tk.E)
tk.Label(f2,text='Make a booking...',font=fnt,bg='#00e676').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

#Manage Profile
tk.Grid.rowconfigure(f2,6,weight=1)	
img4=tk.PhotoImage(file='icons/manage_accts.png')
passbtn=tk.Button(f2,text='Profile',image=img4,command=manage_user)
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