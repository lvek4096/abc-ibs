#import statements
import mysql.connector as ms
import random as rd
import platform as pf
import tkinter as tk

#definitions
id=rd.randint(10000,99999)	#random number for ID
locations='ABCDEFGHIJKLMNOPQRSTUVWXYZ'	#defines locations
#ctype=['Standard','Premium','Express']	#defines coach type
build='30'	#Program build

#mysql connection
con=ms.connect(host='localhost',user='john',password='123456',database='taxi')
cur=con.cursor()
print('Connected to database.')

if con.is_connected()==True:
	dbstatus='Connected to database.'
else:
	dbstatus='Not connected to database.'
#GUI
window=tk.Tk()
#fonts for GUI
fnt=('IBM Plex Mono',12)
fntit=('IBM Plex Mono',12,'italic')
h1fnt=('IBM Plex Sans',24)
#Main Window parameters
window.title('Taxi Booking')
#window.geometry('640x480')

def submit():	#Backend - takes inputs, sends to MySQL db
	#Converts inputs to variables
	start_inp=start.get()
	end_inp=end.get()
	date_inp=date.get()
	time_inp=time.get()

	confirm=tk.Message(window,text='',width=500,font=fnt)
	confirm.grid(column=1,row=9)

	l1=[id,start_inp,end_inp,date_inp,time_inp]

	if start_inp in locations and end_inp in locations:

		#Sends inputs to MySQL db
		sql='insert into taxi_bkgs values (%s,%s,%s,%s,%s)'
		val=(id,start_inp,end_inp,date_inp,time_inp)
		cur.execute(sql,val)
		con.commit()

		#data=[];data.append(l1)
		#df=pd.DataFrame(data,columns=['ID','From','To','Date','Time'])
	
		#Shows confirmation on GUI Window
		confirm.configure(text=('Booking\n'+str(l1)+'\nentered successfully'))
	else:
		confirm.configure(text=('Invalid origin or destination entered.'))
def about():	#About the program
	about=tk.Toplevel()
	#about.geometry('160x120')
	abttitle='About this '+pf.system()+' system'

	#Labels
	tk.Label(about,text='About',font=h1fnt).grid(column=1,row=0)
	tk.Label(about,text=('Build '+build),font=fnt).grid(column=1,row=1)
	tk.Label(about,text='This is pre-release software.\nBugs may exist and features may not be complete.\nUse at your own risk.',font=fntit).grid(column=1,row=2)
	tk.Label(about,text='-------------------------------',font=fnt).grid(column=1,row=3)
	tk.Label(about,text=('Python',pf.python_version()),font=fnt).grid(column=1,row=4)
	tk.Label(about,text=('Tkinter',tk.TkVersion),font=fnt).grid(column=1,row=5)
	tk.Label(about,text=('MySQL',ms.__version__),font=fnt).grid(column=1,row=6)
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
	if pf.system()=='Linux':
		linux=pf.freedesktop_os_release()
		tk.Label(about,text=(linux['NAME']+' '+linux['VERSION']),font=fnt).grid(column=1,row=11)
	
	tk.Label(about,text='-------------------------------',font=fnt).grid(column=1,row=12)
	
	#CPU type - i386 (32-bit); AMD64/x86_64 (64-bit) etc.
	tk.Label(about,text=(pf.machine()+' system'),font=fnt).grid(column=1,row=13)
	
	tk.Label(about,text='-------------------------------',font=fnt).grid(column=1,row=14)

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
	clsimg=tk.PhotoImage(file='ico/emblem-unreadable.png')
	cls=tk.Button(about,font=fnt,text='Close',image=clsimg,command=about.destroy)
	cls.grid(column=1,row=20)
	cls.image=clsimg
	
	about.mainloop()

#Window
tk.Label(window,text='TAXI BOOKING',font=h1fnt).grid(column=1,row=0)
#tk.Label(window,text='This is pre-release software.\nBugs may exist and features may not be complete.\nUse at your own risk.',font=fnt).grid(column=1,row=1)
#Input fields
tk.Label(text='ID',font=fnt).grid(column=0,row=3)
bkgid=tk.Label(window,text=id,font=fnt);bkgid.grid(column=1,row=3)

tk.Label(window,text='From',font=fnt).grid(column=0,row=4)
start=tk.Entry(window,font=fnt);start.grid(column=1,row=4)

tk.Label(window,text='To',font=fnt).grid(column=0,row=5)
end=tk.Entry(window,font=fnt);end.grid(column=1,row=5)

tk.Label(window,text='Date',font=fnt).grid(column=0,row=6)
date=tk.Entry(window,font=fnt);date.grid(column=1,row=6)

tk.Label(window,text='Time',font=fnt).grid(column=0,row=7)
time=tk.Entry(window,font=fnt);time.grid(column=1,row=7)


#buttons

subimg=tk.PhotoImage(file='ico/emblem-default.png')
btn=tk.Button(window,font=fnt,text='Submit',image=subimg,command=submit);btn.grid(column=1,row=8)
btn.image=subimg

abtimg=tk.PhotoImage(file='ico/dialog-information.png')
btn2=tk.Button(window,font=fnt,text='About this program...',image=abtimg,command=about);btn2.grid(column=2,row=11)
btn2.img=abtimg

#Version on system
tk.Label(window,text=('Build '+build+' on\n'+pf.system()+' '+pf.release()),font=fntit).grid(column=0,row=12)
window.mainloop()
