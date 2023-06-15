import json
from utils import database
from sqlalchemy import Table, delete, select, MetaData, insert, func
import bcrypt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Client:
    """
    A class representing a client in the system.
    """

    @staticmethod
    def get_client_id(username):
        """
        Returns the client ID of the specified username.

        :param username: Username of client.
        :type username: str
        :return: Client ID.
        :rtype: int
        """
        engine = database.db_conn()
        clientes = Table('clientes', MetaData(), autoload_with=engine)
        query = select(clientes.c.client_id).where(clientes.c.username == username)
        result = engine.execute(query)

        return result.scalar()

    @staticmethod
    def verify(username, cpf, email):
        """
        Verifies if the specified username, CPF, and email are available for client creation.

        :param username: Username of client.
        :type username: str
        :param cpf: CPF of client.
        :type cpf: str
        :param email: Email of client.
        :type email: str
        :return: True if all specified fields are available, False otherwise.
        :rtype: bool
        """
        engine = database.db_conn()
        clientes = Table('clientes', MetaData(), autoload_with=engine)

        try:
            # Verify username
            query = select(func.count(1)).where(clientes.c.username == username)
            result = engine.execute(query)
            count = result.scalar()
            if count != 0: 
                logger.warning("Username already in use.")
                return False

            # Verify CPF
            query = select(func.count(1)).where(clientes.c.cpf == cpf)
            result = engine.execute(query)
            count = result.scalar()
            if count != 0: 
                logger.warning("CPF already in use.")
                return False

            # Verify email
            query = select(func.count(1)).where(clientes.c.email == email)
            result = engine.execute(query)
            count = result.scalar()
            if count != 0: 
                logger.warning("Email already in use.")
                return False
        
            return True
        
        except Exception as e:
            logger.error("Error verifying client information. Error: %s", e)
            return False

    @staticmethod
    def create(req):
        """
        Creates a new client with the specified information.

        :param username: Username of client.
        :type username: str
        :param password: Password of client.
        :type password: str
        :param cpf: CPF of client.
        :type cpf: str
        :param name: Name of client.
        :type name: str
        :param email: Email of client.
        :type email: str
        :param phone: Phone number of client.
        :type phone: str
        """
        # Connect to database and table
        engine = database.db_conn()
        clientes = Table("clientes", MetaData(), autoload_with=engine)

        data = req

        if Client.verify(data['username'], data['cpf'], data['email']):
            try:
                data['password'] = bcrypt.hashpw(data['password'], bcrypt.gensalt(12))
                
                with engine as conn:
                    conn.execute(insert(clientes).values(**data))
                    conn.commit()
                    logger.info("Client created successfully.")

            except Exception as e:
                logger.error("Client creation failed. Error: %s", e)

    @staticmethod
    def delete(username):
        """
        Deletes the client with the specified username.

        :param username: Username of client.
        :type username: str
        """
        try:
            engine = database.db_conn()
            clientes = Table("clientes", MetaData(), autoload_with=engine)

            client_id = Client.get_client_id(username)

            stmt = delete(clientes).where(clientes.c.client_id == client_id)

            with engine as conn:
                conn.execute(stmt)
                conn.commit()
                logger.info("Client deleted successfully.")

        except Exception as e:
            logger.error("Client deletion failed. Error: %s", e)