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
	os.system('python3 manageusr.py')
	
#main window
welcome=tk.Tk()
welcome.title('')

tk.Grid.columnconfigure(welcome,0,weight=1)
#FRAME 1

tk.Grid.rowconfigure(welcome,0,weight=1)
f1=tk.Frame(welcome)
f1.grid(row=0,column=0,sticky=tk.NSEW)

#frame 1 grid
tk.Grid.columnconfigure(f1,0,weight=1)
tk.Grid.rowconfigure(f1,0,weight=1)

tk.Label(f1,text='Welcome',font=hfnt).grid(column=0,row=0,padx=10,pady=10,sticky=tk.EW)

#FRAME 2

tk.Grid.rowconfigure(welcome,1,weight=1)

f2=tk.Frame(welcome)
f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

#frame 2 grid
tk.Grid.columnconfigure(f2,0,weight=1)
tk.Grid.columnconfigure(f2,1,weight=1)

#tk.Grid.rowconfigure(f2,5,weight=1)
img6=tk.PhotoImage(file='monoico/icon-13.png')
bkgbtn=tk.Button(f2,text='Booking',image=img6,font=fnt,command=make_booking,justify=tk.CENTER)
bkgbtn.grid(column=0,row=5,padx=10,pady=10,sticky=tk.E)
tk.Label(f2,text='Make a booking...',font=fnt,fg='green').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)

#tk.Grid.rowconfigure(f2,6,weight=1)	
img4=tk.PhotoImage(file='monoico/icon-514.png')
passbtn=tk.Button(f2,text='Profile',image=img4,command=manage_user,justify=tk.CENTER)
passbtn.grid(column=0,row=6,padx=10,pady=10,sticky=tk.E)
tk.Label(f2,text='Manage user profile...',font=fnt).grid(column=1,row=6,padx=10,pady=10,sticky=tk.W)

#tk.Grid.rowconfigure(f2,7,weight=1)	
img5=tk.PhotoImage(file='monoico/icon-66.png')
passbtn=tk.Button(f2,text='Exit',image=img5,command=welcome.destroy,justify=tk.CENTER)
passbtn.grid(column=0,row=7,padx=10,pady=10,sticky=tk.E)
tk.Label(f2,text='Exit',font=fnt,fg='red').grid(column=1,row=7,padx=10,pady=10,sticky=tk.W)

welcome.mainloop()
