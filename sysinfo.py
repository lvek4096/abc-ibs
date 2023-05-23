def about():	#System information
	
	#import statements
	import platform as pf
	import tkinter as tk
	from tkinter.ttk import Separator
	import mysql.connector as ms
	from tkinter import scrolledtext
	import ctypes

	#Build number
	build='244 [RC 1]'
	build_date='2022-08-18'	

	#Enables DPI scaling on supported Windows versions
	if pf.system()=='Windows':
		try:
			ctypes.windll.shcore.SetProcessDpiAwareness(True)
		except:
			pass

	disclaimer='''
Icons:

- Material Icons
https://fonts.google.com/icons

- Card icons
https://brand.mastercard.com/brandcenter/artwork.html
https://www.merchantsignage.visa.com/brand_guidelines
https://www.americanexpress.com/en-gb/business/merchant/supplies/details/?pid=WEBLOGO1&linknav=merchant-supplies-nav
https://www.discover.com/company/images/newsroom/media-downloads/
'''

	#mysql connection
	con=ms.connect(host='localhost',user='root',password='123456',database='taxi')

	#Fonts
	fnt=('IBM Plex Mono',12)
	fntit=('IBM Plex Mono',12,'italic')
	h1fnt=('IBM Plex Sans',24)

	about=tk.Toplevel()
	abttitle=' '
	about.resizable(False, False)
	about.title(abttitle)
	
	
	#Labels
	tk.Label(about,text='About',font=h1fnt).grid(column=1,row=0)
	tk.Label(about,text=('Build '+build+'\n ('+build_date+')'),font=fnt).grid(column=1,row=1)
	
	disc=scrolledtext.ScrolledText(about,font=fntit,height=6,width=40)
	disc.grid(column=1,row=2,sticky=tk.EW,padx=10,pady=10)
	disc.insert(tk.INSERT,disclaimer)
	disc.configure(state='disabled')
	
	Separator(about,orient='horizontal').grid(column=1,row=5,sticky=tk.EW,padx=10,pady=10)

	tk.Label(about,text=('Python',pf.python_version()),font=fnt).grid(column=1,row=6)
	tk.Label(about,text=('Tkinter',tk.TkVersion),font=fnt).grid(column=1,row=7)
	tk.Label(about,text=('MySQL',con.get_server_info()),font=fnt).grid(column=1,row=8)
	
	Separator(about,orient='horizontal').grid(column=1,row=9,sticky=tk.EW,padx=10,pady=10)

	if pf.system()=='Windows':
		src=tk.PhotoImage(file='img/win.png')
	elif pf.system()=='Darwin':		#Darwin - macOS
		src=tk.PhotoImage(file='img/macos.png')	
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
	
	#Additional distribution info - Linux ONLY
	#Checking for platform.freedesktop_os_release() support - ONLY in Python 3.10 and newer
	py=pf.python_version_tuple()

	if pf.system()=='Linux':
		try:
			linux=pf.freedesktop_os_release()
			tk.Label(about,text=(linux['NAME']+' '+linux['VERSION']),font=fnt).grid(column=1,row=13)
		except:
			pass
	else:
		pass

	Separator(about,orient='horizontal').grid(column=1,row=14,sticky=tk.EW,padx=10,pady=10)
	
	#Hostname and CPU type (e.g.i386 (32-bit); AMD64/x86_64 (64-bit) etc.)
	tk.Label(about,text=(pf.node()+'\n'+pf.machine()+' system'),font=fnt).grid(column=1,row=15)
	
	Separator(about,orient='horizontal').grid(column=1,row=16,sticky=tk.EW,padx=10,pady=10)
	

	dbinfo=tk.Label(about,text='Connected to database \''+con.database+'\'',font=fnt)
	dbinfo.grid(column=1,row=18)
	
	
	Separator(about,orient='horizontal').grid(column=1,row=24,sticky=tk.EW,padx=10,pady=10)
	
	#Closes the window
	def close():
		about.destroy()

	img1=tk.PhotoImage(file='icons/close.png')
	cls=tk.Button(about,font=fnt,text='Close',image=img1,command=close)
	cls.grid(column=1,row=25,padx=10,pady=10)
	cls.image=img1
