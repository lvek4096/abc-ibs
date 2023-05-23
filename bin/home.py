import platform as pf
import tkinter as tk
import os

#definitions
fnt=('IBM Plex Mono',12)
fntit=('IBM Plex Mono',12,'italic')
h1fnt=('IBM Plex Sans',24)
build='30'

#functions
def open_login():
	os.system('python3 login.py')
def book_taxi():
	os.system('python3 taxi.py')
def book_bus():
	os.system('python3 bus.py')

main_menu=tk.Tk()
main_menu.title('Build '+build+' -- INTERNAL USE ONLY')

#logbtn=tk.Button(main_menu,text='Login',font=fnt,command=open_login)
#logbtn.pack()

taxibtn=tk.Button(main_menu,text='Book taxi',font=fnt,command=book_taxi)
taxibtn.grid(column=1,row=5)

busbtn=tk.Button(main_menu,text='Book bus',font=fnt,command=book_bus)
busbtn.grid(column=1,row=6)


tk.Label(main_menu,text=('Build '+build+' on '+pf.system()+' '+pf.release()),font=fntit).grid(column=1,row=10)
tk.Label(main_menu,text=('---------------------------------------------'),font=fnt).grid(column=1,row=9)

main_menu.mainloop()
