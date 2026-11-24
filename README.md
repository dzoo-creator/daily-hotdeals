# 오늘의 핫딜

매일 아침 육아·생활·음식 핫딜을 모아 보여주는 정적 웹앱입니다. 아이폰 사파리에서 열고 **홈 화면에 추가**하면 앱처럼 쓸 수 있습니다.

## 구성

| 파일 | 역할 |
| --- | --- |
| `index.html` | 화면 전체 (CSS·JS 포함, 빌드 과정 없음) |
| `deals.json` | 딜 데이터. **이 파일만 갱신하면 화면이 자동 반영됩니다.** |
| `.nojekyll` | GitHub Pages에서 Jekyll 처리를 건너뛰게 함 |

## 딜 갱신 방법

1. `deals.json`의 `date`, `updatedAt`, `deals` 배열을 고칩니다.
2. `main` 브랜치에 커밋·푸시하면 GitHub Pages에 반영됩니다(보통 1분 이내).
3. `index.html` 안의 `<script id="fallback-deals">` 는 오프라인·파일 직접 열기용 사본입니다. 딜을 크게 바꿨다면 이 사본도 같은 내용으로 맞춰 주세요.

## deals.json 필드

```json
{
  "schemaVersion": 1,
  "date": "2026-11-25",
  "updatedAt": "2026-11-25T08:50:00+09:00",
  "malls": ["쿠팡", "무신사"],
  "deals": [
    {
      "id": "food-coke-190-30",
      "category": "food",
      "mall": "쿠팡",
      "tag": "골드박스",
      "title": "코카콜라 오리지널 190ml 30개",
      "price": 13280,
      "priceText": "13,280원",
      "unit": "캔당 443원",
      "was": "평소 16,200원대",
      "refs": ["역대 최저 13,180원"],
      "saving": "역대 최저가에 100원 차이",
      "shipping": "무료배송",
      "note": "190ml × 30캔",
      "url": "https://www.coupang.com/...",
      "linkLabel": "쿠팡에서 구매",
      "linkType": "product"
    }
  ]
}
```

- `category`: `baby` | `living` | `food`
- `price`: 숫자. 행사처럼 가격이 없으면 `null` + `priceText`에 문구
- `was`: 취소선으로 보여줄 평소가 (없으면 `null`)
- `refs`: 비교 기준 문구 배열 (기존 최저가·타몰 최저가 등)
- `saving`: 할인 근거 한 줄 (없으면 `null`)
- `shipping`: `무료배송`, `로켓배송` 등 (없으면 `null`)
- `linkType`: `product`(상품 페이지) | `search`(몰 검색 링크) | `app`
- `malls`: 쇼핑몰 필터 칩 순서

## 화면 기능

- 카테고리 탭: 전체 / 육아 / 생활 / 음식 / 찜한 딜
- 쇼핑몰 필터 칩, 상품명·브랜드·몰 검색
- 찜하기(하트)는 브라우저 localStorage에 저장
- `deals.json`을 못 불러오면 내장 데이터로 표시(오프라인 대응)
