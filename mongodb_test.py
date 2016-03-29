def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.sfosm
    return db

if __name__ == "__main__":
    db = get_db()
    
    # postcode
    # results =  db.sfosm.aggregate( [ { "$match" : { "address.postcode" : { "$exists" : 1 }}}, { "$group" : { "_id" : "$address.postcode", "count" : { "$sum" : 1 }}}, { "$sort" : { "count" : 1 }}])
    
    # cities
    # results = db.sfosm.aggregate( [ { "$match" : { "address.city" : { "$exists" : 1 } } } , { "$group" : { "_id" : "$address.city", "count" : { "$sum" : 1 } } } , { "$sort" : { "count" : 1 } } ] )

    # unique users
    # import pprint
    # pprint.pprint(len(db.sfosm.distinct("created.user")))

    # top one contributing user
    # results = db.sfosm.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}},{"$sort":{"count":1}},{"$limit":1}])

    results = db.sfosm.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, {"$group":{"_id":"$count", "num_users":{"$sum":1}}}, {"$sort":{"_id":1}}, {"$limit":1}])

    # print db.sfosm.find_one()
    
    import pprint
    for result in results:
        pprint.pprint(result)