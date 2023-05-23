import tkinter as tk
import random as rd
import mysql.connector as ms
import platform as pf
import ctypes
from tkinter.ttk import Separator

#mysql connection
try:
	con=ms.connect(host='192.168.0.175',user='ubuntu',password='123456',database='taxi')
except:
	con=ms.connect(host='localhost',user='root',password='123456',database='taxi')
cur=con.cursor()

#Initialise the UI
taxi_window=tk.Tk()
taxi_window.title('Welcome to ABC Lines')
fnt=('Segoe UI Variable Text',12)
fntit=('Cascadia Mono',12,'italic')
h1fnt=('Segoe UI Variable Display Semibold',24)
menufnt=('Cascadia Mono',11)
if pf.system()=='Windows':
	try:
		ctypes.windll.shcore.SetProcessDpiAwareness(True)
	except:
		pass
try:
	taxi_window.state('zoomed')
except:		
	w,h=taxi_window.winfo_screenwidth(),taxi_window.winfo_screenheight()
	taxi_window.geometry(str(w)+'x'+str(h))
icon=tk.PhotoImage(file='img/icon.png')
taxi_window.iconphoto(False,icon)

tk.Grid.columnconfigure(taxi_window,0,weight=1)

#Heading Frame
tk.Grid.rowconfigure(taxi_window,0,weight=1)
f1=tk.Frame(taxi_window,bg='#283593')
f1.grid(row=0,column=0,sticky=tk.NSEW)

#HFrame Grid
tk.Grid.columnconfigure(f1,0,weight=1)

#HFrame Content
tk.Grid.rowconfigure(f1,0,weight=1)
logo_img=tk.PhotoImage(file='img/logo.png')
logo=tk.Label(f1,image=logo_img,fg='white',bg='#283593')
logo.grid(column=0,row=0,padx=10,pady=10,sticky=tk.EW)
logo.image=logo_img

tk.Grid.rowconfigure(f1,1,weight=1)
tk.Label(f1,text='Welcome to ABC Lines!',font=h1fnt,fg='white',bg='#283593').grid(column=0,row=1)

Separator(f1,orient='horizontal').grid(row=2,column=0,sticky=tk.EW,padx=10,pady=10)

#Body Frame
tk.Grid.rowconfigure(taxi_window,1,weight=1)
f2=tk.Frame(taxi_window)
f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

#BFrame grid
tk.Grid.columnconfigure(f2,0,weight=1)



taxi_window.mainloop()