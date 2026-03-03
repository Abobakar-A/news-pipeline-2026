import os
import pandas as pd
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time

# جلب رابط قاعدة البيانات من متغيرات البيئة (Docker)
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://airflow:airflow@warehouse-db:5432/airflow')
engine = create_engine(DATABASE_URL)

def get_recommendations(article_title):
    try:
        # 1. جلب البيانات
        df = pd.read_sql("SELECT title FROM analytics.clean_articles", engine)
        
        if article_title not in df['title'].values:
            return "⚠️ الخبر المطلبو غير موجود في قاعدة البيانات حالياً."

        # 2. تحويل النصوص (Vectorization)
        # أضفنا الكلمات العربية الشائعة كـ stop_words إذا لزم الأمر مستقبلاً
        tfidf = TfidfVectorizer(stop_words='english') 
        tfidf_matrix = tfidf.fit_transform(df['title'].fillna(''))
        
        # 3. حساب مصفوفة التشابه (Cosine Similarity)
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        # 4. استخراج التوصيات
        idx = df[df['title'] == article_title].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # نأخذ أعلى 5 (باستثناء الخبر نفسه)
        sim_indices = [i[0] for i in sim_scores[1:6]]
        return df['title'].iloc[sim_indices]

    except Exception as e:
        return f"❌ خطأ في محرك التوصية: {str(e)}"



if __name__ == "__main__":
    while True:
        print("\n🚀 --- محرك التوصية بدأ العمل ---")
        try:
            # محاولة جلب التوصيات
            test_df = pd.read_sql("SELECT title FROM analytics.clean_articles LIMIT 1", engine)
            
            if not test_df.empty:
                sample = test_df['title'].iloc[0]
                print(f"🔎 جاري البحث عن أخبار مشابهة لـ: {sample}")
                results = get_recommendations(sample)
                print("✅ التوصيات المقترحة:")
                print(results)
            else:
                print("⚠️ جدول 'clean_articles' فارغ حالياً. بانتظار بيانات dbt...")
                
        except Exception as e:
            print(f"⏳ بانتظار تهيئة قاعدة البيانات: {e}")

        # الانتظار لمدة دقيقة قبل الفحص مرة أخرى (لكي لا تنغلق الحاوية)
        print("😴 سأقوم بالفحص مجدداً بعد 60 ثانية...")
        time.sleep(60)