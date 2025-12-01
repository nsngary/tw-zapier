<template>
  <div class="header-wrapper">
    <!-- 頂部公告橫幅 (模仿 Zapier 的 ZapConnect 2025 橫幅) -->
    <div v-if="showBanner" class="bg-gradient-to-r from-primary-500 to-accent-red text-white text-center py-3 px-4 relative">
      <div class="flex items-center justify-center gap-2 text-sm font-medium">
        <span class="text-lg">⚡️</span>
        <span>從構想到實現—看看 AI 在 TW_Connect 2025 能做什麼。</span>
        <NuxtLink to="/tw-connect" class="underline hover:no-underline font-semibold ml-2">
          立即報名
        </NuxtLink>
      </div>
      <button @click="closeBanner" class="absolute right-4 top-1/2 transform -translate-y-1/2 text-white/80 hover:text-white transition-colors" aria-label="關閉橫幅">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- 主要 Header -->
    <header class="bg-white sticky top-0 z-50 border-b border-neutral-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          
          <!-- 左側：Logo -->
          <div class="flex items-center">
            <NuxtLink to="/" class="flex items-center gap-3 group mr-8" aria-label="TW_Zapier 首頁">
              <!-- Logo SVG -->
              <svg class="w-8 h-8 text-primary-500 group-hover:text-primary-600 transition-colors" viewBox="0 0 32 32" fill="currentColor">
                <path d="M8 4h16v4H12v8h12v4H8V4z" />
                <path d="M24 28H8v-4h12v-8H8v-4h16v16z" />
                <circle cx="16" cy="16" r="2" />
              </svg>
              <span class="text-xl font-bold text-neutral-900 group-hover:text-primary-600 transition-colors">
                TW_Zapier
              </span>
            </NuxtLink>
          </div>

          <!-- 中間：主導航選單 (桌面版) -->
          <nav class="hidden lg:flex items-center space-x-8" role="navigation">
            <!-- Products 下拉選單 -->
            <div class="relative group">
              <button class="flex items-center gap-1 text-neutral-700 hover:text-primary-500 font-medium transition-colors py-2" aria-expanded="false" aria-haspopup="true">
                產品功能
                <svg class="w-4 h-4 transition-transform group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <!-- 全寬度下拉選單 -->
              <div class="absolute top-full left-1/2 transform -translate-x-1/2 mt-2 w-screen max-w-7xl bg-white shadow-xl border border-neutral-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                <!-- <div class="Submenu-module_root_BoW-D-ZP"> -->
                <div class="flex">
                  <!-- 主要內容區 -->
                  <div class="flex-1 p-8">
                    <div class="mb-6">
                      <h3 class="text-lg font-semibold text-neutral-900 mb-2">TW_Zapier 自動化平台</h3>
                      <p class="text-sm text-neutral-600">無程式碼自動化，整合 7,000+ 應用程式</p>
                    </div>

                    <!-- 產品區塊 -->
                    <div class="mb-8">
                      <h4 class="text-sm font-semibold text-neutral-900 mb-4 uppercase tracking-wide">產品</h4>
                      <div class="grid grid-cols-2 gap-4">
                        <NuxtLink to="/workflows" class="group-item flex items-start gap-3 p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <div class="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                            <svg class="w-6 h-6 text-primary-500" fill="currentColor" viewBox="0 0 256 256">
                              <path d="M245.66,85.66l-32,32a8,8,0,0,1-11.32-11.32L220.69,88H208c-38.67,0-46.59,19-56.62,43.08C141.05,155.88,129.33,184,80,184H79a32,32,0,1,1,0-16h1c38.67,0,46.59-19,56.62-43.08C147,100.12,158.67,72,208,72h12.69L202.34,53.66a8,8,0,0,1,11.32-11.32l32,32A8,8,0,0,1,245.66,85.66Z"></path>
                            </svg>
                          </div>
                          <div>
                            <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">工作流程</h5>
                            <p class="text-sm text-neutral-600">DIY 自動化工作流程</p>
                          </div>
                        </NuxtLink>

                        <NuxtLink to="/tables" class="group-item flex items-start gap-3 p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
                            <svg class="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 24 24">
                              <path d="M12 2.9978H21.0022V7.49897H12V2.9978Z"></path>
                              <path d="M12 7.49897L2.99756 7.4989V12.0001H11.9997L12 7.49897Z"></path>
                              <path d="M11.9997 12.0001L21.0022 12V16.5012H12L11.9997 12.0001Z"></path>
                              <path d="M2.99756 16.5011L12 16.5012L11.9997 21.0023H2.99756V16.5011Z"></path>
                            </svg>
                          </div>
                          <div>
                            <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">資料表</h5>
                            <p class="text-sm text-neutral-600">為工作流程設計的資料庫</p>
                          </div>
                        </NuxtLink>

                        <NuxtLink to="/interfaces" class="group-item flex items-start gap-3 p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center flex-shrink-0">
                            <svg class="w-6 h-6 text-purple-600" fill="currentColor" viewBox="0 0 24 24">
                              <path d="M7.49989 7.50049V16.5001L16.4999 16.5001V21H3.00022L3 3H20.9999V16.5001L16.4999 16.5001L16.5 7.50049L7.49989 7.50049Z"></path>
                            </svg>
                          </div>
                          <div>
                            <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">介面</h5>
                            <p class="text-sm text-neutral-600">自訂頁面驅動您的工作流程</p>
                          </div>
                        </NuxtLink>
                      </div>
                    </div>

                    <!-- 功能區塊 -->
                    <div class="mb-8">
                      <h4 class="text-sm font-semibold text-neutral-900 mb-4 uppercase tracking-wide">功能</h4>
                      <div class="grid grid-cols-2 gap-4">
                        <NuxtLink to="/apps" class="group-item flex items-start gap-3 p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                            <svg class="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                              <path d="M4 4h4v4H4V4zm6 0h4v4h-4V4zm6 0h4v4h-4V4zM4 10h4v4H4v-4zm6 0h4v4h-4v-4zm6 0h4v4h-4v-4zM4 16h4v4H4v-4zm6 0h4v4h-4v-4zm6 0h4v4h-4v-4z"></path>
                            </svg>
                          </div>
                          <div>
                            <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">應用程式整合</h5>
                            <p class="text-sm text-neutral-600">探索 7,000+ 應用程式連接</p>
                          </div>
                        </NuxtLink>

                        <NuxtLink to="/ai" class="group-item flex items-start gap-3 p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <div class="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center flex-shrink-0">
                            <svg class="w-6 h-6 text-orange-600" fill="currentColor" viewBox="0 0 256 256">
                              <path d="M120,72a8,8,0,1,1,8,8A8,8,0,0,1,120,72Zm24,64a8,8,0,1,0,8-8A8,8,0,0,0,144,136Zm48.5,35.47A88.32,88.32,0,0,0,224,101.89q0-1.1-.09-2.19a4,4,0,0,0-4-3.75H195.75L172.62,123.7a24,24,0,1,1-12.28-10.25l25.51-30.62A8,8,0,0,1,192,80h23.14a4,4,0,0,0,3.77-5.35C207.27,42,176.86,18,140.74,16.08l-.59,0a4,4,0,0,0-4.15,4V49.33a24,24,0,1,1-16,0v-27a4,4,0,0,0-4.89-3.91A88.16,88.16,0,0,0,48,102L25.55,145.14l-.22.45a16,16,0,0,0,7.51,20.7l.25.12L56,176.9v31a16,16,0,0,0,16,16h40v8a8,8,0,0,0,8,8h71.77a8.42,8.42,0,0,0,4.06-1,8,8,0,0,0,4.11-8Z"></path>
                            </svg>
                          </div>
                          <div>
                            <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">AI 自動化 🪄</h5>
                            <p class="text-sm text-neutral-600">尖端 AI 升級您的工作流程</p>
                          </div>
                        </NuxtLink>

                        <NuxtLink to="/security-compliance" class="group-item flex items-start gap-3 p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <div class="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center flex-shrink-0">
                            <svg class="w-6 h-6 text-red-600" fill="currentColor" viewBox="0 0 24 24">
                              <path d="M12 1l9 4v6c0 5.55-3.84 10.74-9 12-5.16-1.26-9-6.45-9-12V5l9-4z"></path>
                            </svg>
                          </div>
                          <div>
                            <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">安全性</h5>
                            <p class="text-sm text-neutral-600">企業級安全保障</p>
                          </div>
                        </NuxtLink>
                      </div>
                    </div>

                    <!-- 底部連結 -->
                    <div class="flex gap-6 text-sm">
                      <NuxtLink to="/templates" class="text-primary-500 hover:text-primary-600 font-medium">探索範本</NuxtLink>
                      <NuxtLink to="/use-cases" class="text-primary-500 hover:text-primary-600 font-medium">探索使用案例</NuxtLink>
                      <NuxtLink to="/early-access" class="text-primary-500 hover:text-primary-600 font-medium">加入搶先體驗</NuxtLink>
                    </div>
                  </div>

                  <!-- 右側邊欄 -->
                  <div class="w-80 bg-neutral-50 p-8">
                    <div class="mb-6">
                      <h4 class="text-sm font-semibold text-neutral-900 mb-4 uppercase tracking-wide">最新功能</h4>
                      <div class="space-y-4">
                        <NuxtLink to="/canvas" class="group-item block p-3 rounded-lg hover:bg-white transition-colors">
                          <div class="flex items-center gap-2 mb-1">
                            <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">Canvas</h5>
                            <span class="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full font-medium">Beta</span>
                          </div>
                          <p class="text-sm text-neutral-600">使用 AI 規劃和映射您的工作流程</p>
                        </NuxtLink>

                        <NuxtLink to="/ai/chatbot" class="group-item block p-3 rounded-lg hover:bg-white transition-colors">
                          <div class="flex items-center gap-2 mb-1">
                            <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">聊天機器人</h5>
                            <span class="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full font-medium">Beta</span>
                          </div>
                          <p class="text-sm text-neutral-600">使用 AI 聊天機器人回答客戶問題</p>
                        </NuxtLink>

                        <NuxtLink to="/agents" class="group-item block p-3 rounded-lg hover:bg-white transition-colors">
                          <div class="flex items-center gap-2 mb-1">
                            <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">AI 代理</h5>
                            <span class="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full font-medium">Beta</span>
                          </div>
                          <p class="text-sm text-neutral-600">為任何任務創建您自己的 AI 助手</p>
                        </NuxtLink>

                        <NuxtLink to="/functions" class="group-item block p-3 rounded-lg hover:bg-white transition-colors">
                          <div class="flex items-center gap-2 mb-1">
                            <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">函數</h5>
                            <span class="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full font-medium">Beta</span>
                          </div>
                          <p class="text-sm text-neutral-600">在網頁 IDE 中編寫您的工作流程</p>
                        </NuxtLink>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Solutions 下拉選單 -->
            <div class="relative group">
              <button class="flex items-center gap-1 text-neutral-700 hover:text-primary-500 font-medium transition-colors py-2" aria-expanded="false" aria-haspopup="true">
                解決方案
                <svg class="w-4 h-4 transition-transform group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <!-- 全寬度下拉選單 -->
              <div class="absolute top-full left-1/2 transform -translate-x-1/2 mt-2 w-screen max-w-7xl bg-white shadow-xl border border-neutral-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                <div class="flex">
                  <!-- 主要內容區 -->
                  <div class="flex-1 p-8">
                    <!-- By Team 區塊 -->
                    <div class="mb-8">
                      <h4 class="text-sm font-semibold text-neutral-900 mb-4 uppercase tracking-wide">依團隊分類</h4>
                      <div class="grid grid-cols-2 gap-4">
                        <NuxtLink to="/solutions/marketing" class="group-item flex items-start gap-3 p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <div class="w-10 h-10 bg-pink-100 rounded-lg flex items-center justify-center flex-shrink-0">
                            <svg class="w-6 h-6 text-pink-600" fill="currentColor" viewBox="0 0 24 24">
                              <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z"/>
                            </svg>
                          </div>
                          <div>
                            <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">行銷團隊</h5>
                            <p class="text-sm text-neutral-600">提升行銷活動效果和 ROI</p>
                          </div>
                        </NuxtLink>

                        <NuxtLink to="/solutions/sales" class="group-item flex items-start gap-3 p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
                            <svg class="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 24 24">
                              <path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4zM18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z"/>
                            </svg>
                          </div>
                          <div>
                            <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">業務團隊</h5>
                            <p class="text-sm text-neutral-600">成交更多交易</p>
                          </div>
                        </NuxtLink>

                        <NuxtLink to="/solutions/it" class="group-item flex items-start gap-3 p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                            <svg class="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                              <path fill-rule="evenodd" d="M2 5a2 2 0 012-2h8a2 2 0 012 2v10a2 2 0 002 2H4a2 2 0 01-2-2V5zm3 1h6v4H5V6zm6 6H5v2h6v-2z" clip-rule="evenodd"/>
                            </svg>
                          </div>
                          <div>
                            <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">IT 團隊</h5>
                            <p class="text-sm text-neutral-600">透過自動化更好地管理系統</p>
                          </div>
                        </NuxtLink>

                        <NuxtLink to="/solutions/hr" class="group-item flex items-start gap-3 p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center flex-shrink-0">
                            <svg class="w-6 h-6 text-purple-600" fill="currentColor" viewBox="0 0 24 24">
                              <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM9 8a2 2 0 100-4 2 2 0 000 4zM7 14a5.971 5.971 0 00-3.055-.814H3a3 3 0 00-3 3V20h20v-3.814a3 3 0 00-3-3h-.945A5.971 5.971 0 0013 14H7z"/>
                            </svg>
                          </div>
                          <div>
                            <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">人資團隊</h5>
                            <p class="text-sm text-neutral-600">簡化招聘和員工管理流程</p>
                          </div>
                        </NuxtLink>
                      </div>
                    </div>

                    <!-- By App 區塊 -->
                    <div class="mb-8">
                      <h4 class="text-sm font-semibold text-neutral-900 mb-4 uppercase tracking-wide">依應用程式分類</h4>
                      <div class="grid grid-cols-3 gap-4">
                        <NuxtLink to="/solutions/salesforce" class="group-item flex items-start gap-3 p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <div class="w-10 h-10 bg-white rounded-lg flex items-center justify-center flex-shrink-0 border border-neutral-200">
                            <img src="/images/salesforce_logo.avif" alt="Salesforce" class="w-6 h-6 object-contain" />
                          </div>
                          <div>
                            <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">Salesforce</h5>
                            <p class="text-sm text-neutral-600">自動化您的 CRM 工作流程</p>
                          </div>
                        </NuxtLink>

                        <NuxtLink to="/solutions/hubspot" class="group-item flex items-start gap-3 p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <div class="w-10 h-10 bg-white rounded-lg flex items-center justify-center flex-shrink-0 border border-neutral-200">
                            <img src="/images/hubspot_logo.png" alt="HubSpot" class="w-6 h-6 object-contain" />
                          </div>
                          <div>
                            <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">HubSpot</h5>
                            <p class="text-sm text-neutral-600">整合行銷和銷售流程</p>
                          </div>
                        </NuxtLink>

                        <NuxtLink to="/solutions/slack" class="group-item flex items-start gap-3 p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <div class="w-10 h-10 bg-white rounded-lg flex items-center justify-center flex-shrink-0 border border-neutral-200">
                            <img src="/images/slack_logo.png" alt="Slack" class="w-6 h-6 object-contain" />
                          </div>
                          <div>
                            <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">Slack</h5>
                            <p class="text-sm text-neutral-600">自動化團隊溝通</p>
                          </div>
                        </NuxtLink>

                        <NuxtLink to="/solutions/microsoft-teams" class="group-item flex items-start gap-3 p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <div class="w-10 h-10 bg-white rounded-lg flex items-center justify-center flex-shrink-0 border border-neutral-200">
                            <img src="/images/microsoft-teams_logo.avif" alt="Microsoft Teams" class="w-6 h-6 object-contain" />
                          </div>
                          <div>
                            <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">Microsoft Teams</h5>
                            <p class="text-sm text-neutral-600">提升協作效率</p>
                          </div>
                        </NuxtLink>

                        <NuxtLink to="/solutions/jira" class="group-item flex items-start gap-3 p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <div class="w-10 h-10 bg-white rounded-lg flex items-center justify-center flex-shrink-0 border border-neutral-200">
                            <img src="/images/jira_logo.png" alt="Jira" class="w-6 h-6 object-contain" />
                          </div>
                          <div>
                            <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">Jira</h5>
                            <p class="text-sm text-neutral-600">自動化專案管理</p>
                          </div>
                        </NuxtLink>

                        <NuxtLink to="/solutions/zendesk" class="group-item flex items-start gap-3 p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <div class="w-10 h-10 bg-white rounded-lg flex items-center justify-center flex-shrink-0 border border-neutral-200">
                            <img src="/images/zendesk_logo.png" alt="Zendesk" class="w-6 h-6 object-contain" />
                          </div>
                          <div>
                            <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">Zendesk</h5>
                            <p class="text-sm text-neutral-600">優化客戶服務</p>
                          </div>
                        </NuxtLink>
                      </div>
                    </div>

                    <!-- 底部連結 -->
                    <div class="flex gap-6 text-sm">
                      <NuxtLink to="/solutions" class="text-primary-500 hover:text-primary-600 font-medium">查看所有解決方案</NuxtLink>
                      <NuxtLink to="/case-studies" class="text-primary-500 hover:text-primary-600 font-medium">客戶案例</NuxtLink>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Resources 下拉選單 -->
            <div class="relative group">
              <button class="flex items-center gap-1 text-neutral-700 hover:text-primary-500 font-medium transition-colors py-2" aria-expanded="false" aria-haspopup="true">
                資源中心
                <svg class="w-4 h-4 transition-transform group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <!-- 全寬度下拉選單 -->
              <div class="absolute top-full left-1/2 transform -translate-x-1/2 mt-2 w-screen max-w-5xl bg-white shadow-xl border border-neutral-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                <div class="p-8">
                  <div class="grid grid-cols-3 gap-8">
                    <!-- 學習資源 -->
                    <div>
                      <h4 class="text-sm font-semibold text-neutral-900 mb-4 uppercase tracking-wide">學習資源</h4>
                      <div class="space-y-3">
                        <NuxtLink to="/blog" class="group-item block p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">部落格</h5>
                          <p class="text-sm text-neutral-600">閱讀應用程式和自動化相關文章</p>
                        </NuxtLink>
                        <NuxtLink to="/templates" class="group-item block p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">範本庫</h5>
                          <p class="text-sm text-neutral-600">快速開始的預建範本</p>
                        </NuxtLink>
                        <NuxtLink to="/webinars" class="group-item block p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">網路研討會</h5>
                          <p class="text-sm text-neutral-600">參加即時和錄製的研討會</p>
                        </NuxtLink>
                      </div>
                    </div>

                    <!-- 支援 -->
                    <div>
                      <h4 class="text-sm font-semibold text-neutral-900 mb-4 uppercase tracking-wide">支援</h4>
                      <div class="space-y-3">
                        <NuxtLink to="/help" class="group-item block p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">說明中心</h5>
                          <p class="text-sm text-neutral-600">尋找問題的答案</p>
                        </NuxtLink>
                        <NuxtLink to="/community" class="group-item block p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">社群論壇</h5>
                          <p class="text-sm text-neutral-600">與其他用戶交流經驗</p>
                        </NuxtLink>
                        <NuxtLink to="/contact" class="group-item block p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">聯絡我們</h5>
                          <p class="text-sm text-neutral-600">獲得專業支援</p>
                        </NuxtLink>
                      </div>
                    </div>

                    <!-- 公司 -->
                    <div>
                      <h4 class="text-sm font-semibold text-neutral-900 mb-4 uppercase tracking-wide">公司</h4>
                      <div class="space-y-3">
                        <NuxtLink to="/about" class="group-item block p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">關於我們</h5>
                          <p class="text-sm text-neutral-600">了解 TW_Zapier 的故事</p>
                        </NuxtLink>
                        <NuxtLink to="/careers" class="group-item block p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">職涯機會</h5>
                          <p class="text-sm text-neutral-600">加入我們的團隊</p>
                        </NuxtLink>
                        <NuxtLink to="/press" class="group-item block p-3 rounded-lg hover:bg-neutral-50 transition-colors">
                          <h5 class="font-medium text-neutral-900 hover:text-primary-500 transition-colors">媒體中心</h5>
                          <p class="text-sm text-neutral-600">最新新聞和資源</p>
                        </NuxtLink>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 企業版 -->
            <NuxtLink to="/enterprise" class="text-neutral-700 hover:text-primary-500 font-medium transition-colors py-2">
              企業版
            </NuxtLink>

            <!-- 定價方案 -->
            <NuxtLink to="/pricing" class="text-neutral-700 hover:text-primary-500 font-medium transition-colors py-2">
              定價方案
            </NuxtLink>
          </nav>

          <!-- 右側：功能連結和按鈕 -->
          <div class="flex items-center gap-4">
            <!-- 探索應用程式 -->
            <NuxtLink to="/apps" class="hidden lg:block text-neutral-700 hover:text-primary-500 font-medium transition-colors">
              探索應用程式
            </NuxtLink>

            <!-- 聯絡銷售 -->
            <NuxtLink to="/contact-sales" class="hidden lg:block text-neutral-700 hover:text-primary-500 font-medium transition-colors">
              聯絡銷售
            </NuxtLink>

            <!-- 登入 -->
            <NuxtLink to="/login" class="hidden lg:block text-neutral-700 hover:text-primary-500 font-medium transition-colors">
              登入
            </NuxtLink>

            <!-- 免費註冊按鈕 -->
            <BaseButton variant="primary" size="sm" class="hidden lg:block">
              免費註冊
            </BaseButton>

            <!-- 行動版選單按鈕 -->
            <button @click="toggleMobileMenu" class="lg:hidden p-2 rounded-lg hover:bg-neutral-100 transition-colors" aria-label="開啟選單" :aria-expanded="mobileMenuOpen">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>
  </div>
</template>

<script setup lang="ts">
// Vue 3 Composition API 和 TypeScript
import { ref, onMounted, onUnmounted } from 'vue'

// 響應式狀態管理
const showBanner = ref(true)
const mobileMenuOpen = ref(false)

// 橫幅控制
const closeBanner = () => {
  showBanner.value = false
  // 記住用戶選擇
  if (typeof window !== 'undefined') {
    localStorage.setItem('tw-zapier-banner-closed', 'true')
  }
}

// 行動版選單控制
const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

// 點擊外部關閉選單
const handleClickOutside = (event: Event) => {
  const target = event.target as HTMLElement
  const header = document.querySelector('.header-wrapper')

  if (header && !header.contains(target)) {
    mobileMenuOpen.value = false
  }
}

// 鍵盤導航支援
const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Escape') {
    mobileMenuOpen.value = false
  }
}

// 生命週期管理
onMounted(() => {
  if (typeof window !== 'undefined') {
    // 檢查橫幅狀態
    const bannerClosed = localStorage.getItem('tw-zapier-banner-closed')
    if (bannerClosed === 'true') {
      showBanner.value = false
    }

    // 添加事件監聽器
    document.addEventListener('click', handleClickOutside)
    document.addEventListener('keydown', handleKeyDown)
  }
})

onUnmounted(() => {
  if (typeof window !== 'undefined') {
    // 清理事件監聽器
    document.removeEventListener('click', handleClickOutside)
    document.removeEventListener('keydown', handleKeyDown)
  }
})
</script>

<style scoped>
/* Header 特定樣式 */
.header-wrapper {
  position: relative;
}

/* 全寬度下拉選單樣式 */
.group .group-hover\:opacity-100 {
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.2s ease-in-out;
}

.group:hover .group-hover\:opacity-100 {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

/* 下拉選單箭頭旋轉效果 */
.group:hover .group-hover\:rotate-180 {
  transform: rotate(180deg);
}

/* 確保下拉選單在最上層 */
.group .group-hover\:opacity-100 {
  z-index: 50;
}

/* 懸停效果優化 */
.group-item:hover h5 {
  color: #86735E;
}

/* 無障礙設計：鍵盤導航支援 */
.group button:focus + .group-hover\:opacity-100,
.group .group-hover\:opacity-100:focus-within {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

/* 平滑的懸停過渡效果 */
.group button {
  transition: color 0.2s ease-in-out;
}

.group button svg {
  transition: transform 0.2s ease-in-out;
}

/* 響應式調整 */
@media (max-width: 1024px) {
  .group .group-hover\:opacity-100 {
    display: none;
  }
}
</style>
