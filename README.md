# MakerWorld script sign — Great Vibes

Three-line cut-out sign for the Bambu Lab A1 Mini:

> May your stress  
> turn into a fart  
> and leave your body

## Editable MakerWorld model

**[Open the complete OpenSCAD source](makerworld_sign_v5_measured.scad)**, copy it into MakerWorld's built-in OpenSCAD editor, and render. No local OpenSCAD or Python installation is needed for this option.

The source contains two additional measured joining strokes for `May` and `and`. Its manual join coordinates are calibrated to the exact font, size, and three lines in the source. Do not change the text without recalculating those coordinates.

## STL and 3MF

A GitHub Actions [build workflow](../../actions/workflows/build.yml) renders the source using Google's Great Vibes font, checks that the STL is **one watertight mesh** within the 180 × 180 mm build area, and converts it to a portable 3MF.

If the build passes, both files are committed into [`generated/`](generated/) and bundled in the downloadable **script-sign-models** GitHub Actions artifact. If the connectivity check fails, the workflow stops rather than publishing a misleading “one-piece” model.

The auto-generated 3MF is **geometry only**. Open it in Bambu Studio, choose your A1 Mini, set your preferred slicing settings, and save it as a Bambu Studio project if you need a printer-specific 3MF.

**Note:** These files are rebuilt from the editable v5 source. They may not be byte-for-byte identical to the manually mesh-repaired STL and printer-profile 3MF from the prior ChatGPT session; the GitHub integration cannot transfer those existing binary attachments directly.

## Downloading from GitHub

- Open [generated files](generated/) when a successful build has published them. Select the STL or 3MF and click **Download raw file**.
- Alternatively, visit [Actions](../../actions/workflows/build.yml), open the latest successful run, and download **script-sign-models** under **Artifacts**.
- To download all files, use the green **Code → Download ZIP** menu on the repository's main page.

## Printing

- Plate: Bambu Lab A1 Mini, 180 × 180 mm.
- Model: approximately 154 × 78 × 3.6 mm for the previously measured repair; check the dimensions of each *newly rendered* build before slicing.
- Suggested starting point: three wall loops, carefully cleaned build plate, and a brim for the thin extremities.
- Inspect the tiny word ligatures and the two cross-line links in Bambu Studio's sliced preview.

## Verification

`tools/verify_and_package.py` uses Trimesh to check connectivity, watertightness, and bounding-box dimensions before publishing files. It can also convert an existing printable STL into a simple portable 3MF:

```sh
python -m pip install trimesh
python tools/verify_and_package.py your_sign.stl your_sign.3mf
```
