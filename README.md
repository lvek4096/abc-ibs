
<p align='center'> <img src='https://github.com/lvek4096/abc-ibs/assets/133903654/ecb1918c-20d0-4a13-a692-694cd3ac7cbf' alt='ABC Lines Icon'> </p>

# abc-ibs
 ABC Lines Integrated Booking System (IBS)
## About
This is the booking system for ABC Lines. 
### Features
 - Easy-to-use portal for agents to book and manage bus and taxi journeys
 - Well-stocked and easy administration suite:
	 - Database management
   	 - Export data to CSV
	 - Agent and administration management
	 - Booking and transaction management
	- Ticket integration
- Support for ESC/POS printers over network (with [escpos](https://github.com/python-escpos/python-escpos) library)
- Ticket printing
	- Multiple ticket printing for bus journeys with multiple passengers
 

## How-to
### Setup
1. Clone the repository
2. Set up Python virtual environment
```
cd abc-ibs
python3 -m venv env			# or python -m venv env

env\scripts\activate			# on Windows
source env/scripts/activate		# on Linux
```
4. Install dependencies <br>
```pip install -r requirements.txt```
### Running 
```python3 main.py``` or ```python main.py```
On Linux systems, you can directly run the file by making it executable: ```chmod +x main.py```	
<br>(or make file executable via GUI file manager).

Then, you can run directly with  ```./main.py``` (or from the GUI file manager).

On Windows systems, you can replicate this behaviour with Python Launcher, with minimal additional setup*.<br>
Just double-click 'main.py', and you're good to go!

<b>*NOTE:</b>
- It is highly recommended use <a href="https://www.python.org/downloads">regular Python distribution</a> (.exe installer) for the same.
- Python Launcher needs to be installed during Python setup. 
- Using the <a href="https://apps.microsoft.com/store/detail/python-311/9NRWMJP3717K">Microsoft Store</a> distribution of Python will not work with the above as it lacks Python Launcher.
- Ensure that app execution aliases for python.exe and python3.exe are disabled.

## Development
This program is fully written in Python, and uses the MySQL relational database management system, allowing for cross-platform compatibility
Primary development has been mainly done on a Linux system, and the program has been successfully tested on Windows 10 and 11 as well.
### Additional libraries used
 - [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/)
 - [pandas](https://pandas.pydata.org/)
 - [escpos](https://github.com/python-escpos/python-escpos)
