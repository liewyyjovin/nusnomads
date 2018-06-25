#!/usr/bin/python3
from app import app
from app import db
from app.models import Modules, Mapping

from modules_importer import ModuleImporter
from mapping_importer import MappingImporter

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import and_
from flask import Flask, render_template, url_for, request, session, redirect
from flask_login import current_user, UserMixin, login_user, logout_user, LoginManager
from oauth import OAuthSignIn

from pprint import pprint
from termcolor import colored
import json
import pdb

@app.route('/')
@app.route('/index', methods=['POST'])
def index():
    selected_unis = []
    module_code_list = []
    #combining module_code and module_title imported from ModuleImporter().db.module_load()
    module_data = ModuleImporter().db_module_load()
    #connect to db engine to use sql queries for sqlalchemy
    engine = create_engine('sqlite:///app.db')
    con = engine.connect()
    uni_content = con.execute('''
                SELECT DISTINCT(partner_uni), partner_uni_country, partner_uni_state,
                partner_uni_continent, partner_uni_image, COUNT(DISTINCT nus_module_1) as module_count
                FROM mapping
                GROUP BY partner_uni;
            ''')
    uni_content_list = []
    #return dict key:values for all content
    for uni in uni_content:
        uni_content = dict(uni)
        uni_content_list.append(uni_content)

    #making uni_content_list a json file

    return render_template('index.html', module_data=module_data, uni_content_list=uni_content_list)

#Continents Filter Endpoint
@app.route('/_continent_filters', methods=['POST'])
def continent_filters():
    continent_list = []
    engine = create_engine('sqlite:///app.db')
    con = engine.connect()
    selected_unis = []
    if request.method == 'POST':
        continents = request.get_json()
        for continent in continents['continentList']:
            continent_list.append(continent)
        print(continent_list)
        if len(continent_list) == 1:
            continent_uni = con.execute('''
                    SELECT DISTINCT(partner_uni) FROM mapping
                    WHERE partner_uni_continent = "{}"
                    GROUP BY partner_uni
                    '''.format(str(continent_list[0])))
        elif len(continent_list) == 2: 
            continent_uni = con.execute('''
                    SELECT DISTINCT(partner_uni) FROM mapping
                    WHERE partner_uni_continent = "{}"
                    OR partner_uni_continent = "{}"
                    GROUP BY partner_uni
                    '''.format(str(continent_list[0]), str(continent_list[1])))
        elif len(continent_list) == 3:
            continent_uni = con.execute('''
                    SELECT DISTINCT(partner_uni) FROM mapping
                    WHERE partner_uni_continent = "{}"
                    OR partner_uni_continent = "{}"
                    OR partner_uni_continent = "{}"
                    GROUP BY partner_uni
                '''.format(str(continent_list[0]), str(continent_list[1]), str(continent_list[2])))
        else: 
            continent_uni = con.execute('''
                    SELECT DISTINCT(partner_uni) FROM mapping
                    ''')
        mapped_uni_counter = 0
        for continent in continent_uni:
            selected_unis = [continent for continent, in continent_uni]
        for x in selected_unis:
            mapped_uni_counter += 1
        print(colored("Number of universities mapped:", "red") + " " + colored(str(mapped_uni_counter),"red"))
        print(selected_unis)
        return json.dumps(selected_unis)
 
    else: 
        return ''

#Modules Filter Endpoint
@app.route('/_module_filters', methods=['POST'])
def module_filters():
    module_code_list = []
    engine = create_engine('sqlite:///app.db')
    con = engine.connect()
    unis = con.execute('''
            SELECT DISTINCT(partner_uni) FROM mapping;
            ''')
    for uni in unis:
        all_unis = [uni for uni, in unis]
    if request.method == 'POST':
        selected_unis = all_unis
        mods = request.get_json()
        for mod in mods['selected_modules']:
            module_code = (mod.split()[0])
            module_code_list.append(module_code)

        if len(module_code_list) == 1:
            mapped_uni = con.execute(''' 
                SELECT DISTINCT(partner_uni) FROM mapping
                WHERE nus_module_1 LIKE "{}"
                GROUP BY partner_uni'''.format(str(module_code_list[0])))
        else: 
            mapped_uni = con.execute('''
                SELECT partner_uni FROM mapping
                WHERE nus_module_1 in {}
                GROUP BY partner_uni
                HAVING COUNT(DISTINCT nus_module_1) = {}'''.format(tuple(module_code_list), len(module_code_list)))
        mapped_uni_counter = 0
        for uni in mapped_uni:
            selected_unis = [uni for uni, in mapped_uni]
        for x in selected_unis:
            mapped_uni_counter += 1
        #selected_unis = list of unis after filtered by modules
        print(colored("Number of universities mapped:", "red") + " " + colored(str(mapped_uni_counter),"red"))
        print(selected_unis)
        return json.dumps(selected_unis)
    else: 
        return ''


@app.route('/school/<uni>')
def school_page(uni):
    engine = create_engine('sqlite:///app.db')
    con = engine.connect()
    school_details_query = con.execute('''
            SELECT DISTINCT(partner_uni), partner_uni_image, partner_uni_country, partner_uni_state
            FROM mapping
            WHERE partner_uni = "{}";
            '''.format(uni))
    #detail returns name, image, state, country of distinct university linked to endpoint
    for detail in school_details_query:
        school_details = dict(detail)
        print (school_details)

    module_query = con.execute('''
            SELECT nus_module_1, nus_module_1_title, nus_module_1_credits,
            partner_uni_module_1, partner_uni_module_1_title, partner_uni_module_1_credits, faculty
            FROM mapping
            WHERE partner_uni = "{}"
            GROUP BY nus_module_1;
            '''.format(uni))
    school_modules_list = []
    for module in module_query:
        school_modules = dict(module)
        school_modules_list.append(school_modules)
    print(school_modules_list)

    return render_template('schools.html', school=school_details, modules=school_modules_list)

@app.route('/about')
def about_page():
    return render_template('about.html')
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)


#OAuth authorization phase
@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    #If user is already logged in, redirect to index - if not, authorize with provider
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

#OAuth callback phase
@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user,True)
    return redirect(url_for('index'))




