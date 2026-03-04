import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

# إعدادات الصفحة
st.set_page_config(page_title="News Recommender 2026", layout="wide")

# دالة للاتصال بقاعدة البيانات (Postgres)
def get_connection():
    # نستخدم متغيرات البيئة أو القيم الافتراضية التي استخدمناها في المشروع
    db_url = "postgresql://airflow:airflow@warehouse-db:5432/airflow"
    return create_engine(db_url)

st.title("📰 News Data Pipeline Dashboard")
st.write("Welcome to your intelligent news hub!")
# دالة لجلب البيانات من سكيما analytics
def load_data():
    engine = get_connection()
    # نستخدم الأسماء الحقيقية للأعمدة من الـ Schema التي أرسلتها
    query = """
    SELECT 
        title, 
        source_name, 
        author, 
        published_date, 
        clean_content 
    FROM analytics.clean_articles 
    ORDER BY published_date DESC
    """
    df = pd.read_sql(query, engine)
    
    # إعادة تسمية clean_content إلى content ليتوافق مع بقية كود الـ Recommendation
    df.rename(columns={'clean_content': 'content'}, inplace=True)
    
    return df

# جلب البيانات
df = load_data()

# عرض إحصائيات سريعة في الأعلى (Metrics)
col1, col2 = st.columns(2)
col1.metric("Total Articles", len(df))
col2.metric("Sources", df['source_name'].nunique())

st.divider()

# عرض الجدول التفاعلي
st.subheader("📌 Latest Processed News")
st.dataframe(df, use_container_width=True)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.divider()
st.subheader("🤖 Smart Recommendation Engine")

# اختيار مقال من القائمة لتجربة النظام
selected_title = st.selectbox("Select an article to find similar news:", df['title'].values)

if selected_title:
    # 1. تحويل النصوص إلى أرقام (Vectorization)
    tfidf = TfidfVectorizer(stop_words='english')
    # ندمج العنوان والمحتوى لزيادة دقة البحث
    df['combined_text'] = df['title'] + " " + df['content'].fillna('')
    tfidf_matrix = tfidf.fit_transform(df['combined_text'])
    
    # 2. حساب التشابه (Cosine Similarity)
    # نجد ترتيب المقال المختار في الجدول
    idx = df[df['title'] == selected_title].index[0]
    cosine_sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()
    
    # 3. ترتيب النتائج وجلب أفضل 3 (باستثناء المقال نفسه)
    similar_indices = cosine_sim.argsort()[-4:-1][::-1]
    
    st.write(f"Articles similar to: **{selected_title}**")
    
    # عرض النتائج في أعمدة جميلة
    cols = st.columns(3)
    for i, index in enumerate(similar_indices):
        with cols[i]:
            score = round(cosine_sim[index] * 100, 1)
            st.info(f"**Match: {score}%**")
            st.write(df['title'].iloc[index])
            st.caption(f"Source: {df['source_name'].iloc[index]}")