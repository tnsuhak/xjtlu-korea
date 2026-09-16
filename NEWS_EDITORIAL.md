# XJTLU Korea 뉴스 운영 규칙

XJTLU Korea의 뉴스는 XJTLU 공식 발표를 한국 학생·학부모 관점에서 선별·재구성하는 review-first 콘텐츠입니다.

## 기본 원칙

- 공식 XJTLU 뉴스 상세 페이지를 1차 출처로 사용합니다.
- 한국 학생에게 입학, 장학금, 학비, 전공, 진로, 국제학생 생활, 한국 관련 협력 측면에서 실질적 가치가 있는 항목만 게시합니다.
- 원문을 그대로 복사하거나 단순 번역하지 않고 한국 독자가 이해하기 쉬운 독창적 요약·해설로 작성합니다.
- 기사에는 공식 원문 링크와 원문 게시일을 유지합니다.
- 개인 학생·졸업생 사례는 자동 게시 대상에서 제외합니다.
- 기본 이미지 정책은 `none`입니다. 뉴스 이미지를 임의로 복사해 사용하지 않습니다.
- Apply, How to apply, Application Portal 같은 직접지원 링크는 뉴스 기사에도 기본적으로 넣지 않습니다.

## 게시 흐름

공식 소스 감지 → 중복/가치 판단 → 한국어 편집 → feature branch → Pull Request / Deploy Preview → 검토 → 승인 후 production 반영 순서로 운영합니다.

GitHub Actions는 **트리거된 feature branch 안에서만** 정적 뉴스 파일을 렌더링하고 커밋합니다. `main`으로 자동 병합하거나 Production을 자동 배포하지 않습니다.

## 현재 구조

- 데이터: `news/news-data.json`
- 뉴스 목록: `/news/`
- 개별 기사: `/news/<slug>.html`
- 홈페이지: 공식 원문 게시일 기준 최신 4건 노출
- sitemap: 뉴스 목록과 개별 기사 URL 자동 반영
- 렌더러: `scripts/render_news.py`
- 현재 홈페이지/메뉴 호환 패치: `scripts/integrate_news.py`

전공 관련 내부 링크는 현재 분리된 `xjtlu-undergraduate-programmes.html`과 `xjtlu-graduate-destinations-careers.html`을 사용합니다.
