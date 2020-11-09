from flask import Flask, render_template, request, redirect, make_response
# from db_manager import init_db, add_to_db, get_db_tables, get_db_data
from datetime import datetime, date
from entry import Entry

app = Flask(__name__)
entry = Entry()

@app.route('/', methods = ['POST', 'GET'])
def index():
    cd = request.cookies.get('l') if request.cookies.get('l')!=None else ''
    try:
        entry.get()

        if request.args.get('send')=='send':
            entry.store()

            f = open('log.txt', 'a')
            f.write(';'.join([str(da),str(uz), str(ort), str(temp), str(nitrat), str(nwl), str(nitrit), str(niwl), str(ammo), str(awl), str(phos), str(pwl), str(ph),str(gpsx),str(gpsy)])+'\t'+name+'\n')
            f.close()

    except:
        pass


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
    with open('templates/data.csv', 'r') as f:
        t = f.read().split('\n')
    for i in range(len(t)):
        t[i] = t[i].split(',')
    d = []
    for e in t:
        if e[0] not in d:
            if e[0]!="":
                d.append(e[0])
    print(d[1:], d[1:-1])
    d = d[1:]
    return render_template('viewer.html', d=d)

@app.route('/tables', methods=['POST', 'GET'])
def tables():
    f = open('templates/data.csv', 'r')
    t = f.read()
    f.close()
    t = t.split('\n')[:-1]
    for i in range(len(t)):
        t[i] = t[i].split(',')
    da = request.args.get('date')
    content1 = []
    for i, e in enumerate(t):
        if e[0]==da:
            content1.append(t[i])
    content = []
    for i, gb in enumerate(['GB1', 'GB2', 'GB3', 'GB4', 'GB5']):
        for e in content1:
            if str(e[1]).strip()==str(gb).strip() and str(e[1]).strip() not in [l[1] for l in content]:
                content.append(e)
            else:
                for j, v in enumerate(e):
                    if v.strip()!='' and v.strip()!='-':
                        if content[len(content)-1][j].strip()=='' or content[len(content)-1][j].strip()=='':
                            content[len(content)-1][j]=v
    for i in range(len(content), 5):
        content.append(['-','-','-','-','-','-','-','-','-','-','-'])
    return render_template('tables.html', content=content)

@app.route('/cookiedata')
def cookiedata():
    cd = request.cookies.get('l') if request.cookies.get('l')!=None else ''
    l = cd.split('\n')
    for i in range(len(l)):
        l[i] = l[i].split(' ')
    print(l)
    return render_template('cookie_data.html', l=l)

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port='8081')
