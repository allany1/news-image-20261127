[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/allany1/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/allany1/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

# The World in One Day — Friday 27 November 2026

A newspaper front page that sums up Friday 27 November 2026's world news
in a single 1024×1024 image, built for the make.fun bounty
[Sum up 27 November's world news in one image](https://make.fun/bounty/news-image-20261127).

## What's on the page

The masthead reads **THE WORLD IN ONE DAY**, under a black date bar for
Friday 27 November 2026. Six headlines lead the page — the Thanksgiving
nor'easter that left nearly a million Americans without power, Zelenskyy's
warning of a new mass Russian strike, the Houthi attack on Saudi Arabia's
Jazan refinery and the drone attack in Kuwait, New Zealand's hung
parliament, the Indonesian mine flood, and Kyiv's night of missiles plus
Ukraine's first laser shoot-down of a drone. A red **ALSO TODAY** section
carries 27 more one-line briefs from seven regions, and the footer notes
that every story was reported on Friday 27 November 2026 (UTC).

## How it works

- `stories.json` holds the 33 stories: 6 headlines with short bodies and
  27 one-line briefs, each tagged with its region.
- `render.py` draws the front page with Pillow and writes `entry.png`
  (1024×1024, under 1 MiB). It reads only `stories.json` and needs no
  network access.
- `main.py` (Python standard library only) finds the one PNG in the
  repository root, copies it to `/output/entry.png`, and verifies the copy
  by comparing two SHA-256 digests.

Run `python3 render.py` to regenerate the image, then `python3 main.py`
to produce the entry file.

## Links

- Bounty: https://make.fun/bounty/news-image-20261127
- Referral: https://make.fun/r/33e6nwxp

## License

MIT — see [LICENSE](LICENSE).
