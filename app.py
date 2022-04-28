from flask import render_template
import os
from datetime import datetime
import pytz
from flask import Flask, jsonify, request, abort
import random, string
app = Flask(__name__)
# Google Sheets API Setup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
credential = ServiceAccountCredentials.from_json_keyfile_name("credentials.json",
                                                              ["https://spreadsheets.google.com/feeds",                                                               "https://www.googleapis.com/auth/spreadsheets",                                                        "https://www.googleapis.com/auth/drive.file",                                                        "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credential)
gsheet = client.open("RegistrationDocument").sheet1
@app.route('/all_records', methods=["GET"])
def all_records():
    return jsonify(gsheet.get_all_records())
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
        result = request.form
        print(result) 
        return render_template("index.html")
    else:
        return render_template("index.html")
    
@app.route("/register",methods=['GET', 'POST'])
def register():
    x = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))

    return render_template("register.html",x=x)

@app.route("/registerpage",methods=['GET', 'POST'])
def registerpage():
    if request.method == 'POST':
        result = request.form
        row=[]
        row.append(''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10)))
        row.append(request.form['name'])
        row.append(request.form['email'])
        row.append(request.form['college'])
        row.append(request.form['year'])
        row.append(request.form['department'])
        row.append(request.form['phone'])
        row.append(request.form['transaction'])
        IST = pytz.timezone('Asia/Kolkata')
        datetime_ist = datetime.now(IST)
        row.append(datetime_ist.strftime('%Y:%m:%d %H:%M:%S'))
        print(row)
        gsheet.insert_row(row, 2)  # since the first row is our title header
    
        return render_template("regresponse.html")
    else:   
        return render_template("register.html")
    
    
if __name__ == "__main__":
    app.run(debug=True)
