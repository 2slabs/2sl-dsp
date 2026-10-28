# A plugin repository and the kit

Each 2sl plugin (2sl filter, 2sl dub, 2sl stab) has its own repository, with this kit as a git submodule:

```
<plugin repo>/
  2sl-dsp/                     this kit (git submodule add https://github.com/2slabs/2sl-dsp.git 2sl-dsp)
  2sl-plugin/                  the private plugin layer (twosl_plugin/, cpp/)
  src/                         the device's sources: its Python (<name>_dsp.py: the gen~ code from the kit's blocks;
                               <name>_device.py: the patch, built in memory), its brain template, its preset book,
                               and live-parameters.lock.json (written by plugin/generate.py, reviewed by hand)
  plugin/generate.py           reads the patch and writes plugin/generated/ (the core's C, the parameters, presets)
  tests/  references/  architecture/  README.md  SHORTCUTS.md
```

`plugin/generate.py` puts `2sl-dsp/`, `2sl-plugin/` and `src/` on `sys.path` and builds the patch with
`<name>_device.built_in_memory(DeviceRepository(root))`; `DeviceRepository` refuses a root without `src/` and the
kit's own folder. Nothing in the kit writes a file of a plugin's build: the plugin layer writes plugin/generated/.

Why:
- **One kit, many plugins, each pinned.** The submodule commit is the kit version a plugin was built with; a kit
  change reaches a plugin only when its repository moves the pointer, and its own tests (`generate.py --check`, its
  renders) say whether anything changed.
- **src/ is hand-written only**, but for the parameter lock, the reviewed record of what the host knows the
  parameters by (live-parameter-identity.md).
- **The tests compare the build exactly and sound as sound.** A plugin's tests hold plugin/generated/ to the byte
  and compare any two renders with the kit's `render_comparison`, never `==` (testing.md).

The in-memory patch is a stage: phase 2 of 2sl-plugin PLANS/2026-10-28-plugins-without-max.md describes each plugin
in C++ and ports the DSP, and the patch, the brain templates and this layout go.
