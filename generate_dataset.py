import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

n = 300

genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller', 'Animation', 'Documentary']
genres_messy = genres + ['action', 'COMEDY', 'Drama ', ' Horror', 'sci-fi', 'Sci Fi']

countries = ['USA', 'India', 'UK', 'South Korea', 'France', 'Japan', 'Canada', 'Australia']
countries_messy = countries + ['usa', 'U.S.A', 'india', 'U.K.', 'Uk']

languages = ['English', 'Hindi', 'Tamil', 'Korean', 'French', 'Japanese', 'Spanish']

directors = ['C. Nolan', 'S. Spielberg', 'M. Night', 'Q. Tarantino', 'A. Kurosawa',
             'K. Shankar', 'R. Balki', 'P. Jackson', 'G. Del Toro', 'D. Villeneuve',
             'S. Raja', 'V. Vijay', 'J. Cameron', 'R. Scott', 'M. Gibson']

titles_prefix = ['The', 'A', 'Return of', 'Legend of', 'Rise of', 'Beyond', 'Shadow of', 'Last']
titles_word = ['Fire', 'Kingdom', 'Warrior', 'Dream', 'Silence', 'Storm', 'Journey', 'City',
               'Empire', 'Star', 'River', 'Night', 'Wolf', 'Ocean', 'Sky', 'Truth', 'Ghost']

rows = []
for i in range(n):
    title = f"{random.choice(titles_prefix)} {random.choice(titles_word)} {random.choice(['', 'II', 'Returns', ''])}".strip()
    genre = random.choice(genres_messy)
    director = random.choice(directors)
    year = random.choice(list(range(1980, 2025)) + [None]*5)  # some missing
    duration = np.random.normal(115, 20)
    duration = round(duration) if duration > 0 else 90
    # inject some outlier durations
    if random.random() < 0.02:
        duration = random.choice([5, 400, 600])
    rating = round(np.clip(np.random.normal(6.5, 1.2), 1, 10), 1)
    votes = int(np.random.exponential(50000))
    budget = round(np.random.exponential(40), 1)  # in millions
    # inject outlier budgets
    if random.random() < 0.02:
        budget = round(random.choice([0.001, 5000]), 1)
    revenue = round(budget * np.random.uniform(0.3, 5) + np.random.normal(0, 10), 1)
    if revenue < 0:
        revenue = None if random.random() < 0.5 else 0.1
    country = random.choice(countries_messy)
    language = random.choice(languages)

    rows.append({
        'Title': title,
        'Genre': genre,
        'Director': director,
        'Year': year,
        'Duration_Min': duration,
        'Rating': rating,
        'Votes': votes,
        'Budget_Million': budget,
        'Revenue_Million': revenue,
        'Country': country,
        'Language': language
    })

df = pd.DataFrame(rows)

# Introduce missing values randomly across columns
for col in ['Rating', 'Votes', 'Budget_Million', 'Revenue_Million', 'Director', 'Country', 'Duration_Min']:
    idx = df.sample(frac=0.05).index
    df.loc[idx, col] = np.nan

# Introduce duplicate rows
dupes = df.sample(10, random_state=1)
df = pd.concat([df, dupes], ignore_index=True)

# Shuffle
df = df.sample(frac=1, random_state=7).reset_index(drop=True)

df.to_csv('/home/claude/movies_project/movies_raw.csv', index=False)
print("Raw dataset created:", df.shape)
print(df.head(10))
print("\nMissing values per column:\n", df.isna().sum())
print("\nDuplicate rows:", df.duplicated().sum())
