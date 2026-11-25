// news-image-20261125 entry (Node 22, standard library only).
// The entry image is the entry.png beside this file, drawn locally by
// render.py from the verified 25 November 2026 news brief (see NOTES.md).
// This program only copies it to the grading output directory and checks
// the PNG magic bytes, so both grading runs write identical bytes.
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = new URL("./entry.png", import.meta.url);
const dst = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);

const head = readFileSync(dst).subarray(0, 8);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!head.equals(pngMagic)) {
  throw new Error("entry.png is not a PNG file");
}
console.log("wrote", dst);
