from dotenv import load_dotenv

from infrastructure.server import Server

load_dotenv()

server = Server()

app = server.get_app()