from app import app
from app import db
from app.models import Modules
from pprint import pprint
import json
from urllib.request import urlopen

import sqlalchemy
from sqlalchemy import create_engine
import time
from termcolor import colored
import pdb

class ModuleImporter(object):
    def __init__(self):
        self.modules = []
        with urlopen("http://api.nusmods.com/2017-2018/moduleInformation.json") as url:
            self.data = json.loads(url.read().decode())
            #pprint (self.data)

#json parse to javascript autocomplete
    def module_parser(self):
        mod_counter = 0
    # Currently, returns a list of dictionaries
        for x in self.data: 
            mod_counter += 1
            #print (mod_counter) There are around 5611 modules currently, append to empty list
            module_combined = x['ModuleCode'] + ' ' + x['ModuleTitle']
            self.modules.append(module_combined)
        #print(self.module_list)
        return(self.modules)
            #print (x['ModuleCode'])

#extract modules from json file taken from the api
#some missing values in keys - module_description, workload, preclusion, types, corequisite, prerequisite
    def module_extract(self):
        row_counter = 0
        for result in self.data:
            row = {}
            row['module_code'] = result['ModuleCode']
            row['module_title'] = result['ModuleTitle']
            row['department'] = result['Department']
            try:
                row['module_description'] = result['ModuleDescription']
            except:
                row['module_description'] = 'NIL'
            row['module_credit'] = result['ModuleCredit']
            try:
                row['workload'] = result['Workload']
            except:
                row['workload'] = 'NIL'
            try:
                row['preclusion'] = result['Preclusion']
            except:
                row['preclusion'] = 'NIL'
            try:
                row['types'] = result['Types']
                for types in row['types']:
                    row['types'] = types
            except: row['types'] = 'NIL'
            #don't need history data for now
            #row['history'] = result['History']
            try:
                row['corequisite'] = result['Corequisite']
            except:
                row['corequisite'] = 'NIL'
            try:
                row['prerequisite'] = result['Prerequisite']
            except:
                row['prerequisite'] = 'NIL'

            self.modules.append(row)
        #pprint (self.modules)
        #drop current table and create new one
        try:
            print(colored("Dropping Modules Table...", "red"))
            Modules.__table__.drop(db.session.bind)
            time.sleep(2)
            print(colored("Creating new Modules Table...", "green"))
            Modules.__table__.create(db.session.bind)
            time.sleep(2)
        except: 
        #if no current table exist, create new one
            print(colored("No Modules Table currently exists...", "red"))
            time.sleep(2)
            print(colored("Creating new Modules Table...", "green"))
            Modules.__table__.create(db.session.bind)
            time.sleep(2)
        #some_function(**some_dict) --> row = Modules(**module) --> row = Modules(module_code = 'xxx', module_title = 'xxx', department = 'xxx', ...) Unpacks contents of dictionary into function call
        for module in self.modules:
            row_counter += 1
            print (module)
            row = Modules(**module)
            db.session.add(row)
            print (colored('Row importing no.', 'red') + ' ' + colored(str(row_counter), 'red'))

        db.session.commit()
        print (colored('Importing successful!', 'green'))

    def db_module_load(self):
        engine = create_engine('sqlite:///app.db')
        con = engine.connect()
        module_combined_list = []
        module_combined = con.execute('''
                SELECT module_code as value, (module_code || ' ' || module_title) as label FROM modules;
                ''')
        for mod in module_combined:
            module_combined = dict(mod)
            module_combined_list.append(module_combined)
        
        #print (module_combined_list)
        return (module_combined_list)
            


if __name__ == "__main__":
    app = ModuleImporter()
    #app.module_parser()
    #app.module_extract()
    app.db_module_load()
