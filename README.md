# Wednesday 25 November 2026: 35 stories, 7 regions — Hormuz mined, US tariffs, Asia rout

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/besan11/news-image-20261125-r2-local/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/besan11/news-image-20261125-r2-local/reward.svg)](https://make.fun/bounty/news-image-20261125)

Entry for the [make.fun bounty "Sum up 25 November's world news in one image"](https://make.fun/bounty/news-image-20261125) ($100). One 1024×1024 newspaper front page summarising the world news of **Wednesday 25 November 2026**: 35 stories across 7 regions, drawn from a source-verified brief (Reuters, AP, BBC, BEA, Xinhua, Al Jazeera, AFP, ISW, Just Security).

## The image

`entry.png` — "THE WORLD TODAY", Wednesday 25 November 2026:

- **The top three, drawn large:** two tankers hit mines and burn in the Strait of Hormuz; the US proposes Section 301 tariffs on 14 trading partners; the AI sell-off rolls through Asia (KOSPI −6.16%).
- **The day in numbers:** 2 tankers mined, Brent $93.60 (+2.4%), KOSPI −6.16%, 14 tariff partners, 490,334 Russian soldiers dead (leaked data, BBC), 76 hostages freed in Cartagena.
- **The day in UTC:** an 8-event timeline from the 00:18 Shenzhou-24 launch to the evening Cairo toll.
- **Stories 4–13** drawn as cards, **stories 14–35** in a numbered "ALSO" list, a **"WHERE IT HAPPENED"** world map with numbered pins 1–13, and a red-framed **DATE CHECK** box naming the near-miss stories that are explicitly *not* 25 November (Kyiv bridges, Cyclone Akvan, Iran–Bahrain, Huawei verdict, Dell quarter, the Tuesday market close, and more) plus what had not happened yet.
- Every story carries a region label, a source, and a status pill — **CONFIRMED / OFFICIAL / REPORTED / CLAIM** — with the legend in the footer. Single-source claims are labelled CLAIM, never presented as confirmed.

## How it is built

- `render.py` draws the page with Pillow from the brief in `NOTES.md`, using the Liberation Serif/Sans `.ttf` files shipped in `fonts/` (real font files in the repo — no base64 font blocks, no network, no photos).
- `main.ts` (Node 22, standard library only) copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` and verifies the PNG magic bytes, so both grading runs write identical bytes.

## Run it

```sh
python3 render.py            # redraw entry.png (1024x1024)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # entrypoint contract
```

## Licence

MIT — see [LICENSE](LICENSE).
