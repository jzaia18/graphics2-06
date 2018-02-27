from flask import Flask, render_template, request, url_for, redirect
from utils.poke import *


app = Flask(__name__)

@app.route('/')
def root():
  return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
  if 'query_type' not in request.form or 'query' not in request.form:
    return render_template('index.html', err='Error in form submission, please try again')
  args = ['', request.form['query_type']]
  args.append(request.form['query'])

  print 'ARGS', args

  result = main(args, print_result = True)
  if not result:
    result = 'No results found.'

  return render_template('results.html', result = result ,exit=url_for('root'))

if __name__ == "__main__":
  main(['', 'upload_db']) #Upload the DB
  app.debug = True
  app.run()
