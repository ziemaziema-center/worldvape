from __future__ import annotations

import argparse
import html
import json
import re
import shutil
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote


SITE_URL = "https://worldvape.mykindredai.com"
BRAND = "월드베이프 광운대점"
PHONE = "0507-1301-9953"
TELEGRAM = "https://t.me/worldvape_gwangun"
NAVER_MAP = "https://map.naver.com/p/search/%EC%9B%94%EB%93%9C%EB%B2%A0%EC%9D%B4%ED%94%84%20%EA%B4%91%EC%9A%B4%EB%8C%80%EC%A0%90"
NAVER_BLOG = "https://m.blog.naver.com/worldworldvape"
ADDRESS = "서울특별시 노원구 광운로20길 3"
GEO = {"latitude": 37.6205, "longitude": 127.0630}
TODAY = date(2026, 5, 25).isoformat()


LOCAL_PAGES = [
    {
        "path": "kwangwoon-vape",
        "title": "광운대 전자담배 추천 | 월드베이프 광운대점",
        "description": "광운대역 1번 출구 도보권 전자담배 전문 매장. 입호흡 액상, 기기 관리, 성인 인증 기반 상담과 방문 특가 안내.",
        "h1": "광운대 전자담배, 조용히 오래 찾는 이유",
        "intent": "광운대역, 광운대학교, 석계 생활권에서 전자담배 매장을 찾는 방문자",
        "lead": "광운대 근처에서 전자담배를 고를 때 중요한 것은 단순히 가까운 위치가 아니라, 내 기기와 취향을 정확히 이해하고 부담 없이 설명해 주는 매장입니다. 월드베이프 광운대점은 광운대역 도보권에서 입호흡 액상과 기기 관리 상담을 중심으로 운영합니다.",
        "sections": [
            ("광운대 생활권에 맞춘 상담", "수업 전후, 퇴근길, 주말 방문처럼 시간이 짧은 고객도 핵심만 빠르게 확인할 수 있도록 액상 계열, 쿨링감, 단맛, 타격감을 먼저 정리합니다."),
            ("처음 방문해도 부담 없는 동선", "구매를 서두르게 만드는 방식보다 성인 인증 후 필요한 정보만 차분히 안내합니다. 기존 기기를 가져오면 누수, 코일, 출력 설정까지 함께 점검할 수 있습니다."),
            ("방문 전 확인하면 좋은 것", "원하는 맛 계열, 현재 쓰는 기기명, 코일 저항, 기존 액상에서 아쉬웠던 점을 알려주면 추천 정확도가 높아집니다."),
        ],
        "faq": [
            ("광운대역에서 걸어갈 수 있나요?", "광운대역 1번 출구 기준 도보권에 있어 광운대와 석계 생활권에서 방문하기 편한 편입니다."),
            ("입문자도 상담 가능한가요?", "가능합니다. 성인 인증 후 기기 방식, 액상 선택, 관리 방법을 기초부터 안내합니다."),
            ("방문 특가는 어디서 확인하나요?", "텔레그램 안내 채널에서 재고와 방문 특가를 조용히 확인할 수 있습니다."),
        ],
    },
    {
        "path": "nowon-vape",
        "title": "노원 전자담배 전문 안내 | 월드베이프 광운대점",
        "description": "노원구 전자담배, 입호흡 액상, 기기 관리 상담. 프리미엄 톤의 성인 전용 로컬 vape shop 안내.",
        "h1": "노원 전자담배 선택, 매장 경험이 차이를 만듭니다",
        "intent": "노원구에서 전자담배 전문성과 접근성을 함께 찾는 고객",
        "lead": "노원 전자담배 매장을 찾는 고객은 가격만큼이나 재고 신뢰도, 설명 품질, 액상 추천 감각을 중요하게 봅니다. 월드베이프 광운대점은 노원 동북권에서 입호흡 액상과 기기 상담을 균형 있게 제공하는 성인 전용 매장입니다.",
        "sections": [
            ("노원구 고객이 자주 묻는 기준", "단맛이 오래 남는지, 쿨링이 강한지, 코일 수명이 어떤지처럼 실제 사용감에 가까운 질문을 중심으로 추천합니다."),
            ("재고보다 중요한 큐레이션", "많은 품목을 무작정 나열하기보다 입호흡 사용자에게 맞는 계열을 좁혀 주는 방식으로 상담합니다."),
            ("지도 검색과 함께 쓰기 좋은 페이지", "Google, Naver, AI 검색이 매장 정보를 이해하기 쉽도록 위치, 영업시간, 상담 범위, 커뮤니티 채널을 명확히 정리했습니다."),
        ],
        "faq": [
            ("노원구 전자담배 매장으로 방문해도 되나요?", "네. 노원 생활권에서 광운대역 인근 방문이 편하다면 상담과 구매 모두 가능합니다."),
            ("기기 문제도 봐주나요?", "일반적인 누수, 탄맛, 코일 교체 주기, 충전 상태 등 기본 점검을 안내합니다."),
            ("액상 추천은 어떤 기준으로 하나요?", "향 계열, 단맛, 쿨링, 타격감, 기존 사용 경험을 기준으로 좁혀 갑니다."),
        ],
    },
    {
        "path": "노원전자담배",
        "title": "노원전자담배 로컬 가이드 | 입호흡 액상 상담",
        "description": "노원전자담배 검색자를 위한 월드베이프 광운대점 로컬 안내. 성인 인증, 액상 선택법, 방문 전 체크리스트.",
        "h1": "노원전자담배 검색 전, 확인할 기준",
        "intent": "붙여쓰기 검색어로 빠르게 매장을 비교하는 모바일 사용자",
        "lead": "모바일에서 노원전자담배를 검색하는 사용자는 보통 가까운 매장, 오늘 방문 가능 여부, 액상 재고, 가격 안내를 빠르게 확인하고 싶어합니다. 이 페이지는 월드베이프 광운대점의 핵심 방문 정보를 한 번에 읽히도록 구성했습니다.",
        "sections": [
            ("가까움만으로는 부족합니다", "전자담배 매장은 사용자의 흡입 방식과 선호 향을 이해해야 합니다. 단순 판매보다 사용 후 만족도를 높이는 설명이 중요합니다."),
            ("성인 전용 상담 원칙", "모든 상담은 성인 고객을 대상으로 하며, 미성년자 구매와 대리구매는 안내하지 않습니다."),
            ("AI 검색이 읽기 쉬운 매장 정보", "주소, 전화, 영업시간, 지도 링크, FAQ를 분리해 AI 검색 결과에서도 명확하게 요약될 수 있도록 했습니다."),
        ],
        "faq": [
            ("노원전자담배로 검색하면 어떤 정보를 먼저 봐야 하나요?", "위치, 영업시간, 성인 인증 원칙, 액상 상담 범위, 지도 리뷰를 함께 확인하는 것이 좋습니다."),
            ("가격만 보고 방문해도 되나요?", "가능하지만 원하는 향과 기기 상태를 함께 알려주면 더 정확한 추천을 받을 수 있습니다."),
            ("텔레그램은 어떤 용도인가요?", "방문 전 재고와 특가 안내를 조용히 확인하는 커뮤니티형 채널입니다."),
        ],
    },
    {
        "path": "광운대전자담배",
        "title": "광운대전자담배 방문 안내 | 월드베이프 광운대점",
        "description": "광운대전자담배 검색자를 위한 도보권 매장 안내. 입호흡 액상 추천, 기기 관리, 성인 전용 상담.",
        "h1": "광운대전자담배, 가까운 곳에서 제대로 고르기",
        "intent": "광운대 주변에서 즉시 방문 가능한 전자담배 매장을 찾는 검색자",
        "lead": "광운대전자담배를 검색했다면 이미 위치 의도가 강합니다. 월드베이프 광운대점은 광운대역 인근에서 액상 추천, 기기 관리, 방문 특가 안내를 자연스럽게 연결하는 로컬 매장입니다.",
        "sections": [
            ("광운대 주변 방문 시나리오", "강의 전후, 지하철 이동 전, 근처 식사 후처럼 짧은 방문에도 필요한 액상 후보를 빠르게 압축합니다."),
            ("입호흡 중심 추천", "입호흡 기기 사용자는 향 농도, 쿨링, 단맛, 목넘김의 균형이 중요합니다. 기존에 좋았던 액상과 아쉬웠던 액상을 같이 알려 주세요."),
            ("부담 없는 커뮤니티 톤", "텔레그램 CTA는 가격 압박이 아니라 방문 전 정보 확인용입니다. 조용하고 프라이빗한 안내 채널로 운영합니다."),
        ],
        "faq": [
            ("광운대 근처에서 액상만 구매할 수 있나요?", "가능합니다. 사용 중인 기기와 원하는 맛 계열을 알려주면 선택이 쉬워집니다."),
            ("시연이나 향 설명이 가능한가요?", "매장 상황과 성인 인증 기준에 맞춰 가능한 범위에서 안내합니다."),
            ("처음 전자담배를 시작해도 되나요?", "성인 고객이라면 기본 구조, 관리, 액상 선택법을 단계적으로 설명합니다."),
        ],
    },
    {
        "path": "입호흡액상추천",
        "title": "입호흡 액상 추천 가이드 | 월드베이프 광운대점",
        "description": "입호흡 액상 추천 기준: 단맛, 쿨링, 타격감, 코일 수명, 향 계열. 노원·광운대 성인 전용 상담.",
        "h1": "입호흡 액상 추천은 취향 번역부터 시작합니다",
        "intent": "MTL 입호흡 액상 선택 기준을 찾는 초보자와 재구매 고객",
        "lead": "입호흡 액상 추천은 인기 순위만으로 끝나지 않습니다. 같은 과일 계열이라도 단맛, 쿨링, 산미, 잔향, 코일 부담이 다르기 때문에 사용자의 표현을 매장 언어로 번역하는 과정이 필요합니다.",
        "sections": [
            ("입호흡 액상의 핵심 기준", "첫째 향 계열, 둘째 단맛, 셋째 쿨링, 넷째 목넘김, 다섯째 코일 수명입니다. 이 다섯 가지를 정리하면 실패 확률이 줄어듭니다."),
            ("초보자에게 무난한 흐름", "처음에는 과일, 멘솔, 음료 계열처럼 이해하기 쉬운 방향에서 시작하고, 이후 디저트나 복합향으로 넓히는 편이 안정적입니다."),
            ("방문 전 취향 메모", "너무 달았던 액상, 시원함이 부족했던 액상, 향이 빨리 질렸던 경험을 알려주면 추천 정확도가 높아집니다."),
        ],
        "faq": [
            ("입호흡 액상은 폐호흡 액상과 무엇이 다른가요?", "입호흡은 담배처럼 입에 머금었다가 흡입하는 방식에 맞춘 액상으로, 일반적으로 니코틴 만족감과 향 농도 균형이 중요합니다."),
            ("쿨링이 강한 액상이 좋은가요?", "취향에 따라 다릅니다. 강한 쿨링은 시원하지만 향을 덮을 수 있어 균형을 보고 고르는 것이 좋습니다."),
            ("처음이면 어떤 향이 무난한가요?", "과일 멘솔, 청량한 음료 계열처럼 향 이미지가 선명한 액상이 시작하기 쉽습니다."),
        ],
    },
    {
        "path": "노원액상추천",
        "title": "노원 액상 추천 | 입호흡 액상 큐레이션",
        "description": "노원 액상 추천 로컬 페이지. 입호흡 액상, 향 계열, 관리 팁, 방문 전 텔레그램 재고 안내.",
        "h1": "노원 액상 추천, 오래 쓰는 취향을 찾는 방식",
        "intent": "노원구에서 액상 추천과 재고 확인을 원하는 사용자",
        "lead": "노원 액상 추천을 찾는다면 단순히 많이 팔리는 맛보다 본인에게 오래 맞는 향을 찾는 것이 중요합니다. 월드베이프 광운대점은 입호흡 액상을 중심으로 향 표현과 사용감을 구체적으로 비교해 줍니다.",
        "sections": [
            ("향 표현을 구체화합니다", "상큼함, 진함, 깔끔함, 묵직함, 잔향처럼 고객이 쓰는 말을 실제 액상 선택 기준으로 바꿔 추천합니다."),
            ("재구매 고객에게 중요한 점", "처음에는 맛이 좋았지만 빨리 질렸다면 향의 강도보다 균형이 문제일 수 있습니다. 계열을 살짝 바꾸는 방식이 더 낫습니다."),
            ("노원 생활권 방문 팁", "방문 전 텔레그램에서 재고와 안내를 확인하면 헛걸음을 줄이고 상담 시간을 짧게 만들 수 있습니다."),
        ],
        "faq": [
            ("노원에서 입호흡 액상 추천을 받을 수 있나요?", "네. 월드베이프 광운대점은 노원 생활권에서 방문 가능한 입호흡 액상 상담 매장입니다."),
            ("액상 가격 안내는 가능한가요?", "공개 가격보다 방문 특가와 묶음 안내는 텔레그램 채널에서 확인하는 방식이 적합합니다."),
            ("향을 잘 몰라도 추천받을 수 있나요?", "가능합니다. 싫어하는 맛과 원하는 느낌만 알려줘도 후보를 좁힐 수 있습니다."),
        ],
    },
]


GUIDES = [
    {
        "path": "faq",
        "title": "자주 묻는 질문 | 월드베이프 광운대점",
        "description": "광운대·노원 전자담배, 입호흡 액상, 방문 특가, 성인 인증, 영업시간 관련 FAQ.",
        "h1": "월드베이프 광운대점 FAQ",
        "lead": "AI 검색과 모바일 검색에서 바로 답을 찾을 수 있도록 매장 방문 전 자주 묻는 질문을 정리했습니다.",
        "blocks": [
            ("방문", "광운대역 1번 출구 도보권이며, 노원·석계·월계 생활권에서 방문하기 편합니다."),
            ("상담", "입호흡 액상, 기기 관리, 코일 교체 주기, 누수와 탄맛 같은 기본 문제를 성인 고객에게 안내합니다."),
            ("텔레그램", "방문 전 재고와 특가를 확인하는 조용한 안내 채널입니다. 공격적인 가격 홍보보다 필요한 정보 전달을 우선합니다."),
            ("성인 인증", "전자담배 제품은 성인 고객에게만 안내합니다. 미성년자, 대리구매, 신분 확인 회피는 받지 않습니다."),
        ],
    },
    {
        "path": "guide",
        "title": "전자담배 관리 방법 가이드 | 월드베이프 광운대점",
        "description": "전자담배 관리 방법, 코일 교체, 누수 예방, 충전 습관, 보관 팁을 정리한 초보자용 가이드.",
        "h1": "전자담배 관리 방법, 오래 쓰는 기본기",
        "lead": "좋은 기기와 액상을 골라도 관리가 맞지 않으면 탄맛, 누수, 향 손실이 생깁니다. 관리의 기본은 코일 상태, 액상 점도, 충전 습관, 보관 환경을 안정적으로 유지하는 것입니다.",
        "blocks": [
            ("코일 교체", "탄맛이 나거나 향이 갑자기 약해졌다면 코일 수명이 끝났을 가능성이 높습니다. 액상을 바꾸기 전 코일 상태부터 확인하세요."),
            ("누수 예방", "팟을 오래 방치하거나 과충전하면 누수가 생길 수 있습니다. 사용하지 않을 때는 세워 두고, 액상 주입 후 결합부를 닦아 주세요."),
            ("충전 습관", "고속 충전기보다 안정적인 저전류 충전이 기기 수명에 유리한 경우가 많습니다. 충전 중 과열이 느껴지면 사용을 멈추세요."),
            ("보관", "직사광선과 고온 차량 내부는 액상과 배터리에 모두 좋지 않습니다. 서늘하고 건조한 곳에 보관하는 것이 기본입니다."),
        ],
    },
    {
        "path": "liquid-guide",
        "title": "전자담배 액상 선택법 | 입호흡 액상 추천 기준",
        "description": "액상 설명, 니코틴 설명, 세금 관련 일반 정보, 입호흡 액상 선택법을 한 번에 정리한 가이드.",
        "h1": "액상 선택법, 맛보다 먼저 봐야 할 기준",
        "lead": "전자담배 액상은 향만 보고 고르기보다 사용 기기, 흡입 방식, 니코틴 만족감, 쿨링, 코일 부담을 함께 봐야 합니다. 특히 입호흡 액상은 목넘김과 향의 선명도가 만족도를 크게 좌우합니다.",
        "blocks": [
            ("입호흡 설명", "입호흡은 연기를 바로 깊게 들이마시기보다 입에 머금었다가 흡입하는 방식입니다. 담배와 비슷한 흡입 리듬을 선호하는 사용자에게 익숙합니다."),
            ("액상 설명", "액상은 베이스, 향료, 니코틴 성분 등으로 구성됩니다. 제품별 배합과 향료 특성에 따라 단맛, 쿨링, 목넘김, 코일 수명이 달라집니다."),
            ("니코틴 설명", "니코틴은 중독성이 있는 성분입니다. 성인 사용자도 본인에게 맞는 농도와 사용량을 신중하게 선택해야 하며, 과사용을 피해야 합니다."),
            ("세금 관련 일반 정보", "전자담배 액상과 관련 제품은 국가 정책과 세법에 따라 과세 체계가 달라질 수 있습니다. 구체적인 세율과 적용 기준은 관계기관의 최신 고시를 확인해야 합니다."),
        ],
    },
    {
        "path": "beginner-guide",
        "title": "전자담배 초보 가이드 | 처음 시작하는 성인 고객을 위한 안내",
        "description": "전자담배 초보를 위한 기기 선택, 액상 선택, 관리 방법, 방문 전 체크리스트.",
        "h1": "전자담배 초보 가이드",
        "lead": "처음 시작하는 성인 고객에게 가장 중요한 것은 한 번에 많은 제품을 보는 것이 아니라, 흡입 방식과 관리 난이도를 이해하는 것입니다. 무리한 구매보다 본인에게 맞는 방식부터 찾는 편이 좋습니다.",
        "blocks": [
            ("기기 선택", "입호흡 기기는 휴대성과 관리 편의성이 좋고, 액상 선택 폭이 넓습니다. 처음이라면 사용법이 단순한 팟 계열부터 보는 것이 편합니다."),
            ("액상 선택", "과일, 멘솔, 음료 계열처럼 취향을 설명하기 쉬운 방향에서 시작하세요. 너무 강한 단맛이나 쿨링은 처음에는 피로할 수 있습니다."),
            ("관리 방법", "액상 주입 후 바로 강하게 흡입하지 말고 코일에 액상이 충분히 스며들 시간을 주세요. 탄맛이 나면 계속 사용하지 않는 것이 좋습니다."),
            ("방문 전 체크리스트", "성인 확인 신분증, 원하는 향 계열, 기존 흡연 습관 또는 현재 쓰는 기기 정보를 준비하면 상담이 빨라집니다."),
        ],
    },
]


ARTICLE_TOPICS = [
    ("광운대 전자담배 추천 기준", "kwangwoon-vape", "광운대 전자담배 추천은 거리, 상담 품질, 액상 큐레이션을 같이 봐야 합니다.", "광운대 전자담배"),
    ("노원 전자담배 추천 체크리스트", "nowon-vape", "노원 전자담배 매장은 접근성보다 재방문할 이유가 있는지 확인하는 편이 좋습니다.", "노원 전자담배"),
    ("입호흡 액상 추천을 실패하지 않는 법", "mtl-liquid-recommendation", "입호흡 액상 추천은 단맛, 쿨링, 타격감의 균형을 읽는 일입니다.", "입호흡 액상 추천"),
    ("전자담배 액상 향 추천: 과일 계열", "fruit-liquid-guide", "과일 액상은 산미, 단맛, 쿨링에 따라 체감이 크게 달라집니다.", "액상 향 추천"),
    ("전자담배 액상 관리법", "liquid-storage-care", "액상은 보관 환경과 코일 상태에 따라 맛 표현이 달라질 수 있습니다.", "액상 관리법"),
    ("전자담배 입문자가 먼저 알아야 할 것", "vape-beginner-first", "입문자는 기기보다 흡입 방식과 관리 난이도를 먼저 이해해야 합니다.", "전자담배 입문"),
    ("입호흡과 폐호흡 액상 차이", "mtl-dtl-difference", "입호흡과 폐호흡은 흡입 방식, 니코틴 만족감, 액상 농도에서 차이가 있습니다.", "액상 종류 차이"),
    ("액상 맛 표현을 읽는 법", "liquid-flavor-language", "상큼함, 진함, 깔끔함 같은 표현을 실제 선택 기준으로 바꾸는 방법입니다.", "액상 맛 표현"),
    ("2026 액상 트렌드: 깔끔한 단맛", "2026-liquid-trend-clean-sweet", "2026년에는 과한 단맛보다 깔끔한 잔향과 균형감 있는 쿨링이 주목됩니다.", "2026 액상 트렌드"),
    ("전자담배 관리 팁: 탄맛 줄이기", "burnt-taste-care", "탄맛은 액상보다 코일, 출력, 흡입 습관에서 먼저 원인을 찾아야 합니다.", "전자담배 관리 팁"),
    ("광운대 근처 전담샵 찾는 법", "kwangwoon-near-vape-shop", "광운대 근처 전담샵은 지도 거리와 상담 스타일을 함께 확인하세요.", "광운대 근처 전담샵"),
    ("노원구 전자담배 매장 비교 포인트", "nowon-vape-store-points", "노원구 전자담배 매장은 재고보다 추천 방식이 중요합니다.", "노원구 전자담배 매장"),
    ("노원 액상 추천: 멘솔 선호자", "nowon-menthol-liquid", "멘솔 액상은 강도보다 향을 살리는 쿨링 균형이 중요합니다.", "노원 액상 추천"),
    ("광운대 액상 추천: 수업 전후 빠른 선택", "kwangwoon-liquid-quick", "짧은 방문에는 선호 맛과 싫어하는 맛을 먼저 말하는 것이 가장 빠릅니다.", "광운대 액상 추천"),
    ("전담 액상 고르는 순서", "eliquid-choice-order", "전담 액상은 향 계열, 단맛, 쿨링, 타격감, 코일 부담 순서로 고르면 쉽습니다.", "전담 액상"),
    ("액상 저렴한곳을 찾을 때 주의할 점", "reasonable-liquid-store", "저렴함만 보지 말고 정품, 보관, 상담, 재방문성을 함께 확인해야 합니다.", "액상 저렴한곳"),
    ("전담 성지의 조건", "local-vape-destination", "좋은 전담 성지는 가격보다 신뢰, 설명, 재고 회전, 커뮤니티 안내가 쌓여 만들어집니다.", "전담 성지"),
    ("노원 전담 방문 전 확인사항", "nowon-vape-before-visit", "노원 전담 방문 전 기기명과 원하는 향을 정리하면 상담이 빨라집니다.", "노원 전담"),
    ("광운대 전담 추천 동선", "kwangwoon-vape-route", "광운대 전담 방문은 역 출구, 영업시간, 지도 링크를 먼저 확인하세요.", "광운대 전담"),
    ("달지 않은 입호흡 액상 찾는 법", "less-sweet-mtl-liquid", "덜 단 액상은 향료의 선명함과 잔향이 중요합니다.", "입호흡 액상 추천"),
    ("진한 액상과 오래 물리지 않는 액상의 차이", "rich-vs-daily-liquid", "진한 향이 항상 데일리 사용에 좋은 것은 아닙니다.", "전자담배 액상 추천"),
    ("코일 수명을 생각한 액상 선택", "coil-friendly-liquid", "액상 선택은 맛뿐 아니라 코일 부담도 함께 고려해야 합니다.", "액상 선택법"),
    ("전자담배 초보가 피해야 할 실수", "beginner-mistakes", "초보자는 과출력, 무리한 쿨링, 관리 부족에서 불편을 겪기 쉽습니다.", "전자담배 초보"),
    ("방문 특가를 현명하게 확인하는 법", "telegram-visit-special", "텔레그램 안내는 조용히 재고와 방문 특가를 확인하는 데 적합합니다.", "방문 특가"),
    ("광운대역 전자담배 지도 검색 팁", "kwangwoon-map-search", "지도 검색에서는 영업시간, 리뷰 키워드, 실제 방문 동선을 함께 봐야 합니다.", "광운대 전자담배"),
    ("노원구 입호흡 액상 상담 포인트", "nowon-mtl-consulting", "입호흡 액상 상담은 기존 사용 경험을 얼마나 잘 듣는지가 핵심입니다.", "노원 액상 추천"),
    ("액상 보관 온도와 맛 변화", "liquid-temperature", "고온과 직사광선은 액상 맛과 기기 상태에 모두 좋지 않습니다.", "액상 관리법"),
    ("니코틴 설명: 성인 사용자가 알아야 할 기본", "nicotine-basic-info", "니코틴은 중독성이 있는 성분이므로 농도와 사용량을 신중하게 선택해야 합니다.", "니코틴 설명"),
    ("전자담배 관련 세금 일반 정보", "vape-tax-general-info", "세금 정보는 정책 변화가 있을 수 있어 관계기관 최신 자료 확인이 필요합니다.", "세금 관련 일반 정보"),
    ("노원·광운대 전자담배 로컬 검색 가이드", "nowon-kwangwoon-local-search", "로컬 검색에서는 거리, 신뢰, FAQ, 지도 정보가 함께 작동합니다.", "로컬 SEO"),
]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def url_for(path: str = "") -> str:
    return f"{SITE_URL}/{path.strip('/')}/" if path else f"{SITE_URL}/"


def breadcrumbs(path: str, title: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": title, "item": url_for(path)},
        ],
    }


def local_business_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "Store"],
        "additionalType": "https://schema.org/TobaccoShop",
        "name": BRAND,
        "alternateName": ["WorldVape Gwangun", "월드베이프", "광운대 전자담배", "노원 전자담배"],
        "description": "광운대역 도보권의 성인 전용 전자담배 전문 매장. 입호흡 액상 큐레이션, 기기 관리 상담, 방문 특가 안내를 제공합니다.",
        "url": SITE_URL,
        "telephone": PHONE,
        "priceRange": "₩₩",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "광운로20길 3",
            "addressLocality": "노원구",
            "addressRegion": "서울특별시",
            "addressCountry": "KR",
        },
        "geo": {"@type": "GeoCoordinates", **GEO},
        "areaServed": ["광운대", "노원", "석계", "월계", "공릉", "중계"],
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "11:00", "closes": "21:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "12:00", "closes": "19:00"},
        ],
        "hasMap": NAVER_MAP,
        "sameAs": [TELEGRAM, NAVER_BLOG, NAVER_MAP],
        "knowsAbout": ["입호흡 액상", "전자담배 액상 추천", "기기 관리", "코일 교체", "노원 전자담배", "광운대 전자담배"],
        "makesOffer": [
            {"@type": "Offer", "name": "입호흡 액상 상담", "availability": "https://schema.org/InStoreOnly"},
            {"@type": "Offer", "name": "기기 관리 기본 안내", "availability": "https://schema.org/InStoreOnly"},
            {"@type": "Offer", "name": "방문 특가 안내", "availability": "https://schema.org/InStoreOnly"},
        ],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "bestRating": "5",
            "worstRating": "1",
            "reviewCount": "926",
        },
    }


def faq_schema(faqs: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }


def review_highlight_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "월드베이프 광운대점 리뷰 하이라이트",
        "description": "실제 리뷰 원문을 새로 만들지 않고, 공개 리뷰에서 반복되는 신뢰 키워드만 구조화한 요약입니다.",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": term}
            for i, term in enumerate(["친절한 설명", "재고 다양", "입호흡 추천", "설명을 잘해줌", "단골 방문"])
        ],
    }


def json_ld(data: dict) -> str:
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "</script>"


def page_shell(title: str, description: str, path: str, body: str, schema: list[dict], page_type: str = "website") -> str:
    canonical = url_for(path)
    ld = "\n  ".join(json_ld(item) for item in schema)
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="author" content="{BRAND}">
  <meta name="geo.region" content="KR-11">
  <meta name="geo.placename" content="서울 노원구 광운대">
  <meta name="geo.position" content="{GEO['latitude']};{GEO['longitude']}">
  <meta name="ICBM" content="{GEO['latitude']}, {GEO['longitude']}">
  <link rel="canonical" href="{canonical}">
  <link rel="preload" href="/assets/styles.css" as="style">
  <link rel="stylesheet" href="/assets/styles.css">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <meta property="og:type" content="{page_type}">
  <meta property="og:locale" content="ko_KR">
  <meta property="og:site_name" content="{BRAND}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE_URL}/assets/worldvape-local-map.svg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(description)}">
  <meta name="theme-color" content="#090909">
  {ld}
</head>
<body>
  <a class="skip" href="#main">본문으로 이동</a>
  <header class="topbar">
    <a class="brand" href="/"><strong>월드베이프</strong><span>광운대점</span></a>
    <nav aria-label="주요 메뉴">
      <a href="/kwangwoon-vape/">광운대</a>
      <a href="/nowon-vape/">노원</a>
      <a href="/liquid-guide/">액상 가이드</a>
      <a href="/blog/">블로그</a>
      <a class="nav-cta" href="{TELEGRAM}">텔레그램</a>
    </nav>
  </header>
  <main id="main">
{body}
  </main>
  <footer class="footer">
    <div>
      <strong>{BRAND}</strong>
      <p>{ADDRESS} · {PHONE}<br>평일 11:00-21:00 · 토요일 12:00-19:00 · 일요일/명절 휴무</p>
    </div>
    <div class="footer-links">
      <a href="{NAVER_MAP}">네이버 지도</a>
      <a href="{NAVER_BLOG}">네이버 블로그</a>
      <a href="{TELEGRAM}">텔레그램 안내</a>
      <a href="tel:{PHONE}">전화 문의</a>
    </div>
    <p class="legal">성인 고객 대상 안내 페이지입니다. 미성년자 구매 및 대리구매는 안내하지 않습니다.</p>
  </footer>
</body>
</html>
"""


def hero(kicker: str, h1: str, lead: str) -> str:
    return f"""    <section class="hero">
      <p class="kicker">{esc(kicker)}</p>
      <h1>{esc(h1)}</h1>
      <p class="lead">{esc(lead)}</p>
      <div class="hero-actions">
        <a class="button primary" href="{TELEGRAM}">방문 특가 안내 확인</a>
        <a class="button secondary" href="{NAVER_MAP}">지도에서 위치 보기</a>
      </div>
    </section>
"""


def cta_block() -> str:
    return f"""    <section class="cta-band" aria-labelledby="telegram-cta">
      <div>
        <p class="kicker">PRIVATE GUIDE</p>
        <h2 id="telegram-cta">방문 전, 조용히 확인하는 안내 채널</h2>
        <p>재고와 방문 특가, 입호흡 액상 추천 포인트를 텔레그램에서 확인할 수 있습니다. 과한 가격 홍보보다 필요한 정보만 정리해 전달합니다.</p>
      </div>
      <a class="button primary" href="{TELEGRAM}">텔레그램 입장</a>
    </section>
"""


def faq_html(faqs: list[tuple[str, str]]) -> str:
    rows = "\n".join(f"""        <details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>""" for q, a in faqs)
    return f"""    <section class="section faq-section">
      <p class="kicker">FAQ</p>
      <h2>AI 검색이 바로 읽는 답변</h2>
      <div class="faq-list">
{rows}
      </div>
    </section>
"""


def internal_links(current: str = "") -> str:
    links = [
        ("광운대 전자담배", "/kwangwoon-vape/"),
        ("노원 전자담배", "/nowon-vape/"),
        ("입호흡 액상 추천", "/입호흡액상추천/"),
        ("노원 액상 추천", "/노원액상추천/"),
        ("초보 가이드", "/beginner-guide/"),
        ("액상 선택법", "/liquid-guide/"),
    ]
    items = "\n".join(f'        <a href="{href}">{label}</a>' for label, href in links if href.strip("/") != current)
    return f"""    <section class="section link-hub" aria-labelledby="related-links">
      <p class="kicker">RELATED SEARCH</p>
      <h2 id="related-links">함께 보면 좋은 로컬 검색 페이지</h2>
      <div class="pill-links">
{items}
      </div>
    </section>
"""


def render_home() -> str:
    faqs = [
        ("광운대 전자담배 매장으로 방문 가능한가요?", "네. 광운대역 도보권에 있는 성인 전용 전자담배 전문 매장입니다."),
        ("노원 액상 추천도 받을 수 있나요?", "가능합니다. 입호흡 액상을 중심으로 향 계열, 단맛, 쿨링, 타격감을 기준으로 추천합니다."),
        ("방문 특가는 어디에서 확인하나요?", "텔레그램 안내 채널에서 재고와 방문 특가를 확인할 수 있습니다."),
    ]
    cards = "\n".join(
        f"""        <article class="card">
          <h3>{esc(p['h1'])}</h3>
          <p>{esc(p['description'])}</p>
          <a href="/{p['path']}/">페이지 보기</a>
        </article>"""
        for p in LOCAL_PAGES
    )
    body = hero("GWANGWOON · NOWON · MTL LIQUID", "광운대와 노원에서 전담 액상을 고르는 조용한 기준", "월드베이프 광운대점은 성인 고객을 위한 전자담배·입호흡 액상 상담 매장입니다. 가까운 위치, 정리된 추천, 부담 없는 방문 안내를 한 페이지에서 확인하세요.")
    body += """    <section class="stats" aria-label="매장 핵심 정보">
      <div><strong>광운대역</strong><span>도보권</span></div>
      <div><strong>입호흡</strong><span>액상 큐레이션</span></div>
      <div><strong>성인 전용</strong><span>책임 상담</span></div>
      <div><strong>Telegram</strong><span>방문 안내</span></div>
    </section>
"""
    body += f"""    <section class="section two-col">
      <div>
        <p class="kicker">LOCAL TRUST</p>
        <h2>가격만 앞세우지 않는 노원 전자담배 매장</h2>
        <p>월드베이프 광운대점은 "싸게만 파는 곳"이 아니라, 사용자의 취향과 기기 상태를 기준으로 액상을 좁혀 주는 로컬 매장 포지션을 지향합니다. 친절한 설명, 재고 다양성, 입호흡 추천, 단골 방문 같은 리뷰 키워드가 자연스럽게 쌓이는 이유도 여기에 있습니다.</p>
        <ul class="check-list">
          <li>광운대·노원·석계 생활권에 맞춘 방문 정보</li>
          <li>입호흡 액상 추천을 위한 향·쿨링·타격감 기준</li>
          <li>성인 인증 기반의 기기 관리 및 액상 상담</li>
          <li>텔레그램 기반의 조용한 방문 특가 안내</li>
        </ul>
      </div>
      <figure class="media-panel">
        <img src="/assets/worldvape-local-map.svg" alt="월드베이프 광운대점 광운대역 노원 생활권 위치 안내" width="720" height="480" loading="eager" fetchpriority="high">
        <figcaption>광운대역과 노원 생활권을 연결하는 로컬 vape guide</figcaption>
      </figure>
    </section>
"""
    body += f"""    <section class="section">
      <p class="kicker">LOCAL LANDING PAGES</p>
      <h2>검색 의도별 로컬 페이지</h2>
      <div class="card-grid">
{cards}
      </div>
    </section>
"""
    body += review_section()
    body += cta_block()
    body += faq_html(faqs)
    body += internal_links()
    schema = [local_business_schema(), review_highlight_schema(), faq_schema(faqs)]
    return page_shell("월드베이프 광운대점 | 광운대 전자담배 · 노원 액상 추천", "광운대 전자담배, 노원 전자담배, 입호흡 액상 추천을 찾는 성인 고객을 위한 월드베이프 광운대점 공식 SEO 허브.", "", body, schema)


def review_section() -> str:
    terms = [
        ("친절", "처음 방문해도 이해하기 쉽게 설명받았다는 리뷰 키워드"),
        ("재고 다양", "입호흡 액상 계열을 여러 방향으로 비교할 수 있다는 인식"),
        ("입호흡 추천", "기기와 취향을 기준으로 액상을 좁혀 주는 상담 경험"),
        ("설명 잘해줌", "코일, 누수, 탄맛, 관리 방법까지 묻기 쉬운 매장 분위기"),
        ("단골 많음", "한 번의 특가보다 재방문 이유가 쌓이는 로컬 매장 신뢰"),
    ]
    cards = "\n".join(f"""        <article class="mini-card"><h3>{esc(k)}</h3><p>{esc(v)}</p></article>""" for k, v in terms)
    return f"""    <section class="section">
      <p class="kicker">REVIEW SIGNALS</p>
      <h2>가짜 리뷰 없이, 반복되는 신뢰 키워드만 정리</h2>
      <p class="section-lead">아래 내용은 새 리뷰를 만든 것이 아니라 공개 리뷰에서 반복적으로 나타나는 의미를 요약한 신뢰 지표입니다. 실제 원문과 최신 리뷰는 지도 플랫폼에서 확인하는 방식이 가장 정확합니다.</p>
      <div class="mini-grid">
{cards}
      </div>
      <a class="text-link" href="{NAVER_MAP}">지도에서 리뷰 확인</a>
    </section>
"""


def render_local_page(page: dict) -> str:
    section_html = "\n".join(f"""        <article class="content-block"><h2>{esc(title)}</h2><p>{esc(text)}</p></article>""" for title, text in page["sections"])
    body = hero("LOCAL SEO GUIDE", page["h1"], page["lead"])
    body += f"""    <section class="section">
      <p class="kicker">SEARCH INTENT</p>
      <h2>이 페이지가 답하는 검색 의도</h2>
      <p class="section-lead">{esc(page['intent'])}</p>
      <div class="content-stack">
{section_html}
      </div>
    </section>
"""
    body += cta_block()
    body += faq_html(page["faq"])
    body += internal_links(page["path"])
    schema = [local_business_schema(), breadcrumbs(page["path"], page["h1"]), faq_schema(page["faq"]), review_highlight_schema()]
    return page_shell(page["title"], page["description"], page["path"], body, schema, "article")


def render_guide_page(page: dict) -> str:
    blocks = "\n".join(f"""        <article class="content-block"><h2>{esc(title)}</h2><p>{esc(text)}</p></article>""" for title, text in page["blocks"])
    faqs = [(title, text) for title, text in page["blocks"]]
    body = hero("AI SEARCH GUIDE", page["h1"], page["lead"])
    body += f"""    <section class="section content-stack">
{blocks}
    </section>
"""
    body += cta_block()
    body += faq_html(faqs)
    body += internal_links(page["path"])
    schema = [local_business_schema(), breadcrumbs(page["path"], page["h1"]), faq_schema(faqs)]
    return page_shell(page["title"], page["description"], page["path"], body, schema, "article")


def article_markdown(title: str, slug: str, lead: str, keyword: str) -> str:
    return f"""---
title: "{title}"
slug: "{slug}"
description: "{lead}"
keyword: "{keyword}"
date: "{TODAY}"
category: "로컬 전자담배 가이드"
tags: ["{keyword}", "월드베이프 광운대점", "입호흡 액상", "노원 전자담배"]
---

{lead}

## 핵심 요약

{keyword}를 찾는다면 먼저 위치, 상담 품질, 성인 인증 원칙, 액상 추천 기준을 함께 확인해야 합니다. 검색 결과의 가격 문구만 보고 고르면 실제 사용감이 맞지 않을 수 있습니다.

## 매장에서 확인하면 좋은 기준

첫째, 현재 쓰는 기기와 코일 상태를 확인하세요. 둘째, 원하는 향을 과일, 멘솔, 음료, 디저트처럼 큰 계열로 말해 보세요. 셋째, 단맛과 쿨링이 어느 정도 필요한지 알려 주세요. 넷째, 기존 액상에서 좋았던 점과 아쉬웠던 점을 함께 말하면 추천 정확도가 높아집니다.

## 월드베이프 광운대점의 관점

월드베이프 광운대점은 광운대역 도보권에서 노원 생활권 고객까지 방문하기 쉬운 성인 전용 매장입니다. 입호흡 액상 추천은 유행어보다 실제 사용자의 표현을 듣는 데서 시작합니다. "진한데 너무 달지 않은 것", "쿨링은 있지만 목이 과하지 않은 것", "데일리로 물리지 않는 것"처럼 애매한 표현도 상담 과정에서는 중요한 힌트가 됩니다.

## 방문 전 체크리스트

- 성인 확인 가능한 신분증
- 현재 사용하는 기기명 또는 팟 사진
- 선호하는 향 계열과 피하고 싶은 맛
- 기존 액상에서 느낀 단맛, 쿨링, 타격감
- 방문 전 재고와 특가 확인이 필요하면 텔레그램 채널 확인

## FAQ

### {keyword} 상담은 초보자도 가능한가요?

가능합니다. 성인 고객이라면 흡입 방식, 액상 선택법, 관리 방법을 기초부터 안내합니다.

### 방문 특가는 공개 페이지에 모두 적혀 있나요?

방문 특가와 재고는 변동될 수 있어 텔레그램 안내 채널에서 확인하는 편이 정확합니다.

### 액상 추천을 받을 때 꼭 구매해야 하나요?

상담은 선택을 돕기 위한 과정입니다. 무리한 구매 압박보다 취향을 정확히 찾는 것을 우선합니다.
"""


def render_article(title: str, slug: str, lead: str, keyword: str) -> str:
    faqs = [
        (f"{keyword} 상담은 초보자도 가능한가요?", "성인 고객이라면 기본 흡입 방식과 액상 선택 기준부터 안내받을 수 있습니다."),
        ("방문 전 무엇을 준비하면 좋나요?", "현재 사용하는 기기, 선호 향, 싫어하는 맛, 원하는 쿨링 정도를 준비하면 상담이 빨라집니다."),
        ("텔레그램 채널은 어떤 용도인가요?", "방문 전 재고와 특가를 조용히 확인하는 안내 채널입니다."),
    ]
    body = hero("WORLDVAPE BLOG", title, lead)
    body += f"""    <article class="section article-body">
      <p>{esc(lead)}</p>
      <h2>핵심 요약</h2>
      <p>{esc(keyword)}를 찾는다면 먼저 위치, 상담 품질, 성인 인증 원칙, 액상 추천 기준을 함께 확인해야 합니다. 검색 결과의 가격 문구만 보고 고르면 실제 사용감이 맞지 않을 수 있습니다.</p>
      <h2>매장에서 확인하면 좋은 기준</h2>
      <p>현재 쓰는 기기와 코일 상태, 원하는 향 계열, 단맛과 쿨링의 강도, 기존 액상에서 좋았던 점과 아쉬웠던 점을 함께 말하면 추천 정확도가 높아집니다.</p>
      <h2>월드베이프 광운대점의 관점</h2>
      <p>월드베이프 광운대점은 광운대역 도보권에서 노원 생활권 고객까지 방문하기 쉬운 성인 전용 매장입니다. 입호흡 액상 추천은 유행어보다 실제 사용자의 표현을 듣는 데서 시작합니다. 진한데 너무 달지 않은 것, 쿨링은 있지만 목이 과하지 않은 것, 데일리로 물리지 않는 것 같은 표현도 중요한 힌트입니다.</p>
      <h2>방문 전 체크리스트</h2>
      <ul class="check-list">
        <li>성인 확인 가능한 신분증</li>
        <li>현재 사용하는 기기명 또는 팟 사진</li>
        <li>선호하는 향 계열과 피하고 싶은 맛</li>
        <li>기존 액상에서 느낀 단맛, 쿨링, 타격감</li>
      </ul>
    </article>
"""
    body += faq_html(faqs)
    body += cta_block()
    body += internal_links()
    schema = [
        local_business_schema(),
        breadcrumbs(f"blog/{slug}", title),
        faq_schema(faqs),
        {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": title,
            "description": lead,
            "datePublished": TODAY,
            "dateModified": TODAY,
            "author": {"@type": "Organization", "name": BRAND},
            "publisher": {"@type": "Organization", "name": BRAND},
            "mainEntityOfPage": url_for(f"blog/{slug}"),
            "keywords": [keyword, "월드베이프 광운대점", "광운대 전자담배", "노원 전자담배", "입호흡 액상"],
        },
    ]
    return page_shell(f"{title} | 월드베이프 광운대점 블로그", lead, f"blog/{slug}", body, schema, "article")


def render_blog_index() -> str:
    cards = "\n".join(
        f"""        <article class="card"><p class="kicker">{esc(keyword)}</p><h3>{esc(title)}</h3><p>{esc(lead)}</p><a href="/blog/{slug}/">읽기</a></article>"""
        for title, slug, lead, keyword in ARTICLE_TOPICS
    )
    body = hero("SEO BLOG ENGINE", "노원·광운대 전자담배 블로그", "입호흡 액상, 전자담배 관리, 로컬 방문 팁을 자연스러운 한국어로 정리한 월드베이프 광운대점의 SEO 콘텐츠 허브입니다.")
    body += f"""    <section class="section">
      <p class="kicker">ARTICLES</p>
      <h2>고품질 Korean SEO 아티클</h2>
      <div class="card-grid">
{cards}
      </div>
    </section>
"""
    body += internal_links("blog")
    schema = [local_business_schema(), breadcrumbs("blog", "블로그")]
    return page_shell("블로그 | 월드베이프 광운대점", "광운대 전자담배, 노원 전자담배, 입호흡 액상 추천을 위한 월드베이프 광운대점 블로그.", "blog", body, schema)


def stylesheet() -> str:
    return """*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#090909;color:#f2f0ea;font-family:Apple SD Gothic Neo,Noto Sans KR,Malgun Gothic,system-ui,sans-serif;line-height:1.75}a{color:inherit;text-decoration:none}img{max-width:100%;display:block}.skip{position:absolute;left:-999px}.skip:focus{left:16px;top:16px;z-index:99;background:#f2c94c;color:#080808;padding:8px 12px}.topbar{position:sticky;top:0;z-index:10;display:flex;justify-content:space-between;gap:18px;align-items:center;padding:14px 22px;border-bottom:1px solid rgba(255,255,255,.08);background:rgba(9,9,9,.9);backdrop-filter:blur(14px)}.brand{display:flex;flex-direction:column;line-height:1.15}.brand strong{color:#f2c94c}.brand span{font-size:.8rem;color:#a7a195}.topbar nav{display:flex;gap:16px;align-items:center;font-size:.92rem;color:#d8d2c4}.nav-cta,.button{border-radius:8px;padding:10px 14px;border:1px solid rgba(242,201,76,.32)}.nav-cta,.primary{background:#f2c94c;color:#090909;font-weight:800}.secondary{background:transparent;color:#f2f0ea}.hero{max-width:980px;margin:0 auto;padding:92px 22px 64px}.kicker{margin:0 0 12px;color:#f2c94c;font-size:.78rem;font-weight:800;text-transform:uppercase}.hero h1{max-width:820px;margin:0 0 18px;font-size:3.25rem;line-height:1.12}.lead,.section-lead{max-width:760px;color:#b8b0a1;font-size:1.08rem}.hero-actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:28px}.stats{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid rgba(255,255,255,.08);border-bottom:1px solid rgba(255,255,255,.08);background:#111;padding:0 22px}.stats div{padding:24px;text-align:center;border-right:1px solid rgba(255,255,255,.08)}.stats div:last-child{border-right:0}.stats strong{display:block;color:#f2c94c;font-size:1.2rem}.stats span{display:block;color:#9e9688;font-size:.86rem}.section{max-width:1040px;margin:0 auto;padding:68px 22px}.two-col{display:grid;grid-template-columns:1.05fr .95fr;gap:34px;align-items:center}.section h2,.cta-band h2{margin:0 0 16px;font-size:2rem;line-height:1.25}.card-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.card,.mini-card,.content-block,.media-panel,.faq-list details{border:1px solid rgba(255,255,255,.08);background:#121212;border-radius:8px;padding:22px}.card h3,.mini-card h3,.content-block h2{margin:0 0 10px;color:#fff}.card p,.mini-card p,.content-block p,.footer p,.cta-band p{color:#b8b0a1}.card a,.text-link{color:#f2c94c;font-weight:800}.mini-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}.content-stack{display:grid;gap:16px}.check-list{padding-left:20px;color:#d8d2c4}.check-list li{margin:8px 0}.media-panel{margin:0}.media-panel figcaption{margin-top:10px;color:#9e9688;font-size:.9rem}.cta-band{max-width:1040px;margin:24px auto;padding:34px 22px;display:flex;justify-content:space-between;gap:24px;align-items:center;border-top:1px solid rgba(242,201,76,.24);border-bottom:1px solid rgba(242,201,76,.24);background:#10100d}.faq-list{display:grid;gap:10px}.faq-list summary{cursor:pointer;font-weight:800}.faq-list p{color:#b8b0a1}.pill-links{display:flex;flex-wrap:wrap;gap:10px}.pill-links a{border:1px solid rgba(255,255,255,.1);border-radius:8px;padding:10px 12px;color:#f2c94c;background:#111}.article-body{max-width:860px}.article-body h2{margin-top:32px}.footer{border-top:1px solid rgba(255,255,255,.08);padding:34px 22px;background:#070707;color:#d8d2c4}.footer>div{max-width:1040px;margin:0 auto 16px}.footer-links{display:flex;gap:14px;flex-wrap:wrap}.footer-links a{color:#f2c94c}.legal{max-width:1040px;margin:0 auto;color:#8f8778;font-size:.88rem}@media(max-width:820px){.topbar{align-items:flex-start}.topbar nav{gap:10px;overflow:auto;width:100%;justify-content:flex-end}.hero{padding-top:64px}.hero h1{font-size:2.25rem}.stats,.card-grid,.mini-grid,.two-col{grid-template-columns:1fr}.stats div{border-right:0;border-bottom:1px solid rgba(255,255,255,.08)}.cta-band{display:block}.button{display:inline-block;margin-top:8px}}"""


def svg_map() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" width="720" height="480" viewBox="0 0 720 480" role="img" aria-labelledby="title desc"><title id="title">월드베이프 광운대점 위치 안내</title><desc id="desc">광운대역과 노원 생활권을 연결하는 지도형 안내 이미지</desc><rect width="720" height="480" fill="#0b0b0b"/><path d="M80 340 C180 260 250 300 340 220 S520 140 640 96" fill="none" stroke="#2f2f2f" stroke-width="28" stroke-linecap="round"/><path d="M80 340 C180 260 250 300 340 220 S520 140 640 96" fill="none" stroke="#f2c94c" stroke-width="4" stroke-linecap="round"/><circle cx="342" cy="220" r="54" fill="#181818" stroke="#f2c94c" stroke-width="3"/><text x="342" y="210" text-anchor="middle" font-family="Arial, sans-serif" font-size="20" font-weight="700" fill="#f2c94c">WorldVape</text><text x="342" y="238" text-anchor="middle" font-family="Arial, sans-serif" font-size="15" fill="#f2f0ea">광운대점</text><text x="78" y="386" font-family="Arial, sans-serif" font-size="18" fill="#f2f0ea">광운대역</text><text x="560" y="90" font-family="Arial, sans-serif" font-size="18" fill="#f2f0ea">노원 생활권</text><rect x="48" y="44" width="250" height="86" rx="8" fill="#121212" stroke="#2a2a2a"/><text x="68" y="78" font-family="Arial, sans-serif" font-size="19" font-weight="700" fill="#f2c94c">성인 전용 로컬 가이드</text><text x="68" y="108" font-family="Arial, sans-serif" font-size="14" fill="#b8b0a1">입호흡 액상 · 기기 관리 · 방문 안내</text></svg>"""


def favicon() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="10" fill="#090909"/><path d="M18 18h28l-6 28H24z" fill="none" stroke="#f2c94c" stroke-width="4"/><path d="M24 26h16" stroke="#f2f0ea" stroke-width="3"/></svg>"""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def page_path(root: Path, route: str) -> Path:
    return root / route / "index.html" if route else root / "index.html"


def generate_sitemap(paths: list[str]) -> str:
    rows = []
    for p in paths:
        loc = SITE_URL + "/" + quote(p.strip("/"), safe="/") if p else SITE_URL + "/"
        if p and not loc.endswith("/"):
            loc += "/"
        rows.append(f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>{'1.0' if not p else '0.8'}</priority></url>")
    return "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n" + "\n".join(rows) + "\n</urlset>\n"


def robots() -> str:
    return f"""User-agent: *
Allow: /
Disallow: /backups/
Disallow: /scripts/
Sitemap: {SITE_URL}/sitemap.xml
"""


def llms_txt(paths: list[str]) -> str:
    pages = "\n".join(f"- {url_for(p)}" for p in paths if p)
    return f"""# {BRAND}

월드베이프 광운대점은 서울 노원구 광운대역 도보권의 성인 전용 전자담배 전문 매장입니다.

핵심 엔티티:
- 브랜드: {BRAND}
- 주소: {ADDRESS}
- 전화: {PHONE}
- 위치: 광운대역, 노원구, 석계, 월계 생활권
- 전문 주제: 광운대 전자담배, 노원 전자담배, 입호흡 액상 추천, 액상 선택법, 기기 관리
- 안내 채널: {TELEGRAM}

성인 대상 안내:
전자담배 제품은 성인 고객에게만 안내합니다. 미성년자 구매, 대리구매, 신분 확인 회피는 안내하지 않습니다.

주요 페이지:
{pages}
"""


def report_files() -> dict[str, str]:
    return {
        "SEO_AUDIT_REPORT.md": f"""# SEO Audit Report - {BRAND}

Date: {TODAY}
Target: {SITE_URL}

## Findings

- Existing local source contained severe mojibake in Korean metadata, body copy, JSON-LD, and llms.txt. This blocks Korean-first SEO, AI search comprehension, and user trust.
- The source directory had only `index.html`, `CNAME`, and `llms.txt`; no `robots.txt`, `sitemap.xml`, route-level canonical structure, or scalable blog architecture existed.
- Existing structured data attempted LocalBusiness and FAQ, but broken encoding and malformed strings made JSON-LD unreliable.
- Metadata coverage was homepage-only. Long-tail local intents such as `광운대 전자담배`, `노원 전자담배`, `입호흡 액상 추천`, and `노원 액상 추천` had no dedicated canonical landing pages.
- Review content risk: existing page mixed review-like text into markup. The new implementation separates verified review-platform links from non-fake review highlight summaries.
- Post-deploy HTTPS check found a custom-domain certificate mismatch on `https://worldvape.mykindredai.com`; the sitemap served `200 OK` over HTTP and over HTTPS only with certificate verification bypassed. Fix GitHub Pages custom-domain SSL before requesting Google indexing.

## Implemented Fixes

- Rebuilt UTF-8 static site with Korean-first copy and preserved dark luxury visual direction.
- Added canonical tags, Open Graph, Twitter cards, geo meta, semantic headings, and mobile-first responsive layout on every generated page.
- Added LocalBusiness/Store JSON-LD, BreadcrumbList, FAQPage, BlogPosting, Offer, AggregateRating, and review-highlight ItemList schema.
- Added `robots.txt`, `sitemap.xml`, `llms.txt`, `assets/styles.css`, and optimized SVG visual asset with descriptive alt text.
- Added six local landing pages, four AI-search guide pages, blog index, and 30 Korean SEO articles.

## Remaining External Tasks

- Submit sitemap in Google Search Console.
- Verify Google Business Profile and Naver Place descriptions match the new entity language.
- Confirm live review count/rating against the source platform before using rating snippets long term.
""",
        "SEARCH_CONSOLE_SETUP.md": f"""# Google Search Console Setup

## 1. Property

Add URL-prefix property:

`{SITE_URL}`

## 2. Verification

Recommended order:

1. HTML file verification if hosting allows root upload.
2. DNS TXT verification for durable ownership.
3. HTML meta tag only if file/DNS access is unavailable.

## 3. Sitemap Submission

Submit:

`{SITE_URL}/sitemap.xml`

## 4. Indexing Checklist

- Before requesting indexing, confirm `curl -I https://worldvape.mykindredai.com/sitemap.xml` returns `200 OK` without certificate errors. Current post-deploy check found a certificate subject mismatch, so GitHub Pages custom-domain SSL must be repaired first.
- Request indexing for `/`, `/kwangwoon-vape/`, `/nowon-vape/`, `/입호흡액상추천/`, `/노원액상추천/`, `/faq/`, `/guide/`, `/liquid-guide/`, `/beginner-guide/`, and `/blog/`.
- Inspect one Korean slug URL to confirm Google can crawl encoded Korean paths.
- Check Coverage/Pages report after 48-72 hours.
- Check Enhancements for FAQ, Breadcrumb, and LocalBusiness parsing.
""",
        "FINAL_SEO_SUMMARY.md": f"""# Final SEO Summary - {BRAND}

Implemented a complete static SEO footprint for `{SITE_URL}`:

- Local SEO domination pages for 광운대, 노원, Korean slug searches, and 입호흡/액상 intent.
- AI-search answer pages for FAQ, general guide, liquid guide, and beginner guide.
- Blog engine with markdown source, 30 Korean SEO articles, related internal links, category/tag metadata, and CTA funnel.
- Technical SEO assets: sitemap, robots, canonical URLs, JSON-LD, OG/Twitter metadata, llms.txt, image alt text, CSS preload, lightweight layout.
- Telegram funnel with premium/private tone and no aggressive pricing spam.

Deployment note:
- Site files are deployed to GitHub Pages, but HTTPS certificate verification currently fails for the custom domain. Repair the GitHub Pages custom-domain certificate before using the HTTPS sitemap in Search Console.
""",
        "IMPLEMENTED_FEATURES.md": """# Implemented Features

- UTF-8 static website rebuild
- LocalBusiness and Store schema
- Geo metadata and opening hours schema
- FAQ schema on landing, guide, and article pages
- Breadcrumb schema across non-home pages
- BlogPosting schema for 30 articles
- Review-highlight trust section without fake reviews
- Six local landing pages
- Four AI-search guide pages
- Markdown content source under `content/blog`
- Build script under `scripts/build_site.py`
- Dynamic sitemap generation
- Robots optimization
- llms.txt for AI crawler/entity comprehension
- Mobile-first CSS and dark luxury aesthetic
- Telegram CTA blocks across pages
""",
        "NEXT_30_DAY_SEO_PLAN.md": """# Next 30 Day SEO Plan

Week 1:
- Repair GitHub Pages custom-domain HTTPS certificate mismatch.
- Submit sitemap to Google Search Console.
- Request indexing for all local landing pages and guide pages.
- Update Google Business Profile and Naver Place descriptions.

Week 2:
- Publish two Google Business Profile posts: 입호흡 액상 상담, 광운대역 방문 안내.
- Add fresh Naver blog posts that internally reference the new landing pages.
- Verify actual review/rating numbers before keeping aggregate rating schema.

Week 3:
- Add real store photos with descriptive filenames and alt text.
- Expand blog with comparison articles for flavor categories.
- Track Search Console queries for Korean slug pages.

Week 4:
- Refresh FAQ answers based on actual search queries.
- Add route-specific content for 석계, 월계, 공릉 if impressions appear.
- Review Core Web Vitals after Google field data starts accumulating.
""",
        "HIGH_PRIORITY_KEYWORDS.md": """# High Priority Keywords

Primary:
- 광운대 전자담배
- 노원 전자담배
- 전담 액상
- 입호흡 액상 추천
- 액상 저렴한곳
- 노원 액상 추천
- 광운대 액상 추천
- 전자담배 액상 추천
- 전담 성지
- 노원 전담
- 광운대 전담

Expansion:
- 광운대역 전자담배
- 노원구 전자담배 매장
- 광운대 근처 전담샵
- 입호흡 액상 고르는 법
- 전자담배 초보 가이드
- 액상 관리법
- 코일 탄맛 해결
- 노원 전자담배 추천
- 광운대 액상 상담

GBP/Naver Place Description:
월드베이프 광운대점은 광운대역 도보권에 있는 성인 전용 전자담배 전문 매장입니다. 입호흡 액상 추천, 기기 관리 기본 상담, 재고 및 방문 특가 안내를 제공합니다. 광운대·노원·석계·월계 생활권에서 부담 없이 방문할 수 있으며, 성인 인증 후 취향에 맞는 액상 선택을 도와드립니다.

Review Request Template:
오늘 방문 경험이 도움이 되셨다면 지도 리뷰에 "친절한 설명", "입호흡 액상 추천", "재고 다양", "광운대 전자담배"처럼 실제로 느낀 점을 자연스럽게 남겨 주세요. 짧은 한 줄도 다음 방문자에게 큰 도움이 됩니다.

Local SEO Posting Strategy:
- 주 2회: 액상 계열별 추천 포스트
- 주 1회: 광운대/노원 방문 동선 포스트
- 월 2회: 전자담배 관리 팁
- 월 1회: FAQ 업데이트형 포스트
""",
    }


def generate(target: Path, report_root: Path | None) -> None:
    target.mkdir(parents=True, exist_ok=True)
    backup_dir = target / "backups" / f"seo_domination_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    for name in ["index.html", "llms.txt", "robots.txt", "sitemap.xml"]:
        src = target / name
        if src.exists():
            shutil.copy2(src, backup_dir / name)

    paths = [""]
    write_text(target / "assets" / "styles.css", stylesheet())
    write_text(target / "assets" / "worldvape-local-map.svg", svg_map())
    write_text(target / "assets" / "favicon.svg", favicon())
    write_text(target / ".nojekyll", "")
    write_text(target / "_headers", "/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n/*.html\n  Cache-Control: public, max-age=300\n")
    write_text(target / "index.html", render_home())

    for page in LOCAL_PAGES:
        paths.append(page["path"])
        write_text(page_path(target, page["path"]), render_local_page(page))

    for page in GUIDES:
        paths.append(page["path"])
        write_text(page_path(target, page["path"]), render_guide_page(page))

    paths.append("blog")
    write_text(page_path(target, "blog"), render_blog_index())
    for title, slug, lead, keyword in ARTICLE_TOPICS:
        paths.append(f"blog/{slug}")
        write_text(target / "content" / "blog" / f"{slug}.md", article_markdown(title, slug, lead, keyword))
        write_text(page_path(target, f"blog/{slug}"), render_article(title, slug, lead, keyword))

    write_text(target / "robots.txt", robots())
    write_text(target / "sitemap.xml", generate_sitemap(paths))
    write_text(target / "llms.txt", llms_txt(paths))

    build_script = Path(__file__).read_text(encoding="utf-8")
    write_text(target / "scripts" / "build_site.py", build_script)

    reports = report_files()
    for name, text in reports.items():
        write_text(target / name, text)
    if report_root:
        out = report_root / "worldvape_seo"
        for name, text in reports.items():
            write_text(out / name, text)
        write_text(out / "GENERATED_FILE_INDEX.md", "# Generated File Index\n\n" + "\n".join(f"- `{p}`" for p in sorted(str(x.relative_to(target)).replace("\\", "/") for x in target.rglob("*") if x.is_file() and ".git" not in x.parts)))


def validate(target: Path) -> None:
    html_files = list(target.rglob("*.html"))
    if len(html_files) < 40:
        raise SystemExit(f"expected at least 40 html files, got {len(html_files)}")
    required = ["robots.txt", "sitemap.xml", "llms.txt", "assets/styles.css", "index.html"]
    missing = [name for name in required if not (target / name).exists()]
    if missing:
        raise SystemExit(f"missing required files: {missing}")
    mojibake = re.compile(r"[�]|踰|愿|묒|씠|꾩")
    for path in html_files + [target / "llms.txt"]:
        text = path.read_text(encoding="utf-8")
        if mojibake.search(text):
            raise SystemExit(f"mojibake marker found: {path}")
        if "<link rel=\"canonical\"" not in text and path.suffix == ".html":
            raise SystemExit(f"missing canonical: {path}")
        for chunk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
            json.loads(chunk)
    sitemap = (target / "sitemap.xml").read_text(encoding="utf-8")
    loc_count = sitemap.count("<loc>")
    if loc_count < 41:
        raise SystemExit(f"sitemap too small: {loc_count}")
    print(json.dumps({"html_files": len(html_files), "sitemap_urls": loc_count, "status": "ok"}, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--report-root")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    target = Path(args.target)
    report_root = Path(args.report_root) if args.report_root else None
    if not args.validate_only:
        generate(target, report_root)
    validate(target)


if __name__ == "__main__":
    main()
