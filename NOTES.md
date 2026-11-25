# Notes — news-image-20261125-r2

Built from zero in a fresh session on 26 Nov 2026 from a source-verified
news brief for Wednesday 25 November 2026. (The brief's suggested title
said "Tuesday"; 25 Nov 2026 is a Wednesday — verified with `date` — and
the image says Wednesday throughout.)

## What was verified

- All 35 stories are dated 25 Nov 2026 (happened, or first reported, that
  day) in the brief, with sources named on the image: Reuters, AP, BBC,
  BEA, Xinhua, Al Jazeera, AFP, ISW, Just Security, Open Chronicle, Le Monde.
- Region counts sum to 35: Europe 10, North America 8, Middle East 5,
  Asia 4, Africa 4, Latin America 2, Pacific/Oceania 2.
- Trio order follows the brief's consensus top 3: (1) Hormuz tankers,
  (2) US tariffs, (3) Asia AI rout. Only Wednesday market numbers are
  used for the rout — Tuesday's Wall Street close (Nasdaq −1.48%,
  Nvidia −5.86%) is a 24 Nov event and is listed in DATE CHECK as excluded.
- Date flags are carried on the image, not hidden: the Houthi Ras Tanura
  strike itself was 24 Nov (claim + smoke imagery 25 Nov); the Sudan
  Damazin strikes were Tue night 24 Nov (reported Wed); the Mississippi
  plane crash was Tue 24 Nov (recovery confirmed Wed); Andy Taylor died
  Mon 23 Nov (announced 25 Nov).
- DATE CHECK names 14 excluded near-misses with their real dates and 5
  "not yet" items (Thanksgiving Thu 26 Nov, Macy's parade Sat 28 Nov,
  tariffs only after the 25 Jan 2027 hearing, Fed decision 8–9 Dec,
  Steelers vs Broncos Fri 28 Nov).

## Single-source / claimed — labelled CLAIM on the image

- Hormuz tanker mines: Iranian IRGC claim only; no ships, flags or
  casualties named; no independent confirmation. Labelled CLAIM.
- Houthi claim on Ras Tanura refinery: claim only. Labelled CLAIM.
- Ukraine's claim of 5 Russian jets hit at Savasleyka: Ukrainian claim
  only. Labelled as claimed in the ALSO list.
- The 490,334 Russian dead figure is a BBC analysis of leaked/hacked
  Rosstat records (up to ~700,000 incl. missing) — attributed to the BBC
  on the image, not stated as an official count.

## Limitations (honest)

- The world map is schematic, not to scale: continents are simplified
  polygons and the Europe / Middle East pins (1, 5, 6, 7, 8, 10) sit
  close together, spread with small offsets so each number stays readable.
- The trio illustrations are flat vector schematics (strait map, tariff
  bar chart, rout line chart), not photos or news imagery — the grading
  sandbox has no network, so no real photos could be fetched.
- Small-story cards and the ALSO list are text-dense by design (the
  winner template is a dense one-page newspaper); at 1024×1024 the
  smallest text is ~7–8 pt and is meant to be read zoomed, like a real
  front page.
- News facts are only as good as the brief's source verification; no
  live news feed was consulted during the build (the entry is a static
  image drawn from the brief).

## Repair 26 Nov 2026 (independent-verifier fixes, all re-verified live)

- Brent: was "$93.60, +2.4% on the day" (strip) and "Brent tops $93" (timeline) — wrong level and direction. Corrected to **$90.82, −0.6% on the day** in both places. Source: Makkler Brent daily history — Nov 25 close $90.82, −0.63% (open $88.38, high $90.88, low $86.95); Nov 24 close $91.40, +2.27% (so the old +2.4% was Tuesday's move). Corroborated by Reuters/Euronext 25 Nov: Brent fell >1% on Wednesday, −1.6% to $89.93 by 0730 GMT, "paring the previous day's gains". Note: one outlier (Morningstar/Dow Jones Data Talk) claimed a $94.61 Wednesday settle; it contradicts the daily history table and the Reuters wire, so it was not used.
- SOX: deleted the unsupported "chip index −50% from its June record". Now **"chip index −0.7% after an 8% morning plunge"** (Wednesday 25 Nov). Source: techi.com — SOX "fell as much as 8.0% in the morning and closed down 0.7% at 8,774.86"; corroborated by worldmoneyroadmap ("slipped 0.65% to 8,774.86").
- Nasdaq: "Nasdaq −2% on Wednesday" → **"Nasdaq −0.62% on Wednesday"**. Source: Nasdaq Composite closed Wed 25 Nov −0.62% at 23,585.80 (investingLive, techi.com, MarketWatch; Tuesday's close was −1.48%).
- DATE CHECK: "Steelers vs Broncos Fri 28 Nov" → **"Sat 28 Nov"** (verified with `date`: 28 Nov 2026 is a Saturday).
- Hormuz map: smoke ellipses lowered 12 px so the "STRAIT OF HORMUZ" label is fully readable.
- Vietnam tariff bar: "20%" → **"20%*"**, body now reads "Vietnam 20%* (35% if talks fail)". Source: Kitco/Flexport/HIDA on the USTR 25 Nov proposal — Vietnam 20% only if a reciprocal trade deal is reached, otherwise up to 35%.

Re-rendered entry.png 1024×1024, 216,621 bytes, visually checked at full page + zoomed crops: all six fixes landed, no overlaps or cut-off text.

## Checks run locally

- `python3 render.py` → entry.png 1024×1024, 215,724 bytes (< 1 MiB),
  PNG magic bytes verified.
- `MAKEFUN_OUTPUT_DIR=out node main.ts` → copies entry.png, verifies
  PNG magic, run twice → identical sha256.
- README badges present; LICENSE contains the SPDX line.
- Full kit check (`node cli/makefun.mjs check ... --transcripts <bundle>`)
  could NOT be run locally: transcripts are bundled by the coordinator
  after this build. The coordinator runs the full check before submitting.
