
import pandas as pd

df = pd.read_csv('../testdata/person/closeness/netflix_titles.csv')
df = df[['title','cast', 'country', 'release_year']]
df = df.loc[df['cast'].notna()]

df['cast'] = df['cast'].apply(lambda x: x.split(','))
df = df.explode('cast')

df = df.rename(columns={'cast':'actor'})

df.to_csv('../testdata/person/closeness/netflix_actors.csv',index=False)


### CODE Cut and Paste
df = df[['title', 'type', 'cast', 'release_year']]
df = df.loc[df['cast'].notna()]
df['cast'] = df['cast'].apply(lambda x: x.split(','))
df = df.explode('cast')
df = df.rename(columns={'cast': 'ACTOR'})
df['ACTOR'] = df['ACTOR'].str.strip()

if not api.config.type == '*' and not api.config.type == None:
    df = df.loc[df['type'] == api.config.type]