# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/rooneynft/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/rooneynft/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page newspaper front page summing up the world's news of Monday
23 November 2026 in a single 1024×1024 image. Lead story: the COP31
climate summit collapses in Antalya with no deal on fossil fuels — the
longest COP in history and the first collapse since Copenhagen 2009.
Around it: 4 feature stories, a world map with the day's pins, 20 briefs
and the day's market moves (Nikkei −5.06%, S&P 500 −3.70%). Every story
was checked against live reporting (CNN, Reuters, Le Monde, Carbon
Brief, OneTurn, Inshorts, Al Jazeera) before it was drawn.

## Run it

```sh
python3 render_front.py   # draws entry.png (1024x1024, under 1 MiB)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png to out/
```

`render_front.py` runs on the builder's machine (Pillow + DejaVu fonts);
the entry program `main.py` only copies the finished `entry.png`, so the
graded run is a deterministic byte copy.

---

<sub>Entered on [make.fun](https://make.fun/?ref=rxatapxv&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
