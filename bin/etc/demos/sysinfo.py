#import statements

#import mysql.connector as ms
import platform as pf
import tkinter as tk
import os

'''
#mysql connection
con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
cur=con.cursor()
print('Connected to database.')

if con.is_connected()==True:
	dbstatus='Connected to database.'
else:
	dbstatus='Not connected to database.'
'''
fnt=('IBM Plex Mono',12)
fntit=('IBM Plex Mono',12,'italic')
h1fnt=('IBM Plex Sans',24)
build='40'

about=tk.Tk()
abttitle='About this '+pf.system()+' system'
about.resizable(False, False)
about.title(abttitle)
#Labels
tk.Label(about,text='About',font=h1fnt).grid(column=1,row=0)
tk.Label(about,text='a tkinter demo',font=fntit).grid(column=1,row=1)
tk.Label(about,text=('Build '+build),font=fnt).grid(column=1,row=2)
tk.Label(about,text='-------------------------------',font=fnt).grid(column=1,row=3)
tk.Label(about,text=('Python',pf.python_version()),font=fnt).grid(column=1,row=4)
tk.Label(about,text=('Tkinter',tk.TkVersion),font=fnt).grid(column=1,row=5)
#tk.Label(about,text=('MySQL',ms.__version__),font=fnt).grid(column=1,row=6)
tk.Label(about,text='-------------------------------',font=fnt).grid(column=1,row=7)

if pf.system()=='Windows':
	src=tk.PhotoImage(file='img/oldwin.png')
elif pf.system()=='Darwin':
	src=tk.PhotoImage(file='img/oldmac.png')	
elif pf.system()=='Linux':
	src=tk.PhotoImage(file='img/linux.png')

osimg=tk.Label(about,image=src)
osimg.grid(column=1,row=8)

#System info
if pf.system()=='Windows':		#Additional info - Windows systems ONLY
	tk.Label(about,text=(pf.system(),pf.release(),pf.version()),font=fnt).grid(column=1,row=10)
else:
	tk.Label(about,text=(pf.system(),pf.release()),font=fnt).grid(column=1,row=10)
	
#Additional Linux distribution info - Linux ONLY
py=pf.python_version_tuple()
if int(py[0]) >= 3 and int(py[1]) >= 10:
	if pf.system()=='Linux':
		linux=pf.freedesktop_os_release()
		tk.Label(about,text=(linux['NAME']+' '+linux['VERSION']),font=fnt).grid(column=1,row=11,padx=10,pady=10)
else:
	pass

tk.Label(about,text='-------------------------------',font=fnt).grid(column=1,row=12)
	
#CPU type - i386 (32-bit); AMD64/x86_64 (64-bit) etc.
tk.Label(about,text=(pf.machine()+' system'),font=fnt).grid(column=1,row=13)
	
tk.Label(about,text='-------------------------------',font=fnt).grid(column=1,row=14)
'''
def showdbinfo():
	def hidedbinfo():
		dbinfo.grid_forget()
		showdb.configure(text='Show database information',command=showdbinfo)

	dbinfo=tk.Label(about,text=('MySQL '+con.get_server_info()+'\n'+dbstatus+'\nDatabase: '+con.database),font=fnt)
	dbinfo.grid(column=1,row=16)
	showdb.configure(text='Hide database information',command=hidedbinfo)

showdb=tk.Button(about,text='Show database information',font=fnt,command=showdbinfo);showdb.grid(column=1,row=15)
	
tk.Label(about,text='-------------------------------',font=fnt).grid(column=1,row=19)
#Closes the window
'''

clsimg=tk.PhotoImage(file='ico/emblem-unreadable.png')
cls=tk.Button(about,font=fnt,text='Close',image=clsimg,command=about.destroy)
cls.grid(column=1,row=20,padx=10,pady=10)
cls.image=clsimg
	
about.mainloop()
