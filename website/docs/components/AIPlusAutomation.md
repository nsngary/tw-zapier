# AIPlusAutomation 組件

## 概述

`AIPlusAutomation.vue` 組件是基於 Zapier.com 的「AI + automation」區塊設計的 Vue 3 組件，專為 TW_Zapier 平台設計。該組件展示了 AI 與自動化的整合能力，通過三個主要區塊來呈現平台的核心價值。

## 功能特點

### 🎯 核心功能
- **三區塊結構**: 標題介紹 + 產品功能卡片 + 客戶分享
- **產品功能展示**: 四個主要產品功能的卡片展示
- **響應式設計**: 適配桌面和移動設備
- **互動效果**: hover 效果和平滑過渡動畫
- **導航整合**: 使用 NuxtLink 進行頁面導航

### 📱 響應式設計
- 桌面版：2x2 網格布局
- 移動版：單列堆疊布局
- 自適應間距和字體大小

### 🎨 視覺設計
- 使用 TW_Zapier 設計系統的顏色配置
- 白色卡片配淺灰背景
- 微妙的邊框和陰影效果
- 一致的間距和字體層次

## 組件結構

```vue
<template>
  <section class="ai-plus-automation">
    <!-- 第一區塊：標題介紹 -->
    <div class="grid lg:grid-cols-2">
      <header>
        <p class="eyebrow">AI × 自動化</p>
        <h2>AI × 自動化，集中在同一平台</h2>
        <p class="description">...</p>
      </header>
      <img src="..." alt="插圖" />
    </div>

    <!-- 第二區塊：產品功能卡片 -->
    <div class="grid md:grid-cols-2 gap-6">
      <NuxtLink class="card">
        <img src="..." alt="圖標" />
        <h3>功能標題</h3>
        <p>功能描述</p>
        <div class="cta">探索功能</div>
      </NuxtLink>
      <!-- 重複其他卡片 -->
    </div>

    <!-- 第三區塊：客戶分享 -->
    <div><!-- 待完善 --></div>
  </section>
</template>
```

## 產品功能卡片

### 1. Workflows (工作流程)
- **標題**: 設計具有邏輯分支和 AI 處理的多步驟工作流程
- **描述**: TW_Zapier 工作流程讓最複雜的自動化變得簡單易用
- **連結**: `/workflows`
- **圖標顏色**: `accent-ball` (#bd743a)

### 2. Tables (表格)
- **標題**: 儲存和管理驅動自動化的數據
- **描述**: TW_Zapier 表格將所有自動化數據集中在一個地方
- **連結**: `/tables`
- **圖標顏色**: `accent-ball` (#bd743a)

### 3. Interfaces (界面)
- **標題**: 創建任何人都可以使用的自定義界面—無需編程
- **描述**: TW_Zapier 界面為任何工作流程提供自定義前端
- **連結**: `/interfaces`
- **圖標顏色**: `accent-ball` (#bd743a)

### 4. Templates (模板)
- **標題**: 從個人生產力擴展到公司級工作流程
- **描述**: 使用我們預建的模板來啟發您的下一個系統
- **連結**: `/templates`
- **圖標顏色**: `accent-ball` (#bd743a)

## 樣式類別

### 主要 CSS 類別
- `.ai-plus-automation`: 主容器
- `.section-padding`: 區塊內距
- `.container-custom`: 內容容器
- `.grid lg:grid-cols-2`: 響應式網格布局

### 卡片樣式
- `.group`: 群組 hover 效果
- `.bg-white`: 白色背景
- `.rounded-2xl`: 圓角邊框
- `.border border-neutral-200`: 淺灰邊框
- `.hover:border-primary-300`: hover 時主色邊框
- `.hover:shadow-lg`: hover 時陰影效果

### 互動效果
- `.transition-all duration-300`: 平滑過渡
- `.group-hover:text-primary-600`: 群組 hover 時文字顏色
- `.group-hover:translate-x-1`: 群組 hover 時箭頭移動

## 使用方式

### 基本使用
```vue
<template>
  <AIPlusAutomation />
</template>

<script setup>
import AIPlusAutomation from '@/components/sections/AIPlusAutomation.vue'
</script>
```

### 在頁面中使用
```vue
<template>
  <div>
    <!-- 其他內容 -->
    <AIPlusAutomation />
    <!-- 其他內容 -->
  </div>
</template>
```

## 依賴項目

- Vue 3 Composition API
- Nuxt 3 (NuxtLink)
- Tailwind CSS
- 設計系統顏色配置

## 圖標資源

組件需要以下圖標文件（位於 `/public/images/`）：
- `workflows-icon.svg` - 工作流程圖標
- `tables-icon.svg` - 表格圖標
- `interfaces-icon.svg` - 界面圖標
- `templates-icon.svg` - 模板圖標
- `hp-ai-automation_orange_il5u6h.png` - 主插圖

## 瀏覽器支援

- 現代瀏覽器（Chrome, Firefox, Safari, Edge）
- 支援 CSS Grid 和 Flexbox
- 支援 CSS Transitions

## 效能考量

- 圖片懶加載：使用 `loading="lazy"` 屬性
- 平滑過渡：使用 CSS transitions 而非 JavaScript 動畫
- 響應式圖片：建議使用適當的圖片格式和大小

## 無障礙功能

- 語義化 HTML 結構
- 適當的 heading 層次
- 圖片 alt 文字
- 鍵盤可操作的連結
- 適當的顏色對比度

## 未來改進

1. **第三區塊完善**: 添加客戶分享內容
2. **動畫增強**: 添加進場動畫效果
3. **圖標優化**: 使用 SVG 組件替代圖片
4. **內容管理**: 將卡片數據提取為外部配置
5. **國際化**: 支援多語言內容

## 設計參考

本組件基於 Zapier.com 的「AI + automation, all in one place」區塊設計，保持了原版的：
- 清晰的信息層次
- 一致的視覺風格
- 直觀的用戶體驗
- 有效的內容組織

同時針對 TW_Zapier 進行了本地化調整：
- 繁體中文內容
- 符合台灣用戶習慣的描述
- 本地化的功能命名

## 更新日誌

### v1.1.0 (2025-01-18)
- **圖標顏色更新**: 將所有4個產品功能卡片的 SVG 圖標顏色從 `#ff4f00` 更改為 `accent-ball` (`#bd743a`)
- **設計一致性**: 統一使用 TW_Zapier 設計系統中的 accent-ball 顏色
- **視覺改進**: 提升品牌一致性和視覺和諧度

### v1.0.0 (2025-01-18)
- **初始版本**: 基於 Zapier.com AI + automation 區塊的完整實現
- **四個產品功能卡片**: Workflows, Tables, Interfaces, Templates
- **響應式設計**: 支援桌面和移動設備
- **互動效果**: hover 動畫和過渡效果
