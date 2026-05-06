import sqlite3
from turtle import st
import bcrypt
# connect (creates file if it doesn’t exist)
conn = sqlite3.connect("FinancialTracker.db",check_same_thread=False)

# create a cursor (used to run queries)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS UserInfo(
    Userid INTEGER PRIMARY KEY AUTOINCREMENT,
    Countrycode TEXT,
    Phonenumber TEXT UNIQUE,
    Email_id TEXT UNIQUE,
    Regdate DATE DEFAULT CURRENT_DATE,
    Password BLOB
);
""")
# cursor.execute("""DROP TABLE IF EXISTS AssetsTracking;""")
# conn.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS AssetsTracking(
Userid INTEGER,
AssetId INTEGER PRIMARY KEY AUTOINCREMENT,
AssetType TEXT,
Symbol TEXT,
MovementType TEXT,
PriceBought REAL,
StockCurrencyCode TEXT,
Quantity TEXT,
SMSAlert BOOLEAN,
EmailAlert BOOLEAN,
FOREIGN KEY(userid) REFERENCES UserInfo(userid)
);""")

def check_user_info(phonenumber,emailid,password):
    hashedpassword=password.encode("utf8")
    
    cursor.execute("SELECT * FROM UserInfo WHERE Phonenumber=?  AND Email_id=?", (phonenumber,emailid))
    result=cursor.fetchone()
    cursor.execute("SELECT UserId FROM UserInfo WHERE Phonenumber=?", (phonenumber,))
    userid=cursor.fetchone()
    if result:
        if bcrypt.checkpw(hashedpassword, result[5]):  # Assuming password is the 6th column (index 5): 
         return True,userid
        else:
            return False,"Incorrect password"
    else:
        return False,"User not found"
result=check_user_info("8106378383","ayaanshchawla15@gmail.com","Ash123")
print(result)

def signup_user(phonenumber,emailid,password):
    encrypted_pass=password.encode("utf8")
    #encrypts it
    salt=bcrypt.gensalt()
    hashed_pass=bcrypt.hashpw(encrypted_pass,salt)
    cursor.execute("SELECT * FROM UserInfo WHERE Phonenumber=?", (phonenumber,))
    numcheck=cursor.fetchone()
    if numcheck:
        return False,"User with number already exists"
    else:
         cursor.execute("SELECT * FROM UserInfo WHERE Email_id=?", (emailid,))
         mail=cursor.fetchone()
         if mail:
                print("User with email already exists")
                return False,"User with email already exists"
         else:
               cursor.execute("INSERT INTO UserInfo (CountryCode, Phonenumber, Email_id, Password) VALUES (?, ?, ?, ?)",('+91',phonenumber, emailid, hashed_pass))
               print("User signed up successfully")
               conn.commit()
               cursor.execute("SELECT UserId FROM UserInfo WHERE Phonenumber=?", (phonenumber,))
               userid=cursor.fetchone()
               return True,userid

result,statement=signup_user("9742188333","ayaanshchawla15@gmail.com","Ash123")
print(result,statement)
cursor.execute("SELECT * FROM UserInfo WHERE Phonenumber=?", ("9742188333",))
print(cursor.fetchone())
cursor.execute("SELECT * FROM UserInfo")
print(cursor.fetchall())

def GetUserAssets(userid):
    cursor.execute("SELECT AssetType,Symbol,PriceBought,Quantity FROM AssetsTracking WHERE Userid=?", (userid,))
    assets=cursor.fetchall()
    return assets

# cursor.executemany(
#     "INSERT INTO AssetsTracking (Userid, AssetType, Symbol) VALUES (?, ?, ?)",
#     [
#         (1, "Stock", "AAPL"),
#         (1, "Stock", "AEROFLEX.NS")
#     ]
# )
conn.commit()
# cursor.execute('DELETE FROM AssetsTracking WHERE Symbol = "TSLA"')
conn.commit()

#deleting stock AEROFLEX AND ADANIENSOL
cursor.execute("SELECT * FROM AssetsTracking")
print(cursor.fetchall())
# cursor.execute("DELETE  FROM AssetsTracking")
# conn.commit()
def AddNewAsset(userid,assettype,symbol,MovementType,PriceBought,Quantity,SMSAlert,EmailAlert):
    try:
        cursor.execute("SELECT * FROM UserInfo WHERE Userid=?", (userid,))
        user=cursor.fetchone()
        if not user:
            print("User not found")
            return "User not found"
        else:
            cursor.execute("SELECT Quantity,PriceBought FROM AssetsTracking WHERE Userid=? AND Symbol=?", (userid,symbol))
            sim_asset=cursor.fetchone()
            
            if sim_asset:
                old_quan,old_price=sim_asset
                new_quan=int(old_quan)+int(Quantity)
                new_price=(int(PriceBought)+int(old_price))/2
                #getting average price if same stock is bought again
                cursor.execute("SELECT 1 from AssetsTracking WHERE Userid=? AND Symbol=? AND PriceBought=?",(userid,symbol,PriceBought))
                dup_asset=cursor.fetchone()
                if dup_asset:
                    print("Same stock bought at same price, merging quantity")
                    cursor.execute("""UPDATE AssetsTracking
                                    SET Quantity=?
                                    WHERE Userid=? AND Symbol=? AND PriceBought=?""",(new_quan,userid,symbol,PriceBought))
                    conn.commit()
                    return True, "Asset quantity updated successfully"
                #if price is same of the same stock under same user it merges the quantity
                else:
                    # cursor.execute("SELECT Price from AssetsTracking WHERE Userid=? AND Symbol=?",(userid,symbol))
                    # price=cursor.fetchone()
                    print("Same stock bought at different price, merging quantity and updating price to average of old and new price")
                    cursor.execute("""UPDATE AssetsTracking
                                    SET Quantity=?,PriceBought=?,MovementType=?,SMSAlert=?,EmailAlert=?
                                    WHERE Userid=? AND Symbol=? """,(new_quan,new_price,MovementType,SMSAlert,EmailAlert,userid,symbol))
                    conn.commit()
                    return True,"Asset quantity and price updated successfully"
            else:
                print("New Stock,Adding to DB")
                cursor.execute("INSERT INTO AssetsTracking (Userid, AssetType, Symbol, MovementType, PriceBought,Quantity, SMSAlert, EmailAlert) VALUES (?, ?, ?, ?, ?, ?, ?,?)",(userid,assettype,symbol,MovementType,PriceBought,Quantity,SMSAlert,EmailAlert))
                conn.commit()
                print("Asset added successfully")
                return True,"Asset added successfully"
    except sqlite3.Error as e:
        print(f"Error adding asset: {e}")
        return False,f"Error adding asset: {e}"

# AddNewAsset(1,"Stock","TSLA","Medium Movements",800.00,74,True,True)
# AddNewAsset(1,"Stock","TSLA","Medium Movements",750.00,10,True,True) 
def DeleteAsset(userid,symbol):
    try:
        cursor.execute("SELECT * FROM UserInfo WHERE Userid=?", (userid,))
        user=cursor.fetchone()
        #checks if user exists
        if not user:
            print("User not found")
            return "User not found"
        else:
            cursor.execute("SELECT * FROM AssetsTracking WHERE Userid=? AND Symbol=?", (userid,symbol))
            asset=cursor.fetchone()
            #checks if asset even exists
            if not asset:
                print("Asset not found in user's portfolio")
                return "Asset not found in user's portfolio"
            else:
                cursor.execute("DELETE FROM AssetsTracking WHERE Userid=? AND Symbol=?", (userid,symbol))
                conn.commit()
                #deletes the data
                print("Asset removed successfully")
                return "Asset removed successfully"
    except sqlite3.Error as e:
        print(f"Error removing asset: {e}")
        return f"Error removing asset: {e}"