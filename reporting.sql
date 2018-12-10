DROP VIEW IF EXISTS articles_view;
CREATE view articles_view (
    title text,
    article_id integer,
    author text,
    author_id integer,
    views bigint
)
