# Сборка страницы из базы ~/.claude/znaniya/hormozi: python3 build.py (нужен пакет markdown)
import os, re, html, markdown

BAZA = os.path.expanduser("~/.claude/znaniya/hormozi")
HERE = os.path.dirname(os.path.abspath(__file__))

def md(path, drop_first_h1=True):
    t = open(os.path.join(BAZA, path), encoding="utf-8").read()
    if drop_first_h1:
        t = re.sub(r"^# .*\n", "", t, count=1)
    # служебные строки для агента – не для человека
    t = "\n".join(l for l in t.split("\n") if not l.lstrip("-* ").startswith(("Подробно:", "Правило чтения", "«Подробно")))
    return markdown.markdown(t, extensions=["tables", "sane_lists"])

def agents_table():
    t = open(os.path.join(BAZA, "gotovye-agenty-razbor.md"), encoding="utf-8").read()
    part = t.split("## 1.")[1].split("## 2.")[0]
    part = re.sub(r"(github\.com/[\w./-]+)", r"[\1](https://\1)", part)
    weak = t.split("## 3.")[1].split("## 4.")[0]
    return markdown.markdown("## 1." + part, extensions=["tables"]), markdown.markdown("## 3." + weak)

books = [
    ("offers", "Книга 1. 100M Offers – оффер, от которого трудно отказаться", "shpargalka-offers.md"),
    ("leads", "Книга 2. 100M Leads – откуда брать клиентов и как делать рекламу", "shpargalka-leads.md"),
    ("money", "Книга 3. 100M Money Models – как заработать больше с каждого клиента", "shpargalka-money.md"),
    ("ru", "Перенос на Россию – закон и площадки", "perenos-rossiya.md"),
]
tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
sections = ""
for sid, title, f in books:
    sections += f'<section id="{sid}"><details><summary><h2>{html.escape(title)}</h2><span>развернуть</span></summary><div class="md">{md(f)}</div></details></section>\n'
best, weak = agents_table()
audio = ""
if os.path.exists(os.path.join(HERE, "itog.mp3")):
    audio = '<div class="audio"><b>▶ Послушать итог голосом</b><audio controls preload="none" src="itog.mp3"></audio></div>'
out = tpl.replace("{{AUDIO}}", audio).replace("{{BOOKS}}", sections).replace("{{AGENTS}}", best).replace("{{AGENTS_WEAK}}", weak)
out = out.replace("—", "–")
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(out)
print("index.html", len(out))
