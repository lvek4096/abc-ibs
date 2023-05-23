import tkinter as tk
import os
import mysql.connector as ms

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
	os.chdir('../')
	os.system('python3 taxi.py')

def book_bus():		#Opens bus booking window
	main_menu.destroy()
	os.chdir('../')
	os.system('python3 bus.py')

def home():	#Logs out and returns to the start page.
	main_menu.destroy()
	os.system('python3 admin.py')

main_menu=tk.Tk()
main_menu.title('Admin Booking Menu')
main_menu.resizable(False, False)

tk.Label(main_menu,text=('Admin Booking\nMenu'),font=h1fnt,justify=tk.LEFT).grid(column=1,row=0,padx=10,sticky=tk.W)

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

img7=tk.PhotoImage(file='monoico/icon-714.png')
logoutbtn=tk.Button(main_menu,text='Return home',font=fnt,image=img7,command=home)
logoutbtn.grid(column=0,row=10,padx=10,pady=10)
tk.Label(main_menu,text='Return home.',font=fnt).grid(column=1,row=10,padx=10,pady=10,sticky=tk.W)

main_menu.mainloop()
