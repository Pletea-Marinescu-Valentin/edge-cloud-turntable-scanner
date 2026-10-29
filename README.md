# edge-cloud-turntable-scanner

Scripts and data that generate the figures of the paper *Metric 3D Digitization Without a Workstation: An Edge-to-Cloud
Turntable Scanner with Kinematically Locked Camera Poses*, prepared for ICE 2027 (33rd IEEE ICE/ITMC,
Bucharest).

The paper describes an automated photogrammetric scanning cell (team ScanCore, National University of
Science and Technology POLITEHNICA Bucharest) in which a calibrated kinematic model of the turntable
replaces structure-from-motion, two cameras at 27° interleave with the 18° turntable step, and the dense
reconstruction runs on a GPU rented per job.

## Contents

| Path | What it is |
|---|---|
| `scripts/fig_geometry.py` | Fig. 2, acquisition geometry and interleaving rule (from `data/turntable_tag_layout.json`) |
| `scripts/fig_result.py` | Fig. 5, test object and textured model (from `data/photos/`) |
| `scripts/style.py` | shared figure style (fonts, colors checked for color-vision deficiency) |
| `scripts/build.py`, `Makefile` | regenerate the figures into a local `paper/figs/`; with the manuscript present locally, also the PDF |
| `scripts/check_paper.py` | checks citations, page and word limits and the tracked files before submission |
| `data/` | AprilTag layout of the turntable disc and the two photographs used in Fig. 5 |

## Regenerating the figures

Requirements: Python 3.11 or newer with the packages of `requirements.txt` (the figures were produced with
Python 3.13.12).

```bash
pip install -r requirements.txt
python scripts/build.py figures      # or: make figures
```

This writes `paper/figs/fig_geometry.pdf`, `paper/figs/fig_result_photo.jpg` and
`paper/figs/fig_result_model.jpg` (the folder is created if needed). The block diagrams of
the paper are drawn in TikZ inside the manuscript.

## System repositories

- Edge software (FastAPI, cameras, ToF, Arduino firmware): https://github.com/AlinC10/3d-scanner-raspberry-pi
- Object pipeline (turntable pose model, OpenMVS, texturing): https://github.com/AlinC10/photogrammetry_pipeline
- Face pipeline: https://github.com/AlinC10/face_scan_pipeline
- Touchscreen interface: https://github.com/AlinC10/3d-scanner-front-end
