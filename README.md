# 우아한차트 / Woowa Chart

차트 트레이딩 게임 우아한차트의 한국어·영어 정적 홈페이지입니다. 순수 HTML + 공통 CSS + 작은 JavaScript 파일 두 개로 구성되어 있습니다. 빌드·패키지 설치·외부 라이브러리·CDN·웹 폰트·분석/추적 스크립트가 없습니다.

예정 주소: **https://woowachart.github.io/** · 영어: **https://woowachart.github.io/en/**

현재 로컬 파일만 준비했습니다. 커밋, push, Pages 설정 변경, 배포는 수행하지 않았습니다.

## 로컬 확인

먼저 `py check_site.py`를 실행합니다. Python 표준 라이브러리만 사용해 모든 사이트 HTML의 로컬 링크·앵커·이미지·영상·CSS·JS 경로, CSS 자산 경로, 금지 표현, 게임 분류, 언어 링크와 hreflang, `.gitignore`를 검사합니다. 한국어 페이지는 `ko-` 스크린샷과 `promo_ko` 미디어만, 영어 페이지는 대응하는 영어 파일만 참조해야 합니다. 파일명 기반 검사이며 이미지 속 글자를 OCR로 판독하거나 JavaScript를 실행하는 검사는 아닙니다. 검사 대상은 사이트 HTML/CSS/JS/SVG이며 작업 문서와 인코딩 스크립트는 제외합니다.

PowerShell에서:

```powershell
Set-Location 'C:/00.Workspace/MCP/Codex/08.trading/woowachart-site'
py -m http.server 8765 --bind 127.0.0.1
```

- 한국어: http://127.0.0.1:8765/
- 영어: http://127.0.0.1:8765/en/
- 오류 페이지: http://127.0.0.1:8765/404.html
- 종료: 서버 터미널에서 `Ctrl+C`

두 페이지 상단의 `한국어 | English` 링크와 푸터의 언어 링크를 누르면 `localStorage`의 `woowachart-language`에 `ko` 또는 `en`을 저장합니다. 루트의 `lang.js`는 head 앞에서 동기 실행됩니다. 저장된 선택이 없을 때만 `navigator.languages[0]`, 없으면 `navigator.language`를 확인하고, `ko`로 시작하지 않으면 `location.replace`로 `/en/`으로 이동합니다. 자동 감지 결과 자체는 저장하지 않습니다. `/en/` 직접 방문은 저장된 언어와 무관하게 영어를 유지합니다. 저장소가 차단되면 명시적 선택을 `?lang=ko` 또는 `?lang=en`으로 전달해 한국어 선택이 자동 감지 때문에 되돌아가지 않게 합니다. JavaScript를 꺼도 실제 링크로 두 페이지를 오갈 수 있습니다.

`index.html`을 직접 열어도 기본 내용을 볼 수 있지만, 루트 경로를 사용하는 404 페이지까지 확인하려면 위 HTTP 서버를 사용하세요. Python 기본 서버는 없는 주소에 홈페이지의 `404.html`을 자동 적용하지 않으므로 로컬에서는 `/404.html`을 직접 엽니다. GitHub Pages에서는 배포된 `404.html`을 사용합니다.

확인할 항목:

1. 한국어 ↔ English 전환과 상단 섹션 이동, FAQ 펼치기, 이미지 원본 열기.
2. 320px·390px 모바일과 데스크톱 화면, 운영체제의 밝은/어두운 테마. 테마는 `prefers-color-scheme`으로 자동 적용됩니다.
3. 영상 재생·소리·전체 화면. 자동 재생은 하지 않으며 `preload="metadata"`로 시작합니다.
4. Tab 키로 링크와 FAQ 이동, Enter/Space로 FAQ 조작. 비활성 구매 링크에는 이동할 주소가 없습니다.

## 구매 열기: 한 곳만 수정

`site.js` 상단의 **`PURCHASE_URL` 한 값**에 최종 HTTPS 결제 주소를 넣습니다.

```js
const PURCHASE_URL = ""; // 현재: 비활성
```

빈 문자열이면 두 언어 모두 `곧 열려요 / Coming soon`입니다. HTTPS 주소를 넣으면 두 페이지의 링크가 활성화되고 언어별 결제 문구로 바뀝니다. 결제 준비 중이라는 안내도 함께 숨깁니다. 다시 빈 문자열로 바꾸면 비활성 상태가 됩니다. 현재 결제 업체 호출, 사용자 정보 수집, 결제 실행은 없습니다.

JavaScript를 끈 경우 콘텐츠·메뉴·FAQ·동영상은 사용할 수 있지만 구매 링크는 비활성 상태를 유지합니다.

업데이트의 제공 범위·배포 방식은 미확정이므로 FAQ에서 결제 시작 전 안내 예정으로 표시했습니다. 실제 정책이 확정되면 두 언어 FAQ를 함께 수정하세요.

## 미디어

영상 경로는 고정되어 있습니다. 다음 이름으로 완성 파일을 두면 됩니다. 별도 재인코딩은 하지 않았습니다.

| 파일 | 크기 | 확인된 형식 |
| --- | ---: | --- |
| `media/promo_ko.mp4` | 8,887,888 B | 1280×720, H.264/AAC, 97.185초 |
| `media/promo_en.mp4` | 9,198,430 B | 1280×720, H.264/AAC, 99.276초 |
| `media/promo_ko_poster.jpg` | 139,798 B | 1280×720, 한국어 영상 포스터 |
| `media/promo_en_poster.jpg` | 143,436 B | 1280×720, 영어 영상 포스터 |

두 영상은 사이트 작업 중 기존 인코딩 작업이 완료하여 파일이 도착했습니다. 파일이 없거나 재생 오류가 나면 포스터와 언어별 안내를 유지하도록 했습니다. 인코딩 도구 `media/enc.py`는 기존 파일 그대로 두고 `.gitignore`에서 제외했습니다. `docs/superpowers/`와 `.part.mp4` 등 작업 문서·인코딩 중간 파일도 Git 제외 대상입니다.

스크린샷은 녹화 후보 프레임을 직접 확인한 뒤 FFmpeg로 한 프레임씩 추출했습니다. FFmpeg에서 1280px 폭으로 축소한 뒤 JPEG 인코더의 **품질 80**, 최적화 옵션으로 저장했습니다. 모두 1280×720이며 불필요하게 용량을 늘리지 않아 약 70–149 KiB입니다. UI를 번역·합성하지 않고 각각의 언어 녹화를 사용했습니다.

출처 기준 폴더:

```text
C:/00.Workspace/MCP/Codex/08.trading/WoowaChart-kline/promo/
```

아래 시각은 시장 시각이 아닌 **녹화 파일 시작으로부터의 초**입니다.

| 용도 / 선택 이유 | 한국어 파일 (크기) | 영어 파일 (크기) | 녹화·시점 |
| --- | --- | --- | --- |
| 리플레이: 캔들이 로드된 상태와 재생 조절 막대 | `ko-replay.jpg` (86,338 B) | `en-replay.jpg` (90,968 B) | `rec/replay_line_test.webm`, `rec_en/replay_line_test.webm` · 각 15초 |
| 모의 주문: 오른쪽 주문 패널과 하단 포지션 | `ko-orders.jpg` (96,493 B) | `en-orders.jpg` (97,474 B) | `rec/paper_session.webm`, `rec_en/paper_session.webm` · 각 24초 |
| 리포트: 자산 곡선·손익·최대 낙폭 보고서 | `ko-report.jpg` (79,603 B) | `en-report.jpg` (81,355 B) | `rec/paper_session.webm`, `rec_en/paper_session.webm` · 각 91초 |
| 그리기: 추세선·수평 구간·지표가 함께 보이는 장면 | `ko-drawing.jpg` (104,505 B) | `en-drawing.jpg` (100,099 B) | `rec/draw_plan.webm`, `rec_en/draw_plan.webm` · 각 32초 |
| 8분할: 메뉴를 닫고 여덟 차트가 모두 표시된 장면 | `ko-layouts.jpg` (152,546 B) | `en-layouts.jpg` (138,031 B) | `rec/layout_range.webm`, `rec_en/layout_range.webm` · 각 20초 |
| 1분 봉: 2021-05-19 급락과 거래량이 뚜렷한 장면 | `ko-minute.jpg` (71,993 B) | `en-minute.jpg` (74,261 B) | 아래 crash_1m 파일 · 각 75초 |
| 4분할 강조: 네 코인의 동시 급락과 거래량 | `ko-crash.jpg` (121,822 B) | `en-crash.jpg` (124,508 B) | 아래 split4_crash 파일 · 각 80초 |

스크린샷 저장 위치: `media/shots/`. 하위 폴더 녹화의 정확한 출처:

```text
rec/crash_1m/20261027T041124-4c8455/crash_1m.webm
rec_en/crash_1m/20261030T034956-7cab56/crash_1m.webm
rec/split4_crash/20261027T041750-2e620b/split4_crash.webm
rec_en/split4_crash/20261030T035129-be0313/split4_crash.webm
```

빈 화면, 초기 로딩, 설정·코인 선택 창이 가린 프레임은 제외했습니다. 세션 보고서는 기능 자체를 보여 주기 위해 보고서 창이 열린 프레임을 선택했습니다. 보고서 수치는 모의 매매 예시이며 성과 보장이 아닙니다. 급락 변동률 `−31.5%`는 제공된 홍보 사례로 표시했으며 종가 대비 등 특정 수익률 산식으로 단정하지 않았습니다.

## GitHub Pages 설정 — 사용자 확인 후

1. `woowachart` 계정/조직 아래 **`woowachart.github.io`** 저장소를 사용하면 루트 주소 `https://woowachart.github.io/`를 사용할 수 있습니다. 이 로컬 작업 폴더의 이름은 달라도 됩니다.
2. 파일을 검토한 뒤 사용자가 커밋·push합니다. `index.html`, `en/`, `media/` 등 사이트 파일이 저장소 루트에 있어야 합니다.
3. GitHub 저장소 **Settings → Pages → Build and deployment**에서 **Deploy from a branch**, 배포 브랜치(예: `main`), **`/ (root)`**를 선택하고 저장합니다.
4. `.nojekyll`을 포함하므로 Jekyll 처리 없이 정적 파일을 제공합니다. 별도 빌드 도구나 GitHub Actions 워크플로는 필요 없습니다.
5. 배포가 완료되면 한국어·영어 주소, 영상, 이미지, 존재하지 않는 주소의 404 응답을 확인합니다. HTTPS 적용 상태도 확인합니다.

## 나중에 개인 도메인 연결

기본 `woowachart.github.io` 주소만 사용할 때는 **CNAME 파일을 만들지 않습니다.** 도메인이 정해지면:

1. 저장소의 **Settings → Pages → Custom domain**에 실제 도메인을 입력합니다(예: `example.com`). 루트 **`CNAME`** 파일에는 프로토콜·경로 없이 그 도메인 한 줄만 둡니다. 브랜치 기반 Pages 설정 화면에서 도메인을 저장하면 GitHub가 이 파일을 만들 수 있으므로 로컬 변경과 함께 확인합니다.
2. 도메인 관리 업체의 DNS에서 다음 레코드를 설정합니다.

| 종류 | 이름/호스트 | 값/대상 |
| --- | --- | --- |
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `woowachart.github.io` |

3. DNS 확인과 인증서 발급이 완료되면 Pages에서 **Enforce HTTPS**를 켭니다. `www`와 루트 도메인 모두 정상 연결되는지 확인합니다.
4. 두 언어 HTML의 절대 주소 `canonical`, `hreflang`, `og:url`, `og:image`를 실제 도메인으로 함께 변경합니다. 이미지·CSS·영상·언어 전환은 상대 경로여서 그대로 사용할 수 있습니다.

설정 근거: [GitHub Pages 사용자 지정 도메인 공식 안내](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site). 실제 도메인이 아직 정해지지 않아 현재 CNAME 파일은 없습니다.

## 파일 역할

| 파일 | 역할 |
| --- | --- |
| `index.html` | 한국어 기본 페이지 |
| `en/index.html` | 영어 페이지 |
| `style.css` | 두 언어·404 공통, 반응형 및 시스템 테마 |
| `site.js` | 구매 URL 한 곳과 영상 오류 안내 |
| `favicon.svg` | 초록 캔들 + 노랑 ‘우’ 윤곽선, 폰트 의존 없음 |
| `404.html` | 한국어·영어 홈 복귀 링크 |
| `.nojekyll` | 정적 파일 배포 |
| `.gitignore` | 인코딩 도구·중간 파일 제외 |
| `README.md` | 실행·미디어·배포·도메인 안내 |
| `docs/superpowers/plans/2026-10-30-static-site.md` | 구현·검증 기록 |
| `media/` | 위 영상 2개, 포스터 2개, 스크린샷 14개 |

현재 파일별 바이트 크기는 다음 명령으로 확인할 수 있습니다(`.git`과 로컬 인코더 제외).

```powershell
Get-ChildItem -Recurse -File -Force |
  Where-Object { $_.FullName -notmatch '[\\/]\.git[\\/]' -and $_.Name -ne 'enc.py' } |
  Select-Object @{Name='File';Expression={$_.FullName.Substring($PWD.Path.Length + 1)}}, Length
```

## 검증 기록 / 한계

- 로컬 HTTP에서 두 언어 페이지, 404 문서, CSS, JS, favicon의 HTTP 200 응답을 확인했습니다.
- 이미지·영상·포스터·로컬 링크·섹션 앵커가 존재하며 ID 중복과 누락된 이미지 alt가 없습니다. 로고는 인접한 제품명과 중복 낭독되지 않도록 빈 alt입니다.
- 스크린샷 14개의 1280×720 크기와 200 KiB 미만 용량, 영상 두 개의 H.264/AAC 메타데이터를 확인했습니다.
- 외부 실행 스크립트·스타일·폰트·API 요청 코드가 없습니다. 절대 URL은 검색/공유용 메타데이터에만 있습니다.
- 별도 소스 검토에서 영상의 반응형 높이와 결제 활성화 뒤 남는 준비 중 문구를 찾아 수정했습니다.
- **실제 브라우저 렌더링과 재생 검수는 미완료입니다.** 내장 브라우저 연결 오류와 로컬 Chrome 프로세스 실행 권한 오류로 이 환경에서 확인하지 못했습니다. 모바일 화면, 테마, 키보드 조작, 영상 재생은 위 로컬 확인 방법으로 검토할 수 있습니다.
- GitHub Pages 공개 상태와 실제 결제는 검증 대상이 아닙니다. 배포·결제는 실행하지 않았습니다.

## File sizes (bytes)

| File | Bytes |
| --- | ---: |
| `.gitignore` | 139 |
| `.nojekyll` | 0 |
| `404.html` | 1,334 |
| `docs/superpowers/plans/2026-10-30-static-site.md` | 2,724 |
| `en/index.html` | 14,204 |
| `favicon.svg` | 516 |
| `index.html` | 15,708 |
| `media/promo_en.mp4` | 9,198,430 |
| `media/promo_en_poster.jpg` | 143,436 |
| `media/promo_ko.mp4` | 8,887,888 |
| `media/promo_ko_poster.jpg` | 139,798 |
| `media/shots/en-crash.jpg` | 124,508 |
| `media/shots/en-drawing.jpg` | 100,099 |
| `media/shots/en-layouts.jpg` | 138,031 |
| `media/shots/en-minute.jpg` | 74,261 |
| `media/shots/en-orders.jpg` | 97,474 |
| `media/shots/en-replay.jpg` | 90,968 |
| `media/shots/en-report.jpg` | 81,355 |
| `media/shots/ko-crash.jpg` | 121,822 |
| `media/shots/ko-drawing.jpg` | 104,505 |
| `media/shots/ko-layouts.jpg` | 152,546 |
| `media/shots/ko-minute.jpg` | 71,993 |
| `media/shots/ko-orders.jpg` | 96,493 |
| `media/shots/ko-replay.jpg` | 86,338 |
| `media/shots/ko-report.jpg` | 79,603 |
| `README.md` | 12,308 |
| `site.js` | 860 |
| `style.css` | 14,317 |
