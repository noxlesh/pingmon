# Ping Web Monitor
The web application helps to monitor a host's availability using ping program (Only if remote host can reply 
on ICMP request). It is written on Python v3.4, has build-in web server and uses MySQL as data storage.
It's tested on GNU Linux only.

# Requirements
Before you run Ping Web Monitor you need ***mysql-connector*** and ***mako*** modules installed into your system.
For Ubuntu 14.04 and above you can install ***python3-mysql.connector*** and ***python3-mako*** packages.Also required the MySQL 
database server. 

# Startup
Run ***python3 setup.py*** for initial setup the Ping Web Monitor.
Run ***python3 main.py*** to start the Ping Web Monitor.
