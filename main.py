from flask import Flask,render_template,request,session
import random
import time
import sqlite3

app = Flask(__name__)
app.secret_key = '1234'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test',methods=['GET',"POST"])
def testpage():
    if request.method=='POST':
        uname = request.form['name']
        session['name'] = uname


    '''To generate a random number'''
    new = random.randint(1,5)
    session['new'] = new 
    session['t0']  =  time.time()
    

    '''Data base connection'''
    con = sqlite3.connect('paragraph.db')
    cur = con.cursor()
    cur.execute("SELECT content FROM mypara WHERE ID=?",(new,))
    paradata = cur.fetchone()
    con.close()
    return render_template('test.html',paradata=paradata)


@app.route('/result',methods=['GET',"POST"])
def result():
    if request.method == "POST":
        t1 =  time.time()
        utyped = request.form['utyped']
        old = session['new']

        con = sqlite3.connect('paragraph.db')
        cur = con.cursor()
        cur.execute("SELECT content FROM mypara WHERE ID=?",(old,))
        paradata = cur.fetchone()
        con.close()

        # calculation
        wordcount = len(paradata[0].split( ))
        t0 = session['t0']
        t1 = t1
        timetaken = t1 - t0
        acc  = set(utyped.split()) & set(paradata[0].split())
        acclen = len(acc)
   
        accuracy = round((acclen/wordcount)*100)
        wpm= round( (acclen/timetaken) * 100 )
        na = wordcount - len(utyped.split())
        wrong = len(utyped.split()) - acclen
        tt =round((timetaken/60),2)

        return render_template('result.html',wordcount =wordcount,tt=tt,accuracy=accuracy,wpm=wpm,na=na,wrong=wrong)
    
        
if __name__ == '__main__':
    app.run(debug=True)