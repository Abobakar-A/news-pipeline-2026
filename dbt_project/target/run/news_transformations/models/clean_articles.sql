
      
        
            delete from "airflow"."analytics"."clean_articles"
            where (
                url) in (
                select (url)
                from "clean_articles__dbt_tmp175335683565"
            );

        
    

    insert into "airflow"."analytics"."clean_articles" ("id", "title", "author", "source_name", "published_date", "clean_content", "url", "ingested_at")
    (
        select "id", "title", "author", "source_name", "published_date", "clean_content", "url", "ingested_at"
        from "clean_articles__dbt_tmp175335683565"
    )
  