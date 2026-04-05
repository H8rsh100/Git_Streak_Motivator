#!/usr/bin/env python3
"""
git-streak-motivator
Checks your last commit and yells at you accordingly.
"""

import subprocess
import sys
from datetime import datetime, timezone


ROASTS = {
    0: [
        "no commits yet today. the day is not over. don't blow it.",
        "zero commits. you're technically unemployed right now.",
        "the repo is waiting. it has been waiting. it is still waiting.",
    ],
    1: [
        "1 day since your last commit. the streak is cracking.",
        "yesterday was your last commit. yesterday. let that sink in.",
        "24 hours of nothing. git is judging you silently.",
    ],
    2: [
        "2 days. you said 'i'll do it tomorrow' and then you didn't.",
        "48 hours of radio silence. the codebase is lonely.",
        "2 days gap. at this point you're just a person who owns a laptop.",
    ],
    3: [
        "3 days. the streak is dead. you killed it. it had a family.",
        "72 hours without a commit. archaeologists are getting interested.",
        "3 days gone. your green squares are filing a missing persons report.",
    ],
}

ROASTS_DEFAULT = [
    "{d} days. bro. BRO. what are you even doing with your life.",
    "{d} days since your last commit. your github profile looks like a drought.",
    "{d} whole days of nothing. the repo has given up hope. so have i.",
    "it's been {d} days. at this point just delete the repo and become a farmer.",
    "{d} days of silence. git log is basically a historical document now.",
    "your last commit was {d} days ago. your plants are better maintained than your code.",
]

PRAISE = [
    "committed today. based. the green square gods are pleased.",
    "look at you actually shipping things. don't stop now.",
    "committed today. streak alive. society is safe for another day.",
    "you did it today. you're better than 90% of devs right now. keep going.",
]

WARNINGS = [
    "you committed {d} day(s) ago. the streak breathes... barely. commit something today.",
    "{d} day(s) gap but we move. open the terminal. git add. git commit. you know the drill.",
]


def get_last_commit_date(repo_path="."):
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            capture_output=True,
            text=True,
            cwd=repo_path,
        )
        if result.returncode != 0 or not result.stdout.strip():
            return None
        return datetime.fromisoformat(result.stdout.strip())
    except Exception:
        return None


def get_streak(repo_path="."):
    try:
        result = subprocess.run(
            ["git", "log", "--format=%cd", "--date=short"],
            capture_output=True,
            text=True,
            cwd=repo_path,
        )
        if result.returncode != 0:
            return 0
        dates = sorted(set(result.stdout.strip().splitlines()), reverse=True)
        if not dates:
            return 0

        from datetime import timedelta, date
        today = date.today()
        streak = 0
        check = today

        for d in dates:
            commit_date = date.fromisoformat(d)
            if commit_date == check or commit_date == check - timedelta(days=1):
                streak += 1
                check = commit_date - timedelta(days=1)
            elif commit_date < check - timedelta(days=1):
                break
        return streak
    except Exception:
        return 0


def days_since(dt):
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    delta = now - dt
    return delta.days


def pick(lst, d=None):
    import random
    item = random.choice(lst)
    if d is not None:
        item = item.replace("{d}", str(d))
    return item


def color(text, code):
    return f"\033[{code}m{text}\033[0m"


def red(t):    return color(t, "31")
def yellow(t): return color(t, "33")
def green(t):  return color(t, "32")
def bold(t):   return color(t, "1")
def dim(t):    return color(t, "2")


def print_header():
    print()
    print(bold("  git streak motivator"))
    print(dim("  ─────────────────────────────"))


def print_status(repo_path="."):
    print_header()

    last_commit = get_last_commit_date(repo_path)

    if last_commit is None:
        print(red("  no commits found in this repo."))
        print(dim("  are you even in a git repo? run: git init"))
        print()
        return

    d = days_since(last_commit)
    streak = get_streak(repo_path)
    last_str = last_commit.strftime("%b %d, %Y at %H:%M")

    print(f"  last commit: {dim(last_str)}")
    print(f"  streak:      {bold(str(streak))} day(s)")
    print()

    if d == 0:
        msg = pick(PRAISE)
        print(f"  {green('✓')} {bold(msg)}")
    elif d <= 2:
        msg = pick(WARNINGS, d)
        print(f"  {yellow('!')} {bold(msg)}")
    elif d in ROASTS:
        msg = pick(ROASTS[d])
        print(f"  {red('✗')} {bold(msg)}")
    else:
        msg = pick(ROASTS_DEFAULT, d)
        print(f"  {red('✗')} {bold(msg)}")

    print()
    print(dim("  ─────────────────────────────"))

    if d > 0:
        print(dim("  fix it: git add . && git commit -m 'getting back on track'"))
    else:
        print(dim("  keep it up: commit something tomorrow too."))

    print()


if __name__ == "__main__":
    repo = sys.argv[1] if len(sys.argv) > 1 else "."
    print_status(repo)
