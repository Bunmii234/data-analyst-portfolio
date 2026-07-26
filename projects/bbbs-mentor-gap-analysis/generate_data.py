"""
Synthetic dataset for a Big Brothers Big Sisters (BBBS) local chapter,
calibrated to match real, publicly reported statistics from actual BBBS
chapters (sources in README):

  - Volunteer ("Big") gender split: ~65% women / 35% men
    (BBBS of Broward: 66% women / 34% men, 2024; BBBS Tarrant County:
    240 women vs. 112 men volunteered in 2025)
  - Waitlist ("Little") gender split: ~70-75% boys
    (BBBS Tulsa: 75%+ of waitlist is boys; BBBS Puget Sound: majority-boys
    waitlist of 700; multiple chapters report boys as ~70-75% of waitlist)
  - Boys wait meaningfully longer than girls for a match
    (BBBS Tarrant County: "boys typically wait a year longer on average")
  - Average match duration once matched: ~30-33 months
    (BBBS Broward: 32.8 months in 2024, up from 26.5 months in 2023)
  - Chapter scale modeled loosely on BBBS of Broward County (2024):
    ~911 volunteers, ~1,117 matches facilitated in a year

This is a synthetic dataset built to reflect these real, well-documented
patterns -- not scraped from any specific chapter's actual records.
"""
import random
import csv
import os
from datetime import date, timedelta

random.seed(7)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(OUT_DIR, exist_ok=True)

REGIONS = ["North County", "South County", "East Metro", "West Metro", "Central"]
START_DATE = date(2022, 1, 1)
DATA_CUTOFF = date(2026, 6, 30)

FIRST_NAMES_M = ["James","Michael","David","John","Robert","Daniel","Kevin","Brian","Anthony","Marcus"]
FIRST_NAMES_F = ["Jennifer","Sarah","Ashley","Jessica","Emily","Michelle","Amanda","Nicole","Rachel","Lauren"]
LAST_NAMES = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez",
    "Wilson","Anderson","Taylor","Moore","Jackson","Martin","Lee","Thompson","White","Harris"]

# ---------------------------------------------------------------
# VOLUNTEERS ("Bigs") -- 1,300 total, 62% women / 38% men
# ---------------------------------------------------------------
N_VOLUNTEERS = 1300
volunteers = []
for vid in range(1, N_VOLUNTEERS + 1):
    gender = random.choices(["Female", "Male"], weights=[0.62, 0.38])[0]
    fn = random.choice(FIRST_NAMES_F if gender == "Female" else FIRST_NAMES_M)
    ln = random.choice(LAST_NAMES)
    region = random.choice(REGIONS)
    signup_offset = random.randint(0, (DATA_CUTOFF - START_DATE).days)
    signup_date = START_DATE + timedelta(days=signup_offset)
    onboarding_days = random.randint(21, 95)
    training_completed_date = signup_date + timedelta(days=onboarding_days)
    status = "Active" if training_completed_date <= DATA_CUTOFF else "In Onboarding"
    volunteers.append({
        "volunteer_id": vid,
        "first_name": fn,
        "last_name": ln,
        "gender": gender,
        "region": region,
        "signup_date": signup_date.isoformat(),
        "onboarding_days": onboarding_days,
        "training_completed_date": training_completed_date.isoformat() if status == "Active" else "",
        "status": status,
    })

active_volunteers = [v for v in volunteers if v["status"] == "Active"]

# ---------------------------------------------------------------
# LITTLES (mentees) -- waitlist skews 70% boys; boys wait ~1yr longer
# ---------------------------------------------------------------
N_LITTLES = 1080
littles = []
for lid in range(1, N_LITTLES + 1):
    gender = random.choices(["Boy", "Girl"], weights=[0.70, 0.30])[0]
    age = random.randint(6, 14)
    region = random.choice(REGIONS)
    signup_offset = random.randint(0, (DATA_CUTOFF - START_DATE).days)
    signup_date = START_DATE + timedelta(days=signup_offset)
    littles.append({
        "little_id": lid,
        "gender": gender,
        "age_at_signup": age,
        "region": region,
        "signup_date": signup_date.isoformat(),
    })

# ---------------------------------------------------------------
# MATCHES -- pair littles with same-gender-preference volunteers.
# Boys wait longer because only 38% of volunteers are men but 70%
# of littles are boys -- a structural supply/demand mismatch.
# ---------------------------------------------------------------
male_vols = [v for v in active_volunteers if v["gender"] == "Male"]
female_vols = [v for v in active_volunteers if v["gender"] == "Female"]
random.shuffle(male_vols)
random.shuffle(female_vols)

boys = sorted([l for l in littles if l["gender"] == "Boy"], key=lambda x: x["signup_date"])
girls = sorted([l for l in littles if l["gender"] == "Girl"], key=lambda x: x["signup_date"])

matches = []
match_id = 1
littles_by_id = {l["little_id"]: l for l in littles}
matched_little_ids = set()

def make_matches(little_pool, volunteer_pool, base_wait_days, wait_std):
    global match_id
    n_matches = min(len(little_pool), len(volunteer_pool))
    for i in range(n_matches):
        little = little_pool[i]
        vol = volunteer_pool[i]
        signup = date.fromisoformat(little["signup_date"])
        wait_days = max(14, int(random.gauss(base_wait_days, wait_std)))
        match_date = signup + timedelta(days=wait_days)
        if match_date > DATA_CUTOFF:
            continue

        duration_months = max(1, round(random.gauss(31, 11)))
        end_date = match_date + timedelta(days=duration_months * 30)
        if end_date > DATA_CUTOFF:
            match_status = "Active"
            end_date_str = ""
            end_reason = ""
            duration_months_actual = round((DATA_CUTOFF - match_date).days / 30, 1)
        else:
            match_status = "Completed"
            end_date_str = end_date.isoformat()
            end_reason = random.choices(
                ["Aged Out", "Little Moved Away", "Relationship Ended Early", "Big Relocated"],
                weights=[0.35, 0.20, 0.30, 0.15]
            )[0]
            duration_months_actual = duration_months

        matches.append({
            "match_id": match_id,
            "little_id": little["little_id"],
            "volunteer_id": vol["volunteer_id"],
            "region": little["region"],
            "little_gender": little["gender"],
            "signup_date": little["signup_date"],
            "match_date": match_date.isoformat(),
            "wait_days": wait_days,
            "match_status": match_status,
            "match_end_date": end_date_str,
            "match_duration_months": duration_months_actual,
            "match_end_reason": end_reason,
        })
        matched_little_ids.add(little["little_id"])
        match_id += 1

make_matches(boys, male_vols, base_wait_days=300, wait_std=100)
make_matches(girls, female_vols, base_wait_days=135, wait_std=60)

for l in littles:
    if l["little_id"] not in matched_little_ids:
        l["waitlist_status"] = "Waitlisted"
        l["days_on_waitlist_so_far"] = (DATA_CUTOFF - date.fromisoformat(l["signup_date"])).days
    else:
        l["waitlist_status"] = "Matched"
        l["days_on_waitlist_so_far"] = ""

def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

write_csv(os.path.join(OUT_DIR, "volunteers.csv"), volunteers, list(volunteers[0].keys()))
write_csv(os.path.join(OUT_DIR, "littles.csv"), littles, list(littles[0].keys()))
write_csv(os.path.join(OUT_DIR, "matches.csv"), matches, list(matches[0].keys()))

print(f"Volunteers: {len(volunteers)} ({sum(1 for v in volunteers if v['gender']=='Male')} male, "
      f"{sum(1 for v in volunteers if v['gender']=='Female')} female)")
print(f"Littles: {len(littles)} ({sum(1 for l in littles if l['gender']=='Boy')} boys, "
      f"{sum(1 for l in littles if l['gender']=='Girl')} girls)")
print(f"Matches made: {len(matches)}")
print(f"Currently waitlisted: {sum(1 for l in littles if l['waitlist_status']=='Waitlisted')}")
