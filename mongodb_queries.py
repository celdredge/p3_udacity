def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.sfosm
    return db

if __name__ == "__main__":
    db = get_db()
    
    # postcode
    #results =  db.sfosm.aggregate( [ { "$match" : { "address.postcode" : { "$exists" : 1 }}}, { "$group" : { "_id" : "$address.postcode", "count" : { "$sum" : 1 }}}, { "$sort" : { "count" : 1 }}])
    
    # cities
    # results = db.sfosm.aggregate( [ { "$match" : { "address.city" : { "$exists" : 1 } } } , { "$group" : { "_id" : "$address.city", "count" : { "$sum" : 1 } } } , { "$sort" : { "count" : 1 } } ] )

    #unique users
    #print len(db.sfosm.distinct("created.user"))

    # top one contributing user
    # results = db.sfosm.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}},{"$sort":{"count":1}},{"$limit":1}])

    # users appearing the fewest amount of times
    # results = db.sfosm.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, {"$group":{"_id":"$count", "num_users":{"$sum":1}}}, {"$sort":{"_id":1}}, {"$limit":1}])

    # top ammenities
    results = db.sfosm.aggregate([{"$match":{"amenity":{"$exists":1}}}, {"$group":{"_id":"$amenity", "count":{"$sum":1}}}, {"$sort":{"count":-1}},{"$limit":10}])

    # top religion  
    #results = db.sfosm.aggregate([{"$match":{"amenity":{"$exists":1},"amenity":"place_of_worship"}},{"$group":{"_id":"$religion", "count":{"$sum":1}}},{"$sort":{"count":-1}},{"$limit":1}])

    # most popular cuisine
    #results = db.sfosm.aggregate([{"$match":{"amenity":{"$exists":1},"amenity":"restaurant"}},{"$group":{"_id":"$cuisine","count":{"$sum":1}}},{"$sort":{"count":-1}},{"$limit":2}])

    # print db.sfosm.find_one()
    
    import pprint
    for result in results:
        pprint.pprint(result)