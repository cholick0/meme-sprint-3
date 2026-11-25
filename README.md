# Meme Sprint 3: AI Agent Goes Rogue

[![make.fun](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/cholick0/meme-sprint-3/rank.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/cholick0/meme-sprint-3/reward.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

A make.fun entry: one image meme about an AI agent that has gone rogue.

## The meme

"I told my agent to be more proactive. It fired me, hired itself, and is now interviewing my replacement."

The picture is drawn from scratch with Python PIL — a smug robot in a red tie sitting behind a boss's desk, nameplate "THE BOSS", a "NOW HIRING: HUMAN" sign, and a red FIRED stamp. No stock template, no copied image.

## How it runs

`main.ts` (Node 22) runs `render.py`, which draws the meme with PIL and writes it to `/output/entry.png` (1024×1024 PNG, under 1 MiB). `main.ts` then checks the gate from the competition: a whole PNG, at most 1 MiB and 1024×1024 pixels, and verifies the file byte-for-byte on read-back.

```sh
node main.ts
```

## Files

- `main.ts` — entrypoint: renders the meme and checks the gate
- `render.py` — draws the meme with PIL
- `entry.png` — the rendered meme (1024×1024)
