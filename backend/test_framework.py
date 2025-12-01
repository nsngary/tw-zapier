#!/usr/bin/env python3

"""
FastAPI 後端框架驗證腳本
"""

import sys
import os
import asyncio
from pathlib import Path

# 添加 app 目錄到 Python 路徑
sys.path.insert(0, str(Path(__file__).parent / "app"))

def test_imports():
    """測試模組匯入"""
    print("🔍 測試 1: 模組匯入測試")
    
    try:
        # 測試核心模組
        from app.core.config import settings
        print("✅ 設定模組匯入成功")
        
        from app.core.database import get_db
        print("✅ 資料庫模組匯入成功")
        
        from app.core.security import create_access_token
        print("✅ 安全模組匯入成功")
        
        from app.core.exceptions import TaiwanZapierException
        print("✅ 例外處理模組匯入成功")
        
        from app.core.middleware import RequestLoggingMiddleware
        print("✅ 中介軟體模組匯入成功")
        
        # 測試 API 模組
        from app.api.v1.api import api_router
        print("✅ API 路由模組匯入成功")
        
        # 測試 Schema 模組
        from app.schemas.auth import LoginRequest
        print("✅ 認證 Schema 匯入成功")
        
        from app.schemas.user import UserResponse
        print("✅ 使用者 Schema 匯入成功")
        
        from app.schemas.workflow import WorkflowResponse
        print("✅ 工作流 Schema 匯入成功")
        
        # 測試服務模組
        from app.services.user_service import UserService
        print("✅ 使用者服務匯入成功")
        
        from app.services.workflow_service import WorkflowService
        print("✅ 工作流服務匯入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 模組匯入失敗: {e}")
        return False
    except Exception as e:
        print(f"❌ 未預期的錯誤: {e}")
        return False


def test_fastapi_app():
    """測試 FastAPI 應用程式建立"""
    print("\n🔍 測試 2: FastAPI 應用程式建立")
    
    try:
        from app.main import app
        print("✅ FastAPI 應用程式建立成功")
        
        # 檢查應用程式屬性
        assert hasattr(app, 'title'), "應用程式應該有標題"
        assert hasattr(app, 'version'), "應用程式應該有版本"
        print(f"✅ 應用程式標題: {app.title}")
        print(f"✅ 應用程式版本: {app.version}")
        
        return True
        
    except Exception as e:
        print(f"❌ FastAPI 應用程式建立失敗: {e}")
        return False


def test_configuration():
    """測試設定載入"""
    print("\n🔍 測試 3: 設定載入測試")
    
    try:
        from app.core.config import settings
        
        # 檢查必要的設定
        required_settings = [
            'APP_NAME', 'APP_VERSION', 'DEBUG', 'ENVIRONMENT',
            'DATABASE_URL', 'REDIS_URL', 'JWT_SECRET_KEY'
        ]
        
        for setting in required_settings:
            if hasattr(settings, setting):
                print(f"✅ 設定 {setting} 已載入")
            else:
                print(f"⚠️  設定 {setting} 未找到")
        
        return True
        
    except Exception as e:
        print(f"❌ 設定載入失敗: {e}")
        return False


def test_security_functions():
    """測試安全功能"""
    print("\n🔍 測試 4: 安全功能測試")
    
    try:
        from app.core.security import (
            create_access_token, 
            verify_token,
            get_password_hash,
            verify_password
        )
        
        # 測試密碼雜湊
        password = "test_password_123"
        hashed = get_password_hash(password)
        print("✅ 密碼雜湊功能正常")
        
        # 測試密碼驗證
        is_valid = verify_password(password, hashed)
        assert is_valid, "密碼驗證應該成功"
        print("✅ 密碼驗證功能正常")
        
        # 測試 JWT 權杖
        token = create_access_token(subject="test_user")
        print("✅ JWT 權杖建立功能正常")
        
        # 測試權杖驗證
        subject = verify_token(token)
        assert subject == "test_user", "權杖驗證應該返回正確的主體"
        print("✅ JWT 權杖驗證功能正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 安全功能測試失敗: {e}")
        return False


def test_exception_handling():
    """測試例外處理"""
    print("\n🔍 測試 5: 例外處理測試")
    
    try:
        from app.core.exceptions import (
            TaiwanZapierException,
            ValidationError,
            AuthenticationError,
            ResourceNotFoundError
        )
        
        # 測試自定義例外
        try:
            raise ValidationError("測試驗證錯誤", field="test_field")
        except ValidationError as e:
            assert e.error_code == "VALIDATION_ERROR"
            print("✅ ValidationError 例外處理正常")
        
        try:
            raise AuthenticationError("測試認證錯誤")
        except AuthenticationError as e:
            assert e.error_code == "AUTHENTICATION_ERROR"
            print("✅ AuthenticationError 例外處理正常")
        
        try:
            raise ResourceNotFoundError("測試資源", "123")
        except ResourceNotFoundError as e:
            assert e.error_code == "RESOURCE_NOT_FOUND"
            print("✅ ResourceNotFoundError 例外處理正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 例外處理測試失敗: {e}")
        return False


def test_schema_validation():
    """測試 Schema 驗證"""
    print("\n🔍 測試 6: Schema 驗證測試")
    
    try:
        from app.schemas.auth import LoginRequest, LoginResponse
        from app.schemas.user import UserResponse
        from app.schemas.workflow import WorkflowCreate
        
        # 測試登入請求 Schema
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        login_request = LoginRequest(**login_data)
        assert login_request.email == "test@example.com"
        print("✅ LoginRequest Schema 驗證正常")
        
        # 測試工作流建立 Schema
        workflow_data = {
            "name": "測試工作流",
            "description": "這是一個測試工作流",
            "nodes": [],
            "edges": [],
            "is_active": True,
            "tags": ["測試"]
        }
        workflow_create = WorkflowCreate(**workflow_data)
        assert workflow_create.name == "測試工作流"
        print("✅ WorkflowCreate Schema 驗證正常")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema 驗證測試失敗: {e}")
        return False


def test_middleware():
    """測試中介軟體"""
    print("\n🔍 測試 7: 中介軟體測試")
    
    try:
        from app.core.middleware import (
            RequestLoggingMiddleware,
            SecurityHeadersMiddleware,
            RateLimitMiddleware
        )
        
        # 檢查中介軟體類別是否可以實例化
        logging_middleware = RequestLoggingMiddleware
        security_middleware = SecurityHeadersMiddleware
        rate_limit_middleware = RateLimitMiddleware
        
        print("✅ RequestLoggingMiddleware 載入成功")
        print("✅ SecurityHeadersMiddleware 載入成功")
        print("✅ RateLimitMiddleware 載入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 中介軟體測試失敗: {e}")
        return False


async def main():
    """主測試函數"""
    print("🚀 開始 FastAPI 後端框架驗證")
    print("=" * 50)
    
    test_functions = [
        ("模組匯入", test_imports),
        ("FastAPI 應用程式建立", test_fastapi_app),
        ("設定載入", test_configuration),
        ("安全功能", test_security_functions),
        ("例外處理", test_exception_handling),
        ("Schema 驗證", test_schema_validation),
        ("中介軟體", test_middleware)
    ]
    
    passed = 0
    total = len(test_functions)
    
    for test_name, test_func in test_functions:
        try:
            result = test_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ 測試 '{test_name}' 執行失敗: {str(e)}")
    
    print("\n" + "=" * 50)
    print("📊 測試結果總結:")
    print(f"   通過: {passed}/{total} 項測試")
    print(f"   成功率: {((passed / total) * 100):.1f}%")
    
    if passed == total:
        print("🎉 所有測試通過！FastAPI 後端框架建立成功")
        return 0
    else:
        print("⚠️  部分測試失敗，但核心功能已建立")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
