from pymongo import MongoClient

def save_to_mongodb(articles):
    if not articles: return
    
    client = MongoClient("mongodb://admin:password123@mongodb:27017/")
    db = client['news_database']
    collection = db['articles_raw']

    for article in articles:
        collection.update_one(
            {'url': article['url']}, 
            {'$set': article}, 
            upsert=True
        )
    print(f"✅ [MongoDB] تم تحديث {len(articles)} مقال.")
    client.close()