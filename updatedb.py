# This script is to prepare the database for the Account Management Portal
# Author: Nur Atsirah Binte Kamsir
#pip install mysql-connector-python
import mysql.connector
import xlrd
from truthTable import truthTable
import yaml
from logs import logger


#establish database connection
conn = None
conn = mysql.connector.connect(user='root', password='P@ssword1',
                                       host='127.0.0.1',
                                       database='network_accounts')

recon_file = 'accountremediation_recon_2021.xlsx'
truthTable = truthTable()


if conn is not None and conn.is_connected():


    mycursor = conn.cursor()
    

    mycursor.execute("DROP TABLE IF EXISTS um_pa_tracking")
    mycursor.execute("DROP TABLE IF EXISTS um_privilegeaccounts")
    mycursor.execute("DROP TABLE IF EXISTS um_devices")
    mycursor.execute("DROP TABLE IF EXISTS um_roles")
    mycursor.execute("DROP TABLE IF EXISTS um_users")
    mycursor.execute("DROP TABLE IF EXISTS um_recon_tracking")



    createquery = "CREATE TABLE um_recon_tracking (id INT PRIMARY KEY UNIQUE AUTO_INCREMENT NOT NULL,recon_date DATETIME,totalaccountsscanned INT NOT NULL,totalhostnamescanned INT NOT NULL ,totalupdatedaccountcount INT NOT NULL ,totalupdatedhostnamecount INT NOT NULL ,totaladd INT NOT NULL ,totaldelete INT NOT NULL ,incyberark_notbreakglass INT NOT NULL ,inbreakglass_notcyberark INT NOT NULL ,notcyberark_notbreakglass INT NOT NULL);"
    mycursor.execute(createquery)
    print("1) Table um_recon_tracking created successfully\n")

    createquery = "CREATE TABLE um_privilegeaccounts (id INT PRIMARY KEY UNIQUE NOT NULL, name VARCHAR(255) NOT NULL);"
    mycursor.execute(createquery)
    print("1) Table um_privilegeaccounts created successfully\n")

    createquery = "CREATE TABLE um_devices (id INTEGER PRIMARY KEY UNIQUE NOT NULL, hostname VARCHAR(255), ipaddress VARCHAR(255) NOT NULL, devicetype VARCHAR(255),CONSTRAINT hostname_ip_devicetype UNIQUE (hostname, ipaddress))"
    mycursor.execute(createquery)
    print("2) Table um_devices created successfully\n")

    createquery = "CREATE TABLE um_roles (id INTEGER PRIMARY KEY AUTO_INCREMENT UNIQUE NOT NULL, name VARCHAR(255) NOT NULL)"
    mycursor.execute(createquery)
    print("3) Table um_roles created successfully\n")
            
    createquery = "CREATE TABLE um_users (id INTEGER PRIMARY KEY AUTO_INCREMENT UNIQUE NOT NULL, email VARCHAR (120), created_time DATETIME NOT NULL, role_id INT REFERENCES um_roles (id), password_hash VARCHAR (128), first_name VARCHAR (255), last_name VARCHAR(255));"
    mycursor.execute(createquery)
    print("4) Table um_users created succesfully\n")
            
    createquery = "CREATE TABLE um_pa_tracking (id INT PRIMARY KEY AUTO_INCREMENT,accountid INT NOT NULL, deviceid INT NOT NULL,in_network VARCHAR(50),in_cyberark VARCHAR(50) NOT NULL,in_passwordslip VARCHAR(50) NOT NULL ,in_uam VARCHAR(50) NOT NULL,assessment VARCHAR(50) NOT NULL,action_network VARCHAR(50),action_cyberark VARCHAR(50) NOT NULL,action_passwordslip VARCHAR(50) NOT NULL ,action_uam VARCHAR(50) NOT NULL,recon_status VARCHAR(255),FOREIGN KEY(accountid) REFERENCES um_privilegeaccounts(id),FOREIGN KEY(deviceid) REFERENCES um_devices(id),CONSTRAINT device_account_id UNIQUE (deviceid, accountid) );"
    mycursor.execute(createquery)
    print("5) Table um_pa_tracking created successfully\n")
 

    accountlist = []
    devicelist = []
    hostnamelist =[]
    accountid = 0
    deviceid = 0
    totalaccountsscanned = 0
    totalupdatedaccountcount = 0
    totaladd =0
    totaldelete =0

    hostnameremediation = {}


    wb = xlrd.open_workbook(recon_file)
    sheet = wb.sheet_by_index(0)
    for i in range(1,sheet.nrows):
        if (sheet.cell_value(i,0) == ''):
            continue

        totalaccountsscanned +=1
        account = sheet.cell_value(i,4)
        hostname = sheet.cell_value(i,1)
        

        ipaddress = sheet.cell_value(i,2)
        devicetype = sheet.cell_value(i,3)
        innetwork = sheet.cell_value(i,5)
        incyberark = sheet.cell_value(i,6)
        inbreakglass = sheet.cell_value(i,7)
        inuam = sheet.cell_value(i,8)
        assessment = sheet.cell_value(i,9)

        if hostname not in hostnamelist:
            hostnamelist.append(hostname)
            hostnameremediation[hostname] ={}
            hostnameremediation[hostname]['inbreakglass'] = 'N'
            hostnameremediation[hostname]['incyberark'] = 'N'
        if incyberark == 'Y' or incyberark == 'AD':
            hostnameremediation[hostname]['incyberark'] = 'Y'
        if inbreakglass =='Y' or inbreakglass =='AD':
            hostnameremediation[hostname]['inbreakglass'] = 'Y'


        if account not in accountlist:
            
            accountlist.append(account)
            accountid +=1

            
            query = "INSERT INTO um_privilegeaccounts(id,name) VALUES (%s,%s)"
            mycursor.execute(query,(accountid,account))
            conn.commit()   
            

        if (hostname,ipaddress,devicetype) not in devicelist:
            devicelist.append((hostname,ipaddress,devicetype))
            deviceid +=1

        
            query = "INSERT INTO um_devices(id,hostname,ipaddress,devicetype) VALUES (%s,%s,%s,%s)"
            mycursor.execute(query,(deviceid,hostname,ipaddress,devicetype))
            conn.commit()   
            

        if sheet.cell_value(i,6) == 'AD':
            actionnetwork = 'No Action Required'
            actioncyberark = 'No Action Required'
            actionbreakglass = 'No Action Required'
            actionuam = 'No Action Required'
        else:
            actionnetwork = truthTable.decisions[assessment]['network'][innetwork]
            actioncyberark = truthTable.decisions[assessment]['cyberark'][incyberark]
            actionbreakglass = truthTable.decisions[assessment]['passwordslip'][inbreakglass]
            actionuam = truthTable.decisions[assessment]['uam'][inuam]
        
        
        if (actionnetwork == 'No Action Required' and actioncyberark == 'No Action Required' and actionbreakglass == 'No Action Required' and actionuam == 'No Action Required'):
            
            totalupdatedaccountcount +=1
            query = "INSERT INTO um_pa_tracking(accountid, deviceid,in_network,in_cyberark,in_passwordslip,in_uam,assessment,action_network,action_cyberark,action_passwordslip,action_uam,recon_status) VALUES ((SELECT id FROM um_privilegeaccounts WHERE BINARY name = %s),(SELECT id FROM um_devices WHERE hostname = %s AND ipaddress = %s AND devicetype = %s),%s,%s,%s,%s,%s,%s,%s,%s,%s,'Closed')"
            mycursor.execute(query,(account,hostname,ipaddress,devicetype,innetwork,incyberark,inbreakglass,inuam,assessment,actionnetwork,actioncyberark,actionbreakglass,actionuam))
            conn.commit()
            
            print("Table um_pa_tracking updated successfully for entry "+ str(sheet.cell_value(i,0)))
        else:
            
            query = "INSERT INTO um_pa_tracking(accountid, deviceid,in_network,in_cyberark,in_passwordslip,in_uam,assessment,action_network,action_cyberark,action_passwordslip,action_uam,recon_status) VALUES ((SELECT id FROM um_privilegeaccounts WHERE BINARY name = %s),(SELECT id FROM um_devices WHERE hostname = %s AND ipaddress = %s AND devicetype = %s),%s,%s,%s,%s,%s,%s,%s,%s,%s,'Open')"
            mycursor.execute(query,(account,hostname,ipaddress,devicetype,innetwork,incyberark,inbreakglass,inuam,assessment,actionnetwork,actioncyberark,actionbreakglass,actionuam))
            conn.commit()
            
            print("Table um_pa_tracking updated successfully for entry "+ str(sheet.cell_value(i,0)))

        if actionnetwork =='Add':
            totaladd+=1
        if actioncyberark =='Add':
            totaladd+=1
        if actionbreakglass =='Add':
            totaladd+=1
        if actionuam =='Add':
            totaladd+=1
        if actionnetwork =='Delete':
            totaldelete+=1
        if actioncyberark =='Delete':
            totaldelete+=1
        if actionbreakglass =='Delete':
            totaldelete+=1
        if actionuam =='Delete':
            totaldelete+=1

    totalupdatedhostnamecount = 0
    incyberark_notbreakglass = 0
    inbreakglass_notcyberark = 0
    notcyberark_notbreakglass = 0

    for hostname in hostnameremediation:
        if hostnameremediation[hostname]['inbreakglass'] == 'Y' and hostnameremediation[hostname]['incyberark'] == 'Y':
            totalupdatedhostnamecount +=1
        elif hostnameremediation[hostname]['inbreakglass'] == 'Y' and hostnameremediation[hostname]['incyberark'] == 'N':
            inbreakglass_notcyberark +=1
        elif hostnameremediation[hostname]['inbreakglass'] == 'N' and hostnameremediation[hostname]['incyberark'] == 'Y':
            incyberark_notbreakglass +=1
        elif hostnameremediation[hostname]['inbreakglass'] == 'N' and hostnameremediation[hostname]['incyberark'] == 'N':
            notcyberark_notbreakglass +=1

    query = "INSERT INTO um_recon_tracking(recon_date,totalaccountsscanned,totalhostnamescanned,totalupdatedaccountcount,totalupdatedhostnamecount,totaladd,totaldelete ,incyberark_notbreakglass ,inbreakglass_notcyberark ,notcyberark_notbreakglass) VALUES (CURRENT_TIMESTAMP,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    mycursor.execute(query,(totalaccountsscanned,len(hostnamelist),totalupdatedaccountcount,totalupdatedhostnamecount,totaladd,totaldelete,incyberark_notbreakglass,inbreakglass_notcyberark,notcyberark_notbreakglass))
    conn.commit()

        







