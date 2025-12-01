"""
FastAPI 後端框架測試
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tempfile
import os

from app.main import app
from app.core.database import get_db, Base
from app.core.config import settings


# 建立測試資料庫
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """
    覆蓋資料庫依賴注入
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# 覆蓋依賴注入
app.dependency_overrides[get_db] = override_get_db

# 建立測試客戶端
client = TestClient(app)


@pytest.fixture(scope="module")
def setup_database():
    """
    設定測試資料庫
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_root_endpoint():
    """
    測試根端點
    """
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "status" in data
    assert data["status"] == "running"


def test_health_check():
    """
    測試健康檢查端點
    """
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_api_health_check():
    """
    測試 API 健康檢查端點
    """
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_cors_headers():
    """
    測試 CORS 標頭
    """
    response = client.options("/", headers={
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET"
    })
    
    # 檢查 CORS 標頭
    assert "access-control-allow-origin" in response.headers
    assert "access-control-allow-credentials" in response.headers


def test_security_headers():
    """
    測試安全標頭
    """
    response = client.get("/")
    
    # 檢查安全標頭
    assert "x-content-type-options" in response.headers
    assert response.headers["x-content-type-options"] == "nosniff"
    assert "x-frame-options" in response.headers
    assert response.headers["x-frame-options"] == "DENY"


def test_request_logging_middleware():
    """
    測試請求日誌中介軟體
    """
    response = client.get("/")
    
    # 檢查請求 ID 標頭
    assert "x-request-id" in response.headers
    assert "x-process-time" in response.headers


def test_api_documentation():
    """
    測試 API 文件端點
    """
    if settings.DEBUG:
        # 在除錯模式下應該可以存取文件
        response = client.get("/docs")
        assert response.status_code == 200
        
        response = client.get("/redoc")
        assert response.status_code == 200
        
        response = client.get("/openapi.json")
        assert response.status_code == 200
    else:
        # 在生產模式下文件應該被停用
        response = client.get("/docs")
        assert response.status_code == 404


def test_validation_error_handling():
    """
    測試驗證錯誤處理
    """
    # 發送無效的 JSON 資料
    response = client.post("/api/v1/auth/login", json={
        "email": "invalid-email",  # 無效的電子郵件格式
        "password": "123"  # 密碼太短
    })
    
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_404_error_handling():
    """
    測試 404 錯誤處理
    """
    response = client.get("/nonexistent-endpoint")
    assert response.status_code == 404
    
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "HTTP_ERROR"


def test_method_not_allowed():
    """
    測試不允許的 HTTP 方法
    """
    response = client.post("/health")
    assert response.status_code == 405


def test_rate_limiting():
    """
    測試速率限制（如果啟用）
    """
    if settings.ENABLE_RATE_LIMITING:
        # 快速發送多個請求
        responses = []
        for _ in range(settings.RATE_LIMIT_PER_MINUTE + 5):
            response = client.get("/")
            responses.append(response)
        
        # 檢查是否有請求被限制
        rate_limited = any(r.status_code == 429 for r in responses)
        assert rate_limited, "速率限制應該觸發"


def test_cache_control_headers():
    """
    測試快取控制標頭
    """
    # API 端點不應該被快取
    response = client.get("/api/v1/health/")
    assert "cache-control" in response.headers
    assert "no-cache" in response.headers["cache-control"]
    
    # 健康檢查端點應該有短時間快取
    response = client.get("/health")
    assert "cache-control" in response.headers


def test_json_response_format():
    """
    測試 JSON 回應格式
    """
    response = client.get("/")
    assert response.headers["content-type"] == "application/json"
    
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert "version" in data


def test_error_response_format():
    """
    測試錯誤回應格式
    """
    response = client.get("/nonexistent")
    assert response.status_code == 404
    
    data = response.json()
    assert "success" in data
    assert data["success"] is False
    assert "error" in data
    assert "code" in data["error"]
    assert "message" in data["error"]
    assert "timestamp" in data


if __name__ == "__main__":
    # 執行基本測試
    print("🚀 開始 FastAPI 後端框架測試")
    print("=" * 50)
    
    test_functions = [
        ("根端點測試", test_root_endpoint),
        ("健康檢查測試", test_health_check),
        ("API 健康檢查測試", test_api_health_check),
        ("CORS 標頭測試", test_cors_headers),
        ("安全標頭測試", test_security_headers),
        ("請求日誌中介軟體測試", test_request_logging_middleware),
        ("驗證錯誤處理測試", test_validation_error_handling),
        ("404 錯誤處理測試", test_404_error_handling),
        ("JSON 回應格式測試", test_json_response_format),
        ("錯誤回應格式測試", test_error_response_format)
    ]
    
    passed = 0
    total = len(test_functions)
    
    for test_name, test_func in test_functions:
        try:
            print(f"\n🔍 執行測試: {test_name}")
            test_func()
            print(f"✅ {test_name} - 通過")
            passed += 1
        except Exception as e:
            print(f"❌ {test_name} - 失敗: {str(e)}")
    
    print("\n" + "=" * 50)
    print("📊 測試結果總結:")
    print(f"   通過: {passed}/{total} 項測試")
    print(f"   成功率: {((passed / total) * 100):.1f}%")
    
    if passed == total:
        print("🎉 所有測試通過！FastAPI 後端框架建立成功")
        exit(0)
    else:
        print("⚠️  部分測試失敗，請檢查實作細節")
        exit(1)
