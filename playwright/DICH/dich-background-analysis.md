# DICH 背景漸變動畫分析（初稿）

來源：https://dich-fashion.webflow.io/

本次分析以 Playwright 取樣不同 scrollY，觀測背景相關元素（包含 body 及 className 包含 bg/texture/noise 的候選）之樣式變化、是否載入動畫庫（GSAP/WAAPI），並記錄顏色與觸發點。初步數據如下：

- 頁面總高度（近似）：8097px
- 取樣位置（px）：0, 400, 800, 1200, 1600, 2000, 2600, 3200, 3800, 4400, 5000
- 觀測到的 body 背景色：全程固定為 rgb(255, 223, 196)
- 觀測到的候選最大背景元素：body（未觀測到明顯覆蓋全屏之 .texture-bg/.noise 等元素的背景顏色改變）
- 動畫庫：頁面 console 有載入 Unicorn Studio（Webflow 生態動畫），未偵測到 gsap.globalTimeline。WAAPI 動畫數量未顯示，但未對 body 背景顏色造成明顯變化。

初步推斷：
- DICH 的背景「視覺變化」主要由前景 Three.js/Canvas/WebGL 場景與混合模式、遮罩或圖片堆疊造成，非單純 body 背景色或單一 .texture-bg 的 CSS 漸變。
- 首屏背景基色為淡膚色（rgb(255,223,196) ≈ #FFDFC4）。滾動過程中整體色感變化可能來自前景素材與段落區塊的 overlay，而非直接切換 body 背景色。

建議的復刻策略：
1. 使用品牌色系作為「背景層」的基底漸變，並以滾動觸發進行顏色插值：
   - Primary: #86735E（棕灰）
   - Accent: #C2474A（磚紅）
   - Support: #667539（橄欖綠）
   - 可加入淡膚色 #FFDFC4 作為過渡色，提升與原站相似的柔和度。
2. 使用 GSAP + ScrollTrigger（或原生 IntersectionObserver + requestAnimationFrame）在特定分段（如每 100vh 或內容段落）間進行背景線性或 easeInOut 漸變。
3. prefers-reduced-motion 時，關閉 ScrollTrigger 的 scrub，改為段落切換時瞬間變色或短時間（≤120ms）過渡。

偵測與限制說明：
- 本次以 CSS 計算樣式方式觀測，若原站以 Canvas/WebGL 做主視覺，CSS 背景不會反映出色彩變化，需另以取樣畫面像素或擷取 Canvas shader 參數的方式深入分析（屬進階階段）。

接下來動作：
- 於 playwright/DICH 建立 mockup（HTML/CSS/JS），以 GSAP/ScrollTrigger 實現滾動驅動的背景色漸變，並提供 prefers-reduced-motion 降級。
- 將 mockup 原理封裝至官網 components/BackgroundTest.vue，與 Tailwind 設計系統整合。

