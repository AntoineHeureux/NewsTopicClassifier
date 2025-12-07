import sqlite3
import pandas as pd
db = "backend/articles.db"
conn = sqlite3.connect(db)
# lister les tables
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
print(tables)
# charger 100 lignes d'une table (adapter le nom)
df = pd.read_sql_query("SELECT * FROM article_results LIMIT 100;", conn)
print(df.head())
conn.close()