import collections
from typing import Collection
from flask import Flask, request
import os

from flask.wrappers import Request
from dotenv import load_dotenv
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

client = PyMongo(app)


@app.route('/api/v1/strings', methods=['GET'])
def index():
    try:
        collection = client.db['StringLibrary']

        message = []

        for x in collection.find():
            message.append({'id':str(x['_id']), 'name':x['name']})

        return {'message':'Success','data':message}
    except:
        return {'message':'Failed','data':[]}


@app.route('/api/v1/string', methods = ['POST'])
def add_string():
    try:
        form = request.form
        print(form)

        if 'name' not in form:
            return {'message':'name parameter not available in body text'}

        name = form['name']
        collection = client.db['StringLibrary']

        x = collection.insert_one({'name':name, 'operations':[]})

        return {'id':str(x.inserted_id)}
    except Exception as e:
        return {'message':'Failed'}


@app.route('/api/v1/string/operation/<id>', methods=['GET'])
def retrive_string_operation(id):
    try:
        collection = client.db['StringLibrary']
        query = {'_id':ObjectId(id)}
        x = collection.find_one(query)

        if x:
            return {'message':'success','data':x['operations']}
        else:
            return {'mesage':'No query present with this id'}
    except Exception as e:
        print(e)
        return {'message':'Failed'}


@app.route('/api/v1/string/operation',methods=['POST'])
def perform_operations():
    
    form = request.form
    print(form)

    if (('id' not in form) or ('operation' not in form)):
        print('here')
        return {'message':'parameter needed are not defined'}
    else:    
        id = form['id']        
        if form['operation'] == 'reverse':
            return perform_reverse(id)

        elif form['operation'] == 'reverse_word':
            return reverse_word(id)
        
        elif form['operation'] == 'flip':
            return flip(id)
        
        elif form['operation'] == 'sort':
            return sort(id)
            
        else:
            return {'message':'operation not defined'}
        



def perform_reverse(id):
    try:
        
        collection = client.db['StringLibrary']

        query = {'_id':ObjectId(id)}

        document = collection.find_one(query)

        if not document:
            return {'message':'No such Id present'}

        curr_string = document['name']
        new_string = curr_string[::-1]

        new_id = collection.insert_one({'name':new_string, 'operations':[]})

        update_query = {
            '$push':{
                'operations':{'reverse':new_string}
            }
        }

        collection.update(query,update_query)

        return {'message':'success','id':str(new_id.inserted_id)}
    except:
        return {'message':'Failed'}

def reverse_word(id):
    try:
        collection = client.db['StringLibrary']
        query = {'_id':ObjectId(id)}

        document = collection.find_one(query)

        if not document:
            return {'message':'No such Id present'}

        curr_string = document['name']

        new_string = ' '.join(curr_string.split()[::-1])

        new_id = collection.insert_one({'name':new_string, 'operations':[]})

        update_query = {
            '$push': {
                'operations' : {'reverse_word':new_string}
            }
        }

        collection.update(query, update_query)

        return {'message':'success','id':str(new_id.inserted_id)}
    except:
        return {'message':'Failed'}

def flip(id):
    try:
        collections = client.db['StringLibrary']

        query = {'_id':ObjectId(id)}
        document = collections.find_one(query)

        if not document:
            return {'message':'No such Id present'}

        cur_string = document['name']
        l = len(cur_string)//2

        new_string = cur_string[l+1:] + cur_string[0:l+1]

        new_id = collections.insert_one({'name':new_string, 'operations':[]})

        update_query = {
            '$push': {
                'operations':{'flip':new_string}
            }
        }

        collections.update(query,update_query)

        return {'message':'success','id':str(new_id.inserted_id)}
    except:
        return {'message':'Failed'}

def sort(id):
    try:
        collection = client.db['StringLibrary']

        query = {'_id':ObjectId(id)}
        document = collection.find_one(query)

        if not document:
            return {'message':'No such Id present'}

        curr_string = document['name']
        new_string = ''.join(sorted(curr_string))

        new_id = collection.insert_one({'name':new_string, 'operations':[]})

        update_query = {
            '$push': {
                'operations':{'sort':new_string}
            }
        }

        collection.update(query,update_query)

        return {'message':'success','id':str(new_id.inserted_id)}
    except:
        return {'message':'Failed'}
    
@app.errorhandler(404)
def page_not_found(e):
    return {'message':'No operation perform here :-(. Refere API documentation'}


if __name__ == '__main__':
    app.run()