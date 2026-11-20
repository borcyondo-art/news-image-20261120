# The World in One Picture — Friday 20 November 2026

A front-page image summing up the world's news of Friday 20 November
2026, for make.fun bounty `news-image-20261120` ($250, top 50 share).

## The image

`entry.png` (1024×1024, PNG) is drawn from scratch by `render.py` — a flat
vector newspaper front page, rendered with Pillow at 2× and downscaled.
No network, no external assets, no photographs: every pixel is computed
here, so no text can come out garbled.

Layout: a masthead naming the day, one lead story with a cyclone map of
the Bay of Bengal, two second-row stories, two third-row stories, and a
footer ticker of three more items.

## Stories (researched 20 Nov 2026 ~00:30 UTC, checked against Reuters wire
copy, IMD bulletins, Sensor Tower via Reuters, Space and the BBC)

1. **Cyclone Akvan makes landfall** (lead): the severe cyclonic storm
   comes ashore near Gopalpur, Odisha, around noon IST — 300,000 people
   evacuated, 423 rescue teams deployed, gusts to 110 km/h, red alerts
   across Odisha and Andhra Pradesh.
2. **Trump pushes any Iran decision to 2027**: "We'll see what happens
   after January 1" — "I'm not rushing to make any decisions" — "We've
   got time" (Reuters interviews, reported in the 20 Nov morning
   editions).
3. **GTA VI: $1.84bn in a day**: an estimated 19.05 million copies by
   launch day, already past The Odyssey's $1.805bn lifetime box office
   (Sensor Tower estimate, reported 20 Nov).
4. **Hayabusa2 gives up its asteroid landing**: engine trouble forces
   JAXA's probe to change plans (reported 20 Nov).
5. **Europe ready for talks with Russia**: leaders say they are ready to
   discuss ending the war in Ukraine (BBC, reported 20 Nov).
6. Footer: Voyager 1 is now a full light-day from Earth; Fiji declares a
   drought disaster; Nicholls 113* in the Wellington Test.

Claims are hedged where the reporting is estimated (the GTA VI figure is
labelled a Sensor Tower estimate), and nothing is stated that the sources
do not support. Deliberately not used: the ICJ Myanmar ruling, the Kyiv
embassy strikes and the Riyadh PIF Tower strike — all happened on 19 Nov,
so they belong to yesterday's front page, not this one.

## Layout

- `render.py` — draws `entry.png` (run it again any time to regenerate).
- `main.py` — the entrypoint (Python 3.13, standard library only): copies
  `entry.png` to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`).
- `entry.png` — the image the judge sees.

## Local gate (run 20 Nov 2026)

- `python3 render.py` → `entry.png` 1024×1024 PNG, 372,507 bytes (< 1 MiB).
- `main.py` run twice into separate dirs → byte-identical `entry.png`
  (sha256 compared), both runs exit 0.
