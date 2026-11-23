import pandas as pd

parquet_url = 'https://huggingface.co/datasets/mb7419/career-guidance-reddit/resolve/main/data/test-00000-of-00001.parquet'
try:
    df = pd.read_parquet(parquet_url)
    print('Total records in test parquet:', len(df))

    queries = ['bootcamp', 'remote', 'salary', 'resume', 'burnout', 'data', 'consulting', 'business', 'startup']
    for q in queries:
        m = df[df['title'].str.contains(q, case=False, na=False) | df['body'].str.contains(q, case=False, na=False)]
        print(f"Query '{q}': {len(m)} matching authentic discussions")
except Exception as e:
    print('Error loading parquet:', e)
