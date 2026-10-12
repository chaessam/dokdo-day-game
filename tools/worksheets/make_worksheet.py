"""독도 원정대 학습지 (A4 2쪽) 만들기. 두 번째 인자로 --answers 를 주면 정답지를 만든다."""
import re
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from common import Builder, U, NAVY, TEAL, TEAL_L, GOLD, GOLD_L, INK, GRAY, LINE, WHITE  # noqa: E402

OUT = sys.argv[1]
ANS = "--answers" in sys.argv[2:]
RED = "#D62828"
B = Builder(footer="기획·제작 채쌤 · AI 수업 아카이브(blog.naver.com/ai_classroom) · 게임: dokdo-day-game.chaessam.workers.dev")
cs, ps = B.cs, B.ps
BLANK = "(" + " " * 9 + ")"     # 답을 쓸 괄호
BLANK_S = "(" + " " * 6 + ")"


def blanks(text, answers, size, color=None, bold=False):
    """괄호 빈칸을 나누어 run 목록으로. 정답지면 빈칸에 빨간 정답을 넣는다."""
    color = color or INK
    it, out = iter(answers), []
    for part in re.split("(" + re.escape(BLANK) + "|" + re.escape(BLANK_S) + ")", text):
        if part in (BLANK, BLANK_S):
            out.append(("( " + next(it) + " )", cs(size, RED, True)) if ANS else (part, cs(size, color, bold)))
        elif part:
            out.append((part, cs(size, color, bold)))
    return out

# ======================= 1쪽 =======================
# 머리 띠
t = B.table(1, 2, [126, 54], [28])
t.set_cell_border_fill(0, 0, B.bf(fill=NAVY))
t.set_cell_border_fill(0, 1, B.bf(fill=TEAL_L))
B.fill(t.cell(0, 0), [
    (ps(line=120), [("10월 25일 독도의 날 · 게임 연계 학습지" + (" · 교사용 정답지" if ANS else ""), cs(9.5, "#FFC56E", True))]),
    (ps(line=105, before=2), [("독도 원정대 학습지", cs(23, WHITE, True))] + ([(" 정답", cs(16, "#FF8A80", True))] if ANS else [])),
    (ps(line=125, before=2), [("게임에서 만난 독도의 자연과 역사, 바닷속 생물을 다시 떠올려 정리해 봐요.", cs(9.5, "#CFE3F5"))]),
], margins={"left": 6, "right": 3, "top": 1.5, "bottom": 1.5})
B.fill(t.cell(0, 1), [
    (ps(line=230), [("(   )학년 (   )반 (   )번", cs(10.5, INK))]),
    (ps(line=150, before=2), [("이름 ", cs(10.5, INK, True)), ("(" + " " * 13 + ")", cs(10.5, INK))]),
], margins={"left": 4.5, "right": 3})
B.gap(3.4)

# 1. 독도는 어떤 섬일까요?
B.section_title(1, "독도는 어떤 섬일까요?", "유리병 기록 · 자연 관찰 노트")
B.gap(1.6)
t = B.table(1, 2, [68, 112], [58], border_fill=B.bf(border=LINE))
img = B.image("r-islands", 62 / 42)
B.picture_in(t.cell(0, 0), img, 62, 42, caption=[
    (ps(align="CENTER", line=120, before=2), [("아리랑 2호 위성에서 내려다본 독도", cs(8.5, INK, True))]),
    (ps(align="CENTER", line=120), [("사진: 한국항공우주연구원 · 공공누리 제1유형", cs(7, GRAY))]),
])
c = t.cell(0, 1)
B.fill(c, [(ps(line=130), [("보기", cs(10, GOLD, True)), ("에서 알맞은 말을 골라 ( ) 안에 써 보세요.", cs(10, INK))])],
       valign="TOP", margins={"left": 3.5, "right": 3, "top": 2.5, "bottom": 2})
bank = c.add_table(1, 1, width=U(104))
bank.cell(0, 0).set_size(height=U(8))
bank.set_cell_border_fill(0, 0, B.bf(fill=GOLD_L, border="#F1D29C"))
B.fill(bank.cell(0, 0), [(ps(align="CENTER", line=100), [("동도 · 서도 · 화산 · 조경수역 · 모래", cs(10.5, GOLD, True))])])
qs = [
    ("①", "독도는 큰 섬 두 개인 " + BLANK_S + "와 " + BLANK_S + ", 그리고 89개의 작은 바위섬으로 이루어져 있어요.", ["동도", "서도"]),
    ("②", "두 섬 가운데 168.5m로 더 높고 뾰족한 섬은 " + BLANK_S + "예요.", ["서도"]),
    ("③", "독도는 약 460만 년 전, 바다 밑에서 " + BLANK_S + "이 터지면서 생긴 섬이에요.", ["화산"]),
    ("④", "차가운 바닷물과 따뜻한 바닷물이 만나 물고기가 많이 모이는 곳을 " + BLANK_S + "이라고 해요.", ["조경수역"]),
]
for n, q, a in qs:
    p = c.add_paragraph(n + " ", para_pr_id_ref=ps(line=140, before=2.6, left=5, indent=-5), char_pr_id_ref=cs(10.5, TEAL, True))
    for t_, c_ in blanks(q, a, 10.5):
        p.add_run(t_, char_pr_id_ref=c_)
B.gap(3.6)

# 2. 독도에 사는 생물
B.section_title(2, "독도에 사는 생물", "사진을 보고 물음에 답해 보세요.")
B.gap(1.6)
t = B.table(2, 3, [60, 60, 60], [40, 31], border_fill=B.bf(border=LINE))
cards = [
    ("r-gull", "괭이갈매기", "‘냐아옹’ 하는 울음소리가 " + BLANK_S + "를 닮아서 괭이갈매기라는 이름이 붙었어요. (‘괭이’는 이 동물의 옛말이에요.)", "kirinzi · CC BY 4.0", ["고양이"]),
    ("r-plants", "가을 바위틈의 꽃", "독도의 날 무렵 바위틈에 피는 연보라색 꽃으로, ‘바닷가에 피는 국화’라는 뜻의 이름은?\n" + BLANK, "국립생태원 · 공공누리 제1유형", ["해국"]),
    ("r-sealion", "강치(바다사자)", "울릉도 사람들은 강치를 " + BLANK_S + "라고 불렀어요. 강치가 떼 지어 쉬던 독도의 바위도 이 이름을 따서 불러요.", "1934년 독도 · 퍼블릭 도메인", ["가제"]),
]
for i, (name, title, q, credit, ans) in enumerate(cards):
    B.picture_in(t.cell(0, i), B.image(name, 56 / 37), 56, 37)
    t.cell(0, i).set_margins(left=U(1), right=U(1), top=U(1), bottom=U(1))
    lines = q.split("\n")
    paras = [(ps(line=125), [(title, cs(10.5, NAVY, True))])]
    n0 = lines[0].count(BLANK) + lines[0].count(BLANK_S)
    paras.append((ps(line=140, before=1.5), blanks(lines[0], ans[:n0], 9.5)))
    for extra in lines[1:]:
        paras.append((ps(align="CENTER", line=140, before=1), blanks(extra, ans[n0:], 9.5)))
    paras.append((ps(line=110, before=1.5), [("사진: " + credit, cs(7, GRAY))]))
    t.set_cell_border_fill(1, i, B.bf(fill="#F7FBFC", border=LINE))
    B.fill(t.cell(1, i), paras, valign="TOP", margins={"left": 3, "right": 2.5, "top": 2.2, "bottom": 1.5})
B.gap(3.6)

# 3. 항해 퀴즈
B.section_title(3, "거센 파도를 넘어라!", "항해 날씨 노트")
B.gap(1.6)
t = B.table(1, 2, [118, 62], [27], border_fill=B.bf(border=LINE))
B.fill(t.cell(0, 0), [
    (ps(line=145), [("높은 파도가 몰려올 때, 배는 파도를 어느 쪽으로 받아야 더 안전할까요? 알맞은 것에 ○ 하세요.", cs(10.5, INK))]),
    (ps(line=150, before=2.5, left=3), [("① 뱃머리(앞쪽)" + (" ← 정답" if ANS else ""), cs(10.5, RED if ANS else NAVY, True)), ("    ", cs(10.5)), ("② 배의 옆구리", cs(10.5, NAVY, True))]),
    (ps(line=150, before=2.5), [("그렇게 생각한 까닭: ", cs(9.5, GRAY)), ("파도를 옆구리로 받으면 배가 크게 기울어 위험해요." if ANS else "_" * 34, cs(9.5, RED, True) if ANS else cs(9.5, LINE))]),
], margins={"left": 4, "right": 3})
t.set_cell_border_fill(0, 1, B.bf(fill=GOLD_L, border=LINE))
B.fill(t.cell(0, 1), [
    (ps(line=135), [("알고 있나요?", cs(9.5, GOLD, True))]),
    (ps(line=140, before=1.5), [("독도 바다는 날씨가 자주 바뀌고 파도가 높아서, 배가 독도 앞까지 갔다가도 그냥 돌아가는 날이 많아요. ‘삼대가 덕을 쌓아야 독도 땅을 밟을 수 있다’는 말이 있을 정도예요.", cs(8.6, INK))]),
], valign="TOP", margins={"left": 3.5, "right": 3, "top": 2.5})

# ======================= 2쪽 =======================
B.page_break()
B.section_title(4, "독도 역사 연표 잇기", "알맞은 사건의 기호를 ( ) 안에 써 보세요.")
B.gap(1.6)
events = [
    ("512", "ㄷ"), ("1454", "ㅁ"), ("1696", "ㄱ"), ("1877", "ㅂ"), ("1900", "ㄴ"), ("1953", "ㄹ"),
]
desc = [
    ("ㄱ", "어부 안용복이 일본에 건너가 “울릉도와 독도는 조선 땅”이라고 따졌어요."),
    ("ㄴ", "대한제국 칙령 제41호: 울도군이 석도(지금의 독도)까지 다스린다고 알렸어요."),
    ("ㄷ", "신라 장군 이사부가 나무 사자를 싣고 가 우산국을 신라 땅으로 만들었어요."),
    ("ㄹ", "울릉도 청년들이 독도의용수비대를 만들어 3년 8개월 동안 독도를 지켰어요."),
    ("ㅁ", "『세종실록』 「지리지」에 독도가 ‘우산’이라는 이름으로 적혔어요."),
    ("ㅂ", "일본 정부(태정관)가 “울릉도와 독도는 일본과 관계없다”라고 문서를 내렸어요."),
]
t = B.table(7, 5, [19, 14, 9, 101, 37], [7] + [10.3] * 6, border_fill=B.bf(border=LINE))
for col, label in enumerate(["연도", "기호", "", "사건", ""]):
    if col < 4:
        t.set_cell_border_fill(0, col, B.bf(fill=NAVY, border=LINE))
        B.fill(t.cell(0, col), [(ps(align="CENTER", line=100), [(label, cs(9.5, WHITE, True))])])
t.set_cell_border_fill(0, 2, B.bf(fill=NAVY, border=LINE))
for r in range(6):
    year = events[r][0]
    t.set_cell_border_fill(r + 1, 0, B.bf(fill=TEAL_L, border=LINE))
    B.fill(t.cell(r + 1, 0), [(ps(align="CENTER", line=100), [(year, cs(12, NAVY, True)), ("년", cs(8.5, NAVY))])])
    B.fill(t.cell(r + 1, 1), [(ps(align="CENTER", line=100), [(("( " + events[r][1] + " )") if ANS else "(   )", cs(11, RED, True) if ANS else cs(11, INK))])])
    sym, text = desc[r]
    t.set_cell_border_fill(r + 1, 2, B.bf(fill=GOLD_L, border=LINE))
    B.fill(t.cell(r + 1, 2), [(ps(align="CENTER", line=100), [(sym, cs(11, GOLD, True))])])
    B.fill(t.cell(r + 1, 3), [(ps(line=125), [(text, cs(9.6, INK))])], margins={"left": 2.5, "right": 2})
photo = t.merge_cells(0, 4, 6, 4)
B.picture_in(photo, B.image("r-decree", 33 / 47, crop_box=(372, 0, 699, 470)), 33, 47, caption=[
    (ps(align="CENTER", line=120, before=1.5), [("대한제국 칙령 제41호", cs(8.3, INK, True))]),
    (ps(align="CENTER", line=120), [("(1900년 10월 25일)", cs(7.5, INK))]),
    (ps(align="CENTER", line=120, before=0.5), [("사진: 퍼블릭 도메인", cs(7, GRAY))]),
])
B.gap(1.8)
B.para([("★ ", cs(10.5, GOLD, True)), ("칙령 제41호가 알려진 날을 기념하는 ‘독도의 날’은 몇 월 며칠일까요? ", cs(10.5, INK)), ("( 10 )월 ( 25 )일" if ANS else "(   )월 (   )일", cs(10.5, RED if ANS else NAVY, True))], ps(line=130, left=1))
B.gap(3.6)

# 5. 독도 바닷속 탐험
B.section_title(5, "독도 바닷속 탐험", "바닷속 관찰 노트 · 맞으면 O, 틀리면 X")
B.gap(1.6)
t = B.table(1, 3, [60, 60, 60], [39], border_fill=B.bf(border=LINE))
sea = [
    ("sea-fish", "혹돔", "Totti · CC BY-SA 4.0"),
    ("r-sea", "도화새우 (독도새우)", "Daiju Azuma · CC BY-SA 2.5"),
    ("sea-urchin", "성게가 해조류를 먹어 치운 바다", "Shaun Lee · CC BY 4.0"),
]
for i, (name, cap, credit) in enumerate(sea):
    t.cell(0, i).set_margins(left=U(1), right=U(1), top=U(1), bottom=U(0.8))
    B.picture_in(t.cell(0, i), B.image(name, 56 / 27), 56, 27, caption=[
        (ps(align="CENTER", line=115, before=1), [(cap, cs(8.5, INK, True))]),
        (ps(align="CENTER", line=110), [("사진: " + credit, cs(6.8, GRAY))]),
    ])
B.gap(1.4)
ox = [
    "혹돔은 다 자라면 이마에 혹이 크게 튀어나와서 ‘혹돔’이라는 이름이 붙었어요.",
    "서해에서 많이 잡히는 대하도 독도새우 가운데 하나예요.",
    "해삼은 바닥의 찌꺼기를 먹고 깨끗한 모래를 내보내서 ‘바다의 청소부’라고 불려요.",
    "전복은 작은 물고기를 잡아먹고 살아요.",
    "바다 숲이 사라지고 바위가 하얗게 변하는 일을 ‘썰물’이라고 해요.",
]
OX_ANS = ["O", "X", "O", "X", "X"]
OX_FIX = ["", "독도새우는 도화새우·닭새우·꽃새우", "", "해조류를 먹어요", "‘갯녹음’이에요"]
t = B.table(len(ox), 3, [9, 147, 24], [8.6] * len(ox), border_fill=B.bf(border=LINE))
for r, s in enumerate(ox):
    t.set_cell_border_fill(r, 0, B.bf(fill=TEAL, border=LINE))
    B.fill(t.cell(r, 0), [(ps(align="CENTER", line=100), [(str(r + 1), cs(10, WHITE, True))])])
    fix = OX_FIX[r] if ANS else ""
    B.fill(t.cell(r, 1), [(ps(line=120), [(s, cs(10, INK))] + ([(" → " + fix, cs(9, RED, True))] if fix else []))], margins={"left": 3})
    B.fill(t.cell(r, 2), [(ps(align="CENTER", line=100), [(OX_ANS[r], cs(14, RED, True)) if ANS else ("O  X", cs(11, GRAY, True))])])
B.gap(3.6)

# 6. 독도 지킴이 다짐
B.section_title(6, "나는 독도 지킴이!", "생각 쓰기", color=GOLD)
B.gap(1.6)
t = B.table(1, 1, [180], [37], border_fill=B.bf(border=LINE))
B.fill(t.cell(0, 0), [
    (ps(line=140), [("게임에서 바다 쓰레기를 주웠던 것처럼, 독도와 독도 바다를 지키기 위해 ", cs(10.3, INK)), ("내가 할 수 있는 일", cs(10.3, NAVY, True)), ("을 써 보세요.", cs(10.3, INK))]),
] + ([
    (ps(line=140, before=3), [("예시 답안 (학생마다 다를 수 있어요)", cs(9, GRAY, True))]),
    (ps(line=140, before=1.5), [("· 바닷가와 바다에 쓰레기를 버리지 않고, 보이는 쓰레기는 주워요.", cs(10, RED, True))]),
    (ps(line=140, before=1), [("· 독도의 역사와 자연을 바르게 알고 친구와 가족에게 알려요.", cs(10, RED, True))]),
    (ps(line=140, before=1), [("· 10월 25일 독도의 날을 기억하고 독도에 관심을 가져요.", cs(10, RED, True))]),
] if ANS else [
    (ps(line=100, before=6.5), [("_" * 92, cs(9.5, LINE))]),
    (ps(line=100, before=6.5), [("_" * 92, cs(9.5, LINE))]),
    (ps(line=100, before=6.5), [("_" * 92, cs(9.5, LINE))]),
]), valign="TOP", margins={"left": 4, "right": 3, "top": 3, "bottom": 2})

rep = B.save(OUT)
print("validate:", getattr(rep, "ok", rep))
B.report(OUT)
