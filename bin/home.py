import platform as pf
import tkinter as tk
import os
import mysql.connector as ms
from tkinter import scrolledtext
build='145 (Beta III)'		#Program build

disclaimer='''WARNING
This is pre-release software.
Bugs may exist and features may 
break or not work completely.
Proceed to use this software 
at your own risk.

ATTENTION
Il s'agit d'un logiciel de pré-version.
Des bogues peuvent exister et des 
fonctionnalités peuventcasser ou 
ne pas fonctionner complètement.
Continuez à utiliser ce 
logiciel à vos risques et périls.

ADVERTENCIA
Este es un software de versión 
preliminar.
Pueden existir errores y las 
características puedenromper o 
no funcionar completamente.
Proceda a usar este software 
bajo su propio riesgo.

TRANSLATIONS BY GOOGLE TRANSLATE

Icons:
- Ubuntu Yaru icons
https://github.com/ubuntu/yaru

- Fontawesome
https://fontawesome.com/icons'''

#mysql connection
con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
cur=con.cursor()

if con.is_connected()==True:
	dbstatus='Connected to database.'
else:
	dbstatus='Not connected to database.'

#Fonts
fnt=('IBM Plex Mono',12)
fntit=('IBM Plex Mono',12,'italic')
h1fnt=('IBM Plex Sans',24)


#functions
def book_taxi():	#Opens taxi booking window.
	main_menu.destroy()
	os.system('python3 taxi.py')

def book_bus():		#Opens bus booking window
	main_menu.destroy()
	os.system('python3 bus.py')

def about():	#System information

	about=tk.Toplevel()
	abttitle='About this program on '+pf.system()
	about.resizable(False, False)
	about.title(abttitle)
	
	#Labels
	tk.Label(about,text='About',font=h1fnt).grid(column=1,row=0)
	tk.Label(about,text=('Build '+build),font=fnt).grid(column=1,row=1)
	
	disc=scrolledtext.ScrolledText(about,font=fntit,height=6,width=40)
	disc.grid(column=1,row=2,sticky=tk.EW,padx=10,pady=10)
	disc.insert(tk.INSERT,disclaimer)
	disc.configure(state='disabled')
	
	tk.Label(about,text='-------------------------------',font=fnt).grid(column=1,row=5)
	
	tk.Label(about,text=('Python',pf.python_version()),font=fnt).grid(column=1,row=6)
	tk.Label(about,text=('Tkinter',tk.TkVersion),font=fnt).grid(column=1,row=7)
	tk.Label(about,text=('MySQL',ms.__version__),font=fnt).grid(column=1,row=8)
	
	tk.Label(about,text='-------------------------------',font=fnt).grid(column=1,row=9)

	if pf.system()=='Windows':
		src=tk.PhotoImage(file='img/oldwin.png')
	elif pf.system()=='Darwin':
		src=tk.PhotoImage(file='img/oldmac.png')	
	elif pf.system()=='Linux':
		src=tk.PhotoImage(file='img/linux.png')

	osimg=tk.Label(about,image=src)
	osimg.image=src
	osimg.grid(column=1,row=10)

	#System info
	if pf.system()=='Windows':		#Additional info - Windows systems ONLY
		tk.Label(about,text=(pf.system(),pf.release(),pf.version()),font=fnt).grid(column=1,row=11)
	else:
		tk.Label(about,text=(pf.system(),pf.release()),font=fnt).grid(column=1,row=12)
	
	#Additional Linux distribution info - Linux ONLY
	#Checking for platform.freedesktop_os_release() support - ONLY in Python 3.10 and newer
	py=pf.python_version_tuple()
	if int(py[0]) >= 3 and int(py[1]) >= 10:
		if pf.system()=='Linux':
			linux=pf.freedesktop_os_release()
			tk.Label(about,text=(linux['NAME']+' '+linux['VERSION']),font=fnt).grid(column=1,row=13)
	else:
		pass

	tk.Label(about,text='-------------------------------',font=fnt).grid(column=1,row=14)
	
	#Hostname and CPU type (e.g.i386 (32-bit); AMD64/x86_64 (64-bit) etc.)
	tk.Label(about,text=(pf.node()+'\n'+pf.machine()+' system'),font=fnt).grid(column=1,row=15)
	
	tk.Label(about,text='-------------------------------',font=fnt).grid(column=1,row=16)
	
	def showdbinfo():
		def hidedbinfo():
			dbinfo.grid_forget()
			showdb.configure(text='Show database information',command=showdbinfo)

		dbinfo=tk.Label(about,text=('MySQL '+con.get_server_info()+'\n'+dbstatus+'\nDatabase: '+con.database),font=fnt)
		dbinfo.grid(column=1,row=18)
		
		showdb.configure(text='Hide database information',command=hidedbinfo)

	showdb=tk.Button(about,text='Show database information',font=fnt,command=showdbinfo);showdb.grid(column=1,row=17)
	
	tk.Label(about,text='-------------------------------',font=fnt).grid(column=1,row=24)
	#Closes the window

	def close():
		about.destroy()

	img1=tk.PhotoImage(file='monoico/icon-66.png')
	cls=tk.Button(about,font=fnt,text='Close',image=img1,command=close)
	cls.grid(column=1,row=25,padx=10,pady=10)
	cls.image=img1


def logout():	#Logs out and returns to the start page.
	main_menu.destroy()
	os.system('python3 start.py')

main_menu=tk.Tk()
main_menu.title('Main Menu')
w,h=main_menu.winfo_screenwidth(),main_menu.winfo_screenheight()
main_menu.geometry(str(w)+'x'+str(h))

tk.Grid.columnconfigure(main_menu,0,weight=1)

#FRAME 1
tk.Grid.rowconfigure(main_menu,0,weight=1)
f1=tk.Frame(main_menu)
f1.grid(row=0,column=0,sticky=tk.NSEW)

#frame 1 grid
tk.Grid.columnconfigure(f1,0,weight=1)

tk.Grid.rowconfigure(f1,0,weight=1)
tk.Label(f1,text='Welcome',font=h1fnt).grid(column=0,row=0)

#FRAME 2
tk.Grid.rowconfigure(main_menu,1,weight=1)
f2=tk.Frame(main_menu)
f2.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

#frame 2 grid
tk.Grid.columnconfigure(f2,0,weight=1)
tk.Grid.columnconfigure(f2,1,weight=1)
tk.Grid.columnconfigure(f2,2,weight=1)
tk.Grid.columnconfigure(f2,3,weight=1)

tk.Grid.rowconfigure(f2,2,weight=1)
tk.Label(f2,text=('You can:'),font=fntit).grid(column=1,row=2,padx=10,sticky=tk.W)

#tk.Grid.rowconfigure(f2,5,weight=1)
img6=tk.PhotoImage(file='monoico/icon-827.png')
bkgbtn=tk.Button(f2,text='Book taxi',image=img6,font=fnt,command=book_taxi)
bkgbtn.grid(column=0,row=5,padx=10,pady=10,sticky=tk.E)
tk.Label(f2,text='Book a taxi.',font=fnt,bg='yellow').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)
	
img4=tk.PhotoImage(file='monoico/icon-828.png')
passbtn=tk.Button(f2,text='Book Bus',image=img4,command=book_bus)
passbtn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
tk.Label(f2,text='Book a bus.',font=fnt,fg='blue').grid(column=3,row=5,padx=5,pady=10,sticky=tk.W)

tk.Grid.rowconfigure(f2,9,weight=1)
tk.Label(f2,text=('or:'),font=fntit).grid(column=1,row=9,padx=10,sticky=tk.W)

img7=tk.PhotoImage(file='monoico/icon-670.png')
logoutbtn=tk.Button(f2,text='Logout',font=fnt,image=img7,command=logout)
logoutbtn.grid(column=0,row=11,padx=10,pady=10,sticky=tk.E)
tk.Label(f2,text='Logout',font=fnt).grid(column=1,row=11,padx=10,pady=10,sticky=tk.W)

img8=tk.PhotoImage(file='monoico/icon-66.png')
exitbtn=tk.Button(f2,text='Logout and exit',font=fnt,image=img8,command=main_menu.destroy)
exitbtn.grid(column=2,row=11,padx=10,pady=10,sticky=tk.E)
tk.Label(f2,text='Logout and exit',font=fnt,fg='red').grid(column=3,row=11,padx=10,pady=10,sticky=tk.W)

tk.Grid.rowconfigure(f2,12,weight=1)
img0=tk.PhotoImage(file='monoico/icon-78.png')
infobtn=tk.Button(f2,font=fnt,text='About this program...',image=img0,command=about)
infobtn.grid(column=2,row=12,padx=10,pady=10,sticky=tk.E)
tk.Label(f2,text=('Build '+build+' on\n'+pf.system()+' '+pf.release()),font=fntit,justify=tk.LEFT,fg='green').grid(column=3,row=12,padx=10,pady=10,sticky=tk.W)
main_menu.mainloop()
