#!/usr/bin/env python3
"""
簡單的資料庫連接和模型測試
"""

import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.user import User, RefreshToken
from app.models.workflow import Workflow, WorkflowStatus
from app.models.taiwan import TaiwanPaymentConfig, PaymentProvider, PaymentMethod


def test_database_connection():
    """測試資料庫連接"""
    print("🔗 測試資料庫連接...")
    
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    try:
        db = SessionLocal()
        result = db.execute(text("SELECT 1"))
        print("✅ 資料庫連接成功")
        db.close()
        return True
    except Exception as e:
        print(f"❌ 資料庫連接失敗: {e}")
        return False


def test_user_model():
    """測試用戶模型"""
    print("\n👤 測試用戶模型...")
    
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # 建立測試用戶
        test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        user = User(
            name="測試用戶",
            email=test_email,
            password_hash="hashed_password",
            phone="0912345678",
            email_verified=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        print(f"✅ 用戶建立成功: {user.id}")
        print(f"   姓名: {user.name}")
        print(f"   郵件: {user.email}")
        print(f"   手機: {user.phone}")
        print(f"   郵件已驗證: {user.email_verified}")
        
        # 測試 RefreshToken
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        token = RefreshToken(
            user_id=user.id,
            token="test_refresh_token_123",
            expires_at=expires_at,
            created_ip="127.0.0.1"
        )
        db.add(token)
        db.commit()
        db.refresh(token)
        
        print(f"✅ Refresh Token 建立成功: {token.id}")
        print(f"   Token: {token.token[:20]}...")
        print(f"   過期時間: {token.expires_at}")
        print(f"   是否有效: {token.is_valid}")
        
        # 清理測試資料
        db.delete(token)
        db.delete(user)
        db.commit()
        
        return True
        
    except Exception as e:
        print(f"❌ 用戶模型測試失敗: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def test_workflow_model():
    """測試工作流模型"""
    print("\n⚡ 測試工作流模型...")
    
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # 先建立用戶
        user = User(
            name="工作流測試用戶",
            email="workflow@example.com",
            password_hash="hashed_password"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # 建立工作流
        workflow = Workflow(
            user_id=user.id,
            name="測試工作流",
            description="這是一個測試工作流",
            status=WorkflowStatus.DRAFT,
            category="test",
            nodes=[{"id": "node1", "type": "trigger", "name": "開始"}],
            edges=[{"source": "node1", "target": "node2"}]
        )
        db.add(workflow)
        db.commit()
        db.refresh(workflow)
        
        print(f"✅ 工作流建立成功: {workflow.id}")
        print(f"   名稱: {workflow.name}")
        print(f"   狀態: {workflow.status.value}")
        print(f"   節點數量: {len(workflow.nodes)}")
        print(f"   連接數量: {len(workflow.edges)}")
        
        # 清理測試資料
        db.delete(workflow)
        db.delete(user)
        db.commit()
        
        return True
        
    except Exception as e:
        print(f"❌ 工作流模型測試失敗: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def test_taiwan_payment_model():
    """測試台灣金流模型"""
    print("\n💳 測試台灣金流模型...")
    
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # 先建立用戶
        user = User(
            name="金流測試用戶",
            email="payment@example.com",
            password_hash="hashed_password"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # 建立台灣金流配置
        config = TaiwanPaymentConfig(
            user_id=user.id,
            provider=PaymentProvider.LINE_PAY,
            config_name="Line Pay 測試配置",
            merchant_id="test_merchant_123",
            api_key_encrypted="encrypted_api_key",
            is_sandbox=True,
            supported_methods=[PaymentMethod.CREDIT_CARD, PaymentMethod.APPLE_PAY]
        )
        db.add(config)
        db.commit()
        db.refresh(config)
        
        print(f"✅ 台灣金流配置建立成功: {config.id}")
        print(f"   提供商: {config.provider.value}")
        print(f"   配置名稱: {config.config_name}")
        print(f"   商戶ID: {config.merchant_id}")
        print(f"   沙盒模式: {config.is_sandbox}")
        print(f"   支援付款方式: {[method.value for method in config.supported_methods]}")
        
        # 清理測試資料
        db.delete(config)
        db.delete(user)
        db.commit()
        
        return True
        
    except Exception as e:
        print(f"❌ 台灣金流模型測試失敗: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def main():
    """主測試函數"""
    print("🚀 開始 SQLAlchemy 資料模型測試")
    print("=" * 50)
    
    tests = [
        test_database_connection,
        test_user_model,
        test_workflow_model,
        test_taiwan_payment_model
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 測試結果: {passed}/{total} 通過")
    
    if passed == total:
        print("🎉 所有測試通過！SQLAlchemy 資料模型建立成功！")
        return True
    else:
        print("⚠️  部分測試失敗，請檢查錯誤信息")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
