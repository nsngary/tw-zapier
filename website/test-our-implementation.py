#!/usr/bin/env python3
"""
測試我們的 HeaderNavigation 實現
"""

from playwright.sync_api import sync_playwright
import time

def test_our_implementation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        print('🌐 正在測試我們的實現...')
        try:
            # 使用更長的超時時間
            page.goto('http://localhost:4000/', timeout=30000)
            print('✅ 我們的網站載入成功')
        except Exception as e:
            print(f'❌ 我們的網站載入失敗: {e}')
            browser.close()
            return
        
        # 等待頁面完全載入
        time.sleep(3)
        
        # 截圖初始狀態
        page.screenshot(path='our_initial.png', full_page=False)
        print('📸 已截圖：our_initial.png')
        
        # 測試 Products 下拉選單
        print('🔍 測試我們的 Products 下拉選單...')
        try:
            # 使用更精確的選擇器
            products_nav = page.locator('nav ul li:has-text("產品功能")').first
            if products_nav.count() > 0:
                print('✅ 找到產品功能導航')
                products_nav.click()
                time.sleep(2)
                page.screenshot(path='our_products_dropdown.png', full_page=False)
                print('📸 已截圖：our_products_dropdown.png')
                
                # 測試互斥功能 - 點擊 Solutions
                print('🔍 測試互斥功能 - 點擊解決方案...')
                solutions_nav = page.locator('nav ul li:has-text("解決方案")').first
                if solutions_nav.count() > 0:
                    solutions_nav.click()
                    time.sleep(2)
                    page.screenshot(path='our_solutions_dropdown.png', full_page=False)
                    print('📸 已截圖：our_solutions_dropdown.png')
                
                # 測試 Resources
                print('🔍 測試資源中心下拉選單...')
                resources_nav = page.locator('nav ul li:has-text("資源中心")').first
                if resources_nav.count() > 0:
                    resources_nav.click()
                    time.sleep(2)
                    page.screenshot(path='our_resources_dropdown.png', full_page=False)
                    print('📸 已截圖：our_resources_dropdown.png')
                
                # 測試點擊外部關閉
                print('🔍 測試點擊外部關閉功能...')
                page.click('body', position={'x': 100, 'y': 100})
                time.sleep(1)
                page.screenshot(path='our_closed_dropdown.png', full_page=False)
                print('📸 已截圖：our_closed_dropdown.png')
                
            else:
                print('❌ 未找到產品功能導航')
                
        except Exception as e:
            print(f'❌ 測試失敗: {e}')
        
        print('✅ 我們的實現測試完成')
        
        # 保持瀏覽器開啟 15 秒讓用戶查看
        print('🔍 瀏覽器將保持開啟 15 秒供查看...')
        time.sleep(15)
        browser.close()

if __name__ == '__main__':
    test_our_implementation()
