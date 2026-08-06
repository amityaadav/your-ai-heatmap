# Test Plan: AI Knowledge Quiz & Heatmap

## Unit Tests (Logic)
- **Scoring Validation**: Verify that a "Level 4" input correctly maps to the `--L4` CSS variable in the final output.
- **Progress Tracking**: Ensure the progress bar updates correctly as topics are completed.
- **Data Integrity**: Verify the 143 topics are all present and correctly grouped by domain.
- **State Persistence**: Test that refreshing the page restores the quiz state from LocalStorage.

## Integration Tests
- **Quiz $\to$ Map**: Verify that submitting a full set of answers results in a valid, renderable heatmap.
- **Filter Test**: Ensure the legend filters in the generated heatmap still function correctly.

## UX/UI Testing (Manual)
- **Responsive Design**: Verify the quiz is usable on both desktop and mobile.
- **Accessibility**: Ensure keyboard navigation works for all inputs and the final map is screen-reader friendly.
- **Visual Fidelity**: Compare the generated map against the original `index.html` mockup to ensure no style drift.
