
<p align='center'> <img src='https://github.com/lvek4096/abc-ibs/assets/133903654/ecb1918c-20d0-4a13-a692-694cd3ac7cbf' alt='ABC Lines Icon'> </p>

# abc-ibs
 ABC Lines Integrated Booking System (IBS)
## About
This is the booking system for ABC Lines. 
### Features
 - Easy-to-use portal for agents to book and manage bus and taxi journeys
 - A well-stocked and easy administration suite:
	 - Database management
   	 - Export data to CSV
	 - Agent and administration management
	 - Booking and transaction management
- Support for ESC/POS printers over network (with [escpos](https://github.com/python-escpos/python-escpos) library)
- Ticket integration and printing
 

## How-to
### Setup
1. Clone the repository
2. Set up Python virtual environment
```
cd abc-ibs
python3 -m venv env			# or python -m venv env

env\scripts\activate			# on Windows
source env/bin/activate		# on Linux
```
4. Install dependencies <br>
```pip install -r requirements.txt```
### Running 
```python3 ibs.py``` or ```python ibs.py```<br>

## Development
This program is fully written in Python, and uses the MySQL relational database management system, allowing for cross-platform compatibility.<br>
Primary development has been mainly done on a Linux system, and the program has been successfully tested on Windows 10 and 11 as well.
### Additional libraries used
 - [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/)
 - [pandas](https://pandas.pydata.org/)
 - [escpos](https://github.com/python-escpos/python-escpos)
