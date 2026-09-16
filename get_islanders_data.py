"""
Pull NY Islanders (NYI) roster + player stats from the free, public NHL API

"""

import requests
import csv

TEAM = "NYI"

# Two seasons of data — current season + last season
SEASONS = {
    "current": "now",        # this season's stats
    "2024-25": "20242025",   # last full season
}


def get_json(url):
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.json()


def save_roster():
    """Pulls the current roster (name, position, etc.) and saves it as CSV."""
    url = f"https://api-web.nhle.com/v1/roster/{TEAM}/current"
    data = get_json(url)

    rows = []
    for group in ("forwards", "defensemen", "goalies"):
        for player in data.get(group, []):
            rows.append({
                "player_id": player.get("id"),
                "first_name": player.get("firstName", {}).get("default"),
                "last_name": player.get("lastName", {}).get("default"),
                "position": player.get("positionCode"),
                "shoots_catches": player.get("shootsCatches"),
                "height_in": player.get("heightInInches"),
                "weight_lbs": player.get("weightInPounds"),
                "birth_date": player.get("birthDate"),
                "birth_country": player.get("birthCountry"),
            })

    with open("islanders_roster.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} players to islanders_roster.csv")


def save_stats(label, season_code):
    """Pulls skater stats for a given season and saves as CSV."""
    if season_code == "now":
        url = f"https://api-web.nhle.com/v1/club-stats/{TEAM}/now"
    else:
        # gameType 2 = regular season
        url = f"https://api-web.nhle.com/v1/club-stats/{TEAM}/{season_code}/2"

    data = get_json(url)
    skaters = data.get("skaters", [])

    if not skaters:
        print(f"No skater data found for {label} — check that the season code is valid.")
        return

    rows = []
    for p in skaters:
        rows.append({
            "player_id": p.get("playerId"),
            "name": p.get("firstName", {}).get("default", "") + " " + p.get("lastName", {}).get("default", ""),
            "position": p.get("positionCode"),
            "games_played": p.get("gamesPlayed"),
            "goals": p.get("goals"),
            "assists": p.get("assists"),
            "points": p.get("points"),
            "plus_minus": p.get("plusMinus"),
            "penalty_minutes": p.get("penaltyMinutes"),
            "shots": p.get("shots"),
            "time_on_ice_per_game": p.get("avgTimeOnIcePerGame"),
        })

    filename = f"islanders_stats_{label}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} skaters to {filename}")


if __name__ == "__main__":
    print("Pulling Islanders roster...")
    save_roster()

    for label, season_code in SEASONS.items():
        print(f"Pulling Islanders stats for {label}...")
        try:
            save_stats(label, season_code)
        except Exception as e:
            print(f"Couldn't pull {label} stats: {e}")

    print("\nDone. You should now have:")
    print(" - islanders_roster.csv")
    print(" - islanders_stats_current.csv")
    print(" - islanders_stats_2024-25.csv")
    print("\nImport these into DB Browser for SQLite as separate tables to get started.")
