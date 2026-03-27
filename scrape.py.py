# --- Installeer Supabase client ---
!pip install -q supabase requests beautifulsoup4 pandas

# --- Import libraries ---
import requests
from bs4 import BeautifulSoup
import pandas as pd
from supabase import create_client
from datetime import datetime

# --- Supabase connectie ---
SUPABASE_URL = "https://djrnipewkwovxqfeqcah.supabase.co"   # je project URL
SUPABASE_KEY = "sb_publishable_6LaPd7x0_y8oFGt_kS9jsA_T3Ioe2l2"  # je anon/public key

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Scrape quotes ---
url = "http://quotes.toscrape.com/page/1/"
rows = []

while url:
    response = requests.get(url, timeout=20)
    soup = BeautifulSoup(response.text, "html.parser")
    scrape_time = datetime.now().isoformat()
    for quote_card in soup.select("div.quote"):
        quote_text = quote_card.select_one("span.text").get_text(strip=True)
        author = quote_card.select_one("small.author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote_card.select("div.tags a.tag")]

        rows.append({
            "quote": quote_text,
            "author": author,
            "tags": tags,
            "scraped_at":scrape_time
        })

    # Volgende pagina
    next_btn = soup.select_one("li.next a")
    url = "http://quotes.toscrape.com" + next_btn["href"] if next_btn else None

# --- Optioneel: check eerste paar quotes ---
df = pd.DataFrame(rows)
print(df.head())

# --- Upload naar Supabase ---
result = supabase.table("quotes").insert(rows).execute()
print(f"✅ Inserted {len(rows)} quotes into Supabase")
