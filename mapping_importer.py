from app import app
from app import db
from app.models import Mapping

import time
import csv
from pprint import pprint
from termcolor import colored

class MappingImporter(object):
    #imports from mapping_data.csv to db table 'mapping'
    def mapping_csv_import(self):
        with open('mapping_data.csv', encoding='latin-1') as csvfile:
            row_counter = 0
            mapping_list = []
            mapping_data = csv.DictReader(csvfile)
            for result in mapping_data:
                row = {}
                row['faculty'] = result['faculty']
                row['partner_uni'] = result['partner_uni']
                row['partner_uni_country'] = result['partner_uni_country']
                row['partner_uni_state'] = result['partner_uni_state']
                row['partner_uni_continent'] = result['partner_uni_continent']
                row['partner_uni_image'] = result['partner_uni_image']
                row['partner_uni_module_1'] = result['partner_uni_module_1']
                row['partner_uni_module_1_title'] = result['partner_uni_module_1_title']
                row['partner_uni_module_1_credits'] = result['partner_uni_module_1_credits']
                row['partner_uni_module_2'] = result['partner_uni_module_2']
                row['partner_uni_module_2_title'] = result['partner_uni_module_2_title']
                row['partner_uni_module_2_credits'] = result['partner_uni_module_2_credits']
                row['nus_module_1'] = result['nus_module_1']
                row['nus_module_1_title'] = result['nus_module_1_title']
                row['nus_module_1_credits'] = result['nus_module_1_credits']
                row['nus_module_2'] = result['nus_module_2']
                row['nus_module_2_title'] = result['nus_module_2_title']
                row['nus_module_2_credits'] = result['nus_module_2_credits']
                mapping_list.append(row)
            pprint (mapping_list)
            #drop current table and create new one
            try:
                print(colored("Dropping Mapping Table...", "red"))
                Mapping.__table__.drop(db.session.bind)
                time.sleep(2)
                print(colored("Creating new Mapping Table...", "green"))
                Mapping.__table__.create(db.session.bind)
                time.sleep(2)
            except: 
            #if no current table exist, create new one
                print(colored("No Mapping Table currently exists...", "red"))
                time.sleep(2)
                print(colored("Creating new Mapping Table...", "green"))
                Mapping.__table__.create(db.session.bind)
                time.sleep(2)
            #add row to db
            for mapping in mapping_list:
                row_counter += 1
                print (mapping)
                row = Mapping(**mapping)
                db.session.add(row)
                print (colored('Row import no.', 'red') + ' ' + colored(str(row_counter), 'red'))
            
            db.session.commit()
            print (colored('Importing successful!', 'green'))

if __name__ == "__main__":
    app = MappingImporter()
    app.mapping_csv_import()

        

