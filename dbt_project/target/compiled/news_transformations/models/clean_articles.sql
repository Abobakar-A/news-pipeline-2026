

with raw_data as (
    select * from "airflow"."public"."staging_news"
    
    
      where ingested_at > (select max(ingested_at) from "airflow"."analytics"."clean_articles")
    
),

cleaned_step as (
    select
        id,
        title,
        author,
        source_name,
        published_at::timestamp as published_date,
        -- 1. إزالة رموز [+ chars]
        split_part(content, '[+', 1) as stage1_content,
        url,
        ingested_at
    from raw_data
    where title is not null
)

select
    id,
    title,
    author,
    source_name,
    published_date,
    -- 2. إزالة وسوم HTML (أي شيء بين < >)
    -- 3. إزالة الرموز الغريبة مثل ¶
    regexp_replace(
        regexp_replace(stage1_content, '<[^>]*>', '', 'g'), 
        '[¶\r\n\t]+', ' ', 'g'
    ) as clean_content,
    url,
    ingested_at
from cleaned_step