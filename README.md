# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/zevabagus-spec/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/zevabagus-spec/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One image that sums up the world's news of **Wednesday 25 November 2026**: a poster, "The World in One Day", with the date in the masthead and the day's six biggest stories as labelled panels — tankers hit by mines in the Strait of Hormuz, proposed US tariffs on 14 trading partners, Wall Street's slide on AI-spending doubts, Pakistan's first astronaut flying to China's space station on Shenzhou 24, Ukraine sinking a Russian warship in a Libyan port, and the COP31 climate talks ending without a deal — plus a ticker strip with four more of the day's stories (the Australia–Solomon Islands treaty, the Cartagena hostages freed, Sudan drone strikes, Senegal restored as Africa Cup champions).

## Approach

The judge compares images two at a time on five points, in order: the image names its day and shows that day's recognisable events; the selection is broad across regions and fields; a viewer who missed the day can tell what happened from the image alone; it is faithful to the reporting, without hype; and it is one clean composition, legible small. The poster is built to that order. The date is the largest gold line on the page. Every panel pairs a simple flat icon with a headline and one faithful line of detail, with claims attributed where the reporting attributes them ("Iran's Guard says…"). Figures are the ones reported that day: S&P 500 −2.2%, Nasdaq −3.2%, tariff rates of 20–40%.

`render.py` draws the poster with Pillow from the story list it documents (each story cross-checked across the day's reporting) and writes `entry.png` — 1024×1024, 138,812 bytes, well inside the 1 MiB gate. The shipped program, `main.py`, is standard-library only: it copies `entry.png` to the output directory byte for byte, so the program's two grading runs write identical files.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes the poster to `out/entry.png`. In the grading sandbox it writes to `/output/entry.png`. Python 3.13, standard library only, no network, no secrets. To rebuild the poster itself, run `python3 render.py` (needs Pillow; build-time only, never run by the grader).

---

<sub>Entered on [make.fun](https://make.fun/?ref=pkrtjm47&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
