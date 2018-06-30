from app import app
from app import db
from app.models import Mapping

import time
import csv
import operator
from pprint import pprint
from termcolor import colored

class MappingImporter(object):
    #imports from mapping_data_modules.csv and mapping_data_details.csv to db table 'mapping'
    def mapping_csv_import(self):
        with open('mapping_data_details.csv', encoding='latin-1') as details:
            mapping_details_list = []
            mapping_data_details = csv.DictReader(details)
            for result in mapping_data_details:
                row = {}
                row['partner_uni'] = result['partner_uni']
                row['partner_uni_country'] = result['partner_uni_country']
                row['partner_uni_state'] = result['partner_uni_state']
                row['partner_uni_continent'] = result['partner_uni_continent']
                row['partner_uni_image'] = result['partner_uni_image']
                row['partner_uni_qs_ranking'] = result['partner_uni_qs_ranking']
                row['partner_uni_qs_mba_ranking'] = result['partner_uni_qs_mba_ranking']
                row['cost_sgd_min'] = result['cost_sgd_min']
                row['cost_sgd_max'] = result['cost_sgd_max']
                row['cost_sgd_avg'] = result['cost_sgd_avg']
                row['cost_native_min'] = result['cost_native_min']
                row['cost_native_max'] = result['cost_native_max']
                row['cost_native_avg'] = result['cost_native_avg']
                row['currency_type'] = result['currency_type']
                row['exchange_rate_to_sgd'] = result['exchange_rate_to_sgd']
                mapping_details_list.append(row)
            #pprint(mapping_details_list)

        with open('mapping_data_modules.csv', encoding='latin-1') as modules:
            row_counter = 0
            mapping_modules_list = []
            mapping_data_modules = csv.DictReader(modules)
            for result in mapping_data_modules:
                row = {}
                row['faculty'] = result['faculty']
                row['partner_uni'] = result['partner_uni']
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
                mapping_modules_list.append(row)
            #pprint (mapping_modules_list)

            #Merge both modules and details excel sheet
            for modules in mapping_modules_list:
                for details in mapping_details_list:
                    if modules['partner_uni'] == details['partner_uni']:
                        modules.update(details)

            pprint(mapping_modules_list)

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
            for mapping in mapping_modules_list:
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



