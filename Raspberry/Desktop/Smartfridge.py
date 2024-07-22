import psycopg2 as pg
from time import gmtime, strftime
#from SimpleCV import Camera

class DBcon:
    dbserver = 'localhost';
    dbusername = "postgres";
    dbpassword = "97237445";
    dbname = "SmartFridge";

    def __init__(self):
        self.con = pg.connect(host=DBcon.dbserver,database=DBcon.dbname, user=DBcon.dbusername, password=DBcon.dbpassword)
    
    def close_con(self):
        self.con.close()

    def get_cursor(self):
        self.cursor = self.con.cursor()
        return self.cursor

    def close_cursor(self):
        self.cursor.close()
       
    def commit(self):
        return self.con.commit()

# Get a camera shot.
#def photoShoot(filename='default.jpg'):
#    cam = Camera()
#    img = cam.getImage()
#    img.save(filename)


def getFridgeActualTemperature(fid='0'):
    databaseConnection = DBcon();
    cur = databaseConnection.get_cursor();

    cur.execute("select actualTemperature from fridge where fID='%s'"%(fid))
    actualTemperature = cur.fetchone()[0]
	
    databaseConnection.close_cursor()
    databaseConnection.close_con();
    return actualTemperature

def getFridgeDesiredTemperature(fid='0'):
    databaseConnection = DBcon();
    cur = databaseConnection.get_cursor();

    cur.execute("select desiredTemperature from fridge where fID='%s'"%(fid))
    desiredTemperature = cur.fetchone()[0]
	
    databaseConnection.close_cursor()
    databaseConnection.close_con();
    return desiredTemperature

def getFridgeHumidity(fid='0'):
    databaseConnection = DBcon();
    cur = databaseConnection.get_cursor();

    cur.execute("select humidity from fridge where fID='%s'"%(fid))
    humidity = cur.fetchone()[0]
	
    databaseConnection.close_cursor()
    databaseConnection.close_con();
    return humidity

def setFridgeActualTemperature(actualTemperature, fid='0'):
    databaseConnection = DBcon();
    cur = databaseConnection.get_cursor();

    cur.execute("update fridge set actualTemperature=%f  where fID='%s'"%(actualTemperature, fid))
    databaseConnection.commit()
	
    databaseConnection.close_cursor()
    databaseConnection.close_con();

def setFridgeDesiredTemperature(desiredTemperature, fid='0'):
    databaseConnection = DBcon();
    cur = databaseConnection.get_cursor();

    cur.execute("update fridge set desiredTemperature=%f  where fID='%s'"%(desiredTemperature, fid))
    databaseConnection.commit()
	
    databaseConnection.close_cursor()
    databaseConnection.close_con();

def setFridgeHumidity(humidity, fid='0'):
    databaseConnection = DBcon();
    cur = databaseConnection.get_cursor();

    cur.execute("update fridge set humidity=%f  where fID='%s'"%(humidity, fid))
    databaseConnection.commit()
	
    databaseConnection.close_cursor()
    databaseConnection.close_con();

def getName(pid):
    databaseConnection = DBcon();
    cur = databaseConnection.get_cursor();

    cur.execute("select name from product where pID='%s'"%(pid))
    name = cur.fetchone()[0]
	
    databaseConnection.close_cursor()
    databaseConnection.close_con();
    return name

def getWeight(pid):
    databaseConnection = DBcon();
    cur = databaseConnection.get_cursor();

    cur.execute("select weight from product where pID='%s'"%(pid))
    weight = cur.fetchone()[0]
	
    databaseConnection.close_cursor()
    databaseConnection.close_con();
    return weight

def isInfridge(pid):
    databaseConnection = DBcon();
    cur = databaseConnection.get_cursor();

    cur.execute("select inFridge from product where pID='%s'"%(pid))
    inFridge = cur.fetchone()[0]
	
    databaseConnection.close_cursor()
    databaseConnection.close_con();
    return inFridge

# DO NOT USE!!
def setInfridge(pid, isIn):
    databaseConnection = DBcon();
    cur = databaseConnection.get_cursor();

    cur.execute("update product set inFridge='%s'  where pID='%s'"%(isIn, pid))
    databaseConnection.commit()
	
    databaseConnection.close_cursor()
    databaseConnection.close_con();

def listFridge():
    databaseConnection = DBcon();
    cur = databaseConnection.get_cursor();

    cur.execute("select * from fridge")
    for fridge in cur.fetchall():
        print(fridge)
	
    databaseConnection.close_cursor()
    databaseConnection.close_con();

def listProducts():
    databaseConnection = DBcon();
    cur = databaseConnection.get_cursor();

    cur.execute("select * from product")
    for product in cur.fetchall():
        print(product)
	
    databaseConnection.close_cursor()
    databaseConnection.close_con();

def listTransactions():
    databaseConnection = DBcon();
    cur = databaseConnection.get_cursor();

    cur.execute("select * from transaction")
    for transaction in cur.fetchall():
        print(transaction)
	
    databaseConnection.close_cursor()
    databaseConnection.close_con();

def listProductsInFridge():
    databaseConnection = DBcon();
    cur = databaseConnection.get_cursor();

    cur.execute("select * from product where infridge=1")
    for product in cur.fetchall():
        print(product)
	
    databaseConnection.close_cursor()
    databaseConnection.close_con();

def listProductTransactions(pid):
    databaseConnection = DBcon();
    cur = databaseConnection.get_cursor();

    cur.execute("select * from transaction where product='%s'"%(pid))
    for transaction in cur.fetchall():
        print(transaction)
	
    databaseConnection.close_cursor()
    databaseConnection.close_con();

def updateWeight(pid, newweight):
    databaseConnection = DBcon();
    cur = databaseConnection.get_cursor();
    cur.execute("update product set weight='%s' where pID='%s'"%(newweight, pid))
    databaseConnection.commit()
	
    databaseConnection.close_cursor()
    databaseConnection.close_con();

def addProduct(pid, name, weight, expirationDate="NULL", fid='0'):
    databaseConnection = DBcon();
    cur = databaseConnection.get_cursor();

    cur.execute("insert into product values('%s', '%s', %s, %f, '%s', '%s')"%(pid, name, expirationDate, weight, '0', fid))
    databaseConnection.commit()
	
    databaseConnection.close_cursor()
    databaseConnection.close_con();

def newTransaction(photoPath, pid):
    gotin = True;
    if isInfridge(pid):
        gotin = False
    
    databaseConnection = DBcon();
    cur = databaseConnection.get_cursor();

    # Get transaction ID
    cur.execute('select count(*) from transaction')
    tid = int(cur.fetchone()[0]) + 1

    # Get photo
    photo = pg.Binary(open(photoPath, 'rb').read())

    # Get time and date
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    cur.execute("insert into transaction values('%s', %s, '%s', '%s', '%s')"%(tid, photo, time, pid, gotin))
    databaseConnection.commit()
	
    databaseConnection.close_cursor()
    databaseConnection.close_con();

def getLastPhoto(savepath='lastUser.jpg'):
    databaseConnection = DBcon();
    cur = databaseConnection.get_cursor();
        
    cur.execute("select userPhoto from transaction order by timestamp DESC")
    photo = cur.fetchone()[0]
    open(savepath, 'wb').write(photo)

    databaseConnection.close_cursor()
    databaseConnection.close_con();
    return photo

def checkProductExists(pid):
    databaseConnection = DBcon();
    cur = databaseConnection.get_cursor();
        
    cur.execute("select count(*) from product where pID='"+pid+"';")
    exists = cur.fetchone()[0]

    databaseConnection.close_cursor()
    databaseConnection.close_con();
    return exists
