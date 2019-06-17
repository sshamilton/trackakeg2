import sys
sys.path.append('/usr/local/lib/python2.7/')
from xbee import ZigBee
import mysql.connector
import serial

################################################
#make the database connection	
def getdata(xbee):
    db = 0
    try:
        db = mysql.connector.connect(host="localhost", user="kegerator", passwd="k3gs3v3r", db="kegerator")
    except:
        print("Failed to connect to database")
    #get header for IO data
    #cursor = db.cursor()
    while(True):
        rcvframe = xbee.wait_read_frame()
        decimalvalue = rcvframe['samples'][0]['adc-0']
        print ("Samples %s" % decimalvalue)
        #Prep to put into database
        #Get the last value
        cursor = db.cursor()
        cursor.execute("select * from kegerator_keg order by created_at desc limit 1")
        result = cursor.fetchall()
        for record in result:
            lastweight = record[0]
            #got the last weight, so comapre and insert into the database if different.
            if abs(lastweight-decimalvalue) > 4:
                print ("Inserting into db.  Old: %d" % lastweight)
                print ("New: %d" % decimalvalue)
                print ("INSERT into kegerator_keg(kegweight, created_at) values(%d, Now());" % decimalvalue)
                sqlexecute = cursor.execute("INSERT into kegerator_keg(kegweight, created_at) values(%d, Now());" % decimalvalue)
                print (cursor.rowcount)
            cursor.close()
            db.commit()
	
################################################

def main():
    try:
        print("Starting Kegserver")
        ser=serial.Serial('/dev/ttyUSB0',9600)
        xbee = ZigBee(ser)
        getdata(xbee)

        print ("Done")
    except Exception as e:
        print("Something didn't work: ", e)
	

if __name__ == "__main__":
    main()
