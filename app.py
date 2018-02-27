from flask import Flask, render_template, request, url_for
from utils.poke import *


app = Flask(__name__)

@app.route('/')
def root():
  return render_template('index.html')

@app.route('results',methods=['GET'])
def results():
	return render_template('results.html',result=main(request.form['args']) ,exit=url_for('root'))

if __name__ == "__main__":
  app.debug = True
  app.run()
