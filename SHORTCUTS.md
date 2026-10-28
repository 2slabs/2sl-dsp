# Shortcuts

Things done the quick way, to come back to. Each with when it was taken.

- 2026-10-16: the live.tab button rule (`twosl_dsp/layout_rules.py`: 6 px a character + 1) is calibrated from one case
  that ships and looks right in Live (2sl stab's Sub Mode, "-2 pls" in 37 px), not from Live's font metrics. Proper:
  measure live.tab's text width in Live.
- 2026-10-18 (re-done 2026-10-21): how wide a Live control must be for its text (`twosl_dsp/layout_rules.py`) is
  measured with a stand-in font (Liberation Sans at 11 px, `LIVE_FONT_ADVANCES`, the size calibrated from one
  observation: 2sl gate v0.5's 8-character dial names in 44 px dials, played in Live), not Live's own font, whose
  metrics no source gives (references/README.md, "Live's control font"). Since 2026-10-21 per character with padding
  (renders showed touching labels), so "Symmetry" now measures over 44 px though Live showed it fitting: the stand-in
  is wider than Live there. Proper: measure Live's dial / menu / toggle / tab text in Live (a screenshot of known
  strings at known widths), or find the font and its metrics, and replace the table.
- 2026-10-20: the transistor ladder module's Emphasis runs the circuit's law (k 4 at 7.5 by the Regen Cal) on an
  UNVERIFIED pot curve: `emphasis_pot_audio_taper_at_half_rotation` 0.10, the common 10 %-at-half audio convention
  mirrored (references/circuits/moog-transistor-ladder.md §7), not the 50k REV AUD part's (no datasheet, no measured
  unit). It sets k(10) (7.76 here; 4 to 15 over all curves) and how fast k rises toward 7.5. Proper: the part's
  datasheet or a measured unit's pot, the default from it.
- 2026-10-28: the in-memory patch (`twosl_dsp/patch_builder.py`) still makes the Max device's boxes the plugins'
  builds ignore (the UI script's [js] box, the displays' jsui boxes, the chrome, the Preset menu's placeholder item,
  the layout's places and widths), so the patch, the lock and plugin/generated/ stay byte for byte what they were.
  Proper: phase 2 (2sl-plugin PLANS/2026-10-28-plugins-without-max.md) describes each plugin in C++ and the patch goes.
