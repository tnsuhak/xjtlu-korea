import json
from pathlib import Path

DATA = Path('news/news-data.json')

SUMMARIES = {
    'class-of-2026-dual-degree-graduation': (
        'XJTLU는 2026년 여름 졸업식에서 총 4,816명의 졸업생을 배출했습니다. 이 가운데 학부 졸업생 3,797명은 XJTLU 학위와 함께 영국 리버풀대학교 학사 학위를 받았고, 1,244명은 리버풀대학교 기준 First Class Honours로 졸업했습니다. 한국 학생과 학부모 입장에서는 XJTLU의 복수학위 구조가 실제 졸업 때 어떻게 적용되는지 확인할 수 있는 가장 직접적인 사례입니다. 다만 복수학위와 중국 2년+영국 2년의 2+2 과정은 같은 개념이 아니므로 전공별 2+2 가능 여부는 별도로 확인해야 합니다.'
    ),
    'xjtlu-seoul-suwon-un-habitat-smart-city-report': (
        'XJTLU와 서울대학교가 중심이 되어 수원특례시의 스마트도시 정책을 분석한 국제 공동연구가 공개됐습니다. UN-Habitat, 수원시정연구원, 수원특례시도 참여했으며, 단순히 스마트 기술을 많이 도입했는지가 아니라 그 기술이 시민의 생활을 실제로 개선했는지를 평가하는 방법을 제시했습니다. 쉽게 말하면 교통·공공서비스·도시 데이터 같은 기술이 주민에게 실제 도움이 되는지를 측정하는 연구입니다. 도시계획·건축·스마트시티 분야를 생각하는 학생에게는 XJTLU Design School이 한국 대학과 국제기구, 실제 도시와 함께 연구하는 방식을 보여주는 사례입니다.'
    ),
    'xjtlu-pusan-national-fuel-cell-research': (
        '수소차 연료전지에는 반응을 빠르게 하기 위해 백금 촉매가 많이 쓰이는데, 백금은 가격이 비싸다는 단점이 있습니다. XJTLU와 부산대학교 연구진은 더 저렴한 코발트·탄소 소재가 백금을 대체할 가능성이 있는지 공동으로 연구했고, 이론 계산과 실제 실험을 함께 진행했습니다. XJTLU는 계산과 모델링을, 부산대는 실험 검증을 맡아 서로 다른 연구 역량을 결합했습니다. 아직 바로 상용화된 기술이라는 뜻은 아니지만, 재료과학·화학·에너지 분야에서 XJTLU와 한국 대학의 공동연구가 실제 논문 성과로 이어진 사례라는 점에서 의미가 있습니다.'
    ),
    'xjtlu-suwon-city-mou-sustainable-urban-collaboration': (
        'XJTLU와 수원특례시는 2025년 교육·연구·산업 협력을 확대하기 위한 MOU를 체결했습니다. 협력 분야에는 AI, 바이오, IT, 도시계획과 지속가능한 도시개발이 포함되며, 공동연구와 인재양성 프로그램을 함께 추진하는 방향이 제시됐습니다. 수원에서 XJTLU 관련 교육 프로그램이나 연구센터를 운영할 가능성도 논의됐지만, 한국 캠퍼스나 학위과정이 확정된 것은 아닙니다. 한국 학생 입장에서는 XJTLU가 한국 지방자치단체와 단순 교류를 넘어 연구·교육 협력을 넓히고 있다는 점을 보여주는 소식으로 볼 수 있습니다.'
    ),
    'xjtlu-dgist-student-exchange-research-partnership': (
        'DGIST 대표단이 XJTLU를 방문해 학생·교수 교류와 공동연구 확대 방안을 논의했습니다. 주요 협력 분야로 AI, 생명과학, 재료과학, 환경과학 등이 언급됐고, 공동논문·공동연구비 신청·세미나 같은 연구 협력도 함께 검토됐습니다. 당시 단계는 학생교류 프로그램이 이미 시작된 것이 아니라 향후 공식 MOU 체결과 구체적인 협력 제도를 추진하기로 한 수준입니다. 이공계 학생에게는 XJTLU가 한국의 연구중심 대학과 어떤 분야에서 연결되고 있는지 확인할 수 있는 사례입니다.'
    ),
    'xjtlu-suwon-smart-inclusive-transition-forum-2026': (
        'XJTLU Design School 대표단이 2026년 4월 한국 수원에서 열린 스마트도시 포럼에 참가해 서울대학교·수원시정연구원·UN-Habitat와 진행한 공동연구 결과를 발표했습니다. 연구의 핵심은 스마트 기술 도입 자체보다 그 기술이 시민의 생활과 도시 운영을 실제로 얼마나 개선하는지 평가하는 것입니다. 이는 2025년 XJTLU와 수원특례시가 체결한 MOU가 단순 협약에 그치지 않고 실제 공동연구와 현지 행사로 이어진 후속 사례입니다. 도시계획·건축·디자인·스마트시티 분야에 관심 있는 학생이라면 XJTLU의 한국 연계 연구 활동을 이해하는 데 도움이 됩니다.'
    ),
    'xjtlu-kentech-energy-materials-research-talent-development': (
        'XJTLU는 한국에너지공과대학교(KENTECH)와 에너지 소재 분야의 공동연구와 전문인력 양성을 위한 협력관계를 맺었습니다. 에너지 소재는 배터리, 에너지 저장장치, 친환경 에너지 기술의 성능을 좌우하는 핵심 분야로, 양 기관은 이 분야의 연구 역량을 연결하는 것을 목표로 하고 있습니다. XJTLU는 부산대학교의 연료전지 촉매 연구 등 다른 한국 기관과도 에너지·재료 분야 협력을 이어오고 있습니다. 다만 협약 자체가 학생 개인의 교환학생이나 인턴십을 자동으로 보장하는 것은 아니며, 구체적인 학생 참여 프로그램은 별도 발표를 확인해야 합니다.'
    ),
    'xjtlu-aiat-aolns-restructured-academies-2026': (
        'XJTLU가 2026년 9월 학부 조직을 크게 개편했습니다. AI·컴퓨터·소프트웨어·전자전기·통신 분야는 새 Academy of AI and Advanced Technology(AIAT) 안에 묶고, 생명과학·화학·재료·약학·바이오·디지털헬스 분야는 Academy of Life and Natural Sciences(AoLNS)로 통합했습니다. 쉽게 말하면 서로 가까운 전공들을 한 조직 안에 모아 수업과 연구를 더 연결하려는 변화입니다. 2027학년도 지원자는 전공이 없어졌다고 이해하기보다 희망 전공의 새 소속과 커리큘럼, 학위명, 2+2 가능 여부가 어떻게 정리됐는지를 확인하는 것이 중요합니다.'
    ),
}


def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    changed = False
    for item in data.get('items', []):
        new_summary = SUMMARIES.get(item.get('id'))
        if new_summary and item.get('summary') != new_summary:
            item['summary'] = new_summary
            changed = True
    if changed:
        data['updated_at'] = '2026-09-17'
        DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('updated' if changed else 'already current')


if __name__ == '__main__':
    main()
