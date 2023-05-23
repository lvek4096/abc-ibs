import pandas as pd
import random as rd
import platform as pf

id=rd.randint(00000,99999)
locations='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ctype=['Standard','Premium','Express']

def help():
	print('''
This is the help for the booking gateway.

''')

def prerel():
		print('''
====================
PRE-RELEASE SOFTWARE
====================
This is prerelease software.
Features may be incomplete and bugs may be present.
Continue to use at your own risk.
''')

def sysinfo():
	prerel()
	print('--------------------------')
	print('ABCDE')
	print('Build 0001')
	print('--------------------------')
	print('Python',pf.python_version())
	print()
	print(pf.system(),pf.release())
	if pf.system()=='Linux':
		a=pf.freedesktop_os_release()
		print(a['NAME'],a['VERSION'])
	print('--------------------------')
	print(pf.machine(),'CPU')
	print('--------------------------')
	input('Press [Enter] to continue')

data=[]
while True:
	prerel()
	print('''
Choices:
[B] make a Booking
[ ] Exit the program
[H] view Help file
[K] Know about this program
[L] exit the Loop. 
''')
	choice=input('Enter choice % ').upper()
	if choice == 'B':
		start=input('Enter pick-up point > ')
		if start.upper() not in locations:
			print('Invalid location entered. Terminating program.');exit()
		end=input('Enter destination > ')
		if end.upper() not in locations:
			print('Invalid location entered. Terminating program.');exit()
		date=input('Enter date of travel [YYYY-MM-DD] > ')
		time=input('Enter date of travel [HH:MM] > ')
		ttype=input('Enter coach type > ')
		if ttype.capitalize() not in ctype:
			print('Invalid location entered. Terminating program.');exit()
		print('Booking details:----------------')
		print('You will board from',start)
		print('You will alight at',end)
		print('Journey date',date,time)
		print('You will be travelling in',ttype,'coach')
		print('--------------------------------')
		print('If satisfied with the booking, proceed by entering Y or pressing [Enter].\nElse, type N at the prompt to change.')
		input('> ')
		if input() == 'y':
			break
	elif choice == 'L':
		break
	elif choice == 'H':
		help()
	elif choice== 'K':
		print('System information:')
		sysinfo()
	else:
		print('Terminating program.')
		exit()


data.append([id,start,end,date,time,ttype])

df=pd.DataFrame(data,columns=['ID','From','To','Date','Time','Type'])


write=input('Save changes? [Yes] ')
if write.lower() == 'yes':
	df.to_csv('booking.csv')
	print('Changes saved.')
else:
	print('Changes not saved. Terminating program.')
	exit()
