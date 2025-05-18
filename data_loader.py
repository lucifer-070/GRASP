import pandas as pd

def load_data(csv_path="leetcode_dsa_questions.csv"):
    df = pd.read_csv(csv_path)
    df = df[['Title', 'Tags', 'Slug', 'Difficulty']]
    df.rename(columns={'Title': 'question', 'Tags': 'dependencies'}, inplace=True)
    df['dependencies'] = df['dependencies'].apply(lambda x: [tag.strip() for tag in str(x).split(',')])
    return df