# Presets: one preset book

A device keeps its neutral values, its Init values and its presets in one JSON file, its preset book
(`twosl_dsp/preset_book.py`):

```json
{"neutral": {"Cutoff": 12000, "Env Amount": 0},
 "init": {"Cutoff": 700, "Env Amount": 50, "Chord": "minor", "In Key": "on", "Volume": 0},
 "presets": [{"name": "init", "group": "init", "idea": "the defaults", "values": {}},
             {"name": "chain stab", "group": "dub", "idea": "what it is for", "values": {"Cutoff": 650}}]}
```

Values are in each control's own units: a dial's or number box's number, a menu's or tab's item name, a toggle's
`off` / `on`; a stored table's `{field: [a value per row]}`, a preset giving only the fields it changes
(stored-table.md; a table given `initial_outside_presets` is left alone, as a control is). Every control the presets set has an Init value (it is the control's initial value in the patch, the
default of each gen~ Param it sets); a control given `initial_outside_presets` has
none and presets leave it alone. The build fails on an unknown control, a missing Init value, a value out of range or
not an item, and a preset name used twice.

## Neutral, Init, and a fresh device

A double-click on a Live control sets it to its initial value ("For Live UI objects, you can also double-click on the
object to restore its initial value": Max's Parameter Mode guide, references/README.md). A double-click means "take this
control out of the sound", so a control's initial value is its **neutral** value, never its Init value. Two values per
control, two jobs:

- **neutral** (`"neutral"` in the book): Live's initial value (`parameter_initial`), the double-click target, a
  plugin host's default. The value at which the control does nothing: 0 for an
  amount, a depth, a send, an added effect's mix, any modulation or velocity amount; the centre of a bipolar control;
  unity (0 dB) for a trim or gain; a menu's, tab's or toggle's off (or first neutral) item. A control with no value
  that does nothing (a cutoff, a time, a pitch, a ratio) takes the musically neutral one (a low-pass fully open, unity
  ratio), and the device's architecture lists each such choice.
- **start** (`"init"`, or a control's own `initial_outside_presets`): what a fresh instance plays, the gen~ Params'
  defaults, the brain's starting values, a fresh plugin's values.

Every control a user can double-click declares a neutral; the patch fails on one without (no fallback to Init) and on a
neutral out of range or not an item. The kit declares the neutrals of
the controls it makes: the output level (0 dB), the Preset menu and a group selector (their first item), the seeded
random's Seed (0) and Loop (off), the chord block's Chord (held notes) and In key (off). A **Hidden** control is never
saved, so Live loads it at its initial value every time: its start value is its neutral and the book doesn't name it,
except a stored table's editors, whose neutral is their field's (`"neutral": {"Stages": {"Pitch": 0, "Pulse": "off"}}`,
every field with an editor; stored-table.md). A **Stored Only** parameter has no double-click: its initial value is
its start value.

**A fresh plugin plays the Init sound.** Its host parameters start at their start values (`Parameter::start`, set
on construction: 2sl-plugin architecture/plugins.md) and a host's default is the neutral. The header's Stored Only
"Init Applied" flag (`FRESH_START_FLAG_NAME`) is still a parameter of the patch and the lock (the Max device's
fresh-start flag); the plugins' builds leave it out of the host's parameters. A plugin's tests hold every
parameter's initial value in the lock to its neutral (patch.neutral_values).

**The Init values are the gen~ Params' defaults: one source.** A Param a control sets leaves its default out of the
device's GenExpr (`Param cutoff(min=40, max=12000);`); the patch builder writes it into the code the patch holds, the
value the initial values send that Param (scaled, looked up, or a tempo-synced time at 120 BPM, as the route sends
it: `DevicePatchBuilder.gen_code_as_built`, `genexpr.code_with_param_defaults`). A Param no control sets (Stop's
panic, Live's tempo from the brain) keeps the default its code writes. `gen_code_as_built` fails, listing each, on a Param with a
default in its code that a control also sets (two sources), a Param with neither, two controls starting one Param at
different values, and a value outside the Param's min / max. Whatever renders or exports the code as given sets those
Params first: `GenProgram.run` refuses while one is unset, `genexpr_export.export_c` refuses code without its defaults
(export `DevicePatchBuilder.gen_code_as_built`), and a MatchedVoice must search or fix each.

The book makes the plugin's factory presets (each plugin's plugin/generate.py, through 2sl-plugin's twosl_plugin:
the host values and the `.vstpreset` files). Stored Only parameters go in a preset as values: a stored table's from the
preset itself (stored-table.md), a device's own from its `stored_only_values_of_preset(values)` (2sl stab: the
Pattern's steps).

## Every preset about as loud as Init

A device's presets are levelled to its Init sound: each preset's output level (the header's level control, a preset
value like any other) is set so the preset's loudest moment on one phrase is as loud as Init's: the maximum momentary
loudness, EBU Tech 3341's 400 ms sliding window over ITU-R BS.1770-5's K-weighted loudness (`twosl_dsp/preset_loudness.py`
`phrase_measures`, `twosl_dsp/bs1770.py`, references/itu-r-bs1770.md, references/ebu-tech-3341.md), its peaks under the
device's output ceiling (`presets_over_the_clip`): full scale, 0 dBFS (a device's output is clean: no soft clip,
BUGS.md 2026-10-21), or the device's own limiter's ceiling where it has one. The loudest moment, not the phrase's average: a ping and a pad at the same
level hit as hard, where the integrated loudness would pay the pad for lasting. A device's suite holds every preset
within `LOUDNESS_TOLERANCE_LU` of Init and every peak under its ceiling.

The pattern: the kit holds the phrase, the meter, the comparison, where a voice's oscillators start
(`oscillator_start_phases`: unrelated phases, seeded, as Live's voices are after running on between notes; a player
sets them through `GenProgram.set_history`), and each preset's controls as the device's DSP gets
them, read through the device's own built patch (`messages_by_preset` / `messages_for`: the routes its build wired;
a time synced to Live's tempo at the phrase's 120 BPM). So a device builds its patch in memory (the function its plugin
build calls) and never keeps a second map of its controls. The device's tests hold the rest: how a note
reaches its DSP (standing in for its brain) and its render.

## An audio effect: as loud as bypass

An audio effect has no Init sound of its own to level to: its output is its input plus what it does. So each preset's
output level is set so that its **median gain** is 0 dB: switching the device off and on is level-matched. The gain
on one input is the loudest moment out minus the loudest moment in (the same max momentary loudness, Mix as the
preset has it); the median is over the kit's effect inputs (`effect_inputs`): drums, bass, a pad, a full mix of the
three, and the chord phrase as saws every bar with a kick on every beat, EFFECT_INPUT_SECONDS (four bars at 120 BPM,
Live stopped) each at −18 LUFS integrated, generated from seeds (no samples), at EFFECT_SAMPLE_RATE (44.1 kHz: an
effect's peaks depend on the input's top octave, so no fast rate). `effect_inputs` and `effect_measures_by_preset` take `seconds` and `names` (defaults: all five, EFFECT_INPUT_SECONDS) so a device's quick test asks for fewer, shorter inputs. A device's suite
holds every preset's median within `EFFECT_LOUDNESS_TOLERANCE_LU` (±1.5) of 0 dB (`presets_off_bypass`) and every
preset to the peak rule below. Each preset's **worst miss** (its largest distance from the median over the inputs) is
reported, not tested: an effect whose gain depends on the input by nature (a self-oscillating filter, triggers, a
gate) can't match bypass on everything, and its level is a compromise.

**A circuit whose own level is not bypass's.** Some effects lose or add level as the circuit does, on every setting:
a phaser's passive dry / wet sum notches the music and its coupling capacitors cut the wet's bass (2sl phaser: the
twin phaser loses 2-3 dB on the effect inputs with the phasors in, at moderate feedback, references/circuits/mutron-bi-phase.md §8).
Making that up with each preset's output level is gain the circuit doesn't have. Such a device says so in its
architecture, never raises a preset's output level, reports each preset's median against bypass as the circuit's,
and its suite holds the presets about as loud as each other instead: every median within
`EFFECT_LOUDNESS_TOLERANCE_LU` of Init's (`presets_off_init` over the medians). The output level stays at 0 dB but
where the circuit makes a preset louder than that (full feedback's resonance): there it is turned down, to Init's
level, and the cut is reported.

### Peaks against bypass's

An effect's peaks are judged against the dry input's, not against a fixed ceiling (`effect_presets_clipping_beyond_dry`,
`EffectMeasures.peak_db_by_input` and `dry_peak_db_by_input`). An effect may raise the crest factor, as its circuit does
(a phaser's resonant peaks, a square sweep throwing the notches across a drum hit): that is the sound, and the kit's
inputs already sit near full scale (the drums peak at −1.4 dBFS at −18 LUFS), so a fixed ceiling punished the input's
crest as much as the effect's. What the rule catches is a preset whose **level** drives the device's output over its
ceiling (full scale, or its own limiter's): on some input, the preset's sample peak is over the ceiling **and** the dry
input's own peak, moved by the preset's level (its median gain against bypass), is over it as well: the dry at the
preset's level would go over there too. What the preset does to one input (its crest factor, its gain there away from its median: a resonance on the
kick) is the effect, and passes. Precisely, a preset fails on input i when

    peak_i > ceiling_db  and  dry_peak_i + median_gain > ceiling_db

(`FAST_SAMPLE_RATE_PEAK_ALLOWANCE_DB` added to the ceiling at FAST_SAMPLE_RATE). A preset under the ceiling always passes, so
every preset the old ceiling passed passes this. Each preset's peak against bypass's (peak_i − dry_peak_i) is reported
by the device's player, not tested. No limiter is added to make a preset pass: a preset that fails is too loud.

The device gives a module-level render (its preset's messages and a mono input, played on both channels, to its
left and right); `effect_measures_by_preset` plays every preset on every input in worker processes, one per CPU.
