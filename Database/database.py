import mysql.connector
from datetime import datetime

class MySQL_Database:
    def __init__(self):
        
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "queue"

    # Connection to the database
    # data = mysql.connector.connect(host=host, user=user, password=password, database=database)
    # cursor = data.cursor()  

    # Connection query to the database
    def __connection(self):
        try:
            connection_result = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = connection_result.cursor()
            cursor.execute("SELECT VERSION()")
            result = cursor.fetchone()
       

            return connection_result

        except mysql.connector.Error as err:
            print("connection error:", err)
            return None
        
    # show all tables
    def __listOfTables(self, table_name):
        conn = self.__connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")

        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()

        return table_name in tables

    # str(datetime.today().strftime('%Y-%m-%d'))
    def __create_table(self,table_name):
        try:
   
            conn = self.__connection()
            cursor = conn.cursor()
            
            cursor.execute(f"CREATE TABLE `{table_name}` (`id` INT NOT NULL AUTO_INCREMENT , `uid` VARCHAR(30000) NOT NULL , `name` VARCHAR(30000) NOT NULL , `timein` VARCHAR(30000) NOT NULL , `status` VARCHAR(30000) NOT NULL , PRIMARY KEY (`id`));")
    
            
            cursor.close()
            conn.close()
            
            return True
        except mysql.connector.Error as Err:
            print("__create_table: ",Err)
            return False
        
    # read specific data
    def __read_specific_Data(self,tableName,id_value,uid_value,status):
        try:

            conn = self.__connection()
            cursor = conn.cursor()

  
            # Delete the specified record from the HISTORY table
            read_query = f"SELECT * FROM `{tableName}` WHERE id = %s AND uid = %s"
            cursor.execute(read_query, (id_value, uid_value))
            data = cursor.fetchone()

            if data:
                cursor.close()
                conn.close()
                
                data = list(data)
                data[8] = status
                return tuple(data[1:])
        
            cursor.close()
            conn.close()
            print("__read_specific_Data: No data")
            return None

        except mysql.connector.Error as err:
            
            print("__read_specific_Data:", err)
            cursor.close()
            conn.close()
            return None
        
    # read specific data
    def __read_specific_data_user(self,name):
        try:

            conn = self.__connection()
            cursor = conn.cursor()

            read_query = f"SELECT * FROM `users` WHERE id = %s"
            cursor.execute(read_query, (1,))
            data = cursor.fetchone()
      
            if data:
                cursor.close()
                conn.close()
                return data
        
            cursor.close()
            conn.close()
            print("No data")
            return None

        except mysql.connector.Error as err:
            
            print("Error:", err)
            cursor.close()
            conn.close()
            return None

    # insert specific data
    def __insert_specific_Data(self,tableName,Data):
        try:

            conn = self.__connection()
            cursor = conn.cursor()

            # Execute INSERT query
            insert_query = f"INSERT INTO `{tableName}` (`id`, `name`, `section`, `department`, `course`, `professor`, `date`, `uid`, `status`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, Data)

            # Commit the transaction
            conn.commit()
        
            cursor.close()
            conn.close()

            return True

        except mysql.connector.Error as err:
            
            print("Error:", err)
            cursor.close()
            conn.close()
            return False
    
    # delete specific data
    def __delete_specific_Data(self,tableName,id_value,uid_value):
        try:

            conn = self.__connection()
            cursor = conn.cursor()

  
            # Delete the specified record from the HISTORY table
            delete_query = f"DELETE FROM `{tableName}` WHERE id = %s AND uid = %s"

            cursor.execute(delete_query, (id_value, uid_value))
            conn.commit()

            if cursor.rowcount > 0:
                cursor.close()
                conn.close()
 
                return "Data deleted successfully!"
        
            cursor.close()
            conn.close()
            print("No matching record found.")
            return "No matching record found."

        except mysql.connector.Error as err:
            
            print("Error:", err)
            cursor.close()
            conn.close()
            return err

    # Login as admin
    def login_as_admin(self, username=None, password=None):
        try:
            conn = self.__connection()
            cursor = conn.cursor()
        
            # Check if username exists
            cursor.execute("SELECT `id` FROM users WHERE username=%s", (username,))
            user_id = cursor.fetchone()
        
            if not user_id:
                cursor.close()
                conn.close()
                return False,"user not found"
            
            # Consume the result set
            cursor.fetchall()
        
            # Check if password is correct
            cursor.execute("SELECT `id`,`uid`,`username`,`name` FROM users WHERE username=%s AND password=%s", (username, password))
            user_data = cursor.fetchone()  # Fetch the row if it exists


            if user_data:
                data = [user for user in user_data]
  
                cursor.close()
                conn.close()
                return True,"login successful",data

            cursor.close()
            conn.close()
            return False,"invalid password",None
        
        except Exception as Err:
            print("login_as_admin:", Err)
            
            cursor.close()
            conn.close()
            
            return False,"invalid password",None
    
    # update password
    def update_password(self, uid=None,new_password=None, old_password=None):
        try:
            conn = self.__connection()
            cursor = conn.cursor()
        
            # Check if username exists
            cursor.execute("UPDATE `users` SET `password`=%s WHERE `id`= %s AND password=%s", (new_password,uid,old_password,))
            conn.commit()
            
            # Fetch the number of rows updated
            rows_updated = cursor.rowcount
            resultText,result = "invalid password",False
            
            if bool(rows_updated):
                resultText,result = "password updated",True
                
            print("Number of rows updated:", bool(rows_updated))
            
            # close db connection
            cursor.close()
            conn.close()
            return result,resultText
        
        except Exception as Err:
            print("update_password:", Err)
            
            cursor.close()
            conn.close()
            
            return False,"invalid password"
    
    # create account
    def create_account(self,uid,name,username,password ):
        try:

            conn = self.__connection()
            cursor = conn.cursor()

            # Execute INSERT query
            insert_query = "INSERT INTO `users` (`id`, `uid`, `name`, `username`, `password`) VALUES (NULL, %s, %s, %s, %s)"
            cursor.execute(insert_query, (uid,name,username,password,))

            # Commit the transaction
            conn.commit()
        
            cursor.close()
            conn.close()

            return True,"Account created!"

        except mysql.connector.Error as err:
            
            print("Error:", err)
            cursor.close()
            conn.close()
            return False,"Account could not created"
    # READ the appointment table
    def read_appointment(self,table,name):
        try:

            conn = self.__connection()
            cursor = conn.cursor(dictionary=True)
        
            # Select all rows from the HISTORY table
            select_query = f"SELECT * FROM `{table}` WHERE professor=%s"
            cursor.execute(select_query,(name,))

            # Fetch all rows from the result set
            rows = cursor.fetchall()
            
            # Convert rows to array
            # Transform rows into JSON-like dictionaries
            # data_list = [{
            #     'id': row['id'],
            #     'name': row['name'],
            #     'section': row['section'],
            #     'department': row['department'],
            #     'course': row['course'],
            #     'professor': row['professor'],
            #     'date': row['date'],
            #     'uid': row['uid'],
            #     'status': row['status']
            # } for row in rows]


            cursor.close()
            conn.close()

            # Return the JSON response
            return rows

        except mysql.connector.Error as err:
            print("Error:", err)
            cursor.close()
            conn.close()
            return None

    # UPDATE the appointment table
    def update_appointment(self,uid_value,id_value,status):
        data = self.__read_specific_Data(
            tableName="fillup",
            uid_value=uid_value,
            id_value=id_value,
            status=status)
        
        self.__insert_specific_Data(Data=data,tableName="proceed")
        self.__delete_specific_Data(tableName="fillup",id_value=id_value,uid_value=uid_value)
    
    # create prof attendance 
    def create_table_or_insert(self,name):
        try:
            
            card_uid = self.__read_specific_data_user(name=name)

            date_today =str(datetime.today().strftime('%Y-%m-%d'))
            time_now = str(datetime.now().strftime("%I:%M %p"))
        
            # create table
            if not self.__listOfTables(table_name=date_today):
                self.__create_table(table_name=date_today)
        
            conn = self.__connection()
            cursor = conn.cursor()
            
            # Check if prof is already login
            cursor.execute(f"SELECT `id` FROM `{date_today}` WHERE name=%s", (str(name),))
            user_id = cursor.fetchone()
            
   
            if user_id:
                cursor.close()
                conn.close()
              
                return f"{name} already login",True
            
            # Consume the result set
            cursor.fetchall()
                
            # Execute INSERT query
            insert_query = f"INSERT INTO `{date_today}` (`id`, `uid`, `name`, `timein`, `status`) VALUES (NULL, %s, %s, %s, %s)"
            cursor.execute(insert_query, (card_uid[1],name,time_now,"In Office"))

            # Commit the transaction
            conn.commit()
        
            cursor.close()
            conn.close()

            
            # insert table
            return f"{name} successfully login",True
        except Exception as e:
            print("insert: ",e)
            return "error occur",False

    def get_prof_today(self):        
        try:
            date_today = str(datetime.today().strftime('%Y-%m-%d'))
            
            conn = self.__connection()
            cursor = conn.cursor()
            
            # Check if prof is already login
            cursor.execute(f"SELECT `name` FROM `{date_today}` WHERE status=%s", (str("In Office"),))
            data = cursor.fetchall()
            
            # data fetched
            data_list = [row[0] for row in data]
                
            return data_list
        
        except:
            print("get_prof_today: error occue")
            return None
        
        
        
# MSQL = MySQL_Database()

# # message, result = MSQL.create_table_or_insert(name="Hello Friend")
# # print(message)
# # print(result)

# MSQL.create_account(uid="gusto ako lang gusto",name="KIYO MAPAGMAHAL",password="ikawlang",username="@kiyo")
