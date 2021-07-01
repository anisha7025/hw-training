import pymongo

from pymongo import MongoClient
client=MongoClient('localhost',27017)

db=client['task']
collection=db['sample3']

info=collection.find()
for document in info:
    print(document)

#create an index with URL as the key, also set it as a unique key
collection.create_index('url',unique=True)
index=collection.index_information()
print(index)


# add a new field - address, which has value city + zipcode for eg, "City": "Key West" , "Zip": "33040", then address will be "Key West,33040"
info=collection.find()
for document in info:
    collection.update_many({"_id":document["_id"]},{"$set":{"address":document["City"]+","+document["Zip"]}})
    print(document)


# remove all keys having value 'null'
def rm_null(d):
    if isinstance(d,dict):
        return {
            k:v
            for k,v in ((k,rm_null(v)) for k,v in d.items())
            if v
        }
    if isinstance(d,list):
        return [v for v in map(rm_null,d) if v]
    return d

info=collection.find()
for document in info:
    result=rm_null(document)
    print(result)
    collection.update(document,result)

#adding the data to a new collection
index=collection.index_information()
print(index)

collection1=db['sample_1']
for name,index_info in collection.index_information().items():
    collection1.create_index(keys=index_info['key'], name=name)

new_index=collection1.index_information()
print(new_index)


