# Volunteer Analytics Consultant Project: BBBS Mentor Gender Gap

A consulting-style analytics project for a real nonprofit problem: **Big
Brothers Big Sisters (BBBS)** chapters nationwide report a chronic
shortage of male mentors ("Bigs"), which leaves boys ("Littles") waiting
far longer than girls for a match. This project quantifies that gap using
a synthetic chapter dataset calibrated to match real, publicly reported
BBBS statistics, and answers: how big is the problem, what's driving it,
and what should a chapter do about it.

## Why this project is different from the others in this portfolio

Every other project in this portfolio uses a synthetic dataset grounded
in a domain's *rules* (Medicaid billing, underwriting logic). This one is
grounded in a **real, named organization's publicly reported statistics**
— not just a plausible-sounding domain, but numbers real BBBS chapters
have actually published. It's also the first project built with **real
BI tools** (Excel + Tableau Public) rather than a custom HTML dashboard,
and the first paired with an actual slide deck for presenting findings to
a non-technical stakeholder — following the consulting-project format of
[this video](https://www.youtube.com/watch?v=PLj2On29-fM).

## Real-world sources

The dataset's calibration (not the raw numbers themselves — no real
chapter's actual records are used) is grounded in:

- **BBBS of Tarrant County** (Fort Worth Report, Sept 2025): 112 men vs.
  240 women volunteered in 2025; boys wait about a year longer on average
  for a mentor; ~75% of the waitlist is boys.
- **BBBS Tulsa-Oklahoma** (KJRH, June 2026): over 100 children waiting,
  75%+ of the waitlist is boys.
- **BBBS of Puget Sound** (FOX 13 Seattle, Jan 2026): 700-child waitlist
  across King/Pierce/Snohomish counties, 60% specifically boys of color.
- **BBBS of Broward County** (published impact statistics, 2024): 911
  volunteers, 1,117 matches facilitated, average match duration 32.8
  months (up from 26.5 months in 2023), 66%/34% women/men volunteer
  split.
- **BBBS Sarnia-Lambton, BBBS Guelph, BBBS Calgary** (various 2021-2026
  local news coverage): recurring pattern of male-volunteer shortages
  driving multi-year waitlists specifically for boys.

## Dataset

Synthetic, 3 linked tables (`generate_data.py`, `data/`):

| Table | Rows | Description |
|---|---|---|
| `volunteers.csv` | 1,300 | Gender (62% F / 38% M), region, signup date, onboarding time, status |
| `littles.csv` | 1,080 | Gender (70% boy / 30% girl at signup), age, region, waitlist status |
| `matches.csv` | 765 | Wait time, match duration, status (Active/Completed), end reason |

**Calibration note:** parameters (volunteer gender split, relative wait
times) were tuned to produce a waitlist that's the vast majority boys and
a multi-month wait-time gap — directionally matching real chapters, even
somewhat more pronounced than the specific 70-75% figures cited above.
That's a function of this dataset's particular supply/demand parameters,
not a claim that any real chapter's waitlist is exactly 90% boys.

## Key findings

- **315 children currently waitlisted, 90.5% of them boys** (285 boys,
  30 girls) — the imbalance those real chapter reports describe, playing
  out in this dataset.
- **Boys wait 10.1 months on average to be matched; girls wait 4.6
  months** — a 5.5-month gap, consistent with (if larger than) BBBS
  Tarrant County's reported "about a year longer" for boys.
- **Root cause is a structural supply/demand mismatch**, not a seasonal
  dip: only 38% of active volunteers are men, while 70% of children who
  sign up are boys.
- **Match durability isn't the problem.** Average completed match
  duration is 24.1 months, and only 29% of endings were early
  relationship strain — most are structural (aging out, moving). The
  bottleneck is entirely upstream, at recruitment.

## Deliverables

1. **`BBBS_Mentor_Gap_Analysis.xlsx`** — Excel dashboard: formula-driven
   KPIs (SUMIFS/COUNTIFS/AVERAGEIFS against raw data, zero hardcoded
   results), 4 native charts, full raw data on separate sheets.
2. **Tableau Public dashboard** — built by hand following
   `TABLEAU_GUIDE.md`, a step-by-step guide covering data joins,
   calculated fields, all 4 sheets, and dashboard assembly with filter
   actions.
3. **`BBBS_Mentor_Gap_Analysis.pptx`** — an 8-slide deck: problem, method,
   3 key findings, recommendations, and skills demonstrated — built for
   presenting to a non-technical stakeholder (e.g. a chapter director).

## Recommendations (from the slide deck)

1. **Target male recruitment specifically** — generic volunteer
   campaigns don't fix a gender-specific supply gap.
2. **Track wait time by gender as a chapter KPI**, not just total
   waitlist size — the aggregate number hides this problem.
3. **Protect what's already working** — match durability is healthy; a
   recruitment push shouldn't come at the cost of screening quality.

## Skills demonstrated

Grounding a synthetic dataset in real, cited public statistics rather
than an invented domain; Excel dashboard design with formula-driven KPIs
(no hardcoded results); Tableau Public dashboard construction (joins,
calculated fields, filter actions); and translating a data analysis into
a stakeholder-ready slide narrative with concrete recommendations.
