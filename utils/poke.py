# Team PokeMongo

'''
The data we are using is from https://pokeapi.co . It is a list of all the pokemon and their stats and abilities. We will be storing this information for the 1st 151 pokemon in the database.
command line argument examples:
python poke.py has_type grass

run with no command line arguments for list of commands
'''

import urllib2, json, sys
from pymongo import MongoClient

## Some globals
connection = MongoClient("homer.stuy.edu")
db = connection.PokeMongo
api_url = "http://pokeapi.co/api/v2/"


def get_poke_data(num):
    url = api_url + 'pokemon/' + str(num)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    obj = opener.open(url)
    obj = obj.read()
    return json.loads(obj)


def insert_pokemon(num):
    document = get_poke_data(num)
    db.pokemon.insert_one(document)


def heavier_than(weight):
    return db.pokemon.find({ "weight" : { "$gt" : weight } })

def lighter_than(weight):
    return db.pokemon.find({ "weight" : { "$lt" : weight } })

def has_type(_type):
    return db.pokemon.find({'types.type.name' : _type})

def has_name(name):
    return db.pokemon.find({'name' : name.lower()})

def has_id(pid):
    return db.pokemon.find({'id' : int(pid)})


def get_types(poke):
    types = []
    for type in poke['types']:
        types.append(type['type']['name'])
        # if(poke['types'][0]['slot'] == 2):
        #     tmp = types[0]
        #     types[0] = types[1]
        #     types[1] = tmp
    return types


def insert_all():
    db.pokemon.drop()
    x = 1
    while(x <= 151):
            insert_pokemon(x)
            print "completed " + str(x) + " out of 151"
            x += 1


def main(args):
    if(len(args) <= 1):
        print "not enough arguments"
        print "args"
        print "-----"
        print "upload_db - imports the dataset"
        print "heavier_than <weight> - gets every pokemon heavier than <weight>"
        print "lighter_than <weight> - gets every pokemon lighter than <weight>"
        print "has_type <type> - gets every pokemon with that type"
        print "has_name <species name> - gets the pokemon with that name"
        print "has_id <pokemon id num> - gets the pokemon with that id number"
    elif(args[1] == "upload_db"):
        print "\ngetting data from api"
        print "this might take a while"
        print "------------------------"
        insert_all()
    elif(args[1] == "heavier_than"):
        c = heavier_than(int(args[2]))
        for i in c:
            print i['name'] + ' : ' + str(i['weight'])
    elif(args[1] == "lighter_than"):
        c = lighter_than(int(args[2]))
        for i in c:
            print i['name'] + ' : ' + str(i['weight'])
    elif(args[1] == "has_type"):
        c = has_type(args[2])
        for i in c:
            print i['name'] + ' : ' + str(get_types(i))
    elif(args[1] == "has_name"):
        c = has_name(args[2])
        for i in c:
            print 'Found pokemon!'
            print 'id: ' + str(i['id'])
            print 'name: ' + str(i['name'])
            print 'types: ' + str(get_types(i))
    elif(args[1] == "has_id"):
        c = has_id(args[2])
        for i in c:
            print 'Found pokemon!'
            print 'id: ' + str(i['id'])
            print 'name: ' + str(i['name'])
            print 'types: ' + str(get_types(i))





if __name__ == '__main__':
    main(sys.argv)