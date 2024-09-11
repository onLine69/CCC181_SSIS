from app_module import start_app
from dotenv import load_dotenv

load_dotenv('.env')

app = start_app()
app.debug = True

#if __name__ == '__main__':
#	start_app()