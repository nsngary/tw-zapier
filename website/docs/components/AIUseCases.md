# AIUseCases 組件

## 概述

`AIUseCases.vue` 組件是基於 Zapier.com AI Use Cases 區塊的分析而製作的 Vue 3 組件，專為 TW_Zapier 平台設計。該組件展示了 AI 自動化的實際應用案例，使用標籤頁界面來展示不同的使用場景。

## 功能特點

### 🎯 核心功能
- **標籤頁界面**: 三個標籤頁展示不同的 AI 應用案例
- **動態內容切換**: 點擊標籤頁時內容平滑切換
- **視頻播放控制**: 每個案例都有對應的演示視頻
- **鍵盤導航**: 支援方向鍵在標籤頁間切換
- **無障礙設計**: 完整的 ARIA 標籤和鍵盤操作支援

### 📱 響應式設計
- 桌面版：左右分欄布局（內容 + 視頻）
- 移動版：上下堆疊布局
- 標籤頁在小螢幕上自動調整

### 🎨 視覺設計
- 使用 TW_Zapier 設計系統的顏色配置
- 漸層背景和陰影效果
- 平滑的過渡動畫
- 一致的間距和字體大小

## 組件結構

```vue
<template>
  <section class="ai-use-cases">
    <!-- 區塊標題 -->
    <div class="text-center mb-12">
      <p class="eyebrow">AI 應用案例</p>
      <h2>真實團隊，真實 AI 工作流程，真實成果</h2>
      <p class="description">...</p>
    </div>

    <!-- 標籤頁導航 -->
    <div class="tabs">
      <button v-for="item in useCases" role="tab">
        {{ item.title }}
      </button>
    </div>

    <!-- 內容區域 -->
    <div class="content">
      <div class="grid lg:grid-cols-2">
        <!-- 左側內容 -->
        <div class="content-left">
          <h3>{{ item.header }}</h3>
          <p>{{ item.description }}</p>
          <BaseButton>使用此模板</BaseButton>
        </div>

        <!-- 右側視頻 -->
        <div class="content-right">
          <video :src="item.video" />
        </div>
      </div>
    </div>
  </section>
</template>
```

## 數據結構

### UseCase 介面
```typescript
interface UseCase {
  id: string          // 唯一識別碼
  title: string       // 標籤頁標題
  header: string      // 內容區標題
  description: string // 描述文字
  link: string        // 模板連結
  video?: string      // 視頻檔案路徑（可選）
}
```

### 預設案例數據
```typescript
const useCases: UseCase[] = [
  {
    id: 'it-helpdesk',
    title: 'IT 服務台',
    header: '讓 AI 自動回應工單',
    description: 'Remote.com 的 3 人 IT 團隊透過 AI 自動處理 28% 的公司請求...',
    link: '/templates/it-helpdesk',
    video: '/video/it-helpdesk-demo.mp4'
  },
  // ... 其他案例
]
```

## 主要功能

### 1. 標籤頁切換
- `setActiveTab(tabId: string)`: 設置活動標籤頁
- 自動暫停其他視頻並播放當前視頻
- 平滑的內容過渡效果

### 2. 鍵盤導航
- `handleTabKeydown(event, index)`: 處理鍵盤事件
- 支援左右方向鍵切換標籤頁
- 自動聚焦到新的標籤頁按鈕

### 3. 視頻控制
- `toggleVideo()`: 播放/暫停視頻
- 自動播放當前標籤頁的視頻
- 支援靜音和循環播放

### 4. 生命週期管理
- `onMounted()`: 初始化第一個視頻
- `onUnmounted()`: 清理所有視頻資源

## 無障礙功能

### ARIA 標籤
- `role="tablist"`: 標籤頁列表
- `role="tab"`: 個別標籤頁
- `role="tabpanel"`: 內容面板
- `aria-selected`: 標籤頁選中狀態
- `aria-controls`: 標籤頁控制的面板
- `aria-labelledby`: 面板對應的標籤頁

### 鍵盤操作
- `Tab`: 聚焦到標籤頁
- `Arrow Left/Right`: 在標籤頁間切換
- `Enter/Space`: 激活標籤頁

## 樣式類別

### 主要 CSS 類別
- `.ai-use-cases`: 主容器
- `.container-custom`: 內容容器
- `.section-padding`: 區塊內距
- `.text-center`: 文字置中
- `.grid lg:grid-cols-2`: 響應式網格布局

### 狀態類別
- `.opacity-100`: 顯示狀態
- `.opacity-0`: 隱藏狀態
- `.absolute inset-0`: 絕對定位覆蓋
- `.pointer-events-none`: 禁用滑鼠事件

## 使用方式

### 基本使用
```vue
<template>
  <AIUseCases />
</template>

<script setup>
import AIUseCases from '@/components/sections/AIUseCases.vue'
</script>
```

### 自定義案例數據
如需修改案例數據，可以直接編輯組件內的 `useCases` 陣列，或者將其提取為 props 以支援外部傳入。

## 依賴項目

- Vue 3 Composition API
- BaseButton 組件
- Tailwind CSS
- 設計系統顏色配置

## 瀏覽器支援

- 現代瀏覽器（Chrome, Firefox, Safari, Edge）
- 支援 ES6+ 語法
- 支援 CSS Grid 和 Flexbox
- 支援 HTML5 Video API

## 效能考量

- 視頻懶加載：只有當前標籤頁的視頻才會播放
- 平滑過渡：使用 CSS transitions 而非 JavaScript 動畫
- 記憶體管理：組件卸載時清理視頻資源
- 響應式圖片：建議使用適當的視頻格式和大小

## 未來改進

1. **視頻優化**: 支援多種視頻格式和解析度
2. **數據驅動**: 將案例數據提取為外部配置
3. **動畫增強**: 添加更豐富的過渡動畫
4. **國際化**: 支援多語言內容
5. **分析追蹤**: 添加使用者互動追蹤
