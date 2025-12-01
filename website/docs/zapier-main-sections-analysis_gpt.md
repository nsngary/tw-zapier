# Zapier.com 首頁技術分析報告

## 整體頁面架構概覽
- 導覽列：主導覽（Products/Solutions/Resources/Enterprise/Pricing）、次導覽（Explore apps/Contact sales）、登入/註冊
- Hero（MegaIntro）：標語「Scale AI agents with Zapier」、H1「The most connected AI orchestration platform」、雙 CTA
- Product gallery（toolkit tabs）：可水平捲動的 Tablist（AI Workflows/Agents/Chatbots/Tables/Interfaces/Canvas/Enterprise/Functions/8,000 apps）+ 內容卡片 + 模板滑軌
- Logos Ticker：Trusted by 3.4 million companies（品牌 Logo 連續滑動）
- Customer Stories（輪播卡）：Okta/Vendasta/Arden/Contractor Appointments/Pretto/Laudable（Prev/Next）
- Scale AI（結果導向敘事 + 計數器 + 圖表）
- Feedback Strip：Learn It Live 成效條 + CTA
- Explore Zapier’s AI Tools：四張功能卡（Workflows / Agents / Chatbots / Canvas）
- AI Use Cases：可切換的用例 Tab（IT Help Desk / Enrich Leads / Sales ops），含 Pause 控制
- AI + automation：整合平台敘事 + 4 個導向卡（Workflows/Tables/Interfaces/Templates）+ 引言
- Move fast. Stay in control.：治理/安全賣點 + 大量企業 Logo + 3 入口（Enterprise features / Security / Get a demo）+ 見證
- Before/After：二分對照（Bear the bottleneck vs Or use Zapier）+ CTA
- Security Section：合規徽章 + 六大安全能力 + CTA
- Enterprise CTA：終局轉換（Start free / Contact Sales）
- Footer：大量 SEO 內鏈區（Top searches / Popular apps / Trending apps / Top apps by category / Our best content）+ 法務/社群

## 技術棧識別
- 應用框架：Next.js（hasNext: true；_next/ 資產）、Vercel（assetPrefix 指向 pagebuilder-*）
- 視覺/內容管理：Builder.io Pagebuilder（layoutData/component 與 screenshot 標記）
- 設計系統：Zapier Design System（大量 [data-zds] 組件，zds reset 與 tokens）
- 字體：Degular / Degular Display / GT Alpina（Cloudinary / fonts.zapier.com）
- 圖像/資產：Cloudinary（f_auto/q_auto）、SVG 與位圖並用
- 分析/追蹤：Google Tag Manager（GTM-K7GFJTV）、Intercom、TikTok Pixel

## 效能指標分析（Desktop — 擬合觀察）
- 圖像最佳化：Cloudinary + f_auto/q_auto；SVG 優先；多 Logo 以矢量載入
- 版面關鍵 CSS：以原子化樣式（hash 類名，如 .css-10oo67n）與 ZDS tokens 實作；首屏 Hero + Tabs 為關鍵渲染
- 懶載入：非首屏圖片/卡片多以 lazy/延後載入；滑軌內容隨可見切換
- JS 交互：Tablist/Carousel 為核心，具鍵盤可用性（aria-selected/tablist/tab）
- SEO：結構化標題階層、海量內鏈區塊、可爬行的內容鏈接

---

## 區塊詳細分析

### 1. MegaIntro
#### HTML 結構
- 標題層級：h1「The most connected AI orchestration platform」
- 副標/說明：p「Build and ship AI workflows in minutes…」
- 眼眉文案：「Scale AI agents with Zapier」
- CTA：兩個 a 按鈕（/sign-up 與 /google-sso/start…）

示例：
```html
<section aria-labelledby="hero-title">
  <p class="eyebrow">Scale AI agents with Zapier</p>
  <h1 id="hero-title" class="css-fi5d4">The most connected AI orchestration platform</h1>
  <p class="css-7y2k4q">Build and ship AI workflows in minutes—no IT bottlenecks…</p>
  <div class="css-gzsfdz">
    <a class="css-10oo67n" href="/sign-up">Start free with email</a>
    <a class="css-e1e01w" href="/google-sso/start?...">
      <span class="css-10oo67n" data-variant="secondary">Start free with Google</span>
    </a>
  </div>
</section>
```

#### CSS 樣式分析（關鍵類）
- .css-fi5d4：Degular Display, font-size 40→64px, line-height 0.9, text-wrap: balance
- .css-7y2k4q：max-width: 400→576px, font-size 16→18px, letter-spacing -0.01em
- .css-10oo67n：主 CTA，height 44→48px，font-weight: 600，背景 #FF4F00，focus-visible 外框

#### JavaScript 功能
- 無需重 JS；主要為 CTA 事件與 A/B 內容載入（由 Builder/Next 注入）

#### 動畫效果
- Hero 無重動畫；重點在下方 Tabs/數字動畫

#### TW_Zapier 適用建議
- Nuxt3 + Tailwind：以容器 max-w-7xl、grid lg:grid-cols-2
- 按鈕：使用自訂 Tailwind 元件（bg-[#FF4F00] hover:bg-[#D24304] focus-visible:ring-2）
- 字體：以 Degular 替代或本地備援（Inter）

---

### 2. CustomersStories
#### HTML 結構
- 區塊標題：h2「For the Fortune 500 and first-time founders」，眼眉「CUSTOMER STORIES」
- 卡片輪播：公司 Logo、引言、KPI 指標、CTA「Read full story」

示例（單卡）：
```html
<article class="css-1gqjtkw card" aria-roledescription="slide">
  <header><img alt="Okta" /></header>
  <blockquote class="css-folndw">Zapier lets us spin up and test automations…</blockquote>
  <footer>
    <p>— Korey Marciniak…</p>
    <dl class="metrics"><div><dt>13%</dt><dd>…automated…</dd></div></dl>
    <a href="https://zapier.com/..." class="cta">Read full story</a>
  </footer>
</article>
```

#### CSS 樣式技術
- 滑軌容器：.css-s88hxx；軌道：.css-oudvll（transform: translateX; transition cubic-bezier）
- 卡片：邊框 #C5C0B1、背景 #F8F4F0、間距在 lg 放大

#### JavaScript 功能
- Prev/Next 按鈕（disabled 狀態）、滑動動畫；建議 ARIA：aria-live="polite"、aria-label 指示目前頁

#### 動畫與視覺效果
- translateX + opacity 切換；KPI 數字靜態顯示

#### TW_Zapier 適用建議
- 用 Swiper（SSR 安全）或自建滑軌（GSAP Draggable/ScrollTrigger）
- A11y：WAI-ARIA carousel 模式（aria-roledescription="carousel"）

---

### 3. ScaleAI（No AI hype here. Just results.）
#### HTML 結構
- 眼眉「Scale AI the Easy Way」+ h2 主標
- 巨量計數區：多組 0–9 的列，組合成累進數字（AI tasks automated...）
- 描述性圖表（img）+ 里程碑標記（Jan 2023 / Today）

#### CSS/JS 重要點
- 計數列：連續 digit 欄位（多個 generic/數字元素），可能以步進動畫堆疊
- JS：以 requestAnimationFrame 或 IntersectionObserver 觸發；可用 GSAP timeline 實作數字滾動

示例（TW_Zapier，GSAP）：
```js
import { gsap } from 'gsap'
import ScrollTrigger from 'gsap/ScrollTrigger'
gsap.registerPlugin(ScrollTrigger)

onMounted(() => {
  const cols = document.querySelectorAll('.odometer-col')
  cols.forEach((col, i) => {
    gsap.fromTo(col, { yPercent: 0 }, {
      yPercent: -900, duration: 2 + i * 0.2, ease: 'power2.out',
      scrollTrigger: { trigger: col, start: 'top 80%', once: true }
    })
  })
})
```

#### TW_Zapier 適用建議
- 封裝成 <ScaleAI> 元件，props 控制目標數字；SSR 僅在 client 啟動動畫

---

### 4. FeedbackStrip（Learn It Live）
#### HTML/CSS/JS
- 單列卡：品牌圖標 + 文案 + CTA（Read customer story）
- 以 Flex 橫向、lg 時圖文分佈
- JS 僅連結行為，圖像 lazy loading

#### TW_Zapier 建議
- Nuxt Img（@nuxt/image）或原生 <img loading="lazy">；卡片通用化

---

### 5. ExploreAITools
#### HTML 結構
- h2「EXPLORE ZAPIER’S AI TOOLS」+ 四卡（Workflows/Agents/Chatbots/Canvas）
- 每卡：icon/img + 標題 + 副標 + Explore CTA

#### CSS/互動
- 卡片 hover 邊框/陰影；網格在 md/lg 斷點調整

#### TW_Zapier 適用建議
- 建立工具卡資料陣列，v-for 渲染；Focus ring 與鍵盤順序

---

### 6. AIUseCases
#### HTML/ARIA
- 眼眉「AI Use Cases」+ h2 主標 + 說明
- role="tablist" + 多個 button[role="tab"]（.css-1rxg4ds），aria-selected 切換
- 內容面板（tabpanel）含「Pause」按鈕與模板 CTA

#### CSS/JS
- Tab 水平捲動（mobile），centered（lg）
- JS 切換選單與面板，維持 tabindex 與 aria-controls 關聯

示例（切換）：
```js
const active = ref(0)
function onKey(e){ /* ArrowLeft/Right 切換索引，更新 aria-selected */ }
```

#### TW_Zapier 建議
- 依 WAI-ARIA Tabs 實作；提供 Pause 控制關閉自動輪播

---

### 7. AIPlusAutomation（AI + automation, all in one place）
#### HTML/布局
- 左側敘事 + 右側大圖（lg）
- 下方 4 導向卡（Workflows/Tables/Interfaces/Templates）

#### CSS/互動
- 卡片含縮圖、兩行文案、Explore CTA；hover 陰影/位移

#### TW_Zapier 建議
- 卡片元件複用（與 ExploreAITools 共用樣式基底）

---

### 8. MoveFast（Move fast. Stay in control.）
#### HTML/內容
- h2 拆行樣式（Move fast. / Stay in control.）+ 說明
- 大量品牌 Logo（多列 Grid）
- 六項治理/安全賣點 + 三個 CTA（Enterprise features / Security and Compliance / Get a demo）
- Okta 引言卡

#### CSS/動畫
- Logo 以等比縮放；可作連續無限滾動（marquee）或靜態 grid

#### TW_Zapier 建議
- 企業治理重點按 TW_Zapier 能力對照（RBAC、審計、SSO、觀測性），各以 icon + 文案

---

### 9. BeforeAfter（Want AI automation IT and innovators agree on?）
#### HTML/互動
- 左右二分敘事；右側「Or use Zapier」以 ①②③ 步驟
- CTA「Start automating today」

#### 動畫
- 使用 Builder 組件名稱顯示為 BeforeAfterAnimation；TW_Zapier 可用 CSS clip-path 或 GSAP reveal

示例（GSAP reveal）：
```js
gsap.from('.after', { xPercent: 20, opacity: 0, duration: 0.6, scrollTrigger: { trigger: '.before-after', start: 'top 80%', once: true }})
```

---

### 10. SecuritySection
#### HTML/內容
- 眼眉「Security」+ h2 主標 + 說明
- 合規徽章（SOC 2/3, GDPR, CCPA, GDPR UK）
- 六大安全能力卡（Icons+Title+Desc）
- CTA「Get started with secure AI automation」

#### CSS/無障礙
- 徽章 img 需完整 alt；卡片語義可用 section + h3

#### TW_Zapier 建議
- 安全頁連結與法遵聲明對應至文件；以 @nuxt/image 最佳化徽章載入

---

### 11. EnterpriseCTA
#### HTML/內容
- h2 + 說明 + 兩個主轉換 CTA（Start free / Contact Sales）

#### TW_Zapier 建議
- 保持與 Hero CTA 一致樣式；次要鈕為邊框樣式

---

## 整體設計模式總結
1) 眼眉（Eyebrow）+ 強主標（Degular Display）+ 次敘事：建立清晰層級、極少 JS 依賴
2) 可滾動 Tablist + 內容區：ARIA 完整、mobile-first 的水平捲動
3) 卡片化導向（Icon/Title/Desc/CTA）復用：一致 hover/focus、可鍵盤操作
4) 數字/圖表敘事：以 GSAP 或 CSS transitions 建立即視覺衝擊
5) SEO 內鏈區：大量類目清單提升可見度與爬蟲效率

## TW_Zapier 實作建議
- Nuxt 3 + Tailwind：以 tokens 落地（Primary #86735E / Accent #C2474A / Support #667539）；Hero/CTA 與卡片建立設計系統
- 動畫：以 plugins/anim/ 下封裝 GSAP + ScrollTrigger，提供 useMotion* composables；提供 reduced-motion 降級
- 可及性：WAI-ARIA Tabs/Carousel/Accordion 模式；Focus ring（ring-2 ring-offset-2）
- 圖片：Nuxt Image + AVIF/WEBP；Cloudinary 可選
- 組件化：11 區塊皆重構為純元件（不依賴全域狀態），在 pages/index.vue 依序引入

## 技術債務與改進機會（相對於初版）
- 輪播/Tab A11y：需補齊 aria-* 與鍵盤導覽、Pause 控制
- 動畫降級：prefers-reduced-motion 支援
- 代碼拆分：首屏 ≤ 180KB gzip；延後載入非關鍵腳本
- 安全頁素材：合規徽章需具備高對比與 alt
- 國際化：文案分離與 i18n 構建

---

# 依據與證據（來自 Playwright / 抓取）
- 主要標題與區塊：
  - H1: "The most connected AI orchestration platform"
  - H2: "Your complete toolkit for AI automation", "For the Fortune 500 and first-time founders",
    "No AI hype here. Just results.", "EXPLORE ZAPIER’S AI TOOLS", "Real teams, real AI workflows, real results",
    "AI + automation, all in one place", "Move fast. Stay in control.",
    "Want AI automation IT and innovators agree on?", "Zapier is secure automation that sticks",
    "Ready to transform how your enterprise uses AI?"
- 關鍵 CSS 類（擷取）：.css-fi5d4（H1）、.css-7y2k4q（副標）、.css-10oo67n（主 CTA）、.css-1rxg4ds（Tab 按鈕）、
  .css-s88hxx（stories 容器）、.css-oudvll（stories 軌道）
- 第三方與平台：Next.js（_next 資產）、Builder.io（pagebuilder-*）、GTM、Intercom、Cloudinary 圖片

（註）實際 SVG path、更多類名與屬性可於後續補充文件中擴充，並以 adapters 封裝動畫細節。
