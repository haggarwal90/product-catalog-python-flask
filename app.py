from flask import Flask, request, render_template, redirect
import csv

# Initialize flask application
app = Flask(__name__);

@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html')

@app.route('/products' ,methods = ['GET', 'POST', 'PUT'])
def getOrSetProducts():
    if request.method == 'GET':
        productsResponse = {"items": []}
        with open('database/products.csv', 'r') as productscsv:
            productsReader = csv.reader(productscsv, delimiter=',')
            for idx, row in enumerate(productsReader):
                temp = ','.join(row)
                productsResponse['items'].insert(idx, temp)
            return render_template('products.html', products = productsResponse)
    elif request.method == 'POST':
        formProductName = request.form['name']
        frmProductQuantity = request.form['quantity']
        formProductPrice = request.form['price']
        try:
            with open('database/products.csv', 'a') as productscsv:
                productsWriter = csv.writer(productscsv, delimiter=',')
                productsWriter.writerow([formProductName, frmProductQuantity, formProductPrice])
        except:
            return 'Failed'
        return 'Success'
    elif request.method == 'PUT':
        return "Product update not supported yet"



@app.route('/products/<name>' ,methods = ['GET', 'DELETE'])
def getOrDeleteProductById(name):
    if request.method == 'GET':
        with open("database/products.csv", 'r') as productscsv:
            productReader = csv.reader(productscsv, delimiter=',')
            for row in productReader:
                if row[0] == name:
                    return ','.join(row)
            return 'Error'
    elif request.method == 'DELETE':

        return "Delete by id called"

@app.route('/login', methods = ['POST'])
def authenticate():
    if request.method =='POST':
        print "post request recieved" + request.form['username']
        formUser = request.form['username']
        formPassword = request.form['password']
        with open('database/users.csv', 'r') as usercsv:
            userReader = csv.reader(usercsv, delimiter=',')
            for row in userReader:
                if row[0] == formUser and row[1] == formPassword:
                    return redirect('/products')
            return render_template('login.html', message = "Incorrect credential")

@app.route('/signup', methods = ['POST'])
def register():
    formUser = request.form['username']
    formPassword = request.form['password']
    try:
        with open('database/users.csv' , 'a') as usercsv:
            userWriter = csv.writer(usercsv, delimiter=',')
            userWriter.writerow([formUser, formPassword])
    except:
        return 'Failed'
    return 'Success'


if __name__ == '__main__':
    app.run();