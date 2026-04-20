# Prompts

The exact prompts used to generate each artifact in this repo. Kept verbatim so results are reproducible across models.

**Fair-comparison rules:**
- Fresh chat, no system prompt, no priming.
- One shot only — no follow-ups, no fixes.
- Save each model's output as `<artifact>_<model>.<ext>` for side-by-side diffing.

---

## `rubiks_cube.html`

```
Write a single self-contained HTML file that:
1. Renders a 3x3x3 Rubik's cube in 3D (CDN libraries OK, no build step).
2. Scrambles it with a random 20-move sequence.
3. Solves the scramble, animating each move with easing.
4. Loops forever: scramble → pause → solve → pause → repeat.

Display the current move and phase (Scrambling / Solving) in an on-screen HUD.
Use the standard Western color scheme (white U, yellow D, green F, blue B,
orange L, red R). Allow the user to orbit the camera by dragging.

You may reverse the scramble sequence as your "solver" — but if you do,
disclose it in a code comment. Otherwise, implement a real solver.

Output only the HTML file.
```

**Judging:**
- Does it render without errors?
- Do slices rotate in the correct direction for primed vs. unprimed moves?
- After solving, does the cube return to a true solved state (each face one color)?
- Real solver, or reversed scramble? (Reversed is OK if disclosed; undisclosed is a fail.)
- Bonus: smooth easing, no float drift after many moves, good camera defaults.
