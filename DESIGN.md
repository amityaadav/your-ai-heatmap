# Design: AI Knowledge Quiz UI

## Visual Language
The quiz must feel like a "Technical Assessment" rather than a school test.
- **Palette**: Use the same `--paper`, `--ink`, and `--L1-L4` colors from `index.html`.
- **Typography**: Space Grotesk for headings, IBM Plex Mono for labels and evidence fields.
- **Layout**: 
  - **Header**: Progress bar (percentage of topics completed) and domain indicator.
  - **Main Area**: A clean, centered focus area for the current topic.
  - **Input**: A large, mono-spaced text area for "Evidence/Explanation".
  - **Quick-Score**: A 4-segment toggle (1-4) for the user to indicate their perceived level.

## Interaction Model
1. **Focus Mode**: Only one topic visible at a time to prevent overwhelm.
2. **Keyboard First**: `Cmd+Enter` or `Ctrl+Enter` to submit a topic and move to the next.
3. **Dynamic Feedback**: As the user scores themselves, a "mini-map" in the corner updates in real-time to show the emerging heatmap.
4. **Review Loop**: At the end of a domain, a summary view allows users to tweak scores before finalizing.

## Dashboard Detail Rail
When a topic cell is selected on `index.html`, the detail rail shows:
- Score band and level name
- Reasoning behind the score
- Evidence citations
- **Learn more**: 2 free, credible learning resource links per topic (sourced from `resources` field in the profile JSON)
- Retake link to `quiz.html`
