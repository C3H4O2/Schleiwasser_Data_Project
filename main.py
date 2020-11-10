from flask import Flask, render_template, request, redirect, make_response
# from db_manager import init_db, add_to_db, get_db_tables, get_db_data
from datetime import datetime, date
from entry import Entry
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
entry = Entry()

@app.route('/', methods = ['POST', 'GET'])
def index():
    cd = request.cookies.get('l') if request.cookies.get('l')!=None else ''
    try:
        entry.get(request)

        if request.args.get('send')=='send':
            entry.store()
    except Exception as e:
        if e == 'overwriting':
            return render_template('.html', a=a)
        else:
            print("ERROR:", e)


    dat = date.today()
    dat = str(dat)
    dat = dat[-2:]+'.'+dat[-5:-3]
    if request.args.get('url') != None:
        link = request.args.get('url')
        resp = make_response(render_template('main.html', date=dat, link=link))
    else:
        resp = make_response(render_template('main.html', date=dat, link='static/images.jpg'))

    try:
        resp.set_cookie('l', cd+' '.join([str(i) for i in l])+'\n')
        print(True, '; '.join([str(i) for i in l]))
    except:
        pass
    return resp

@app.route('/down')
def download():
    return render_template('log.txt')

@app.route('/viewer')
def viewer():
    l = ['GB1', 'GB2', 'GB3', 'GB4', 'GB5']
    return render_template('viewer.html', l=l)

@app.route('/tables', methods=['POST', 'GET'])
def tables():
    loc = request.args.get('loc')
    content = entry.get_table(loc)
    content2 = []
    for i in content:
        content2.append([None for i in content[0]])
    for i in range(len(content)):
        for j in range(len(content[i])):
            if content[i][j] == None or content[i][j] == 'None':
                content2[i][j]='-'
            else:
                content2[i][j]=content[i][j]
    content = content2
    return render_template('tables.html', c = content, loc=loc)

@app.route('/cookiedata')
def cookiedata():
    cd = request.cookies.get('l') if request.cookies.get('l')!=None else ''
    l = cd.split('\n')
    for i in range(len(l)):
        l[i] = l[i].split(' ')
    print(l)
    return render_template('cookie_data.html', l=l)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8081')
