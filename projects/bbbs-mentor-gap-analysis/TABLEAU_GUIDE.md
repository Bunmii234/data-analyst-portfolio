# Building the Tableau Public Dashboard

I can't run Tableau myself, so here's an exact, step-by-step guide to build
the real interactive dashboard yourself in Tableau Public (free).

## 1. Get Tableau Public

Download from [public.tableau.com](https://public.tableau.com/en-us/s/download) —
free, no license needed. Sign in / create an account (this is where your
published dashboard link will live).

## 2. Connect the data

- Open Tableau Public → **Connect → Text File**
- Select `data/littles.csv` first
- In the data source screen, drag `data/matches.csv` on top of it to create
  a join. Join on: `littles.little_id = matches.little_id` (Left join, so
  waitlisted-but-unmatched Littles are kept — a Left join is important
  here, an Inner join would silently drop your entire waitlist).
- Drag `data/volunteers.csv` in as a second join: `matches.volunteer_id = volunteers.volunteer_id`
  (also Left join)

## 3. Build Sheet 1 — Waitlist Composition by Gender

- New Worksheet
- Drag `Gender` (from Littles) to **Columns**
- Drag `Little Id` to **Rows**, set to **Count Distinct**
- Filter: `Waitlist Status` = "Waitlisted" (drag to Filters shelf)
- Chart type: **Bar chart** (should default to this)
- Right-click the color legend → color Boy in a distinct color (e.g. red)
  vs Girl (blue/gray) to make the imbalance visually obvious
- Add a **label**: right-click the bars → Show Mark Labels
- Rename the sheet "Waitlist by Gender"

## 4. Build Sheet 2 — Average Wait Time by Gender

- New Worksheet
- Drag `Little Gender` (from Matches — matched Littles only) to **Columns**
- Create a calculated field: right-click Data pane → Create Calculated Field
  - Name: `Wait Months`
  - Formula: `[Wait Days] / 30`
- Drag `Wait Months` to **Rows**, set aggregation to **Average**
- Chart type: Bar chart
- Rename the sheet "Avg Wait Time by Gender"

## 5. Build Sheet 3 — Waitlisted by Region

- New Worksheet
- Drag `Region` (from Littles) to **Columns**
- Drag `Little Id` to **Rows**, Count Distinct
- Filter: `Waitlist Status` = "Waitlisted"
- Optionally add `Gender` to **Color** to show the boy/girl split within
  each region as a stacked bar
- Rename the sheet "Waitlisted by Region"

## 6. Build Sheet 4 — Match End Reasons

- New Worksheet
- Filter: `Match Status` = "Completed"
- Drag `Match End Reason` to **Columns** (or to Angle/Color for a pie —
  Show Me → pie chart)
- Drag `Match Id` to **Rows** / **Angle**, Count Distinct
- Rename the sheet "Match End Reasons"

## 7. Assemble the Dashboard

- **Dashboard → New Dashboard**
- Set size to **Automatic** or a fixed 1200x800
- Drag all 4 sheets onto the canvas — a 2x2 grid layout works well
- Add a **Text object** at the top as a title:
  "BBBS Chapter: Mentor Gender Gap Analysis"
- Add a second small Text object underneath the title with the core
  finding: "90.5% of the waitlist is boys, who wait 10.1 months on average
  vs. 4.6 months for girls."
- Add a **Filter action**: click the Region chart → use as filter, so
  clicking a region filters the other three sheets (Dashboard → Actions →
  Add Action → Filter)

## 8. Publish

- **Server → Tableau Public → Save to Tableau Public**
- Name it "BBBS Mentor Gender Gap Analysis"
- Once published, copy the shareable link — that's what goes in your
  portfolio card and resume

## 9. Bring the link back to your portfolio

Once you have the published Tableau Public URL, send it to me (or drop it
in the project's README) and I'll wire it into your portfolio site's
project card and write-up page, the same way the other dashboards work.
