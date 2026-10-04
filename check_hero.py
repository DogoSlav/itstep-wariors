"""Local self-check for your hero - run it BEFORE you upload.

    py check_hero.py my_hero.py          (checks + sparring matches)
    py check_hero.py my_hero.py --log    (also prints a sample fight)

Keep base.py, match.py and check_hero.py in the same folder as your hero file.
"""
import sys, os, json, time, subprocess, traceback
from itertools import product
from types import SimpleNamespace

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import base, match

ok = True


def good(msg): print("  [OK]  ", msg)
def warn(msg): print("  [WARN]", msg)


def bad(msg):
    global ok
    ok = False
    print("  [FAIL]", msg)


def sparring(parent):
    """A simple opponent: uses its special whenever it is ready."""
    class Sparring(parent):
        def choose_action(self, enemy):
            return "special" if self.special_ready else "attack"
    return Sparring


def check_situations(cls):
    """Call choose_action() in many made-up situations and look for problems."""
    me = cls("test")
    max_hp = match.stats_of(cls)["max_hp"]
    problems, warnings, count = {}, {}, 0
    for hp, ready, etype, ehp, eready, last in product(
            (max_hp, max_hp // 2, 5), (True, False), ("Character", "Warrior", "Mage", "Archer"),
            (100, 10), (True, False), ("none", "attack", "special")):
        me.round, me.hp, me.max_hp = 7, hp, max_hp
        me.special_ready, me.cooldown = ready, 0 if ready else 2
        enemy = SimpleNamespace(name="Enemy", hero_type=etype, hp=ehp, max_hp=100,
                                special_ready=eready, last_action=last)
        situation = f"my hp={hp}, special_ready={ready}, enemy={etype} hp={ehp}, enemy special_ready={eready}"
        count += 1
        try:
            result = me.choose_action(enemy)
        except Exception as e:
            problems.setdefault(f"crashed with {type(e).__name__}: {e}", situation)
            continue
        if result not in ("attack", "special"):
            problems.setdefault(f"returned {result!r} - must be exactly \"attack\" or \"special\"", situation)
        elif result == "special" and not ready:
            warnings.setdefault("asked for \"special\" while it is NOT ready (arena will use attack instead)", situation)
    return count, problems, warnings


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    path = os.path.abspath(args[0] if args else "my_hero.py")
    print(f"\nChecking {path}\n")

    print("1) File")
    if not os.path.isfile(path):
        bad("File not found. Usage: py check_hero.py my_hero.py")
        return finish()
    if os.path.getsize(path) > 30000:
        bad("File is bigger than 30 000 bytes - the server would reject it.")
        return finish()
    try:
        cls = match.load(path)
    except Exception as e:
        bad("Cannot load your file:\n         " + "".join(traceback.format_exception_only(type(e), e)).strip().replace("\n", "\n         "))
        return finish()
    parent = match.stats_of(cls)["type"]
    good(f"Found hero class {cls.__name__} (inherits from {parent}); moves and stats are untouched")

    print("\n2) Test match the way the server runs it (separate process, 10 s limit)")
    started = time.time()
    try:
        p = subprocess.run([sys.executable, os.path.join(HERE, "match.py"), path, "builtin:Warrior", "You", "Dummy"],
                           capture_output=True, text=True, timeout=10)
        d = json.loads(p.stdout.strip().splitlines()[-1])
        if d["error"]:
            bad(d["error"])
        else:
            good(f"Match finished in {time.time() - started:.1f}s")
    except subprocess.TimeoutExpired:
        bad("Your code takes longer than 10 s - is there an infinite loop (while True / endless recursion)?")
        return finish()
    except (IndexError, ValueError):
        bad("The match crashed:\n" + p.stderr[-600:])
        return finish()

    print("\n3) choose_action() in many different situations")
    count, problems, warnings = check_situations(cls)
    for msg, sit in problems.items():
        bad(f"{msg}\n         e.g. when: {sit}")
    for msg, sit in warnings.items():
        warn(f"{msg}\n         e.g. when: {sit}")
    if not problems:
        good(f"{count} situations tested, always returned a valid move")

    if not problems:
        print("\n4) Sparring matches (40 fights each, opponent uses its special whenever ready)")
        for opp in (base.Character, base.Warrior, base.Mage, base.Archer):
            results = [match.fight(cls, sparring(opp), "You", opp.__name__)[0] for _ in range(40)]
            w, d, l = results.count(0), results.count(None), results.count(1)
            print(f"        vs {opp.__name__:10} win {w:2d} | draw {d:2d} | lose {l:2d}   {'#' * (w // 2)}")
        print("        (a draw = exactly equal HP at the end - rare)")
        if "--log" in sys.argv:
            print("\n   Sample fight vs Warrior:")
            print("\n".join(match.fight(cls, sparring(base.Warrior), "You", "Warrior")[1][:12]))
    return finish()


def finish():
    print("\n" + ("READY TO UPLOAD - everything works!" if ok else "NOT READY - fix the [FAIL] lines above and run the check again."))
    sys.exit(0 if ok else 1)


main()
