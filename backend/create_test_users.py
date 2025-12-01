#!/usr/bin/env python3
"""
建立測試用戶腳本
"""

import sys
import os
from pathlib import Path

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.security import get_password_hash

def create_test_users():
    """建立測試用戶 001-005"""
    print("🔧 建立測試用戶...")
    
    # 建立資料庫連接
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # 密碼雜湊
        password_hash = get_password_hash("123")
        
        # 檢查並建立測試用戶
        test_users = [
            ("001", "001@tw-zapier.com", "測試用戶001"),
            ("002", "002@tw-zapier.com", "測試用戶002"),
            ("003", "003@tw-zapier.com", "測試用戶003"),
            ("004", "004@tw-zapier.com", "測試用戶004"),
            ("005", "005@tw-zapier.com", "測試用戶005"),
        ]
        
        for username, email, full_name in test_users:
            # 檢查用戶是否已存在
            result = db.execute(
                text("SELECT id FROM users WHERE email = :email"),
                {"email": email}
            ).fetchone()
            
            if result:
                print(f"✅ 用戶 {username} ({email}) 已存在")
                continue
            
            # 建立新用戶
            db.execute(
                text("""
                    INSERT INTO users (id, name, email, password_hash, is_active, is_superuser, email_verified)
                    VALUES (gen_random_uuid(), :name, :email, :password_hash, true, false, true)
                """),
                {
                    "name": full_name,
                    "email": email,
                    "password_hash": password_hash
                }
            )
            
            print(f"✅ 建立用戶 {username} ({email})")
        
        # 提交變更
        db.commit()
        print("🎉 所有測試用戶建立完成！")
        
        # 顯示建立的用戶
        print("\n📋 測試用戶列表：")
        result = db.execute(
            text("""
                SELECT id, email, name, created_at
                FROM users
                WHERE email LIKE '%@tw-zapier.com'
                ORDER BY email
            """)
        ).fetchall()
        
        for user in result:
            print(f"   ID: {user[0]}, Email: {user[1]}, 姓名: {user[2]}")
        
        return True
        
    except Exception as e:
        print(f"❌ 建立測試用戶失敗: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def verify_users():
    """驗證用戶是否可以登入"""
    print("\n🔍 驗證用戶登入...")
    
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        from app.core.security import verify_password
        
        # 測試每個用戶
        for i in range(1, 6):
            email = f"00{i}@tw-zapier.com"
            
            # 取得用戶資料
            result = db.execute(
                text("SELECT id, email, password_hash, name FROM users WHERE email = :email"),
                {"email": email}
            ).fetchone()

            if result:
                user_id, user_email, password_hash, name = result
                
                # 驗證密碼
                if verify_password("123", password_hash):
                    print(f"✅ 用戶 {email} 密碼驗證成功")
                else:
                    print(f"❌ 用戶 {email} 密碼驗證失敗")
            else:
                print(f"❌ 用戶 {email} 不存在")
        
        return True
        
    except Exception as e:
        print(f"❌ 驗證用戶失敗: {e}")
        return False
    finally:
        db.close()

def main():
    """主函數"""
    print("🚀 TW_Zapier 測試用戶建立工具")
    print("=" * 50)
    
    # 檢查資料庫連接
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ 資料庫連接成功")
    except Exception as e:
        print(f"❌ 資料庫連接失敗: {e}")
        return False
    
    # 建立測試用戶
    if not create_test_users():
        return False
    
    # 驗證用戶
    if not verify_users():
        return False
    
    print("\n" + "=" * 50)
    print("🎉 測試用戶建立和驗證完成！")
    print("\n📝 登入資訊：")
    print("   帳號: 001@tw-zapier.com ~ 005@tw-zapier.com")
    print("   密碼: 123")
    print("\n💡 提示：前端需要修改為使用 email 而非 username 登入")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
