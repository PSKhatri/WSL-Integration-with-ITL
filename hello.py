import os
from flask import Flask, request, redirect, url_for,render_template,jsonify,json
from werkzeug import secure_filename
from flask_jsglue import JSGlue
import csv
filenames=[]
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
    #print (os.getcwd())
    if request.method == 'POST':  
      uploaded_files = request.files.getlist("file[]")
      for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)

      #return redirect(url_for('uploaded_file', filename=filename))
      filenames=set(filenames)
      filenames=list(filenames)
      return render_template('hello1.html',filenames=filenames)    
    else:
      return render_template('hello1.html' , filenames=filenames)
@app.route('/readcsv', methods=['GET','POST'])
def readcsv():
      if request.method == 'POST':
        
        fname=request.get_data()
        #infiles=open('/inputFiles/input_files.csv')
        resultset = {}
        with open(fname, 'r+') as f:
          reader = csv.reader(f)
          i = 0;
          for row in reader:
            resultset[i] = row
            i= i+1

    
        print resultset
        return json.dumps(resultset)