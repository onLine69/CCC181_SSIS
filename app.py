from flask import Flask  

app = Flask(__name__)  

@app.route("/") 
def hello_world():     
	return "<img src='https://i.pinimg.com/originals/51/fc/af/51fcaff8616d09f6893b9ee52efe7dfb.jpg'/>"
