from flask import Flask, request, render_template, redirect, session
import csv

app = Flask(__name__)
app.secret_key = "MaSuperCleSecrete"  

@app.route('/',methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route('/save', methods=['POST'])
def save_message():
    new_message = []
    nom = request.form['nom']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']
    prenom = request.form['prenom']
    
    if prenom == "":

        new_message = [{'nom' : nom,"email" : email,"phone" : phone,"message" : message}]


   
        with open('message.csv', mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile,new_message[0].keys())
            writer.writerows(new_message)

    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    session["authentifie"]= "non"
    return render_template("login.html")


@app.route('/connect', methods = ['GET'])
def seConnecter():
    login = request.args.get('login')
    password = request.args.get('password')

    if login == "admin" and password == "1234":
        #je suis connecté
        session['authentifie'] = "oui"
        return redirect('/admin')
    else:
        session['authentifie'] = "non"
        return redirect('/login')

@app.route('/admin',methods=['GET', 'POST'])
def admin():

    logOK = session['authentifie']

    if logOK == "oui":
        with open('message.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  
            for row in reader:
                message = row[0]
            print(f'ID: {message}') 
        return render_template("admin.html")        
    else :
        return redirect('/login')
    
@app.route('/rgpd',methods=['GET', 'POST'])
def rg():
    return render_template("politiqueConf.html")
 


if __name__ == '__main__':
    app.run(host = "0.0.0.0" , port= 8000, debug=True)
