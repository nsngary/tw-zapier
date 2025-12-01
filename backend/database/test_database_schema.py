#!/usr/bin/env python3

"""
資料庫 Schema 測試腳本
驗證資料庫設計和功能
"""

import sys
import os
from pathlib import Path

# 添加 app 目錄到 Python 路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_database_connection():
    """測試資料庫連線"""
    print("🔍 測試 1: 資料庫連線測試")
    
    try:
        # 使用測試資料庫 URL
        DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/taiwan_zapier_test")
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ 資料庫連線成功")
            print(f"   PostgreSQL 版本: {version[:50]}...")
            
        return True
        
    except Exception as e:
        print(f"❌ 資料庫連線失敗: {e}")
        return False


def test_table_creation():
    """測試資料表建立"""
    print("\n🔍 測試 2: 資料表建立測試")
    
    try:
        DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/taiwan_zapier_test")
        engine = create_engine(DATABASE_URL)
        
        # 檢查核心資料表是否存在
        core_tables = [
            'users', 'user_profiles', 'user_preferences',
            'workflows', 'workflow_versions', 'workflow_executions', 'workflow_templates',
            'node_types', 'nodes', 'taiwan_services', 'payment_records',
            'api_keys', 'webhook_endpoints', 'audit_logs', 'system_settings'
        ]
        
        with engine.connect() as conn:
            for table in core_tables:
                result = conn.execute(text(f"""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = '{table}'
                    )
                """))
                
                exists = result.fetchone()[0]
                if exists:
                    print(f"✅ 資料表 '{table}' 存在")
                else:
                    print(f"❌ 資料表 '{table}' 不存在")
                    return False
        
        print(f"✅ 所有 {len(core_tables)} 個核心資料表都存在")
        return True
        
    except Exception as e:
        print(f"❌ 資料表檢查失敗: {e}")
        return False


def test_indexes():
    """測試索引建立"""
    print("\n🔍 測試 3: 索引建立測試")
    
    try:
        DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/taiwan_zapier_test")
        engine = create_engine(DATABASE_URL)
        
        # 檢查重要索引
        important_indexes = [
            'idx_users_email',
            'idx_workflows_user_id',
            'idx_workflow_executions_workflow_id',
            'idx_workflow_executions_status',
            'idx_audit_logs_created_at'
        ]
        
        with engine.connect() as conn:
            existing_indexes = 0
            for index in important_indexes:
                result = conn.execute(text(f"""
                    SELECT EXISTS (
                        SELECT FROM pg_indexes 
                        WHERE schemaname = 'public' 
                        AND indexname = '{index}'
                    )
                """))
                
                exists = result.fetchone()[0]
                if exists:
                    print(f"✅ 索引 '{index}' 存在")
                    existing_indexes += 1
                else:
                    print(f"⚠️  索引 '{index}' 不存在")
        
        print(f"✅ {existing_indexes}/{len(important_indexes)} 個重要索引存在")
        return existing_indexes > 0
        
    except Exception as e:
        print(f"❌ 索引檢查失敗: {e}")
        return False


def test_constraints():
    """測試約束條件"""
    print("\n🔍 測試 4: 約束條件測試")
    
    try:
        DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/taiwan_zapier_test")
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            # 檢查外鍵約束
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.table_constraints 
                WHERE constraint_type = 'FOREIGN KEY' 
                AND table_schema = 'public'
            """))
            
            fk_count = result.fetchone()[0]
            print(f"✅ 外鍵約束數量: {fk_count}")
            
            # 檢查唯一約束
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.table_constraints 
                WHERE constraint_type = 'UNIQUE' 
                AND table_schema = 'public'
            """))
            
            unique_count = result.fetchone()[0]
            print(f"✅ 唯一約束數量: {unique_count}")
            
            # 檢查檢查約束
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.table_constraints 
                WHERE constraint_type = 'CHECK' 
                AND table_schema = 'public'
            """))
            
            check_count = result.fetchone()[0]
            print(f"✅ 檢查約束數量: {check_count}")
        
        return fk_count > 0 and unique_count > 0
        
    except Exception as e:
        print(f"❌ 約束條件檢查失敗: {e}")
        return False


def test_triggers():
    """測試觸發器"""
    print("\n🔍 測試 5: 觸發器測試")
    
    try:
        DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/taiwan_zapier_test")
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            # 檢查觸發器
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.triggers 
                WHERE trigger_schema = 'public'
            """))
            
            trigger_count = result.fetchone()[0]
            print(f"✅ 觸發器數量: {trigger_count}")
            
            # 檢查觸發器函數
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.routines 
                WHERE routine_schema = 'public' 
                AND routine_type = 'FUNCTION'
            """))
            
            function_count = result.fetchone()[0]
            print(f"✅ 觸發器函數數量: {function_count}")
        
        return trigger_count > 0
        
    except Exception as e:
        print(f"❌ 觸發器檢查失敗: {e}")
        return False


def test_seed_data():
    """測試種子資料"""
    print("\n🔍 測試 6: 種子資料測試")
    
    try:
        DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/taiwan_zapier_test")
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            # 檢查系統設定
            result = conn.execute(text("SELECT COUNT(*) FROM system_settings"))
            settings_count = result.fetchone()[0]
            print(f"✅ 系統設定數量: {settings_count}")
            
            # 檢查節點類型
            result = conn.execute(text("SELECT COUNT(*) FROM node_types"))
            node_types_count = result.fetchone()[0]
            print(f"✅ 節點類型數量: {node_types_count}")
            
            # 檢查台灣服務
            result = conn.execute(text("SELECT COUNT(*) FROM taiwan_services"))
            services_count = result.fetchone()[0]
            print(f"✅ 台灣服務數量: {services_count}")
            
            # 檢查工作流模板
            result = conn.execute(text("SELECT COUNT(*) FROM workflow_templates"))
            templates_count = result.fetchone()[0]
            print(f"✅ 工作流模板數量: {templates_count}")
            
            # 檢查使用者
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            users_count = result.fetchone()[0]
            print(f"✅ 使用者數量: {users_count}")
        
        return (settings_count > 0 and node_types_count > 0 and 
                services_count > 0 and templates_count > 0 and users_count > 0)
        
    except Exception as e:
        print(f"❌ 種子資料檢查失敗: {e}")
        return False


def test_data_integrity():
    """測試資料完整性"""
    print("\n🔍 測試 7: 資料完整性測試")
    
    try:
        DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/taiwan_zapier_test")
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            # 檢查孤立記錄
            result = conn.execute(text("""
                SELECT COUNT(*) FROM user_profiles 
                WHERE user_id NOT IN (SELECT id FROM users)
            """))
            orphaned_profiles = result.fetchone()[0]
            
            result = conn.execute(text("""
                SELECT COUNT(*) FROM workflows 
                WHERE user_id NOT IN (SELECT id FROM users)
            """))
            orphaned_workflows = result.fetchone()[0]
            
            if orphaned_profiles == 0 and orphaned_workflows == 0:
                print("✅ 沒有發現孤立記錄")
                return True
            else:
                print(f"⚠️  發現孤立記錄: profiles={orphaned_profiles}, workflows={orphaned_workflows}")
                return False
        
    except Exception as e:
        print(f"❌ 資料完整性檢查失敗: {e}")
        return False


async def main():
    """主測試函數"""
    print("🚀 開始資料庫 Schema 驗證")
    print("=" * 50)
    
    test_functions = [
        ("資料庫連線", test_database_connection),
        ("資料表建立", test_table_creation),
        ("索引建立", test_indexes),
        ("約束條件", test_constraints),
        ("觸發器", test_triggers),
        ("種子資料", test_seed_data),
        ("資料完整性", test_data_integrity)
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
        print("🎉 所有測試通過！資料庫 Schema 設計驗證成功")
        return 0
    else:
        print("⚠️  部分測試失敗，請檢查資料庫設定")
        return 1


if __name__ == "__main__":
    import asyncio
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
