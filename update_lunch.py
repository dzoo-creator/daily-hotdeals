import json, io, re, datetime

P = 'deals.json'
d = json.load(open(P, encoding='utf-8'))
deals = d['deals']

NOW = '2026-11-28T13:05:00+09:00'

# ---------- 1. remove deals ----------
remove_ids = {'food-shinemuscat-gmarket-2kg', 'fashion-uniqlo-pufftech-jacket-479755'}
kept = []
for x in deals:
    if x['id'] in remove_ids:
        removed = {
            'id': x['id'],
            'title': x['title'],
            'mall': x['mall'],
            'listedPrice': x['price'],
            'currentPrice': 9900 if x['id'].startswith('food-shine') else x['price'],
            'reason': (
                '11/28 12:18 재확인: 11/27 판매가 7,160원(기존가 11,920원 39% 할인) → 오늘 9,900원(기존가 11,920원 16% 할인·쿠폰 종료). 2,740원(38%) 인상 — 가격 인상 딜 제외 규칙 적용'
                if x['id'].startswith('food-shine') else
                '11/28 12:22 재확인: 59,900원 그대로이나 09 BLACK 전 사이즈(S~4XL) 품절, 57 OLIVE는 S만 재고 — 남편 사이즈 구매 불가로 제외'
            ),
            'url': x['url'],
            'checkedAt': '2026-11-28T12:22:00+09:00',
        }
        d['removedDeals'].insert(0, removed)
    else:
        kept.append(x)
deals = kept

# ---------- 2. re-verification refs for existing deals ----------
recheck = {
 'food-apple-busa-5kg': '지마켓 상품페이지 11/28 12:17 재확인: 13,580원(기존가 14,600원 6% 할인) · 무료배송 · 평점 4.6(1,919건) · 11/30(월) 출고 — 가격 그대로',
 'food-maniker-basasak-4pack': '옥션 상품페이지 11/28 12:19 재확인: 원가 30,470원 · 상품쿠폰 적용가 25,420원 · 카드 7% 즉시할인 적용 시 23,640원 — 11/27과 동일(오늘도 구매 가능)',
 'living-priel-jacquard-mat': '오늘의집 상품페이지 11/28 12:31 재확인: 9,900원(정가 19,900원 50%) · 무료배송 · 리뷰 4.8(9,845건) — 기획전이 아닌 단품 페이지 URL로 교체',
 'living-natureliving-laundry-trolley': '오늘의집 상품페이지 11/28 12:26 재확인: 15,900원(25,900원 38% 할인) · 무료배송 · 리뷰 8만2,452건 — 그대로',
 'living-saenghwal-kitchen-8L': '오늘의집 상품페이지 11/28 12:23 재확인: 20,900원(44,000원 52% 할인) · 무료배송 · 11/30(월) 출발 — 그대로',
 'living-iriscorea-drawer-box-2': '오늘의집 상품페이지 11/28 12:26 재확인: 20,900원(25,800원 18% 할인) · 무료배송 · 리뷰 3만6,415건 — 그대로',
 'living-listerine-750x4': '오늘의집 상품페이지 11/28 12:26 재확인: 21,300원(39,600원 46% 할인) · 무료배송 · 쿨민트 750ml×4+250ml 증정 — 그대로',
 'living-drwater-shower-filter': '오늘의집 상품페이지 11/28 12:26 재확인: 25,900원(38,900원 33% 할인) · 무료배송 · 카카오페이 7% 추가할인 가능 — 그대로',
 'living-cottonliving-towel-10': '오늘의집 상품페이지 11/28 12:27 재확인: 34,900원(79,900원 56% 할인) · 무료배송 · 리뷰 12만9,983건 — 그대로',
 'living-basicton-comforter-set': '오늘의집 상품페이지 11/28 12:27 재확인: 76,800원(112,900원 31% 할인) · 무료배송 · 사계절/한파용 옵션 — 그대로',
 'baby-doubleheart-laundry-2plus2': '오늘의집 상품페이지 11/28 12:28 재확인: 26,900원(54,900원 51% 할인) · 배송비 3,000원(3만원 이상 무료) → 단독 구매 실결제 29,900원 — 그대로',
 'food-maeilbio-greek-yogurt-400x6': '무신사 상품페이지 11/28 12:29 재확인: 쿠폰적용가 17,040원(정가 40,000원 57% 할인) · 무진장 특가 · 후기 4.9(448건) — 그대로',
 'fashion-uniqlo-pufftech-vest-487348': '유니클로 상품페이지 11/28 12:23 재확인: 59,900원(S~4XL 전 사이즈 재고 있음) · 기간한정가격 11/27~12/3 — 그대로',
 'food-drink-sprite-350x24': '쿠팡 상품페이지 11/28 12:57 재확인: 정가 23,000원 → 9,980원(와우쿠폰 3,000원 적용, 100ml당 119원) · 로켓배송 · 와우회원 무료배송 · 11/29 새벽 도착 — 그대로',
}
for x in deals:
    if x['id'] in recheck:
        x.setdefault('refs', []).append(recheck[x['id']])

for x in deals:
    if x['id'] == 'food-maeilbio-greek-yogurt-400x6':
        x['shipping'] = '무료배송 (11/28 확인)'

# ---------- 3. flyeogii (여기어때) price update ----------
for x in deals:
    if x['id'] == 'travel-sugar-pension-dec3':
        x['price'] = 39000
        x['priceText'] = '39,000원 (회원 쿠폰 10,000원 적용)'
        x['was'] = '정가 49,000원 → 선착순 10,000원 쿠폰 적용 회원가 39,000원 (11/27 확인가 46,060원)'
        x['saving'] = '11/27 확인가(46,060원)보다 7,060원(15%) 저렴 · 같은 날짜 A동 전체 객실 동일 조건'
        x.setdefault('refs', []).append('여기어때 11/28 12:20 재확인: 12/3(목) 1박·2인 기준 A동 103호 39,000원(선착순 10,000원 쿠폰 적용 회원가, 정가 49,000원) · 부분환불 12/2 23:59까지 · 입실 15:00/퇴실 11:00 · 예약 가능')
        x['shipping'] = '객실 기준 2인(최대 2인) · 12/3(목) 1박 · 부분환불 12/2 23:59까지'

# ---------- 4. mat URL fix ----------
for x in deals:
    if x['id'] == 'living-priel-jacquard-mat':
        x['url'] = 'https://store.ohou.se/goods/2868834'
        x['linkLabel'] = '오늘의집에서 구매'
    if x['id'] == 'food-apple-busa-5kg':
        x['shipping'] = '무료배송(CJ택배) · 11/30(월) 출고'

# ---------- 5. new deals ----------
new = [
{
 "id": "food-tangerine-jeju-5kg-coupang",
 "category": "food",
 "subCategory": "fresh",
 "mall": "쿠팡",
 "tag": "100g당 198원",
 "title": "제주 노지감귤 당도선별 5kg 로얄과 (2·3·5·10kg 선택)",
 "price": 9900,
 "priceText": "9,900원 (쿠폰 1,000원 적용)",
 "unit": "100g당 198원",
 "was": "정가 표시 60,000원 → 쿠폰할인 9,900원 (100g당 198원)",
 "refs": [
   "쿠팡 상품페이지 11/28 12:45 확인: 5kg 로얄과 9,900원(쿠폰 1,000원 적용, 100g당 198원) · 무료배송(한진택배) · 12/3(목) 도착 예정 · 상품평 2,799건 · 판매자 전씨네가족(판매자평가 89%, 8,673건) · 원산지 제주도",
   "같은 페이지 옵션가: 2kg 4,900원(245원/100g) · 3kg 5,900원(197원/100g) · 10kg 16,300원(163원/100g)",
   "쿠팡 검색 11/28 12:44 5kg 로얄과 시세: 10,470원(209원/100g) · 12,900 · 13,130 · 14,900 · 15,500 · 16,050원(귤담원, 리뷰 8만6,167건) · 16,500원 — 100g당 209~330원",
   "타몰 11/28 12:20 비교: 옥션 올킬 타이벡 감귤 4.5kg 중대과 11,990원(100g당 266원) · 컬리 [KF365] 11brix 감귤 2.5kg 14,900원(100g당 596원) · [귤로장생] 타이벡 2.5kg 12,900원(516원)",
   "판매자 안내: '지금 귤은 초록 귤(극조생)' · 반손질·씨없음·냉장보관"
 ],
 "saving": "5kg 시세(13,130~16,050원)보다 3,230원 이상 저렴 · 100g당 198원은 옥션 4.5kg(266원)·컬리 2.5kg(516~596원)보다 낮음",
 "shipping": "무료배송(한진택배) · 12/3(목) 도착 예정",
 "note": "제주 노지 감귤(극조생·현재 초록귤) · 5kg 로얄과 · 2/3/5/10kg 옵션 · 씨없음 · 반손질",
 "how_to": "상품페이지 '쿠폰받기' 1,000원 적용 시 5kg 9,900원. 10kg은 16,300원으로 100g당 163원이 가장 저렴",
 "coupon_links": [{"label": "쿠팡 상품페이지(1,000원 쿠폰)", "url": "https://www.coupang.com/vp/products/9224935011?itemId=26630928643"}],
 "url": "https://www.coupang.com/vp/products/9224935011?itemId=26630928643",
 "linkLabel": "쿠팡에서 구매",
 "linkType": "product",
 "priceCondition": "상품 쿠폰 1,000원",
 "priceOffers": [
   {"mall": "옥션", "price": 11990, "condition": "타이벡 감귤 4.5kg 중대과 (100g당 266원)", "checkedOn": "2026-11-28", "shippingCost": 0},
   {"mall": "컬리", "price": 12900, "condition": "[귤로장생] 타이벡 제주 감귤 2.5kg (100g당 516원)", "checkedOn": "2026-11-28"}
 ],
 "shippingCost": 0
},
{
 "id": "food-banana-dole-1p2",
 "category": "food",
 "subCategory": "fresh",
 "mall": "쿠팡",
 "tag": "100g당 248원",
 "title": "돌(Dole) 필리핀산 바나나 1.2kg 내외",
 "price": 2980,
 "priceText": "2,980원",
 "unit": "100g당 248원",
 "was": "판매가 2,980원 (100g당 248원) · 로켓프레시",
 "refs": [
   "쿠팡 상품페이지 11/28 12:52 확인: 2,980원(100g당 248원) · 로켓프레시 · 상품평 41만570건 · 한 달 2만명 이상 구매 · 제조년월일 2026-11-27 · 내일(일) 11/29 새벽 7시 전 도착",
   "같은 페이지 옵션: 800g 1,990원(249원/100g) · 13kg 28,130원(216원/100g, 와우할인) · 1kg 2,980원(298원/100g)",
   "쿠팡 검색 11/28 12:50 바나나 시세: 델몬트 필리핀 1.4kg 4,090원(292원/100g) · 스미후루 필리핀 1.3kg 3,770원(290원) · 델몬트 허니글로우 1.2kg 3,300원(275원) · 스텔라나 베트남 1.2kg 3,980원(332원)",
   "11/28 아침 델몬트 1.4kg이 2,780원→4,090원으로 올라 제외된 과일 자리를 대체"
 ],
 "saving": "같은 날 델몬트 1.4kg(4,090원·292원/100g)보다 총액 1,110원, 100g당 44원(15%) 저렴",
 "shipping": "로켓프레시 · 무료배송 · 내일(일) 11/29 새벽 7시 전 도착(밤 12시 전 주문 시)",
 "note": "필리핀산 일반 바나나 · 1.2kg 내외 1송이 · 2026-11-27 입고분",
 "how_to": "쿠팡 2,980원 · 쿠폰 없이 이 가격 (돌 바나나는 로켓프레시 정상가)",
 "coupon_links": [],
 "url": "https://www.coupang.com/vp/products/6398359177?itemId=13671856774",
 "linkLabel": "쿠팡에서 구매",
 "linkType": "product",
 "priceOffers": [
   {"mall": "쿠팡", "price": 4090, "condition": "델몬트 필리핀 바나나 1.4kg (100g당 292원)", "checkedOn": "2026-11-28", "shippingCost": 0}
 ],
 "shippingCost": 0
},
]

# insert new fruit deals after the fresh-meat block (keep order: put right after 카카오/쿠팡 fresh block start)
idx = next(i for i, x in enumerate(deals) if x['id'] == 'food-pork-shoulder-suyuk-1kg') + 1
deals[idx:idx] = new

d['deals'] = deals

# ---------- 6. mallChecks ----------
d['mallChecks'] = [
 {"mall": "쿠팡", "status": "특가 발견", "checkedAt": "2026-11-28T12:57:00+09:00",
  "note": "골드박스 랜딩 + 과일 검색·상품페이지 직접 확인. 신규 2건: 제주 노지감귤 5kg 로얄과 9,900원(100g당 198원) · 돌 바나나 1.2kg 2,980원(248원). 스프라이트 350ml×24 9,980원(와우쿠폰)·탐사 액체세제 10L 9,980원 유지 확인. 아침 제외분(핫팩·코카콜라제로·블랙홀감귤·델몬트바나나·서귀포감귤)은 그대로 제외."},
 {"mall": "카카오 톡딜", "status": "특가 발견", "checkedAt": "2026-11-28T12:34:00+09:00",
  "note": "5건 상품페이지 재확인 전부 가격 동일: 목살 1kg 최대혜택 16,010 · 메가도스C 21,300(정가 35,000/톡딜가 23,900) · 오뚜기밥 36개 30,970(톡딜가 33,300) · 나랑드사이다 24캔 11,160(톡딜가 12,000) · 대건명가 국밥 6팩 24,650(톡딜가 28,500). 톡딜 기간 11/23 17:00~11/30 16:59."},
 {"mall": "지마켓", "status": "특가 발견", "checkedAt": "2026-11-28T12:18:00+09:00",
  "note": "상품페이지 2건 직접 확인. 사과 5kg 13,580원 유지(무료배송·평점 4.6/1,919건). 샤인머스켓 2kg는 7,160원→9,900원으로 2,740원 인상되어 제외(removedDeals 기록)."},
 {"mall": "옥션", "status": "특가 발견", "checkedAt": "2026-11-28T12:20:00+09:00",
  "note": "마니커 바사삭 4봉 상품페이지 확인: 쿠폰적용가 25,420원, 카드 7% 포함 23,640원으로 11/27과 동일. 올킬 탭에서 타이벡 감귤 4.5kg 11,990원·한상궁김치 겉절이 2kg 10,290원 등 확인했으나 감귤은 100g당 266원으로 쿠팡(198원)보다 비싸 제외."},
 {"mall": "오늘의집", "status": "특가 발견", "checkedAt": "2026-11-28T12:31:00+09:00",
  "note": "게재 중 9건 전부 상품페이지 재확인, 가격 변동 0건(발매트 9,900 · 트롤리 15,900 · 주방세제 8L 20,900 · 수비르 1+1 20,900 · 리스테린 21,300 · 필터샤워기 25,900 · 타월 10장 34,900 · 더블하트 2+2 26,900 · 베이직톤 이불 76,800). 발매트는 기획전 모음 주소에서 단품 주소(goods/2868834)로 교체. 더블하트는 배송비 3,000원 포함 29,900원으로 표기."},
 {"mall": "컬리", "status": "확인했으나 해당 특가 없음", "checkedAt": "2026-11-28T12:20:00+09:00",
  "note": "메인 특가관 확인. 감귤 [KF365] 2.5kg 14,900원(100g당 596원)·[귤로장생] 2.5kg 12,900원(516원)으로 쿠팡 5kg(198원)보다 2.6~3배 비쌈. 단독 구매 이득 상품 없음."},
 {"mall": "11번가", "status": "확인했으나 해당 특가 없음", "checkedAt": "2026-11-28T12:22:00+09:00",
  "note": "홈 특가관(시선집중·타임딜·긴급공수) 확인. 종가 포기김치 10kg 49,900원·올반 찰핫도그 20봉 17,990원·삼육 김밥김 4봉 14,040원 등은 있으나 동일 규격 쿠팡가 대비 우위 근거 없어 제외. 의류·브랜드 기획전 위주."},
 {"mall": "SSG닷컴", "status": "확인했으나 해당 특가 없음", "checkedAt": "2026-11-28T12:21:00+09:00",
  "note": "메인 '관심 급상승' 섹션 확인 — 신세계백화점·트레이더스 명품/건강식품 위주, 생필품·먹거리 단독 특가 없음."},
 {"mall": "네이버쇼핑", "status": "확인 실패", "checkedAt": "2026-11-28T12:21:00+09:00",
  "note": "search.shopping.naver.com HTTP 418(자동화 차단), shopping.naver.com 로그인 요구 — 웹에서 실시간 가격 확인 불가. 가격 비교는 각 후보의 쿠팡·옥션·컬리 상품페이지 직접 조회로 대체."},
]

d['updatedAt'] = NOW
d['checkedAt'] = NOW
d['date'] = '2026-11-28'

json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print('deals:', len(d['deals']), 'mallChecks:', len(d['mallChecks']), 'removed:', len(d['removedDeals']))
from collections import Counter
print(Counter(x['mall'] for x in d['deals']))
print(Counter(x['category'] for x in d['deals']))
