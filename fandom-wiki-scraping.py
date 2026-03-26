"""
Minecraft Archive Fandom Wiki - Mob Scraper
============================================
Scrapes mob data from https://minecraft-archive.fandom.com/wiki/Mob
Collects mob names, links, and classifications (Utility, Passive,
Neutral, Hostile, Boss) from the main Mob page, then follows each
mob's link to scrape additional details (health, attack strength,
drops, location, description) from their individual pages.

Research Purpose:
    Preserve a structured record of all Minecraft mobs and their
    classifications for future game-development reference and
    cultural preservation of the game's ecosystem.

Robots.txt Compliance:
    https://minecraft-archive.fandom.com/robots.txt
    Fandom wikis allow scraping /wiki/* content pages for general
    user agents. Only Special:, User:, Template:, Help: pages are
    disallowed. We only scrape /wiki/Mob and /wiki/<MobName> pages.

License:
    Fandom wiki content is licensed under CC BY-SA 3.0.
    Attribution: https://minecraft-archive.fandom.com/
"""

import cloudscraper
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://minecraft-archive.fandom.com"
MOB_LIST_URL = f"{BASE_URL}/wiki/Mob"
OUTPUT_FILE = "minecraft_mobs.csv"
DELAY = 2  # seconds between requests to be polite


def get_page(url):
    """Fetch a page using cloudscraper and return a BeautifulSoup object."""
    scraper = cloudscraper.create_scraper()
    try:
        response = scraper.get(url, timeout=15)
        print(f"  GET {url} -> {response.status_code}")
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        else:
            print(f"  Warning: received status {response.status_code}")
            return None
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return None


def get_mob_list(soup):
    """
    Extract mob names, links, and classifications from the main Mob page.
    The page organizes mobs under h3 headings (Utility, Passive, Neutral,
    Hostile, Boss), each followed by a table where each row has an image
    in td[0] and the mob name/link in td[1].

    Returns a list of dicts with keys: name, link, classification.
    """
    mobs = []
    categories = ["Utility", "Passive", "Neutral", "Hostile", "Boss"]

    for h3 in soup.find_all("h3"):
        heading_text = h3.get_text(strip=True).replace("[]", "")
        if heading_text not in categories:
            continue

        # Find the next table after this heading
        table = h3.find_next("table")
        if not table:
            continue

        # Skip the header row, iterate data rows
        rows = table.find_all("tr")[1:]
        for row in rows:
            tds = row.find_all("td")
            if len(tds) < 2:
                continue

            # The mob name is the first link in the second cell
            first_link = tds[1].find("a")
            if not first_link:
                continue

            name = first_link.get_text(strip=True)
            href = first_link.get("href", "")

            if name and href.startswith("/wiki/"):
                mobs.append({
                    "name": name,
                    "link": BASE_URL + href,
                    "classification": heading_text,
                })

    # Deduplicate by name (keep first occurrence)
    seen = set()
    unique_mobs = []
    for mob in mobs:
        if mob["name"] not in seen:
            seen.add(mob["name"])
            unique_mobs.append(mob)

    return unique_mobs


def get_mob_details(url):
    """
    Follow a mob's link and scrape details from its individual page.
    Each mob page has a portable-infobox (aside tag) with fields like
    Health Points, Attack Strength, Drops, and Location. The first
    paragraph after the infobox provides a text description.

    Returns a dict with: health, attack_strength, drops, location, description.
    """
    details = {
        "health": "",
        "attack_strength": "",
        "drops": "",
        "location": "",
        "description": "",
    }

    soup = get_page(url)
    if not soup:
        return details

    # Parse the portable-infobox
    infobox = soup.find("aside", class_="portable-infobox")
    if infobox:
        for item in infobox.find_all("div", class_="pi-item"):
            label_tag = item.find("h3", class_="pi-data-label")
            value_tag = item.find("div", class_="pi-data-value")
            if not label_tag or not value_tag:
                continue

            label = label_tag.get_text(strip=True).lower()
            value = value_tag.get_text(strip=True)

            if "health" in label:
                details["health"] = value
            elif "attack" in label:
                details["attack_strength"] = value
            elif "drop" in label:
                details["drops"] = value
            elif "location" in label:
                details["location"] = value

    # Get the first real paragraph as description
    # Remove the infobox first so it doesn't interfere
    content = soup.find("div", class_="mw-parser-output")
    if content:
        aside = content.find("aside")
        if aside:
            aside.decompose()
        for p in content.find_all("p"):
            text = p.get_text(strip=True)
            if len(text) > 50:
                if len(text) > 300:
                    text = text[:297] + "..."
                details["description"] = text
                break

    return details


def main():
    print("=" * 60)
    print("Minecraft Archive Fandom Wiki - Mob Scraper")
    print("=" * 60)

    # Step 1: Fetch the main Mob page
    print("\n[1] Fetching main Mob list page...")
    soup = get_page(MOB_LIST_URL)
    if not soup:
        print("Failed to fetch the Mob list page. Exiting.")
        return

    # Step 2: Extract all mobs and their classifications
    print("\n[2] Extracting mob names and classifications...")
    mobs = get_mob_list(soup)
    print(f"    Found {len(mobs)} mobs.")

    # Step 3: Follow each mob's link to scrape details
    print(f"\n[3] Scraping individual mob pages ({DELAY}s delay between requests)...")
    for i, mob in enumerate(mobs):
        print(f"  [{i+1}/{len(mobs)}] {mob['name']}")
        details = get_mob_details(mob["link"])
        mob.update(details)
        time.sleep(DELAY)

    # Step 4: Save to CSV
    print(f"\n[4] Saving data to {OUTPUT_FILE}...")
    headers = [
        "name", "classification", "health", "attack_strength",
        "drops", "location", "link", "description"
    ]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for mob in mobs:
            writer.writerow([mob.get(h, "") for h in headers])

    print(f"    Saved {len(mobs)} mobs to {OUTPUT_FILE}")
    print("\nDone!")


if __name__ == "__main__":
    main()
