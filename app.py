from flask import Flask, render_template, request
from utils.poke import *


app = Flask(__name__)

@app.route('/')
def root():
  return render_template('index.html')

@app.route('results',methods=['GET'])
def results():
	return main(request.form['args'])

if __name__ == "__main__":
  app.debug = True
  app.run()
