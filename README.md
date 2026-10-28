# 2sl-dsp

We're [2sl](https://2sl.to), producers and engineers in Emeryville, CA. This is the DSP kit our plugins are built
from: gen~ code (GenExpr) modelled on real circuits, written from Python, rendered and exported as C by our own
translator, with tests that hold each block to its sources. It's MIT, and we wrote it to be worked on by coding agents.

Our plugins' builds read this kit's gen~ code and circuit modules today. We're moving the DSP to C++; until each
port is done, the Python here is the reference it is checked against.

## start with your agent

Open your coding agent in an empty folder and ask for what you want:

> Clone https://github.com/2slabs/2sl-dsp, read its AGENTS.md, and give me its transistor ladder as C for my plugin.

> Use 2sl-dsp's complex oscillator and low pass gate as gen~ code in my patch.

The agent starts at [AGENTS.md](AGENTS.md), then reads [architecture/](architecture/), where every contract and
module is written down. When something's wrong, the kit stops with an error that says what and where to fix it,
so the agent can fix its own mistakes. Each DSP block cites its sources in [references/](references/) and keeps
its claims as tests, so you can check what it's told you.

Using a block takes a few lines:

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

The rest of the kit is what our plugins' builds read and what the tests measure with: the in-memory patch a
plugin's parameters, routes and presets are read off, the preset book, the lock that keeps what a host knows each
parameter by, the brain blocks (seeded random, chord block, stored table), our GenExpr renderer and C exporter, and
the render comparison, loudness and model-accuracy measures. [architecture/overview.md](architecture/overview.md)
lists every module.

## made with it

[2sl stab](https://2sl.to/projects/2sl-stab), 2sl filter and 2sl dub run this kit's gen~ code, exported as C.

## work with us

We build Max for Live devices, Live Extensions, plugins and DSP modelled on hardware for audio and hardware
companies, and ML for audio products. If you want something built, the first call is 30 minutes and free, and
you'll get a fixed price. [2sl.to/contact](https://2sl.to/contact)

## credit

Use it in anything, free or paid. MIT asks you to keep the [LICENSE](LICENSE) notice with the code. We'd also like
a line in your credits or README:

    DSP from 2sl-dsp by 2sl (https://2sl.to)

## setup

Python 3.9 or later (standard library only), node for the script tests, a C compiler (`cc`) for the DSP
tests (twosl_dsp/genexpr.py builds each gen~ program to render it).

## use it in a plugin repository

    git submodule add https://github.com/2slabs/2sl-dsp.git 2sl-dsp

and see [architecture/device-repository.md](architecture/device-repository.md) for the layout our plugin
repositories keep. The fixture device the tests build (`tests/fixture_device.py`) is a small worked example.

## the folders

- `twosl_dsp/`: the library and the DSP blocks.
- `templates/`: the brain blocks a device's brain includes (the transport clock, the seeded random, the chord block,
  the stored table) and the LTC1060 / MF10 section's response for a graph.
- `tools/`: `max_sandbox.js` (Max's [js] globals for node tests of a brain), `match_patch.py` (the patch matcher).
- `references/`: the sources the kit follows (the techniques' papers: `dsp.md`; circuits' datasheets: `circuits/`;
  the host formats).
- `architecture/`: how the kit is partitioned and the contracts a plugin repository keeps.

## tests

    python3 -m unittest discover -s tests
