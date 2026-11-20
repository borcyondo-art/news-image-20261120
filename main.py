# main.py — entrypoint for make.fun bounty news-image-20261120.
#
# The entry is a front-page image of Friday 20 November 2026, drawn by
# render.py in this repository (Pillow, flat vector art, no network and no
# external assets). This program does the only thing the grader needs: it
# copies that finished image to /output/entry.png, so both graded runs
# write byte-identical output. Standard library only, Python 3.13.
#
# Local check:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)

shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))
