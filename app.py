from flask import Flask, redirect
from app_module import app

if __name__ == '__main__':
	app.run(debug=True)