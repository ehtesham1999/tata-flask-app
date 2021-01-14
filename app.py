from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
from os.path import join, dirname, realpath

app = Flask(__name__)

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = '/home/ehtesham1999/mysite/tata-flask-app/static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/return')
def return_status():
    return render_template('return.html',length=0)


@app.route("/record", methods=['POST'])
def record():
    mycursor = db.cursor()
    transaction_id = request.form['transaction_id']
    print('trasnsacion id :' + transaction_id)
    mycursor.execute("select * from orders where transaction_id=" + transaction_id)
    rows = []
    for x in mycursor:
        rows.append(x)
        print(x)
        print()

    mycursor.close()
    if len(rows)>0:
        return render_template("return.html", length=len(rows[0]), rows=rows[0])
    else:
        return render_template("return.html", length=0)

# Get the uploaded files
@app.route("/uploadfile", methods=['POST'])
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        print('File uploaded successfully')
        parseCSV(file_path)
    # save the file
    return render_template('upload.html')


def parseCSV(filepath):
    col_names = ['Order Date', 'Dispute Register Date ', 'Order ID', 'Transaction',
                 'Ticket Number ', 'Return Type', 'Product Name', 'Category L1',
                 'Amount', 'Seller name', 'Dispute Reason', 'Additional Comments',
                 'Case Status', 'Case closed date', 'Payment Status']
    csvData = pd.read_csv(filepath, names=col_names, header=None)
    mycursor = db.cursor()
    mycursor.execute("delete from orders")
    for i, row in csvData.iterrows():
        try:

            mySql_insert_query = """INSERT INTO orders (order_date,dispute_rg,order_id,transaction_id,ticket_number,return_type,product_name,category,amount,seller_name,dispute_reason,comments,
       case_status, close_date, payment_status) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s,%s) """

            recordTuple = (row['Order Date'], row['Dispute Register Date '], row['Order ID'], row['Transaction'],
                           row['Ticket Number '], row['Return Type'], row['Product Name'], row['Category L1'],
                           row['Amount'], row['Seller name'], row['Dispute Reason'], row['Additional Comments'],
                           row['Case Status'], row['Case closed date'], row['Payment Status'])

            mycursor.execute(mySql_insert_query, recordTuple)

            print(i, recordTuple)
            print()

        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))

    db.commit()
    mycursor.close()


if (__name__ == "__main__"):
    app.run(port=5000)

