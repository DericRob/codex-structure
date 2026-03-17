# Prompt 04 — Design CSV Data Transfer

Transfer the eight design CSV data files into:

```text
~/.codex/skills/design/data/
```

## Files expected

- `charts.csv`
- `colors.csv`
- `creative-tim.csv`
- `landing.csv`
- `styles.csv`
- `typography.csv`
- `ui-reasoning.csv`
- `ux-guidelines.csv`

## Recommended transfer methods

```bash
# From source machine
scp -r ~/.codex/skills/design/data/ user@newmachine:~/.codex/skills/design/data/

# Or create a tarball
tar czf codex-design-data.tar.gz -C ~/.codex/skills/design data/
# Transfer and extract on the new machine
tar xzf codex-design-data.tar.gz -C ~/.codex/skills/design/
```

## Validation reference

| File | Columns |
|------|---------|
| charts.csv | data_type, best_chart, colors, accessibility, library, when_to_use, anti_pattern |
| colors.csv | product_type, primary, secondary, cta, background, text, border |
| creative-tim.csv | product_type, kit_name, framework, description, best_components, use_case, url_path |
| landing.csv | pattern_name, section_order, cta_placement, color_strategy, effects, conversion_tips, best_for |
| styles.csv | name, description, implementation, use_cases, do_examples, dont_examples |
| typography.csv | name, category, heading_font, body_font, mood, best_for, google_fonts_url |
| ui-reasoning.csv | product_type, recommended_style, color_mood, typography_mood, key_effects, anti_patterns, severity |
| ux-guidelines.csv | category, rule, do_pattern, do_code, dont_pattern, dont_code, severity |
