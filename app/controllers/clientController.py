from fastapi import FastAPI, Request
from models.clientModel import create_client, get_clients, update_client, delete_client
import logging
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(debug=True)

@app.get("/clients")
def get():
    """
    Endpoint to get clients.
    Return: All clients.
    """
    return get_clients()

@app.post("/clients")
async def create_client_endpoint(request: Request):
    """
    Endpoint to create a new client.

    :param request: HTTP request object.
    :type request: Request
    :return: Created client.
    """
    try:
        data = await request.json()
        created_client = await create_client(data)
        logger.info("Client created: %s", created_client)
        return created_client

    except Exception as e:
        logger.error("Error creating client: %s", e)
        return e
    

@app.put("/clients/{client_id}")
async def update_client_endpoint(client_id: int, request: Request):
    """
    Endpoint to update an existing client.

    :param client_id: ID of client to update.
    :type client_id: int
    :param request: HTTP request object.
    :type request: Request
    :return: Updated client.
    """
    try:
        data = await request.json()
        updated_client =  update_client(client_id, data)
        logger.info("Client updated: %s", updated_client)
        return updated_client
    
    except Exception as e:
        logger.error("Error updating client: %s", e)
        return e
    

@app.delete("/clients/{client_id}")
async def delete_client_endpoint(client_id: int):
    """
    Endpoint to delete an existing client.

    :param client_id: ID of client to delete.
    :type client_id: int
    :param request: HTTP request object.
    :type request: Request
    :return: Deletion status message.
    """
    try:
        deletion_status = delete_client(client_id)
        logger.info("Client deleted: %s", client_id)
        return deletion_status
    
    except Exception as e:
        logger.error("Error deleting client: %s", e)
        return e
    
if __name__ =="__main__":
    uvicorn.run(app)