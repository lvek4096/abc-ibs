import tkinter as tk
import platform as pf
	
a=pf.freedesktop_os_release()	
distro=a['NAME']
version=a['VERSION']

def sysinfo():
	hr=tk.Label(window,text=('===================================')).pack()
	h1=tk.Label(window,text=('Hardware')).pack()
	arch=tk.Label(window,text=('Architecture:',pf.machine())).pack()
	hr=tk.Label(window,text=('===================================')).pack()
	h2=tk.Label(window,text=('Software:')).pack()
	arch=tk.Label(window,text=('Python',pf.python_version())).pack()
	if pf.system() == 'Linux':
		kernel=tk.Label(window,text=('Kernel:',pf.system(),pf.release())).pack()
		os=tk.Label(window,text=('Distribution:',distro,version)).pack()
	hr=tk.Label(window,text=('===================================')).pack()
window=tk.Tk()
window.title(pf.system())
if pf.system() == 'Linux':
	welcome=tk.Label(window,text='Welcome to GNU/Linux').pack()
else:
	welcome=tk.Label(window,text=('Welcome to',pf.system())).pack()

tk.Button(window,text='Click to see about your system',command=sysinfo).pack()
window.mainloop()
