from flask import Flask, render_template, request, redirect, make_response
# from db_manager import init_db, add_to_db, get_db_tables, get_db_data
from datetime import datetime, date
from entry import Entry
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
entry = Entry()

@app.route('/')
def index():
    visited_before = request.cookies.get('vb')
    if visited_before=='' or visited_before==None:
        resp = make_response(render_template('index.html'))
        resp.set_cookie('vb', 'True')
    else:
        return render_template('noanimation.html')
    return resp

@app.route('/data', methods = ['POST', 'GET'])
def data():
    cd = request.cookies.get('l') if request.cookies.get('l')!=None else ''
    try:
        entry.get(request)

        if request.args.get('send')=='send':
            entry.store()
    except Exception as e:
        if e == 'overwriting':
            return '''Overwriting ERROR'''
        else:
            print("ERROR:", e)


    dat = date.today()
    dat = str(dat)
    dat = dat[-2:]+'.'+dat[-5:-3]
    if request.args.get('url') != None:
        link = request.args.get('url')
        resp = make_response(render_template('main.html', date=dat, link=link))
    else:
        resp = make_response(render_template('main.html', date=dat, link='static/img/backgrounds/images.jpg'))

    try:
        resp.set_cookie('l', cd+' '.join([str(i) for i in l])+'\n')
        print(True, '; '.join([str(i) for i in l]))
    except:
        pass
    return resp

@app.route('/down')
def download():
    return render_template('log.txt')

# @app.route('/viewer', methods=['POST', "GET"])
# def viewer():
#     loc = request.args.get('loc')
#     l = ['GB1', 'GB2', 'GB3', 'GB4', 'GB5']
#     return render_template('viewer.html', l=l, loc=loc)

@app.route('/viewer', methods=['POST', 'GET'])
def tables():
    loc = request.args.get('loc')
    l = ['GB1', 'GB2', 'GB3', 'GB4', 'GB5']
    if loc == None:
        loc = 'GB1'
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
    return render_template('viewer.html', c = content, loc=loc, l=l)

@app.route('/cookiedata')
def cookiedata():
    cd = request.cookies.get('l') if request.cookies.get('l')!=None else ''
    l = cd.split('\n')
    for i in range(len(l)):
        l[i] = l[i].split(' ')
    print(l)
    return render_template('cookie_data.html', l=l)

@app.route('/chart', methods=['GET', 'POST'])
def chart():
    loc = request.args.get('loc')
    keyword = request.args.get('keyword')
    keys = ['date', 'time', 'temp', 'nitratAQ', 'nitratWIN', 'nitritAQ', 'nitritWIN', 'ammoniumAQ', 'ammoniumWIN', 'phosphatAQ', 'phostphatWIN', 'pHWert', 'gpsLaenge', 'gpsBreite']
    ind = keys.index(keyword)

    name = {'date':'Datum', 'time':'Zeit', 'temp':'Temperatur', 'nitratAQ':'Nitrat Aquanal', 'nitratWIN':'Nitrat WINLAB', 'nitritAQ':'Nitrit Aquanal', 'nitritWIN':'Nitrit WINLAB', 'ammoniumAQ':'Ammonium Aquanal', 'ammoniumWIN':'Ammonium WINLAB', 'phosphatAQ':'Phosphat Aquanal', 'phostphatWIN':'Phosphat WINLAB', 'pHWert':'pH-Wert', 'gpsLaenge':'GPS-Laengengrad', 'gpsBreite':'GPS-Breitengrad'}

    dic = dict()
    title = loc + ' - ' + name[keyword]

    for e in entry.get_table(loc):
        if not e[ind] == None:
            date = e[0]
            date = date.split('.')
            date = int(date[0])+int(date[1])*30+int(date[2])*365
            dic[date]=float(str(e[ind]).replace('<','').replace('>',''))
    di = dict()
    for i in sorted(dic):
        di[i] = dic[i]
    print(di)
    d = zip(di.keys(), di.items())
    return render_template('chart.html', d = d, title = title)




if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8081')
