// Entry for make.fun's "Sum up 22 November's world news in one image".
//
// The picture itself is entry.png beside this file: a front page of Sunday
// 22 November 2026 drawn by render.py (kept in this repository so the image
// can be reproduced). This program's whole job is to deliver those exact
// bytes to the output directory, unchanged, on every run.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

// The gate wants a whole PNG of at most 1 MiB; fail loudly rather than
// deliver a truncated file if the copy somehow came out a different size.
const delivered = statSync(target).size;
if (delivered !== statSync(source).size || delivered > 1_048_576) {
  throw new Error(`entry.png copy is ${delivered} bytes, expected the source size within 1 MiB`);
}
