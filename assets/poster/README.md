# 강원이어라 포스터 (A3 세로)

천지창조 구도를 빌려, 청년 창업자의 손(왼쪽 아래)과 건물주의 손(오른쪽 위)이 손끝을 마주하는 포스터입니다.
손은 선으로만 그리고, 손 안은 각자의 고충 문장과 관련 수치로 채웠습니다. 손끝 사이에 '강원 / 이어라' 타이틀이 들어갑니다.

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
- `YOUTH`, `OWNER`: 손 안 문장과 수치 (`1`이면 굵게)
- `YOUTH_KEY`, `OWNER_KEY`: 검지에 크게 넣는 대표 수치
- `HAND`: 손 윤곽선 경로(코드로 그린 초안). 최종본은 디자인 도구로 다시 그리는 것을 권장합니다.
  손 안 글자는 이 윤곽으로 잘라내는(clipPath) 구조라, 윤곽을 바꾸면 글자도 따라갑니다.

## 주의
- 명동 27.0%는 보도에 상가 유형이 없어 중대형으로 추정한 값입니다. 출처 줄에 표시되어 있습니다.
- 자금 확보 53.7%, 실패 두려움 45.9%, 30세 미만 창업 −6.6%는 전국 수치입니다.
- 글꼴은 Pretendard → 나눔스퀘어 → Noto Sans KR 순으로 지정되어 있습니다. 컴퓨터에 있는 글꼴에 따라 모양이 달라질 수 있습니다.
