"""독도 원정대 게임 문제 모음집 (정답·해설) + 학습지 정답."""
import json
import re
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from common import Builder, U, NAVY, TEAL, TEAL_L, GOLD, GOLD_L, INK, GRAY, LINE, WHITE  # noqa: E402

OUT, QUIZ = sys.argv[1], sys.argv[2]
D = json.load(open(QUIZ, encoding="utf-8"))
strip = lambda s: re.sub(r"<[^>]+>", "", s or "")

B = Builder(footer="기획·제작 채쌤 · AI 수업 아카이브(blog.naver.com/ai_classroom) · 게임: dokdo-day-game.chaessam.workers.dev")
cs, ps = B.cs, B.ps
CIRC = ["①", "②", "③", "④"]

# 머리 띠
t = B.table(1, 1, [180], [24])
t.set_cell_border_fill(0, 0, B.bf(fill=NAVY))
B.fill(t.cell(0, 0), [
    (ps(line=120), [("10월 25일 독도의 날 · 교사용 자료", cs(9.5, "#FFC56E", True))]),
    (ps(line=110, before=2), [("독도 원정대 문제 모음집", cs(21, WHITE, True)), (" 정답과 해설", cs(12, "#CFE3F5", True))]),
    (ps(line=130, before=2), [("게임에 나오는 퀴즈 19문제를 모두 모았어요. 게임에서는 보기 순서가 매번 바뀌어요.", cs(9.3, "#CFE3F5"))]),
], margins={"left": 6, "right": 4, "top": 1.5, "bottom": 1.5})
B.gap(3.5)

counter = [0]


def quiz_table(items):
    """items: [(출처 위 줄, 출처 아래 줄, quiz)]"""
    widths = [9, 30, 72, 25, 44]
    t = B.table(len(items) + 1, 5, widths, [7.5] + [15] * len(items), border_fill=B.bf(border=LINE))
    t.set_treat_as_char(False)
    t.element.set("repeatHeader", "1")
    for col, label in enumerate(["번호", "게임 속 기록", "문제와 보기", "정답", "해설"]):
        t.set_cell_border_fill(0, col, B.bf(fill=NAVY, border=LINE))
        B.fill(t.cell(0, col), [(ps(align="CENTER", line=100), [(label, cs(9, WHITE, True))])])
    for r, (top, sub, q) in enumerate(items, start=1):
        counter[0] += 1
        n = counter[0]
        opts = list(q["a"])
        ans = q["c"]
        if n % 2 == 0 and len(opts) == 2:     # 정답이 늘 ①이 되지 않게 짝수 번은 보기 순서를 바꾼다
            opts = opts[::-1]
            ans = 1 - ans
        shade = "#F7FBFC" if r % 2 == 0 else None
        for col in range(5):
            t.set_cell_border_fill(r, col, B.bf(fill=shade, border=LINE) if shade else B.bf(border=LINE))
        t.set_cell_border_fill(r, 0, B.bf(fill=TEAL_L, border=LINE))
        B.fill(t.cell(r, 0), [(ps(align="CENTER", line=100), [(str(n), cs(11, NAVY, True))])])
        B.fill(t.cell(r, 1), [
            (ps(line=118), [(top, cs(9.2, NAVY, True))]),
            (ps(line=118, before=0.8), [(sub, cs(8, GRAY))]),
        ], margins={"left": 2, "right": 1.5})
        B.fill(t.cell(r, 2), [
            (ps(line=128), [(q["q"], cs(9.6, INK, True))]),
            (ps(line=128, before=1.2), [(" ".join(f"{CIRC[i]} {o}" for i, o in enumerate(opts)), cs(9.3, INK))]),
        ], margins={"left": 2.5, "right": 2})
        B.fill(t.cell(r, 3), [(ps(align="CENTER", line=125), [(f"{CIRC[ans]} {opts[ans]}", cs(9.6, GOLD, True))])], margins={"left": 1.5, "right": 1.5})
        B.fill(t.cell(r, 4), [(ps(line=125), [(strip(q["why"]), cs(8.6, INK))])], margins={"left": 2, "right": 1.5})
    return t


def heading(num, title, sub, color=NAVY):
    B.section_title(num, title, sub, color=color)
    B.gap(1.6)


# 1. 유리병 속 기록
heading(1, "유리병 속 기록", "울릉도에서 독도로 가는 항해 중 건지는 유리병 12개")
items = []
for i, r in enumerate(D["RECORDS"]):
    unit = r.get("unit", "년" if r["kind"] == "history" else "")
    year = r["year"] + ("년" if r["kind"] == "history" else "")
    items.append((f"유리병 {i + 1} · {year}", r["title"], r["quiz"]))
quiz_table(items)
B.gap(3.5)

# 2. 항해 날씨 노트 (새 쪽에서 시작)
B.page_break()
heading(2, "항해 날씨 노트", "항해 중 풍랑주의보를 만나면 나오는 문제")
w = D["WEATHER"]
quiz_table([("풍랑주의보", w["title"], w["quiz"])])
B.gap(3.5)

# 3. 바닷속 관찰 노트
heading(3, "바닷속 관찰 노트", "독도 바닷속 잠수 탐사에서 생물을 찾으면 나오는 문제")
quiz_table([(f"바닷속 {i + 1} · {r['year']}", r["title"], r["quiz"]) for i, r in enumerate(D["SEA"])])
B.gap(3.5)

# 4. 학습지 정답
heading(4, "학습지 정답", "「독도 원정대 학습지」 2쪽짜리 학생용 활동지의 정답", color=GOLD)
ans = [
    ("1. 독도는 어떤 섬일까요?", "① 동도, 서도 (순서는 바뀌어도 돼요) ② 서도 ③ 화산 ④ 조경수역"),
    ("2. 독도에 사는 생물", "괭이갈매기: 고양이 · 가을 바위틈의 꽃: 해국 · 강치: 가제 (가제바위)"),
    ("3. 거센 파도를 넘어라!", "① 뱃머리(앞쪽) 까닭 예시: 파도를 옆구리로 받으면 배가 크게 기울어 위험하고, 뱃머리로 파도를 가르며 넘어야 안전해요."),
    ("4. 독도 역사 연표 잇기", "512-ㄷ 1454-ㅁ 1696-ㄱ 1877-ㅂ 1900-ㄴ 1953-ㄹ ★ 10월 25일"),
    ("5. 독도 바닷속 탐험", "1. O 2. X (대하는 서해에서 많이 잡히는 새우) 3. O 4. X (해조류를 먹어요) 5. X (갯녹음)"),
    ("6. 나는 독도 지킴이!", "예시: 바닷가와 바다에 쓰레기를 버리지 않고 주워요. 독도의 역사와 자연을 바르게 알고 친구와 가족에게 알려요. 10월 25일 독도의 날을 기억해요."),
]
t = B.table(len(ans), 2, [44, 136], [11] * len(ans), border_fill=B.bf(border=LINE))
for r, (k, v) in enumerate(ans):
    t.set_cell_border_fill(r, 0, B.bf(fill=GOLD_L, border=LINE))
    B.fill(t.cell(r, 0), [(ps(line=120), [(k, cs(9.6, GOLD, True))])], margins={"left": 3, "right": 2})
    B.fill(t.cell(r, 1), [(ps(line=135), [(v, cs(9.6, INK))])], margins={"left": 3, "right": 2})

rep = B.save(OUT)
print("validate:", getattr(rep, "ok", rep))
B.report(OUT)
