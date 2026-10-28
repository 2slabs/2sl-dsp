"""2sl-dsp: the 2sl DSP kit in Python: gen~ blocks modelled on circuits (techniques/, circuit_modules/), our GenExpr
renderer and C exporter (genexpr.py, genexpr_export.py), the in-memory patch the plugins' builds read
(patch_builder.py) and the tests' measures (render_comparison.py, model_accuracy.py, bs1770.py).

A plugin repository has this repository as a git submodule at `<repo>/2sl-dsp`; its plugin/generate.py puts it on
sys.path (architecture/device-repository.md). Python 3.9 or later, standard library only (a C compiler to render
gen~ code).
"""
