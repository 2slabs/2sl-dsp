# 2sl-dsp

We're [2sl](https://2sl.to), producers and engineers in Emeryville, CA. This is the kit we build every one of our Max
for Live devices and plugins with. Python writes the patch box by box, the DSP is gen~ code modelled on real
circuits, and tests check both before anything is written. It's MIT, and we wrote it to be worked on by coding agents.

## start with your agent

Open Claude Code, Codex or Cursor in an empty folder and ask for what you want:

> Clone https://github.com/2slabs/2sl-dsp, read its AGENTS.md, and make me a Max for Live audio effect: a
> transistor ladder filter with a drive and an emphasis control.

> Use 2sl-dsp's complex oscillator and low pass gate as gen~ code in my Max patch.

> Export 2sl-dsp's studio spring reverb as C for my JUCE plugin.

The agent starts at [AGENTS.md](AGENTS.md), then reads [architecture/](architecture/), where every contract and
module is written down. When something's wrong, the build stops with an error that says what and where to fix it,
so the agent can fix its own mistakes. Each DSP block cites its sources in [references/](references/) and keeps
its claims as tests, so you can check what it's told you.

Using a block outside a device takes a few lines:

```python
from twosl_dsp.gen_blocks import gen_code_with_blocks
from twosl_dsp.circuit_modules.transistor_ladder import TransistorLadder
from twosl_dsp.genexpr_export import export_c

ladder = TransistorLadder("ladder", input_volts="in1", control_volts="cv", emphasis="emphasis", oversampling=2)
code = gen_code_with_blocks("""/*GEN_BLOCK_FUNCTIONS*/
Param cv(0);
Param emphasis(0.5);
/*GEN_BLOCK_DECLARATIONS*/
/*LADDER*/
out1 = ladder_out;
""", [ladder], "ladder-example")      # GenExpr for a gen~ codebox
c_source, c_header = export_c(code, 1, 1, "ladder")      # the same program as C
```

## what's in it

The DSP blocks ([architecture/dsp-blocks.md](architecture/dsp-blocks.md)) come in two layers. Circuit modules model
one piece of hardware each, named in the code after the circuit they model:

| module | what it is |
|---|---|
| `transistor_ladder` | a five-stage transistor ladder low-pass, all five tanh stages, solved with no unit delay |
| `complex_oscillator_*` | a complex oscillator: the main and modulation oscillators and the timbre section |
| `low_pass_gate` | one low pass gate channel, vactrol included |
| `synth_spring_reverb`, `studio_spring_reverb`, `three_spring_tank` | spring reverbs |
| `ltc1060_mf10_section` | one LTC1060 / MF10 switched-capacitor filter section |
| `twin_phaser` | a dual opto phaser: two phasers, their sweeps and routing |
| `passive_stepped_high_pass` | a passive ten-step high-pass, the dub mixer's big filter knob |

Techniques are the parts underneath: zero-delay ladder, state variable, one-pole and allpass filters, antialiased
tanh and wave shapers, band-limited edges, half-band oversampling, tape, bucket brigade and three-head echoes, a
dispersive spring tank and a sidechain pump. Every block says its oversampling and its latency in samples.

The rest of the kit builds and checks the device. It writes the patch, the Init values and Live presets, keeps
what Live knows each parameter by stable across versions, freezes the release, renders each page to a PNG to check
the layout, and compares two builds of a device. [architecture/overview.md](architecture/overview.md) lists every
module.

## made with it

[2sl stab](https://2sl.to/projects/2sl-stab) is built on this kit, and so are our other devices on
[2sl.to](https://2sl.to). Our plugins run the same gen~ code, exported as C into JUCE.

## work with us

We build Max for Live devices, Live Extensions, plugins and DSP modelled on hardware for audio and hardware
companies, and ML for audio products. If you want something built, the first call is 30 minutes and free, and
you'll get a fixed price. [2sl.to/contact](https://2sl.to/contact)

## credit

Use it in anything, free or paid. MIT asks you to keep the [LICENSE](LICENSE) notice with the code. We'd also like
a line in your credits or README:

    DSP from 2sl-dsp by 2sl (https://2sl.to)

Devices built with the kit have the 2sl chip in the header, which links to 2sl.to. Please leave it in.

## setup

Live 12 Suite with its bundled Max 9.1.5. Python 3.9 or later (standard library only), Duktape for the ES5 check
(`brew install duktape`, or `apt install libduktape207`), node for the script tests, a C compiler (`cc`: Xcode's
command line tools, or `apt install gcc`) for the DSP tests (twosl_dsp/genexpr.py builds each gen~ program to render it).
Pillow for `tools/render_pages.py` and the tests (`brew install pillow`, or `pip install -r requirements-test.txt`).
Building a device needs none of it beyond Python itself.

## use it in a device repository

    git submodule add https://github.com/2slabs/2sl-dsp.git 2sl-dsp

and give the repository a `build.py`, a `src/` and the rest of the layout in
[architecture/device-repository.md](architecture/device-repository.md). A minimal `build.py`:

```python
import os, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(ROOT, "2sl-dsp"), os.path.join(ROOT, "src")]
from twosl_dsp.device_repository import DeviceRepository
import my_device                       # src/my_device.py: builds a DevicePatchBuilder, calls build_device
my_device.build(DeviceRepository.of_build_script(__file__), sys.argv[1:])
```

The fixture device the tests build (`tests/fixture_device.py`) is a small worked example.

## the folders

- `twosl_dsp/`: the library and the DSP blocks.
- `templates/`: the UI and views scripts every device gets, the blocks a device includes (the transport clock, the
  seeded random, the chord block and its display, the filters' responses for a display), and the Cozette glyphs
  (Cozette, MIT: `templates/LICENSE-Cozette.txt`).
- `tools/`: `amxd.py` (pack / freeze / unpack / list .amxd files), `es5check.py`, `compare_device_builds.py` (compare
  two builds of a device; exit 0 when what Live sees is the same), `bdf2js.py` (Cozette's BDF to glyphs),
  `max_sandbox.js` (Max's [js] globals for node tests), `render_pages.py` (a built device's pages as PNGs + layout facts,
  the overlap rule; needs Pillow), `match_patch.py` (the patch matcher).
- `references/`: the sources the kit follows (Max, Live, Live's preset format, the techniques' papers: `dsp.md`;
  circuits' datasheets: `circuits/`).
- `architecture/`: how the kit is partitioned and the contracts a device repository keeps.

## tests

    python3 -m unittest discover -s tests

## working on a device in Max

Drop the development device (`devices/<name>/<name>.amxd` in the device repository) on a track; it finds its scripts
next to it. Edit the Python, not the patch: the build overwrites the patch. Only `live.*` objects with
`parameter_enable` are Live parameters. Useful: the Max for Live Production Guidelines
(github.com/Ableton/maxdevtools), the Live Object Model docs (Max: Help > Reference > "Live Object Model").
