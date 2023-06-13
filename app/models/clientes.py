from utils import database
from sqlalchemy import *
import bcrypt


class Client:
    @staticmethod
    def get_id(username, cpf):
        cursor = database.db_conn()
        cursor.execute("use bookrdb")
        query = "select client_id from `clientes` where username = %s"

    
        cursor.execute(query, (username))
        result = cursor.fetchall()
        return result

    def verify(username, cpf, email):
        bool = True
        cursor = database.db_conn()
        query ="use bookrdb"
        cursor.execute(query)


    #verificando o username
        query = "select count(1) from clientes where username = %s"
        cursor.execute(query, (username))
        result = cursor.fetchone()[0]
        if result != 0: 
            print("username em uso")
            bool = False
            return bool
  

    #verificando o cpf
        query = "select count(1) from clientes where %s = %s"
        cursor.execute(query, ("cpf",cpf))
        result = cursor.fetchone()[0]
        if result != 0: 
            print("cpf em uso")
            bool = False
            return bool
        

    #verificando o email
        query = "select count(1) from clientes where email = %s"
        cursor.execute(query, (email))
        result = cursor.fetchone()[0]
        if result != 0: 
            print("cpf em uso")
            bool = False
            return bool
        
        return bool

    def creation(username, password, cpf, name, email, phone):

        if Client.verify(username, password, cpf):
            try:
                salt = bcrypt.gensalt(12)
                password = bcrypt.hashpw(password.encode("utf-8"), salt)
                cursor = database.db_conn()


                cursor.execute("USE bookrdb")
                query=  '''
                        insert into `clientes`  (username, password, cpf, name, email, phone, salt) values (%s, %s, %s, %s, %s, %s, %s)
                        '''
                cursor.execute(query, (username, password, cpf, name, email, phone, salt))
                cursor.fetchall()

                print("Usuario criado com sucesso")

            except Exception as e:
                print(f"Failed - error: {e}")
        
        
        else: print("O cliente não passou na verificação.")
    
    def delete(username):
        pass


Client.creation("mathlimam", "abracadabra", "11111111111", "Matheus", "matheus", 71999448860)
