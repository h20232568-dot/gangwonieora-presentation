"""강원이어라 포스터 초안 (A3 세로) 생성기
- 손 윤곽선 없이, 고충 문장과 데이터 수치의 배치만으로 손 모양을 만든다 (clipPath로 손 모양 안에만 글자를 둔다).
- 대각선 구도: 왼쪽 아래에서 청년 창업자 손, 오른쪽 위에서 건물주 손이 뻗어 가운데에서 손끝이 만난다.
- 손 안 글자는 팔 방향으로 기울이고, 검지에는 대표 수치를 크게 넣는다.
- 대각선이 만드는 빈 삼각형에 글자를 둔다: 제목은 왼쪽 위, 설명은 오른쪽 아래.
- 손끝 사이 빈틈에 '강원 / 이어라' 타이틀.
출력: poster.svg (A3 297×420mm, viewBox 1188×1680 = 1mm당 4단위)
"""
import io
import math
import sys
import qrcode
import qrcode.image.svg

W, H = 1188, 1680
OUT = sys.argv[1] if len(sys.argv) > 1 else "poster.svg"
SITE = "https://gangwonieora-presentation.vercel.app/"

# 오른쪽을 가리키는 손 (손등이 위, 검지를 뻗고 나머지 손가락은 가볍게 굽힘). 손목 쪽 x=0, 손끝 ≈ (698,160)
HAND = (
    "M0,125 C120,118 250,114 330,118 "     # 팔 윗선
    "C390,110 440,102 478,108 "            # 손등 → 검지 뿌리
    "C540,118 620,134 680,146 "            # 검지 윗선
    "C696,149 700,170 682,173 "            # 손끝
    "C625,171 565,167 515,164 "            # 검지 아랫선
    "C530,176 532,206 512,214 "            # 중지
    "C520,226 508,244 486,242 "            # 약지
    "C486,254 470,264 450,258 "            # 새끼
    "C420,256 380,246 340,236 "            # 손바닥 아래
    "C230,228 120,230 0,233 Z"             # 팔 아랫선
)
DETAILS = [
    "M372,214 C420,200 470,186 510,177 C519,175 522,169 515,164",  # 엄지
    "M512,214 C500,205 494,192 498,180",                          # 중지 마디
    "M486,242 C474,232 470,222 474,210",                          # 약지 마디
    "M664,150 C673,152 677,159 675,166",                          # 손톱
    "M478,108 C484,118 486,130 484,140",                          # 검지 뿌리 마디
]
TIP = (698, 160)
FINGER_MID = (565, 147)   # 검지 가운데(대표 수치 자리)
BACK_MID = (300, 176)     # 손목 쪽(짧은 설명 자리)

S = 1.75       # 손 크기
ANG = 50       # 대각선 각도(도). 클수록 가파르다
CX, CY = W / 2, 760   # 두 손끝 사이 한가운데
GAP = 200      # 가운데에서 각 손끝까지 거리
C, SN = math.cos(math.radians(ANG)), math.sin(math.radians(ANG))
LTIP = (CX - GAP * C, CY + GAP * SN)   # 청년 창업자 손끝
RTIP = (CX + GAP * C, CY - GAP * SN)   # 건물주 손끝


def tf_left():
    return f"translate({LTIP[0]:.1f},{LTIP[1]:.1f}) rotate({-ANG}) scale({S}) translate({-TIP[0]},{-TIP[1]})"


def tf_right():
    return f"translate({RTIP[0]:.1f},{RTIP[1]:.1f}) scale(-1,1) rotate({ANG}) scale({S}) translate({-TIP[0]},{-TIP[1]})"


def to_global(pt, side):
    """손 좌표 → 포스터 좌표"""
    x, y = (pt[0] - TIP[0]) * S, (pt[1] - TIP[1]) * S
    if side == "L":
        a = math.radians(-ANG)
        return (LTIP[0] + x * math.cos(a) - y * math.sin(a), LTIP[1] + x * math.sin(a) + y * math.cos(a))
    a = math.radians(ANG)
    gx, gy = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
    return (RTIP[0] - gx, RTIP[1] + gy)


# 손 안을 채울 말: (설명, 수치). 수치는 크고 굵게, 설명은 작게. 수치가 None이면 고충 문장
YOUTH = [
    ("강원 20대 순유출", "11,916명"), ("보증금이 너무 커요", None), ("30세 미만 창업", "−6.6%"),
    ("창업 장애 1위 자금 확보", "53.7%"), ("1년 계약은 부담돼요", None), ("실패 두려움", "45.9%"),
    ("강원 창업기업", "31,886개"), ("딱 2주만 해 보고 싶어요", None), ("전년 대비", "−4.5%"),
    ("원하는 지원: 공간", "54.5%"), ("실패하면 어떡하죠", None), ("신생기업 5년 생존율", "36.5%"),
    ("같은 기간 전 연령 순유출", "1,991명"), ("공간은 어디서 찾죠", None),
]
OWNER = [
    ("춘천 명동 공실률", "27.0%"), ("다음 임차인은 언제 올까", None), ("강원 중대형 공실률", "19.3%"),
    ("전국과의 격차", "12.7%p"), ("비어 있는 동안 수입이 없어요", None), ("투자수익률", "0.15%"),
    ("자본수익률", "−0.57%"), ("짧게 빌려줬다가 망가지면요?", None), ("원주 중앙·일산", "36.8%"),
    ("빌딩 거래", "약 30%↓"), ("단기 계약은 번거로워요", None), ("3분기 거래", "129건"),
    ("명동 2021 → 2026", "18.5→27.0%"), ("불 꺼진 1층이 늘어요", None),
]
# 검지(대표 수치)와 손목 쪽(짧은 설명)
YOUTH_KEY = ("11,916명", "")
OWNER_KEY = ("27.0%", "")


def text_rows(items, x0, y0, y1, color, seed):
    """회전 전 좌표계에서 빈틈없이 채운다.
    작은 줄 두 줄(설명+수치, 같은 크기) 다음에 수치만 큰 줄 한 줄이 오는 리듬.
    글자가 작고 촘촘할수록 손 모양 가장자리가 또렷해진다."""
    rows, y, k, line = [], y0, seed, 0
    while y < y1:
        big = (line % 3 == 2)
        parts = []
        if big:
            size = 34
            y += size - 2
            for n in range(26):
                label, num = items[(k + n) % len(items)]
                if num:
                    parts.append(f'<tspan font-weight="900">{num}</tspan>')
            body = '<tspan fill-opacity="0.35"> · </tspan>'.join(parts)
        else:
            size = 15
            y += size + 1
            for n in range(40):
                label, num = items[(k + n) % len(items)]
                if num:
                    parts.append(f'<tspan font-weight="600" fill-opacity="0.8">{label} </tspan><tspan font-weight="900">{num}</tspan>')
                else:
                    parts.append(f'<tspan font-weight="500" fill-opacity="0.7">“{label}”</tspan>')
            body = " ".join(parts)
        rows.append(f'<text x="{x0:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" letter-spacing="-0.3">{body}</text>')
        k += 2
        line += 1
    return "\n".join(rows)


def key_number(side, key, color, fill):
    """검지 안에 대표 수치를 크게, 손목 쪽에 짧은 설명 (팔 방향으로 기울임, 바탕색 테두리로 또렷하게)."""
    fx, fy = to_global(FINGER_MID, side)
    bx, by = to_global(BACK_MID, side)
    halo = f'stroke="{fill}" stroke-width="5" stroke-linejoin="round" paint-order="stroke"'
    return (f'<text x="{fx:.1f}" y="{fy:.1f}" transform="rotate({-ANG} {fx:.1f} {fy:.1f})" text-anchor="middle" '
            f'dominant-baseline="central" font-size="64" font-weight="900" fill="{color}" {halo}>{key[0]}</text>'
            f'<text x="{bx:.1f}" y="{by:.1f}" transform="rotate({-ANG} {bx:.1f} {by:.1f})" text-anchor="middle" '
            f'dominant-baseline="central" font-size="26" font-weight="800" fill="{color}" {halo}>{key[1]}</text>')


def qr_svg(url, x, y, size):
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=0)
    buf = io.BytesIO(); img.save(buf)
    s = buf.getvalue().decode()
    path = s[s.index("<path"):s.index("/>", s.index("<path")) + 2]
    n = float(s[s.index('viewBox="') + 9:].split('"')[0].split()[2])
    return f'<g transform="translate({x},{y}) scale({size / n})">{path.replace("<path", "<path fill=\"#191F28\"")}</g>'


NAVY, BLUE, INK, GLOW, PAPER = "#0F3D6E", "#3182F6", "#191F28", "#FFD66B", "#F7F5F0"
FILL_L, FILL_R = "#E8F1FF", "#E3EAF3"   # 손 바탕색 (배경과 구분)
FONT = "'Pretendard', 'NanumSquare', 'Noto Sans KR', 'Apple SD Gothic Neo', sans-serif"
details = "".join(f'<path d="{d}"/>' for d in DETAILS)
outline = f'fill="none" stroke="{INK}" stroke-width="{5 / S:.2f}" stroke-linejoin="round"'
detail_style = f'fill="none" stroke="{INK}" stroke-width="{2.6 / S:.2f}" stroke-linecap="round" stroke-opacity="0.6"'
LC = to_global((330, 175), "L")   # 글자 회전 기준점
RC = to_global((330, 175), "R")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="297mm" height="420mm" viewBox="0 0 {W} {H}" font-family="{FONT}">
<defs>
  <path id="hand" d="{HAND}"/>
  <clipPath id="clipL"><use href="#hand" transform="{tf_left()}"/></clipPath>
  <clipPath id="clipR"><use href="#hand" transform="{tf_right()}"/></clipPath>
  <radialGradient id="glow" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="{GLOW}" stop-opacity="0.95"/>
    <stop offset="0.45" stop-color="{GLOW}" stop-opacity="0.42"/>
    <stop offset="1" stop-color="{GLOW}" stop-opacity="0"/>
  </radialGradient>
</defs>
<rect width="{W}" height="{H}" fill="{PAPER}"/>

<!-- 왼쪽 위 빈 삼각형: 제목 -->
<text x="90" y="170" font-size="32" font-weight="700" fill="{INK}" fill-opacity="0.55" letter-spacing="1">빈 상가와 청년 사이</text>
<text x="90" y="262" font-size="82" font-weight="800" fill="{INK}">손끝</text>
<text x="90" y="352" font-size="82" font-weight="800" fill="{INK}">하나의 거리</text>

<!-- 손끝 사이 빛 -->
<ellipse cx="{CX}" cy="{CY}" rx="320" ry="300" fill="url(#glow)"/>

<!-- 왼쪽 아래: 청년 창업자 손 -->
<g clip-path="url(#clipL)">
  <g transform="rotate({-ANG} {LC[0]:.1f} {LC[1]:.1f})">{text_rows(YOUTH, LC[0] - 1300, LC[1] - 260, LC[1] + 260, BLUE, 0)}</g>
  {key_number("L", YOUTH_KEY, BLUE, PAPER)}
</g>

<!-- 오른쪽 위: 건물주 손 -->
<g clip-path="url(#clipR)">
  <g transform="rotate({-ANG} {RC[0]:.1f} {RC[1]:.1f})">{text_rows(OWNER, RC[0] - 700, RC[1] - 260, RC[1] + 260, NAVY, 2)}</g>
  {key_number("R", OWNER_KEY, NAVY, PAPER)}
</g>

<!-- 손끝 사이 타이틀 -->
<text x="{CX}" y="{CY - 8}" text-anchor="middle" font-size="72" font-weight="800" fill="{INK}">강원</text>
<text x="{CX}" y="{CY + 68}" text-anchor="middle" font-size="72" font-weight="800" fill="{INK}">이어라</text>

<!-- 손 이름표: 각 손끝 옆 빈 삼각형 -->
<text x="{LTIP[0] + 90:.0f}" y="{LTIP[1] + 60:.0f}" font-size="30" font-weight="800" fill="{BLUE}">청년 창업자</text>
<text x="{LTIP[0] + 90:.0f}" y="{LTIP[1] + 94:.0f}" font-size="21" fill="{INK}" fill-opacity="0.6">작게, 먼저 해 보고 싶은</text>
<text x="{RTIP[0] - 90:.0f}" y="{RTIP[1] - 70:.0f}" text-anchor="end" font-size="30" font-weight="800" fill="{NAVY}">건물주</text>
<text x="{RTIP[0] - 90:.0f}" y="{RTIP[1] - 36:.0f}" text-anchor="end" font-size="21" fill="{INK}" fill-opacity="0.6">다음 임차인을 기다리는</text>

<!-- 오른쪽 아래 빈 삼각형: 설명 -->
<text x="{W - 90}" y="1250" text-anchor="end" font-size="40" font-weight="800" fill="{INK}">비어 있는 기간을 잇습니다</text>
<text x="{W - 90}" y="1302" text-anchor="end" font-size="23" fill="{INK}" fill-opacity="0.7">다음 임차인을 기다리는 빈 상가를</text>
<text x="{W - 90}" y="1336" text-anchor="end" font-size="23" fill="{INK}" fill-opacity="0.7">하루~4주 단위로 청년 창업자에게</text>
<text x="{W - 90}" y="1370" text-anchor="end" font-size="23" fill="{INK}" fill-opacity="0.7">AI 공간 진단 · 한 줄 요청 · 제안서 작성까지</text>

{qr_svg(SITE, W - 90 - 130, 1430, 130)}
<text x="{W - 90 - 150}" y="1470" text-anchor="end" font-size="30" font-weight="800" fill="{INK}">강원이어라</text>
<text x="{W - 90 - 150}" y="1502" text-anchor="end" font-size="18" fill="{INK}" fill-opacity="0.65">강원 원도심 빈 상가 × 청년 창업 단기 공간 매칭</text>
<text x="{W - 90 - 150}" y="1530" text-anchor="end" font-size="16" fill="{INK}" fill-opacity="0.55">gangwonieora-presentation.vercel.app</text>
<text x="{W - 90}" y="1620" text-anchor="end" font-size="13" fill="{INK}" fill-opacity="0.5">출처: 한국부동산원 상업용부동산 임대동향(보도 인용, 2026 · 명동 27.0%는 상가 유형 추정), 강원연구원(2026),</text>
<text x="{W - 90}" y="1642" text-anchor="end" font-size="13" fill="{INK}" fill-opacity="0.5">중소벤처기업부·창업기업실태조사·한국경제인협회(전국 수치), 부동산플래닛. 손 안의 문장은 예상되는 고충을 표현한 것입니다.</text>
</svg>
'''
open(OUT, "w", encoding="utf-8").write(svg)
print("wrote", OUT)
