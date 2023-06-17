from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from utils.database import db_conn, db_session

Base = declarative_base()

class Cliente(BaseModel):
    """
    Pydantic model for client data.
    """
    username: str
    password: str
    name: str
    cpf: str
    email: str
    phone: str


engine = db_conn()

class ClienteDB(Base):
    """
    SQLAlchemy model for client data.
    """
    __tablename__ = "clientes"
    client_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(12), nullable=False, unique=True)

    
    def __repr__(self):
        return f"username: {self.username}, password: {self.password}, name: {self.name}, cpf: {self.cpf}, email: {self.email}, phone: {self.phone}"

    def save(self, session):
        """
        Saves client data to database.

        :param session: Database session.
        :type session: sqlalchemy.orm.session.Session
        """
        try:
            session.add(self)
            session.commit()
            session.refresh(self)
            session.close()

        except Exception as e:
            print(e)


    def update(self, session, **kwargs):
        """
        Updates client data in database.

        :param session: Database session.
        :type session: sqlalchemy.orm.session.Session
        :param kwargs: Key-value pairs of fields to be updated.
        :type kwargs: dict
        """
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
                self.save(session)

        except Exception as e:
            print(e)


    def delete(self, session):
        """
        Deletes client data from database.

        :param session: Database session.
        :type session: sqlalchemy.orm.session.Session
        """
        session.delete(self)
        session.commit()
        session.close()


Base.metadata.create_all(bind=engine)


async def create_client(data):
    """
    Creates a new client in the database.

    :param data: Client data.
    :type data: dict
    :return: Newly created client data.
    :rtype: dict
    """
    cliente = Cliente(**data)
    db_cliente = ClienteDB(
        username = cliente.username,
        password = cliente.password,
        name = cliente.name,
        cpf = cliente.cpf,
        email = cliente.email,
        phone = cliente.phone
    )

    try:
        sess= db_session()
        db_cliente.save(sess)
        return db_cliente

    except Exception as e:
        print(e)
        return {"error": "Failed to create client."}



def update_client(clientid, data):
    """
    Updates an existing client in the database.

    :param id: Client ID.
    :type id: int
    :param data: Client data to be updated.
    :type data: dict
    :return: Updated client data.
    :rtype: dict
    """
    db = db_session()
    db_cliente = db.query(ClienteDB).filter_by(client_id=clientid).first()

    try:
        db_cliente.update(db, **data)
        return db_cliente

    except Exception as e:
        print(e)
        return {"error": "Failed to update client."}


def delete_client(clientid):
    """
    Deletes an existing client from the database.

    :param id: Client ID.
    :type id: int
    """
    db = db_session()
    db_cliente = db.query(ClienteDB).filter_by(client_id=clientid).first()
    db_cliente.delete(db)


def get_clients():
    db = db_session()
    clients = db.query(ClienteDB).all()
    
    return clients