def about():	#System information
	
	#import statements
	import platform as pf
	import tkinter as tk
	from tkinter.ttk import Separator
	import mysql.connector as ms
	from tkinter import scrolledtext
	import ctypes

	#Build number
	build='255'
	build_date='2022-09-24'	

	credits_txt='''
Developed by
LIYO K. JOHN - MEGHNATH M.D. - MOHAMMED SAAD
'''

	#Enables DPI scaling on supported Windows versions
	if pf.system()=='Windows':
		try:
			ctypes.windll.shcore.SetProcessDpiAwareness(True)
		except:
			pass


	#mysql connection
	con=ms.connect(host='localhost',user='root',password='123456',database='taxi')

	#Fonts
	fnt=('IBM Plex Mono',12)
	h1fnt=('IBM Plex Sans',24)

	about=tk.Toplevel()
	abttitle='About this program'
	about.resizable(False, False)
	about.title(abttitle)
	
	
	#Labels
	tk.Label(about,text='About',font=h1fnt).grid(column=0,row=0,columnspan=3)
	tk.Label(about,text=('Build '+build+' ('+build_date+')'),font=fnt).grid(column=0,row=1,columnspan=3)
	
	logo_img=tk.PhotoImage(file='img/logo150px.png')
	logo=tk.Label(about,image=logo_img)
	logo.grid(column=0,row=2,padx=10,pady=10)
	logo.image=logo_img
	

	credits=tk.Label(about,font=('IBM Plex Mono',12,'bold italic'),text=credits_txt,justify=tk.CENTER)
	credits.grid(row=2,column=2,sticky=tk.EW,padx=10,pady=10)
	
	Separator(about,orient='horizontal').grid(column=0,row=5,sticky=tk.EW,padx=10,pady=10,columnspan=3)
	
	pyimgsrc=tk.PhotoImage(file='img/python.png')
	pyimg=tk.Label(about,image=pyimgsrc)
	pyimg.image=pyimgsrc
	pyimg.grid(column=0,row=6)

	tk.Label(about,text=('Python',pf.python_version()),font=fnt).grid(column=0,row=7,padx=10)
	tk.Label(about,text=('Tkinter',tk.TkVersion),font=fnt).grid(column=0,row=8,padx=10)
	tk.Label(about,text=('MySQL',con.get_server_info()),font=fnt).grid(column=0,row=9,padx=10)
	

	if pf.system()=='Windows':
		src=tk.PhotoImage(file='img/win.png')
	elif pf.system()=='Darwin':		#Darwin - macOS
		src=tk.PhotoImage(file='img/macos.png')	
	elif pf.system()=='Linux':
		src=tk.PhotoImage(file='img/linux.png')

	osimg=tk.Label(about,image=src)
	osimg.image=src
	osimg.grid(column=2,row=6,padx=10,pady=10)

	#System info
	if pf.system()=='Windows':		#Additional info - Windows systems ONLY
		tk.Label(about,text=(pf.system(),pf.release(),pf.version()),font=('IBM Plex Mono',12,'bold italic')).grid(column=2,row=7,padx=10)
	else:
		tk.Label(about,text=(pf.system(),pf.release()),font=('IBM Plex Mono',12,'bold italic')).grid(column=2,row=7,padx=10)
	
	#Additional distribution info - Linux ONLY

	if pf.system()=='Linux':
		try:
			linux=pf.freedesktop_os_release()
			tk.Label(about,text=(linux['NAME']+' '+linux['VERSION']),font=fnt).grid(column=2,row=8,padx=10)
		except:
			pass
	else:
		pass

	Separator(about,orient='horizontal').grid(column=0,row=10,sticky=tk.EW,padx=10,pady=10,columnspan=3)
	
	#Hostname and CPU type (e.g.i386 (32-bit); AMD64/x86_64 (64-bit) etc.)
	tk.Label(about,text=pf.node(),font=('IBM Plex Mono',12,'bold italic')).grid(column=0,row=11,columnspan=3,padx=10)
	tk.Label(about,text=(pf.machine()+' system'),font=fnt).grid(column=0,row=12,columnspan=3,padx=10)
	Separator(about,orient='horizontal').grid(column=0,row=16,sticky=tk.EW,padx=10,pady=10,columnspan=3)
	

	dbinfo=tk.Label(about,text='Connected to database \''+con.database+'\'',font=fnt)
	dbinfo.grid(column=0,row=18,columnspan=3,padx=10)
	
	
	Separator(about,orient='horizontal').grid(column=0,row=24,sticky=tk.EW,padx=10,pady=10,columnspan=3)
	
	#Closes the window
	def close():
		about.destroy()

	img1=tk.PhotoImage(file='icons/close.png')
	cls=tk.Button(about,font=fnt,text='Close',image=img1,command=close)
	cls.grid(column=0,row=25,padx=10,pady=10,columnspan=3)
	cls.image=img1
