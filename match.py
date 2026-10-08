"""Runs one best-of-3 match in its own process. Usage: match.py fileA fileB nameA nameB
A path can also be "builtin:Warrior" etc. Prints one JSON line.

FAIR PLAY: all damage, healing, blocking and cooldowns are computed HERE.
Hero stats are snapshotted from base.py before any student code is loaded.
Student code only decides WHICH move to use ("attack" or "special")."""
import sys, json, copy, random, importlib.util
from types import SimpleNamespace
import base
import safety

_randint = random.Random().randint   # private RNG, captured before student code runs
_BASES = (base.Character, base.Warrior, base.Mage, base.Archer)
SNAP = {c: {"type": c.__name__, "max_hp": c.max_hp, "basic": tuple(c.basic),
            "sname": c.special_name, "cd": c.special_cooldown, "sp": copy.deepcopy(c.special)}
        for c in _BASES}
FORBIDDEN = {"max_hp", "basic", "special", "special_name", "special_cooldown",
             "basic_attack", "special_ability", "attack"}


def stats_of(cls):
    for c in cls.__mro__:        # nearest arena hero in the inheritance chain
        if c in SNAP:
            return SNAP[c]


def load(path):
    if path.startswith("builtin:"):
        return getattr(base, path.split(":")[1])
    with open(path, encoding="utf-8", errors="replace") as fh:
        problems = safety.check_source(fh.read())
    if problems:
        raise ValueError("Not allowed in the arena:\n         " + "\n         ".join(problems[:6]))
    spec = importlib.util.spec_from_file_location("student_" + str(abs(hash(path))), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    found = [c for c in vars(mod).values()
             if isinstance(c, type) and issubclass(c, base.Character) and c.__module__ == spec.name]
    if not found:
        raise ValueError("No class that inherits from Character/Warrior/Mage/Archer")
    cls = found[-1]
    for c in cls.__mro__:
        if c.__module__ == spec.name:
            bad = FORBIDDEN & set(vars(c))
            if bad:
                raise ValueError(f"You may not change {sorted(bad)} - the hero's moves are fixed. "
                                 "Only write choose_action() (and your own helper methods).")
    cls("test")  # make sure it can be created
    return cls


def resolve(s, action):
    """-> (damage, heal, recoil, block) of one move, computed by the arena"""
    if action == "attack":
        return _randint(*s["basic"]), 0, 0, 0.0
    sp = s["sp"]
    lo, hi = sp.get("damage", (0, 0))
    dmg = sum(_randint(lo, hi) for _ in range(sp.get("hits", 1)))
    return dmg, sp.get("heal", 0), sp.get("recoil", 0), sp.get("block", 0.0)


def fight(A, B, na, nb):
    names = [na, nb]
    fighters = [A(na), B(nb)]
    S = [stats_of(A), stats_of(B)]
    hp = [S[0]["max_hp"], S[1]["max_hp"]]
    cd, last, log = [0, 0], ["none", "none"], []
    for r in range(1, 41):
        acts = []
        for i in (0, 1):
            me = fighters[i]
            me.round, me.hp, me.max_hp = r, hp[i], S[i]["max_hp"]
            me.cooldown, me.special_ready = cd[i], cd[i] == 0
            enemy = SimpleNamespace(name=names[1 - i], hero_type=S[1 - i]["type"], hp=hp[1 - i],
                                    max_hp=S[1 - i]["max_hp"], special_ready=cd[1 - i] == 0,
                                    last_action=last[1 - i])
            try:
                a = me.choose_action(enemy)
            except Exception as e:
                log.append(f"  {names[i]} crashed: {type(e).__name__}: {e}  (used attack)")
                a = "attack"
            if a == "special" and cd[i] > 0:
                log.append(f"  {names[i]}: special not ready, used attack instead")
                a = "attack"
            elif a not in ("attack", "special"):
                log.append(f"  {names[i]}: invalid action {a!r}, used attack instead")
                a = "attack"
            acts.append(a)
        res = [resolve(S[i], acts[i]) for i in (0, 1)]
        dealt = [res[i][0] - int(res[i][0] * res[1 - i][3]) for i in (0, 1)]   # after enemy block
        for i in (0, 1):
            hp[i] = min(S[i]["max_hp"], hp[i] - dealt[1 - i] - res[i][2] + res[i][1])
        for i in (0, 1):
            if acts[i] == "special":
                cd[i] = S[i]["cd"]
            cd[i] = max(0, cd[i] - 1)
            last[i] = acts[i]
        lab = [("SPECIAL " + S[i]["sname"]) if acts[i] == "special" else "attack" for i in (0, 1)]
        log.append(f"  R{r}: {na} {lab[0]} ({dealt[0]}) | {nb} {lab[1]} ({dealt[1]})  ->  {max(hp[0],0)} : {max(hp[1],0)} HP")
        if hp[0] <= 0 or hp[1] <= 0:
            break
    # whoever has more HP left wins (if both fell in the same round, the less negative HP wins)
    winner = 0 if hp[0] > hp[1] else 1 if hp[1] > hp[0] else None
    return winner, log


def main():
    pa, pb, na, nb = sys.argv[1:5]
    classes, errors = [None, None], []
    for i, p in enumerate((pa, pb)):
        try:
            classes[i] = load(p)
        except Exception as e:
            errors.append(f"{(na, nb)[i]}: {type(e).__name__}: {e}")
    if errors:
        both = classes[0] is None and classes[1] is None
        winner = None if both else (1 if classes[0] is None else 0)
        out = {"winner": winner, "wins": [0, 0], "log": "Forfeit", "error": " | ".join(errors)}
    else:
        wins, logs = [0, 0], []
        for k in range(1, 4):
            w, log = fight(classes[0], classes[1], na, nb)
            if w is not None:
                wins[w] += 1
            logs.append(f"Fight {k}:\n" + "\n".join(log))
        winner = 0 if wins[0] > wins[1] else 1 if wins[1] > wins[0] else None
        out = {"winner": winner, "wins": wins, "log": "\n".join(logs), "error": None}
    print(json.dumps(out))


if __name__ == "__main__":
    main()
