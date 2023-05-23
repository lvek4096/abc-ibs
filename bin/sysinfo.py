#import statements

import platform as pf
import tkinter as tk

fnt=('IBM Plex Mono',12)
fntit=('IBM Plex Mono',12,'italic')
h1fnt=('IBM Plex Sans',24)
build='26'

about=tk.Tk()
#about.geometry('160x120')
abttitle='About this '+pf.system()+' system'
about.tk.call('tk', 'scaling', 1.5)
about.title(abttitle)

#Labels
tk.Label(about,text='About - TkInter demo',font=h1fnt).grid(column=1,row=0)
tk.Label(about,text=('Build '+build),font=fnt).grid(column=1,row=1)
#tk.Label(about,text='This is pre-release software.\nBugs may exist and features may not be complete.\nUse at your own risk.',font=fntit).grid(column=1,row=2)
tk.Label(about,text='-------------------------------',font=fnt).grid(column=1,row=3)
tk.Label(about,text=('Python',pf.python_version()),font=fnt).grid(column=1,row=4)
tk.Label(about,text=('Tkinter',tk.TkVersion),font=fnt).grid(column=1,row=5)
tk.Label(about,text='-------------------------------',font=fnt).grid(column=1,row=7)

if pf.system()=='Windows':
	src=tk.PhotoImage(file='img/win.png')
elif pf.system()=='Darwin':
	src=tk.PhotoImage(file='img/macos.png')	
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

#Closes the window
clsimg=tk.PhotoImage(file='ico/emblem-unreadable.png')
cls=tk.Button(about,font=fnt,text='Close',image=clsimg,command=about.destroy)
cls.grid(column=1,row=20)
cls.image=clsimg

about.mainloop()
