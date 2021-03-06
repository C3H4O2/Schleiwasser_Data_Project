import sqlite3


class OverwritingDetected(Exception):
    def __init__(self):
        super().__init__('overwriting')



class Entry():
    def __init__(self):
        self.locations = ['GB1', 'GB2', 'GB3', 'GB4', 'GB5']

    def setup_db(self):
        self.locations = ['GB1', 'GB2', 'GB3', 'GB4', 'GB5']
        with sqlite3.connect('data.db') as conn:
            for i in self.locations:
                conn.execute(f'''CREATE TABLE IF NOT EXISTS {i}
                            (date DATE, time TIME, temp INTEGER, nitratAQ INTEGER, nitratWIN NUMERIC(10, 5), nitritAQ NUMERIC(10, 5), nitritWIN NUMERIC(10, 5), ammoniumAQ NUMERIC(10,5), ammoniumWIN NUMERIC(10,5), phosphatAQ NUMERIC(10,5), phosphatWIN NUMERIC(10,5), phWert NUMERIC(3,1), gpsLaenge NUMERIC(20,10), gpsBreite NUMERIC(20,10))''')

    def get(self, request):
        # global d
        name = request.args.get('name')
        da = request.args.get('date').replace(',', '.')
        da = '.'.join([i if len(i)>1 else "0"+i for i in da.split('.')[:-1]])+"."+da.split('.')[2]
        print(da)
        uz = request.args.get('uz').replace(',','.')
        uz = uz if not uz == '' else None
        ort = request.args.get('G').replace(',', '.')
        temp = request.args.get('temperatur').replace(',', '.')
        temp = float(temp) if len(temp)>0 and temp!='-' else None
        nitrat = request.args.get('nitrat').replace(',', '.')
        nitrat = float(nitrat) if len(nitrat)>0 and nitrat!='-' else None
        nwl = request.args.get('nwl').replace(',', '.')
        nwl = float(nwl) if len(nwl)>0 and nwl!='-' else None
        nitrit = request.args.get('nitrit').replace(',', '.')
        nitrit = float(nitrit) if len(nitrit)>0 and nitrit!='-' else None
        niwl = request.args.get('niwl').replace(',', '.')
        niwl = float(niwl) if len(niwl)>0 and niwl!='-' else None
        ammo = request.args.get('ammonium').replace(',', '.')
        ammo = float(ammo) if len(ammo)>0 and ammo!='-' else None
        awl = request.args.get('awl').replace(',', '.')
        awl = float(awl) if len(awl)>0 and awl!='-' else None
        phos = request.args.get('phosphat').replace(',', '.')
        phos = float(phos) if len(phos)>0 and phos!='-' else None
        pwl = request.args.get('pwl').replace(',', '.')
        pwl = float(pwl) if len(pwl)>0 and pwl!='-' else None
        ph = request.args.get('phwert').replace(',', '.')
        ph = float(ph) if len(ph)>0 and ph!='-' else None
        gpsx = request.args.get('gpsx').replace(',','.')
        gpsx = float(gpsx) if len(gpsx)>0 and gpsx!='-' else None
        gpsy = request.args.get('gpsy').replace(',','.')
        gpsy = float(gpsy) if len(gpsy)>0 and gpsy!='-' else None
        l = [da, uz, ort, temp, nitrat, nwl, nitrit, niwl, ammo, awl, phos, pwl, ph, gpsx, gpsy]

        f = open('log.txt', 'a')
        f.write(';'.join([str(i) for i in l])+'\t'+name+'\n')
        f.close()

        self.entry = dict()
        self.entry['loc'] = ort
        self.entry['date'] = da
        self.entry['time'] = uz
        self.entry['temp'] = temp
        self.entry['nitratAQ'] = nitrat
        self.entry['nitratWIN'] = nwl
        self.entry['nitritAQ'] = nitrit
        self.entry['nitritWIN'] = niwl
        self.entry['ammoniumAQ'] = ammo
        self.entry['ammoniumWIN'] = awl
        self.entry['phosphatAQ'] = phos
        self.entry['phosphatWIN'] = pwl
        self.entry['phWert'] = ph
        self.entry['gpsLaenge'] = gpsx
        self.entry['gpsBreite'] = gpsy

    def check_if_entry_exists(self, loc, date):
        with sqlite3.connect('data.db') as conn:
            c = conn.cursor()
            c.execute(f"SELECT * FROM {loc} WHERE date=?", (date,))
            if c.fetchone() == None:
                return False
            else:
                return True

    def edit_entry(self, date, loc, value_name, value):
        with sqlite3.connect('data.db') as conn:
            c = conn.cursor()
            # print(loc)
            c.execute(f"UPDATE {loc} SET {value_name}=? WHERE date=?", (value, date))
            conn.commit()

    def get_stored_entry(self, loc, date):
        with sqlite3.connect('data.db') as conn:
            c = conn.cursor()
            c.execute(f"SELECT * FROM {loc} WHERE date=?", (date,))
            row = c.fetchone()
            stored_entry = {'date': row[0], 'time': row[1], 'temp': row[2], 'nitratAQ': row[3], 'nitratWIN': row[4], 'nitritAQ': row[5], 'nitritWIN': row[6], 'ammoniumAQ': row[7], 'ammoniumWIN': row[8], 'phosphatAQ': row[9], 'phosphatWIN': row[10], 'phWert': row[11], 'gpsLaenge': row[12], 'gpsBreite': row[13]}
            return stored_entry

    def create_entry(self, loc, date):
        with sqlite3.connect('data.db') as conn:
            c = conn.cursor()
            c.execute(f"INSERT INTO {loc} (date) VALUES (?)", (date,))
            conn.commit()

    def check_for_overwriting(self):
        s_entry = self.get_stored_entry(self.entry['loc'], self.entry['date'])
        for i,v in s_entry.items():
            if self.entry[i] != v and v != None and self.entry[i] != None:
                print('OVERWRITING VALUES:', [i,v], [self.entry[i], self.entry['date'], self.entry['loc']])
                return True



    def prevent_overwriting(self):
        if self.check_if_entry_exists(self.entry['loc'], self.entry['date']):
            if self.check_for_overwriting():
                self.error()
        else:
            self.create_entry(self.entry['loc'], self.entry['date'])


    def error(self):
        raise OverwritingDetected

    def store(self):
        try:
            self.prevent_overwriting()
            for m, v in self.entry.items():
                if v != None and m != 'loc' and m != 'date':
                    self.edit_entry(self.entry['date'], self.entry['loc'], m, v)
        except OverwritingDetected:
            print('OVERWRITING PREVENTED. Values above')
            raise OverwritingDetected

    def get_table(self, table_name):
        with sqlite3.connect('data.db') as conn:
            c = conn.cursor()
            c.execute(f"SELECT * FROM {table_name}")
            return c.fetchall()

    def get_all_tables(self):
        tables = []
        for i in self.locations:
            tables.append(self.get_table(i))
        return tables
