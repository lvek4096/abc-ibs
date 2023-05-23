def main():
	import tkinter as tk
	from tkinter.ttk import Separator
	import os
	
	import taxi
	import bus
	import sysinfo
	
	#Fonts
	fnt=('IBM Plex Mono',12)
	fntit=('IBM Plex Mono',12,'italic')
	h1fnt=('IBM Plex Sans',24)
	menufnt=('IBM Plex Mono',12)

	#functions
	def book_taxi():	#Opens taxi booking window.
		taxi.main()

	def book_bus():		#Opens bus booking window
		bus.main()
	
	def about_this_program():
		sysinfo.about()

	def logout():
		main_menu.destroy()
		os.system('python3 emplogin.py')

	main_menu=tk.Tk()
	main_menu.title('Employee Booking Menu')
	w,h=main_menu.winfo_screenwidth(),main_menu.winfo_screenheight()
	main_menu.geometry(str(w)+'x'+str(h))

	menubar=tk.Menu(main_menu)

	user=tk.Menu(menubar,tearoff=0)
	menubar.add_cascade(label='User',menu=user,font=menufnt)
	user.add_command(label='Logout',command=logout,font=menufnt,underline=0)
	user.add_command(label='Logout and exit',command=main_menu.destroy,font=menufnt,underline=11)
	main_menu.config(menu=menubar)
	
	more=tk.Menu(menubar,tearoff=0)
	menubar.add_cascade(label='Info',menu=more,font=menufnt)
	more.add_command(label='About this program...',command=about_this_program,font=menufnt,underline=0)
	main_menu.config(menu=menubar)

	tk.Grid.columnconfigure(main_menu,0,weight=1)


	#FRAME 1
	tk.Grid.rowconfigure(main_menu,0,weight=1)
	f1=tk.Frame(main_menu)
	f1.grid(row=0,column=0,sticky=tk.NSEW)

	tk.Grid.columnconfigure(f1,0,weight=1)

	tk.Grid.rowconfigure(f1,0,weight=1)
	tk.Label(f1,text=('Employee Booking Menu'),font=h1fnt,justify=tk.CENTER).grid(column=0,row=0,padx=10,pady=10)

	Separator(f1,orient='horizontal').grid(column=0,row=1,sticky=tk.EW,padx=10,pady=10)
	#FRAME 2
	tk.Grid.rowconfigure(main_menu,1,weight=1)
	f2=tk.Frame(main_menu)
	f2.grid(row=1,column=0,sticky=tk.NSEW)

	tk.Grid.columnconfigure(f2,0,weight=1)
	tk.Grid.columnconfigure(f2,1,weight=1)
	tk.Grid.columnconfigure(f2,2,weight=1)
	tk.Grid.columnconfigure(f2,3,weight=1)

	tk.Label(f2,text=('You can:'),font=fntit).grid(column=1,row=2,padx=10,sticky=tk.W)

	tk.Grid.rowconfigure(f2,5,weight=1)
	img6=tk.PhotoImage(file='icons/bus.png')
	bkgbtn=tk.Button(f2,text='Book taxi',image=img6,font=fnt,command=book_taxi)
	bkgbtn.grid(column=0,row=5,padx=10,pady=1,sticky=tk.E)
	tk.Label(f2,text='Book a taxi.',font=fnt,bg='yellow').grid(column=1,row=5,padx=10,pady=10,sticky=tk.W)
			
	img4=tk.PhotoImage(file='icons/taxi.png')
	passbtn=tk.Button(f2,text='Book Bus',image=img4,command=book_bus)
	passbtn.grid(column=2,row=5,padx=10,pady=10,sticky=tk.E)
	tk.Label(f2,text='Book a bus.',font=fnt,fg='blue').grid(column=3,row=5,padx=5,pady=10,sticky=tk.W)

	tk.Grid.rowconfigure(f2,12,weight=1)

	main_menu.mainloop()