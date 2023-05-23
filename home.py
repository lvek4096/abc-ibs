import platform as pf
import tkinter as tk
import os

#definitions
fnt=('IBM Plex Mono',12)
fntit=('IBM Plex Mono',12,'italic')
h1fnt=('IBM Plex Sans',24)
hfnt=('IBM Plex Sans',36,'bold')

#build
build='30'

#functions	
def enter():
	welcome.destroy()
	os.chdir('bin')
	os.system('python3 login.py')

welcome=tk.Tk()
welcome.title('Welcome')

#logbtn=tk.Button(welcome,text='Login',font=fnt,command=open_login)
#logbtn.pack()

tk.Label(welcome,text='Welcome to',font=hfnt).pack()
tk.Label(welcome,text=('---------------------------------------------'),font=fnt).pack()
busbtn=tk.Button(welcome,text='Enter >',font=fnt,command=enter)
busbtn.pack()


tk.Label(welcome,text=('Build '+build+' on '+pf.system()+' '+pf.release()),font=fntit).pack(side='bottom')
tk.Label(welcome,text=('---------------------------------------------'),font=fnt).pack(side='bottom')

welcome.mainloop()
