import os
from flask.json import dumps
from flask.json import JSONEncoder
from flask import Flask, request, redirect, url_for,render_template,jsonify,json
from werkzeug import secure_filename
from flask_jsglue import JSGlue
import csv
#filenames=[]
UPLOAD_FOLDER = 'inputFiles'
ALLOWED_EXTENSIONS = set(['csv'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET','POST'])#this '/' will be the root ie it will display the home play of the website
def hello():
     return render_template('hello1.html')

@app.route('/uploaded', methods=['GET','POST'])#this '/' will be the root ie it will display the home play of the website
def uploaded():
    global filenames
    filenames=[]
    print (os.getcwd())
    if request.method == 'POST':  
      uploaded_files = request.files.getlist("uploadedfiles[]")
      print(uploaded_files)
      for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)

      #return redirect(url_for('uploaded_file', filename=filename))
      filenames=set(filenames)
      filenames=list(filenames)
      print(filenames)
      return json.dumps(filenames)
    
@app.route('/readcsv', methods=['GET','POST'])
def readcsv():
      if request.method == 'POST':
        
        fname=request.get_data()
        #infiles=open('/inputFiles/input_files.csv')
        resultset = {}
        with open(fname, 'r+') as f:
          reader = csv.reader(f)
          i = 0
          for row in reader:
            resultset[i] = row
            i= i+1
        print resultset
        return json.dumps(resultset)


@app.route('/save', methods=['POST'])
def save():
    # read the posted values from the UI
    print("save me aya re")
    head=["Name","Domain","Source","Description"]
    name = request.form['name']
    print (name)
    domain = request.form['domain']
    #print (domain)
    source = request.form['source']
    description = request.form['description']
    if(not os.path.exists('inputFiles/input_files.csv')):
      f=open('inputFiles/input_files.csv','w')
      writer= csv.writer(f)
      writer.writerow(head)
      f.close()
    
    line=[name,domain,source,description]
    print(line)
    with open('inputFiles/input_files.csv') as inf, open('inputFiles/tmp_i.csv', 'w') as outf :
    	reader = csv.reader(inf) 
    	writer = csv.writer(outf)
      	flag=0
      	for row in reader:
	   		print(row)
	   		if(row[0]==name):
	   			flag=1
	   			writer.writerow(line)
	   		else:
	   			writer.writerow(row)
    	if(flag==0):
    		writer.writerow(line)


	
	os.remove('inputFiles/input_files.csv')

	os.rename('inputFiles/tmp_i.csv','inputFiles/input_files.csv')

@app.route('/retrieve', methods=['POST'])
def retrieve():
  fname=request.get_data()
  resultset1 = {}
  flag=0
  with open('inputFiles/input_files.csv', 'r+') as f:
    reader = csv.reader(f)
    for row in reader:
      if row[0]==fname:
        resultset1[0] = row
        flag=1
        break
    if flag==0:
      resultset1[0]=[fname,'','','']
        
  print resultset1
  return json.dumps(resultset1)
  

@app.route('/delete', methods=['POST'])
def delete():
  dfname=request.get_data()
  print(dfname)
  filenames.remove(dfname)
  print(filenames)
  os.remove('inputFiles/'+dfname)
  return json.dumps(filenames)
  