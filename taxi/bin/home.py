def main():
	import tkinter as tk
	import os
	import taxi
	import bus
	import sysinfo

	#Fonts
	fnt=('IBM Plex Mono',12)
	fntit=('IBM Plex Mono',12,'italic')
	h1fnt=('IBM Plex Sans',24)


	#functions
	def book_taxi():	#Opens taxi booking window.
		taxi.main()

	def book_bus():		#Opens bus booking window
		bus.main()

	def about_this_program():
		sysinfo.about()

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
	infobtn=tk.Button(f2,font=fnt,text='About this program...',image=img0,command=about_this_program)
	infobtn.grid(column=2,row=12,padx=10,pady=10,sticky=tk.E)
	tk.Label(f2,text=('Know about this program...'),font=fntit,justify=tk.LEFT,fg='green').grid(column=3,row=12,padx=10,pady=10,sticky=tk.W)
	main_menu.mainloop()