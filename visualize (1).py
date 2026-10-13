import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams['figure.dpi'] = 110

df = pd.read_csv('/home/claude/movies_project/movies_cleaned.csv')
OUT = '/home/claude/movies_project'

# 1. Genre distribution
plt.figure(figsize=(9,5))
order = df['Genre'].value_counts().index
sns.countplot(data=df, y='Genre', order=order, palette='viridis')
plt.title('Number of Movies by Genre')
plt.xlabel('Count')
plt.ylabel('Genre')
plt.tight_layout()
plt.savefig(f'{OUT}/chart1_genre_distribution.png')
plt.close()

# 2. Average rating by genre
plt.figure(figsize=(9,5))
avg_rating = df.groupby('Genre')['Rating'].mean().sort_values(ascending=False)
sns.barplot(x=avg_rating.values, y=avg_rating.index, palette='mako')
plt.title('Average Rating by Genre')
plt.xlabel('Average Rating')
plt.ylabel('Genre')
plt.tight_layout()
plt.savefig(f'{OUT}/chart2_avg_rating_genre.png')
plt.close()

# 3. Budget vs Revenue scatter
plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x='Budget_Million', y='Revenue_Million', hue='Genre', alpha=0.7, s=60)
plt.title('Budget vs Revenue (Million $)')
plt.xlabel('Budget (Million $)')
plt.ylabel('Revenue (Million $)')
plt.legend(bbox_to_anchor=(1.02,1), loc='upper left', fontsize=8)
plt.tight_layout()
plt.savefig(f'{OUT}/chart3_budget_vs_revenue.png')
plt.close()

# 4. Ratings trend over decades
plt.figure(figsize=(9,5))
decade_order = sorted(df['Decade'].unique())
sns.lineplot(data=df, x='Decade', y='Rating', marker='o', sort=False,
             estimator='mean', errorbar=None)
plt.title('Average Movie Rating Trend by Decade')
plt.xlabel('Decade')
plt.ylabel('Average Rating')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{OUT}/chart4_rating_trend_decade.png')
plt.close()

# 5. Correlation heatmap
plt.figure(figsize=(7,6))
num_cols = ['Duration_Min','Rating','Votes','Budget_Million','Revenue_Million','Profit_Million','ROI_Percent']
corr = df[num_cols].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap of Numeric Features')
plt.tight_layout()
plt.savefig(f'{OUT}/chart5_correlation_heatmap.png')
plt.close()

# 6. Top 10 movies by profit
plt.figure(figsize=(9,6))
top10 = df.nlargest(10, 'Profit_Million')[['Title','Profit_Million']]
sns.barplot(data=top10, x='Profit_Million', y='Title', palette='crest')
plt.title('Top 10 Movies by Profit (Million $)')
plt.xlabel('Profit (Million $)')
plt.ylabel('')
plt.tight_layout()
plt.savefig(f'{OUT}/chart6_top10_profit.png')
plt.close()

# 7. Movies by country
plt.figure(figsize=(8,5))
country_count = df['Country'].value_counts()
plt.pie(country_count.values, labels=country_count.index, autopct='%1.1f%%',
        colors=sns.color_palette('pastel'))
plt.title('Movie Distribution by Country')
plt.tight_layout()
plt.savefig(f'{OUT}/chart7_country_distribution.png')
plt.close()

# 8. Duration distribution (boxplot to show outlier handling)
plt.figure(figsize=(8,5))
sns.boxplot(data=df, x='Genre', y='Duration_Min', palette='Set2')
plt.title('Movie Duration by Genre (After Outlier Capping)')
plt.xlabel('Genre')
plt.ylabel('Duration (Minutes)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{OUT}/chart8_duration_boxplot.png')
plt.close()

print("All 8 charts generated successfully.")

# Print key insights as text
print("\n--- KEY INSIGHTS ---")
print(f"Total movies analyzed: {len(df)}")
print(f"Most common genre: {df['Genre'].mode()[0]}")
print(f"Highest average rating genre: {avg_rating.idxmax()} ({avg_rating.max():.2f})")
print(f"Most profitable movie: {top10.iloc[0]['Title']} (${top10.iloc[0]['Profit_Million']:.1f}M profit)")
print(f"Overall average rating: {df['Rating'].mean():.2f}")
print(f"Overall average budget: ${df['Budget_Million'].mean():.2f}M")
print(f"Overall average revenue: ${df['Revenue_Million'].mean():.2f}M")
print(f"Correlation between Budget and Revenue: {corr.loc['Budget_Million','Revenue_Million']:.2f}")
