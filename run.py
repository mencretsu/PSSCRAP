from google_play_scraper import reviews, Sort
from collections import Counter
import csv

app_id = input('ex: com.example.android')

# code ISO 3166
all_countries = [
    'us', 'id', 'in', 'br', 'gb', 'de', 'fr', 'jp', 'ru', 'cn',
    'kr', 'it', 'es', 'mx', 'ca', 'tr', 'vn', 'th', 'ar', 'pl',
    'ir', 'pk', 'eg', 'za', 'au', 'nl', 'sa', 'my', 'sg', 'bd',
    'hk', 'uae', 'ch', 'se', 'be', 'dk', 'no', 'fi', 'gr', 'pt',
    'il', 'nz', 'cl', 'co', 'cz', 'hu', 'ro', 'sk', 'bg', 'hr'
]

all_reviews = []

for country in all_countries:
    print(f"Scraping {country} ...")
    try:
        rvws, _ = reviews(
            app_id,
            lang='en',
            country=country,
            count=500,  # Adjust max 500 per request stabil
            filter_score_with=None,
            sort=Sort.NEWEST
        )
        for r in rvws:
            all_reviews.append({
                'userName': r['userName'],
                'score': r['score'],
                'content': r['content'],
                'country': country,
                'at': r['at'].strftime("%Y-%m-%d"),
                'version': r['reviewCreatedVersion']
            })
    except Exception as e:
        print(f"Error scraping {country}: {e}")

# Analisis & Summary
country_counts = Counter([r['country'] for r in all_reviews])
score_counts = Counter([r['score'] for r in all_reviews])

print("\n=== Summary ===")
print(f"Total: {len(all_reviews)}")
print("\nReview:")
for c, cnt in country_counts.most_common():
    print(f"{c}: {cnt}")

print("\nDistribution Rating:")
for s, cnt in sorted(score_counts.items(), reverse=True):
    print(f"{s}★ : {cnt}")

# Simpan ke CSV
with open('reviews_output.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=all_reviews[0].keys())
    writer.writeheader()
    writer.writerows(all_reviews)

print("\n✅ CSV saved as 'reviews_output.csv'")
