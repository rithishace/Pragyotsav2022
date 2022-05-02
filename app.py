from flask import flash,render_template,redirect,url_for
import os
from datetime import datetime
import pytz,json
from flask import Flask, jsonify, request, abort
import random, string
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
# Google Sheets API Setup
import gspread
UPLOAD_FOLDER = '/tmp'
from pcloud import PyCloud

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']

from oauth2client.service_account import ServiceAccountCredentials
credential = ServiceAccountCredentials.from_json_keyfile_name("credentials.json",
                                                              ["https://spreadsheets.google.com/feeds",                                                               "https://www.googleapis.com/auth/spreadsheets",                                                        "https://www.googleapis.com/auth/drive.file",                                                        "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credential)
gsheet = client.open("RegistrationDocument").sheet1
gfeedback = client.open("Feedback").sheet1


@app.route('/all_records', methods=["GET"])
def all_records():
    y=gsheet.get_all_records()
    print(y,type(y))
    x=jsonify(y)
    print(x,type(x))
    return jsonify(y)
@app.route('/add_record')
def add_record():    
    row = ['kumar',"date","score"]
    gsheet.insert_row(row, 2)  # since the first row is our title header
    return jsonify(gsheet.get_all_records())
@app.route('/del_record/<email>', methods=["DELETE"])
def del_record(email):
    cells = gsheet.findall(str(email))
    for c in cells:
        gsheet.delete_row(c.row)
    return jsonify(gsheet.get_all_records())
@app.route('/update_record', methods=["PATCH"])
def update_record():
    req = request.get_json()
    cells = gsheet.findall(req["email"])
    for c in cells:
        gsheet.update_cell(c.row, 3, req["score"])
    return jsonify(gsheet.get_all_records())

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        row=[]
        row.append(request.form['name'])
        row.append(request.form['email'])
        row.append(request.form['message'])
        IST = pytz.timezone('Asia/Kolkata')
        datetime_ist = datetime.now(IST)
        row.append(datetime_ist.strftime('%Y:%m:%d %H:%M:%S'))
        gfeedback.insert_row(row, 2)
        return render_template("index.html")
    else:
        return render_template("index.html")
    
@app.route("/register",methods=['GET', 'POST'])
def register():
    x='rithish'
    return render_template("register.html",x=x)

@app.route("/registerpage",methods=['GET', 'POST'])
def registerpage():
    if request.method == 'POST':
        row=[]
        zy=''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        row.append(zy)       
        IST = pytz.timezone('Asia/Kolkata')
        datetime_ist = datetime.now(IST)
        row.append(datetime_ist.strftime('%Y:%m:%d %H:%M:%S'))        
        for list_type in request.form.items():
            row.append(list_type[1])
            print(list_type)
        if 'file' not in request.files:
            return 'Add the screenshot of the transaction!!'
        file1 = request.files['file']
        extension=file1.filename.split(".")[1]
        file1.filename=zy+'.'+extension
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        
        gsheet.insert_row(row, 2)  # since the first row is our title header
        # storage.child('images/foo.jpg').put(path)
        pc = PyCloud('rithish2k18@gmail.com', 'luffy00$')
        pc.uploadfile(files=[path],path='/pragyotsav')
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'],file1.filename ))
        
        return render_template("regresponse.html",reg=row[0],name=request.form['TeamLead'],ename=request.form['Event'])
    else:   
        return render_template("register.html")

@app.route("/admin",methods=['GET', 'POST'])
def admin():
    if request.method=='POST':
        records=gsheet.get_all_records()
        if(request.form['regid'] and request.form['regid'].strip()):
            res=[d for d in records if d['Id'] == request.form['regid'].strip()]
        elif(request.form['name'] and request.form['name'].strip()):
            res=[d for d in records if d['TName'] ==request.form['name'].strip()]
        elif(request.form['email'] and request.form['email'].strip()):
            res=[d for d in records if d['TEmail'] == request.form['email'].strip()]
        elif(request.form['transaction'] and request.form['transaction'].strip()):
            res=[d for d in records if d['Transaction'] == request.form['transaction'].strip()]
        else:
            res=records   
        
        
        return render_template("admin.html",data=res)
    else:
        return render_template("admin.html",data={})
@app.route("/test",methods=['GET', 'POST'])
def test():
   

    return 'ok'
    
if __name__ == "__main__":
    app.run(debug=True)
