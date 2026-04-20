# glenmosset

A personal collection of one-shot prompts used to probe the capabilities of new AI coding models. Each file is the unedited output of a single prompt given to a frontier model — kept here so I can diff outputs as new models ship.

In the spirit of [Simon Willison's pelican SVG test](https://simonwillison.net/2025/Apr/16/qwen-beats-opus/): small, self-contained, visually or behaviorally legible, hard to fake.

## The tests

### `bouncing_ball.py` — "ball bouncing inside a spinning hexagon"
The viral early-2025 physics prompt. Exercises a model's grasp of rotating-frame collision response: reflecting the ball's velocity relative to the moving wall, penetration correction, tangential friction. Easy to fail silently (ball tunnels through, ignores wall velocity, jitters in corners).

```bash
pip install pygame
python bouncing_ball.py
```

### `spider.py` — "simple website crawler that lists live URLs"
A boring-but-honest test: same-domain BFS, relative-link resolution, fragment stripping, polite delay, graceful failure on non-200. Measures whether a model reaches for the right stdlib/3rd-party pieces without over-engineering.

```bash
pip install requests beautifulsoup4
python spider.py
```

## Why "glenmosset"

It's a name. The repo needed one.

## License

MIT — see `LICENSE`.
