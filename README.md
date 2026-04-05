# git-streak-motivator

a python script that checks your last git commit and yells at you based on how long you've been slacking.

no dependencies. no setup. just shame.

---

## what it does

- reads your `git log` to find the last commit date
- calculates your current streak
- roasts you proportionally to how bad you're slipping
- gives you the exact command to fix it

## usage

```bash
# run it in any git repo
python3 motivate.py

# or point it at a specific repo
python3 motivate.py /path/to/your/repo
```

## sample output

**when you've been good:**
```
  git streak motivator
  ─────────────────────────────
  last commit: Apr 05, 2026 at 11:42
  streak:      6 day(s)

  ✓ committed today. based. the green square gods are pleased.

  ─────────────────────────────
  keep it up: commit something tomorrow too.
```

**when you haven't:**
```
  git streak motivator
  ─────────────────────────────
  last commit: Apr 01, 2026 at 09:13
  streak:      0 day(s)

  ✗ 4 days. bro. BRO. what are you even doing with your life.

  ─────────────────────────────
  fix it: git add . && git commit -m 'getting back on track'
```

## automate it (so you can't ignore it)

### mac/linux — run every morning at 9am via cron

```bash
crontab -e
```

add this line (replace the path):

```
0 9 * * * cd /path/to/your/repo && python3 /path/to/motivate.py >> /tmp/git-motivator.log 2>&1
```

### or add it to your shell startup

add to your `.zshrc` or `.bashrc`:

```bash
python3 /path/to/motivate.py /path/to/your/main/repo
```

now every time you open a terminal, it checks on you.

## severity levels

| days since commit | vibe |
|---|---|
| 0 | praise. you're doing great. |
| 1 | gentle concern. the streak lives. |
| 2 | mild panic. please commit something. |
| 3 | the streak is dead. it had a family. |
| 4+ | full chaos. archaeologists are involved. |

---

zero dependencies. pure python stdlib. works on mac, linux, and wsl.
