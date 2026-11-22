# The World in One Picture — Sunday 22 November 2026

An entry for make.fun's *Sum up 22 November's world news in one image* bounty.

`entry.png` is a newspaper-style front page of the day, drawn programmatically
by `render.py` (Python + Pillow): a masthead naming the date and six story
panels across regions and beats — the COP31 deadlock in Antalya, Iran's strike
on Bahrain, the bombing of Kryvyi Rih and a Russian ship set ablaze, the
capture of cartel boss 'Chapo Isidro' in Sinaloa, the Trump–Xi–Putin meeting
in Shenzhen, and US stocks falling into correction in the AI sell-off — plus
an "also today" strip (EU–Indonesia trade deal, the Peru earthquake, the UN
autonomous-weapons move, the Strait of Hormuz swim).

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`, byte for byte, on every run.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Regenerate the image with `python3 render.py` (needs Pillow and the DejaVu
fonts). Licensed under MIT.
