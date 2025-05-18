import pandas as pd
from collections import defaultdict

def load_data(csv_path="leetcode_dsa_questions.csv"):
    df = pd.read_csv(csv_path)
    df = df[['Title', 'Tags', 'Slug', 'Difficulty']]
    df.rename(columns={'Title': 'question', 'Tags': 'dependencies'}, inplace=True)
    df['dependencies'] = df['dependencies'].apply(lambda x: [tag.strip() for tag in str(x).split(',')])
    return df

def build_tag_cooccurrence(df):
    cooccur = defaultdict(lambda: defaultdict(int))
    for tags in df['dependencies']:
        for i, tag1 in enumerate(tags):
            for tag2 in tags[i+1:]:
                if tag1 != tag2:
                    cooccur[tag1][tag2] += 1
                    cooccur[tag2][tag1] += 1
    return cooccur

def get_top_k_tags(df, k=10):
    """Return the top K most frequent tags in the dataset."""
    tag_count = defaultdict(int)
    for tags in df['dependencies']:
        for tag in tags:
            tag_count[tag] += 1
    # Sort tags by frequency (descending) and return top K
    return sorted(tag_count.items(), key=lambda x: -x[1])[:k]