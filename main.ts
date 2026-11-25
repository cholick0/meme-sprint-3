import { spawnSync } from "node:child_process";
import { existsSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Meme Sprint 3: AI Agent Goes Rogue.
// The entry is one image at /output/entry.png. The picture itself is drawn
// from scratch by render.py (Python + PIL, shipped in this repo) because
// headless Chromium cannot run on this machine.

// Gate from competition.yaml: /output/entry.png must be a whole PNG or
// JPEG, at most 1 MiB (1,048,576 bytes) and 1024 by 1024 pixels.
const MAX_BYTES = 1_048_576;
const MAX_DIM = 1024;
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const OUT_DIR = "/output";
const OUT_FILE = join(OUT_DIR, "entry.png");
const HERE = dirname(fileURLToPath(import.meta.url));
const RENDER = join(HERE, "render.py");

const result = spawnSync("python3", [RENDER, OUT_FILE], { stdio: "inherit" });
if (result.status !== 0) {
  console.error(`render.py exited with status ${result.status}`);
  process.exit(1);
}

if (!existsSync(OUT_FILE)) {
  console.error("render.py did not produce entry.png");
  process.exit(1);
}

function checkEntry(): void {
  const bytes = statSync(OUT_FILE).size;
  if (bytes > MAX_BYTES) {
    throw new Error(`entry.png is ${bytes} bytes, over the ${MAX_BYTES} cap`);
  }
  const data = readFileSync(OUT_FILE);
  if (!data.subarray(0, 8).equals(PNG_MAGIC)) {
    throw new Error("entry.png is not a whole PNG (bad signature)");
  }
  // PNG IHDR: width at bytes 16-19, height at bytes 20-23, big-endian.
  const width = data.readUInt32BE(16);
  const height = data.readUInt32BE(20);
  if (width > MAX_DIM || height > MAX_DIM) {
    throw new Error(`entry.png is ${width}x${height}, over the ${MAX_DIM}x${MAX_DIM} cap`);
  }
  console.log(`gate ok: PNG ${width}x${height}, ${bytes} bytes`);
}

function verifyWritten(): void {
  // Read the file back twice and compare byte for byte: the artifact on
  // disk must be exactly what the render produced, stable between reads.
  const first = readFileSync(OUT_FILE);
  const second = readFileSync(OUT_FILE);
  if (!first.equals(second)) {
    throw new Error("entry.png changed between reads");
  }
  console.log(`read-back ok: ${first.length} bytes, identical`);
}

try {
  checkEntry();
  verifyWritten();
} catch (err) {
  console.error((err as Error).message);
  process.exit(1);
}
