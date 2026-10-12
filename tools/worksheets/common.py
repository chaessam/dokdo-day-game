"""독도 원정대 학습지·문제 모음집 공통 도우미 (python-hwpx)."""
import io
import os
import warnings

from PIL import Image
from hwpx import HwpxDocument

warnings.filterwarnings("ignore", category=DeprecationWarning)

PHOTOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "photos") + os.sep
HP = "{http://www.hancom.co.kr/hwpml/2011/paragraph}"
FONT = "함초롬돋움"

NAVY = "#0F2A4A"
TEAL = "#138A99"
TEAL_L = "#E3F4F6"
GOLD = "#C9781A"
GOLD_L = "#FFF4DE"
INK = "#1E2933"
GRAY = "#6B7785"
LINE = "#BFD3DC"
WHITE = "#FFFFFF"


def U(mm):
    return int(round(mm * 7200 / 25.4))


class Builder:
    def __init__(self, footer=None):
        self.doc = HwpxDocument.new()
        self.doc.set_page_setup(paper_size="A4", margins_mm={"left": 15, "right": 15, "top": 12, "bottom": 10, "header": 0, "footer": 9})
        self.header = self.doc.headers[0]
        self._cs, self._ps, self._bf = {}, {}, {}
        if footer:
            f = self.doc.set_footer_text(footer)
            for fp in f.paragraphs:
                fp.para_pr_id_ref = self.ps(align="CENTER", line=100)
                for run in fp.runs:
                    run.char_pr_id_ref = self.cs(size=7.5, color=GRAY)
        # 맨 위 구역 정의 문단은 아주 작게 (빈 줄 높이를 줄인다)
        p0 = self.doc.paragraphs[0]
        p0.para_pr_id_ref = self.ps(line=100)
        for run in p0.runs:
            run.char_pr_id_ref = self.cs(size=2)

    # ---- 글자·문단·테두리 모양 ----
    def cs(self, size=10.5, color=INK, bold=False):
        key = (size, color, bold)
        if key not in self._cs:
            self._cs[key] = self.doc.ensure_run_style(bold=bold, size=size, color=color, font=FONT)
        return self._cs[key]

    def ps(self, align="LEFT", line=150, before=0.0, after=0.0, left=0.0, indent=0.0):
        key = (align, line, before, after, left, indent)
        if key not in self._ps:
            m = {"prev": int(before * 100), "next": int(after * 100), "left": U(left), "intent": U(indent)}
            self._ps[key] = self.header.ensure_paragraph_format(alignment=align, line_spacing_percent=line, margins=m)
        return self._ps[key]

    def bf(self, fill=None, border=None, width="0.12 mm", sides=None, kind="SOLID"):
        key = (fill, border, width, tuple(sides) if sides is not None else None, kind)
        if key not in self._bf:
            kw = {"border_color": border or "#FFFFFF", "border_width": width, "border_type": kind}
            if fill:
                kw["fill_color"] = fill
            kw["active_borders"] = list(sides) if sides is not None else ([] if border is None else None)
            if kw["active_borders"] is None:
                del kw["active_borders"]
            self._bf[key] = self.doc.ensure_border_fill(**kw)
        return self._bf[key]

    # ---- 그림 ----
    def image(self, name, aspect, crop_box=None, max_w=900):
        """사진을 칸 비율(가로/세로)에 맞게 가운데 자르고 줄여서 넣는다."""
        im = Image.open(PHOTOS + name + ".jpg").convert("RGB")
        if crop_box:
            im = im.crop(crop_box)
        w, h = im.size
        if w / h > aspect:
            nw = int(h * aspect); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else:
            nh = int(w / aspect); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        if im.width > max_w:
            im = im.resize((max_w, int(max_w / aspect)), Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=84, optimize=True, progressive=False)
        return self.doc.add_image(buf.getvalue(), "jpg")

    # ---- 본문 ----
    def para(self, runs, ps=None):
        """runs: [(글자, 글자모양id)] 를 가진 본문 문단."""
        first_text, first_cs = runs[0]
        p = self.doc.add_paragraph(first_text, char_pr_id_ref=first_cs, para_pr_id_ref=ps or self.ps(), inherit_style=False)
        for t, c in runs[1:]:
            p.add_run(t, char_pr_id_ref=c)
        return p

    def gap(self, mm):
        """mm 높이의 빈 줄(작은 글자, 줄간격 100%)."""
        size = max(1.0, mm / 0.3528 / 1.0)
        return self.para([("", self.cs(size=round(min(size, 30), 1)))], self.ps(line=100))

    def page_break(self):
        p = self.gap(0.8)
        idx = len(self.doc.paragraphs) - 1
        self.doc.set_paragraph_format(paragraph_index=idx, page_break_before=True)
        return p

    def table(self, rows, cols, widths_mm, heights_mm=None, border_fill=None):
        t = self.doc.add_table(rows, cols, width=U(sum(widths_mm)), border_fill_id_ref=border_fill or self.bf())
        t.set_column_widths(widths_mm)
        if heights_mm:
            for r, h in enumerate(heights_mm):
                for c in range(cols):
                    try:
                        t.cell(r, c).set_size(height=U(h))
                    except Exception:
                        pass
            sz = t.element.find(f"{HP}sz")
            if sz is not None:
                sz.set("height", str(U(sum(heights_mm))))
        return t

    @staticmethod
    def valign(cell, v="CENTER"):
        sub = cell.element.find(f"{HP}subList")
        if sub is not None:
            sub.set("vertAlign", v)

    def fill(self, cell, paras, valign="CENTER", margins=None):
        """paras: [(문단모양id, [(글자, 글자모양id), ...]), ...] 를 칸에 채운다."""
        if margins:
            cell.set_margins(**{k: U(v) for k, v in margins.items()})
        first = cell.paragraphs[0]
        for i, (ps, runs) in enumerate(paras):
            if i == 0:
                p = first
                p.para_pr_id_ref = ps
                for run in list(p.runs):
                    try:
                        run.text = ""
                    except Exception:
                        pass
                if p.runs:
                    p.runs[0].text = runs[0][0]
                    p.runs[0].char_pr_id_ref = runs[0][1]
                    rest = runs[1:]
                else:
                    rest = runs
            else:
                p = cell.add_paragraph(runs[0][0], para_pr_id_ref=ps, char_pr_id_ref=runs[0][1])
                rest = runs[1:]
            for t, c in rest:
                p.add_run(t, char_pr_id_ref=c)
        self.valign(cell, valign)
        return cell

    def picture_in(self, cell, image_id, w_mm, h_mm, caption=None, valign="CENTER"):
        p = cell.paragraphs[0]
        p.para_pr_id_ref = self.ps(align="CENTER", line=100)
        p.add_picture(image_id, width=U(w_mm), height=U(h_mm), treat_as_char=True)
        if caption:
            for ps, runs in caption:
                q = cell.add_paragraph(runs[0][0], para_pr_id_ref=ps, char_pr_id_ref=runs[0][1])
                for t, c in runs[1:]:
                    q.add_run(t, char_pr_id_ref=c)
        self.valign(cell, valign)

    def section_title(self, num, text, sub=None, color=NAVY):
        t = self.table(1, 2, [10, 170], [8.2])
        t.set_cell_border_fill(0, 0, self.bf(fill=color))
        t.set_cell_border_fill(0, 1, self.bf(fill=TEAL_L))
        self.fill(t.cell(0, 0), [(self.ps(align="CENTER", line=100), [(str(num), self.cs(12.5, WHITE, True))])], margins={"left": 0.5, "right": 0.5, "top": 0.3, "bottom": 0.3})
        runs = [(text, self.cs(12.5, NAVY, True))]
        if sub:
            runs.append(("   " + sub, self.cs(9, GRAY)))
        self.fill(t.cell(0, 1), [(self.ps(line=100, left=1), runs)], margins={"left": 2.5, "right": 2, "top": 0.3, "bottom": 0.3})
        return t

    def report(self, path):
        from hwpx.layout.pages import estimate_pages
        e = estimate_pages(path)
        body = 297 - 12 - 10 - 9
        print("pages:", e.pages, "unsupported:", e.unsupported)
        for i, ln in enumerate(e.lines):
            l = ln[0]
            print(f"  #{i:02d} p{l.page + 1} {l.vertpos * 25.4 / 7200:6.1f}mm")
        return e

    def save(self, path):
        rep = self.doc.validate()
        self.doc.save_to_path(path)
        return rep
