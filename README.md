# ⚔️ Inheritance Arena

Třídní turnaj v Pythonu. Zdědíš si hrdinu (`Warrior`, `Mage` nebo `Archer`), napíšeš mu **strategii** a tvůj hrdina se utká s hrdiny spolužáků. Cílem je procvičit **dědičnost**, `super()` a přepisování metod.

## Jak to funguje

Každý hrdina má dva pevné tahy:

| Tah | Co dělá |
|---|---|
| `"attack"` | základní útok, vždy dostupný |
| `"special"` | speciální schopnost, po použití má cooldown |

Poškození, životy ani schopnosti **měnit nemůžeš**, počítá je arena. Programuješ jen metodu `choose_action(self, enemy)`, která v každém kole rozhodne, jaký tah hrdina použije.

| Hrdina | Speciální schopnost |
|---|---|
| `Warrior` | Shield Bash: zasáhne a zablokuje půlku soupeřova poškození |
| `Mage` | Fireball: obrovské poškození, dlouhý cooldown |
| `Archer` | Double Shot: dva výstřely |

## Jak začít

1. Stáhni si repozitář (**Code → Download ZIP**) a rozbal ho.
2. Otevři `my_hero.py`, přejmenuj třídu a napiš vlastní `choose_action()`. Inspiraci najdeš ve složce `examples/`.
3. Otestuj ho u sebe:
   ```
   py check_hero.py my_hero.py
   ```
   Když se objeví `READY TO UPLOAD`, můžeš nahrávat.
4. Nahraj soubor na **https://dogoslav.pythonanywhere.com**. Zadej název týmu a vlastní **PIN** (budeš ho potřebovat, když budeš chtít nahrát novou verzi).
5. Výsledky sleduj na **/board**.

## Co v souboru smíš a nesmíš

- Povolené importy: `base`, `random`, `math`, `itertools`, `functools`, `collections`, `typing`, `dataclasses`, `enum`, `statistics`.
- Zakázané: `open`, `eval`, `exec`, `getattr`, přístup přes `__class__` a podobné triky. Takový soubor arena odmítne.
- Přepisovat `max_hp`, `basic`, `special` a další pevné hodnoty nelze.

## Soubory

- `my_hero.py` – šablona tvého hrdiny
- `examples/` – tři ukázkoví hrdinové
- `check_hero.py` – lokální test před nahráním
- `base.py`, `match.py`, `safety.py` – pravidla arény (jen čti, neupravuj)
