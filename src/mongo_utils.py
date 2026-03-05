import os
from pymongo import MongoClient

def save_to_mongodb(articles):
    if not articles: return
    
    # الكود الآن نظيف تماماً؛ يقرأ من البيئة ولا يحتوي على روابط نصية
    # إذا وجد رابط السحاب سيستخدمه، وإذا لم يجده سيبحث عن الرابط المحلي
    mongo_uri = os.getenv("MONGO_URI_CLOUD") or os.getenv("MONGO_URI_LOCAL")
    
    if not mongo_uri:
        print("❌ خطأ: لم يتم العثور على أي رابط اتصال في ملف الـ .env")
        return

    client = MongoClient(mongo_uri)
    db = client['news_database']
    collection = db['articles_raw']

    for article in articles:
        collection.update_one(
            {'url': article['url']}, 
            {'$set': article}, 
            upsert=True
        )
    print(f"✅ [MongoDB] تم تحديث {len(articles)} مقال في السحاب.")
    client.close()