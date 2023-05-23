import platform as pf
from re import X
import tkinter as tk
import os
import mysql.connector as ms
from tkinter import scrolledtext
from tkinter import messagebox
build='100 (Public Beta III)\n'		#Program build

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
#print('Connected to database.')

if con.is_connected()==True:
	dbstatus='Connected to database.'
else:
	dbstatus='Not connected to database.'

#Fonts
fnt=('IBM Plex Mono',12)
fntit=('IBM Plex Mono',12,'italic')
h1fnt=('IBM Plex Sans',24)
#arfnt=('IBM Plex Sans Arabic',12)

#functions
def book_taxi():	#Opens taxi booking window.
	main_menu.destroy()
	os.system('python3 taxi.py')

def book_bus():		#Opens bus booking window
	main_menu.destroy()
	os.system('python3 bus.py')

def about():	#System information
	def ee():
		q_win=tk.Toplevel()
		q_win.resizable(False,False)
		q_win.title('')
		def anspy():
			messagebox.showinfo('Correct Answer','The image shows Python code.\n"print()" is used in Python to print; and text with # are comments.',parent=q_win)

		def ansc():
			messagebox.showerror('Wrong Answer','The image shows Python, not C code.\n"print()" is used in Python to print; and text with # are comments;\nIn C, "#include<.h>" imports modules like "import" in Python.',parent=q_win)
		img=tk.PhotoImage(file='img/py.png')
		a=tk.Label(q_win,image=img)
		a.pack(fill='x')
		a.image=img

		tk.Label(q_win,text='Q. Is the above code written in Python or C ?',font=fntit).pack()

		tk.Button(q_win,text='Python code',command=anspy,font=fnt).pack()

		tk.Button(q_win,text='C code',command=ansc,font=fnt).pack()
	
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

	img2=tk.PhotoImage(file='monoico/icon-80.png')
	q=tk.Button(about,font=fnt,text='EE',image=img2,command=ee)
	q.grid(column=1,row=26,padx=10,pady=10)
	q.image=img2

def logout():	#Logs out and returns to the start page.
	main_menu.destroy()
	os.system('python3 start.py')

main_menu=tk.Tk()
main_menu.title('Main Menu')
main_menu.resizable(False, False)

tk.Label(main_menu,text=('Welcome'),font=h1fnt).grid(column=1,row=0,padx=10,sticky=tk.W)

tk.Label(main_menu,text=('You can:'),font=fntit).grid(column=1,row=2,padx=10,sticky=tk.W)
		
img6=tk.PhotoImage(file='monoico/icon-827.png')
bkgbtn=tk.Button(main_menu,text='Book taxi',image=img6,font=fnt,command=book_taxi)
bkgbtn.grid(column=0,row=5,padx=10,pady=10)
tk.Label(main_menu,text='Book a taxi.',font=fnt,bg='yellow').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)
		
img4=tk.PhotoImage(file='monoico/icon-828.png')
passbtn=tk.Button(main_menu,text='Book Bus',image=img4,command=book_bus)
passbtn.grid(column=2,row=5,padx=10,pady=10)
tk.Label(main_menu,text='Book a bus.',font=fnt,fg='blue').grid(column=3,row=5,padx=5,pady=10,sticky=tk.W)

tk.Label(main_menu,text=('or:'),font=fntit).grid(column=1,row=9,padx=10,sticky=tk.W)

img7=tk.PhotoImage(file='monoico/icon-670.png')
logoutbtn=tk.Button(main_menu,text='Logout',font=fnt,image=img7,command=logout)
logoutbtn.grid(column=0,row=10,padx=10,pady=10)
tk.Label(main_menu,text='Logout',font=fnt).grid(column=1,row=10,padx=10,pady=10,sticky=tk.W)

img8=tk.PhotoImage(file='monoico/icon-66.png')
exitbtn=tk.Button(main_menu,text='Logout and exit',font=fnt,image=img8,command=main_menu.destroy)
exitbtn.grid(column=2,row=10,padx=10,pady=10)
tk.Label(main_menu,text='Logout and exit',font=fnt,fg='red').grid(column=3,row=10,padx=10,pady=10,sticky=tk.W)

tk.Label(main_menu,text=('Know more about\nthis program'),font=fntit,fg='green',justify=tk.LEFT).grid(column=3,row=11,padx=10,pady=10)
img0=tk.PhotoImage(file='monoico/icon-78.png')
infobtn=tk.Button(main_menu,font=fnt,text='About this program...',image=img0,command=about)
infobtn.grid(column=2,row=11,padx=10,pady=10)
tk.Label(main_menu,text=('Build '+build+' on\n'+pf.system()+' '+pf.release()),font=fntit,justify=tk.RIGHT).grid(column=1,row=11,padx=10,pady=10)
main_menu.mainloop()
