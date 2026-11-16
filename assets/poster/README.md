# 강원이어라 포스터 (A3 세로)

천지창조 구도를 빌려, 청년 창업자의 손(왼쪽 아래)과 건물주의 손(오른쪽 위)이 손끝을 마주하는 포스터입니다.
손 윤곽선 없이, 각자의 고충 문장과 데이터 수치의 배치만으로 손 모양을 만들었습니다(손 모양 clipPath 안에만 글자를 채움). 손끝 사이에 '강원 / 이어라' 타이틀이 들어갑니다.

## 파일
| 파일 | 내용 |
|---|---|
| `make_poster.py` | 포스터 SVG를 만드는 스크립트. 문구·수치·각도·색을 여기서 바꿉니다 |
| `render.js` | SVG를 PNG(미리보기)와 A3 PDF로 렌더링 (Playwright) |
| `poster.svg` | 편집용 원본. Figma·일러스트레이터에서 열 수 있습니다 |
| `poster.png`, `poster.pdf` | 미리보기, A3 인쇄용 |

## 다시 만들기
```bash
python3 -m pip install qrcode
python3 make_poster.py poster.svg
node render.js poster.svg poster.png poster.pdf 2
```
`render.js`는 Playwright(`npm i playwright` 후 `npx playwright install chromium`)가 필요합니다.

## 자주 바꾸는 값 (`make_poster.py`)
- `ANG`: 대각선 각도(기본 50°), `S`: 손 크기, `GAP`: 손끝 사이 거리
- `YOUTH`, `OWNER`: 손 안을 채울 (설명, 수치) 목록. 수치가 `None`이면 고충 문장으로 들어갑니다
- `YOUTH_KEY`, `OWNER_KEY`: 검지에 크게 넣는 대표 수치
- `HAND`: 손 모양 경로(화면에 선으로 그리지 않고, 글자를 채울 영역으로만 씀). 이 경로를 바꾸면 글자로 된 손 모양이 따라 바뀝니다.

## 주의
- 명동 27.0%는 보도에 상가 유형이 없어 중대형으로 추정한 값입니다. 출처 줄에 표시되어 있습니다.
- 자금 확보 53.7%, 실패 두려움 45.9%, 30세 미만 창업 −6.6%는 전국 수치입니다.
- 글꼴은 Pretendard → 나눔스퀘어 → Noto Sans KR 순으로 지정되어 있습니다. 컴퓨터에 있는 글꼴에 따라 모양이 달라질 수 있습니다.
