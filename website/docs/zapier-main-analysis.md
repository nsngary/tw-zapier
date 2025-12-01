# Zapier 首頁 main 區塊結構分析（2025-08 快照）

- 來源：https://zapier.com/
- 抓取方式：web-fetch + 人工瀏覽核對
- 目的：拆解 main 內子區塊、結構語義、樣式與互動，作為 TW_Zapier 官網復刻與在地化的實作基準

## 一、主結構與區塊索引

1) Hero（首屏）
- 內容：Eyebrow（Scale AI agents…）、H1（The most connected AI orchestration platform）、支援說明段落、雙 CTA（Primary + Secondary）、社會性證明小標（"Your complete toolkit for AI automation"）
- 版面：左右兩欄（lg: grid-cols-[576px,1fr]；sm: 單欄 centered），外框有 container 與邊框分隔線
- 互動：按鈕 focus ring、hover 色階，背景無重動畫（僅內容漸入）

2) 產品導覽 Tabs（toolkit/產品索引帶輪播預覽）
- 水平分頁標籤：AI Workflows / AI Agents / AI Chatbots / Tables / Interfaces / Canvas / Enterprise / Functions / 8,000 apps
- 右側/下方：對應分頁之說明文案 + 動畫媒體（圖/影片）
- 互動：水平滾動 tabs（mobile 可橫向捲動、選中 tab 有下劃線 bar）、右側媒體淡入切換，"Get started fast with pre-built templates" 卡片橫向滑動列表

3) Trusted by（Logo Marquee）
- 文案：Trusted by 3.4 million companies
- 互動：水平無限捲動的 logo 列（CSS keyframes + translateX）、hover 暫停

4) Customer stories（客戶案例）
- 結構：左/右兩欄卡片；上半部 logo + 引言，底部 KPI（百分比、時間節省等）
- 互動：卡片 hover 陰影，文字/圖像無複雜動態；RWD 時堆疊為單欄

5) Security section（資安）
- 元件化輸出（自訂組件名稱 SecuritySection），含標章（SOC2、GDPR、CCPA、GDPR UK）與重點功能（Access Control、Uptime/SLA、Observability 等）
- 互動：卡片 hover 邊框深色；CTA 區塊

6) Enterprise CTA（收尾行動）
- 文案：Ready to transform how your enterprise uses AI?
- 互動：雙 CTA（Start free / Contact Sales），簡潔居中

> 註：頁尾 footer 與全域 header 已在前置任務處理，此處僅聚焦 main。

## 二、語義化對照與 BEM/語義 class 規劃

- <main class="site-main">：主內容容器
  - <section class="hero"> … </section>
  - <section class="product-switch"> … </section>
  - <section class="logo-marquee" aria-labelledby="trusted-heading"> … </section>
  - <section class="customer-stories" aria-labelledby="stories-heading"> … </section>
  - <section class="security" aria-labelledby="security-heading"> … </section>
  - <section class="enterprise-cta" aria-labelledby="enterprise-cta-heading"> … </section>

命名原則：BEM 或語義式混用，結合 Tailwind utilities。例：customer-stories__card、security__feature-list。

## 三、樣式要點（Tailwind 對照）
- 容器：max-w-[1280px] px-5 sm:px-10 border-x border-neutral-200（Zapier 的邊界線視覺）
- 色彩：
  - Primary #86735E（TW_Zapier 主色，用於邊框/強調）
  - Accent #C2474A（行動/重點）
  - Support #667539（次要強調）
- 文字：Noto Sans TC（已在 nuxt.config.ts 設定）
- 動畫：
  - 進場：animate-fade-in-up
  - Logo Marquee：@keyframes scroll-x（已存在 index.vue，可複用）
  - prefers-reduced-motion: reduce → 停用動畫

## 四、互動要點（a11y）
- Tabs：role="tablist" / role="tab" / aria-selected / aria-controls；鍵盤左右切換
- CTA：:focus-visible ring-2 ring-offset-2，顏色符合對比
- 圖片：alt 文案完整；裝飾圖 aria-hidden

## 五、TW_Zapier 對應實作計畫（元件切片）

- Sections（components/sections）：
  1. ProductSwitchTabs.vue（若沿用 index.vue 現有 tabs，可保留）
  2. LogoMarquee.vue（本次新增）
  3. CustomerStories.vue（本次新增）
  4. SecuritySection.vue（本次新增）
  5. EnterpriseCTA.vue（本次新增）

- 置入順序建議：Hero → ProductSwitchTabs → LogoMarquee → CustomerStories → SecuritySection → EnterpriseCTA → Footer

## 六、驗收標準（對應 Testing & Validation rev B）
- 結構：對照 zapier_home.html，以上 6 區皆存在且層級/語義正確
- 互動：
  - Tabs 可鍵盤操作；ARIA 屬性正確
  - Logo Marquee 可 hover 暫停；reduced-motion 時靜止
- 視覺回歸：Hero / Enterprise CTA / Tabs / Marquee 各一張黃金圖，差異 ≤ 0.1%
- Lighthouse（Desktop）：Perf ≥ 90 / A11y ≥ 90 / BP ≥ 90 / SEO ≥ 95
- 首屏 JS ≤ 180KB gzip（保持現狀，不引入大型新依賴）

## 七、差異與在地化策略
- Zapier 的分頁標籤眾多，TW_Zapier 可精簡為 4–5 項（已在 index.vue 實作雛形）
- Customer stories 以台灣產業案例替換（目前先用佔位）
- Security 保留通用措辭與結構，細節連結導向 /security-compliance（未來自製頁）

---

本檔將作為後續 e2e 測試與 diff-report 的對照基準。
