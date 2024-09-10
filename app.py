from app_module import start_app
from dotenv import load_dotenv

load_dotenv('.env')

app = start_app()

#if __name__ == '__main__':
#	start_app()