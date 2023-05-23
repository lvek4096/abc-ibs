#import statements
import tkinter as tk
import os
import mysql.connector as ms

#definitions
fnt=('IBM Plex Mono',12)
fntit=('IBM Plex Mono',12,'italic')
h1fnt=('IBM Plex Sans',24)
hfnt=('IBM Plex Sans',36,'bold')

con=ms.connect(host='localhost',user='john',password='123456')
cur=con.cursor()

#functions	
def make_booking():
	welcome.destroy()
	os.system('python3 userlogin.py')

def manage_user():
	welcome.destroy()
	os.system('python3 manageusers.py')
	
#main window
welcome=tk.Tk()
welcome.title('')
welcome.resizable(False, False)

tk.Label(welcome,text='Welcome',font=hfnt).grid(column=1,row=0,padx=10,pady=10,sticky=tk.W)

img6=tk.PhotoImage(file='monoico/icon-13.png')
bkgbtn=tk.Button(welcome,text='Booking',image=img6,font=fnt,command=make_booking)
bkgbtn.grid(column=0,row=5,padx=10,pady=10)
tk.Label(welcome,text='Make a booking...',font=fnt,fg='green').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)
		
img4=tk.PhotoImage(file='monoico/icon-514.png')
passbtn=tk.Button(welcome,text='Profile',image=img4,command=manage_user)
passbtn.grid(column=0,row=6,padx=10,pady=10)
tk.Label(welcome,text='Manage user profile...',font=fnt).grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

img5=tk.PhotoImage(file='monoico/icon-66.png')
passbtn=tk.Button(welcome,text='Exit',image=img5,command=welcome.destroy)
passbtn.grid(column=0,row=7,padx=10,pady=10)
tk.Label(welcome,text='Exit',font=fnt,fg='red').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)

welcome.mainloop()
