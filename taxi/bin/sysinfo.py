def about():	#System information
	import platform as pf
	import tkinter as tk
	import mysql.connector as ms
	from tkinter import scrolledtext
	build='172'	

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
