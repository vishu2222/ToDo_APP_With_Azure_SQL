import pyodbc, keys

server = keys.server
database = keys.database
username = keys.username 
password = keys.password

cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()  

sql_command = """CREATE TABLE todo ( 
id INTEGER IDENTITY(1,1) PRIMARY KEY, 
content VARCHAR(200),
completed VARCHAR(4) DEFAULT 'No',
date_created DATE DEFAULT GETDATE()
);"""

cursor.execute(sql_command)

cnxn.commit()
cnxn.close()



