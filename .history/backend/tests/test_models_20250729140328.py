"""
資料模型測試
"""

import pytest
import uuid
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.user import User, RefreshToken, UserProfile, UserPreferences
from app.models.workflow import Workflow, WorkflowExecution, WorkflowStatus, ExecutionStatus
from app.models.node import NodeType, Node, TaiwanService
from app.models.taiwan import (
    TaiwanPaymentConfig, 
    TaiwanPaymentTransaction, 
    PaymentProvider, 
    PaymentMethod, 
    PaymentStatus
)


# 測試資料庫設定
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """建立測試資料庫 session"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_user(db_session):
    """建立測試用戶"""
    user = User(
        name="測試用戶",
        email="test@example.com",
        password_hash="hashed_password",
        phone="0912345678",
        email_verified=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


class TestUserModel:
    """用戶模型測試"""
    
    def test_create_user(self, db_session):
        """測試建立用戶"""
        user = User(
            name="新用戶",
            email="newuser@example.com",
            password_hash="hashed_password",
            phone="0987654321"
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.name == "新用戶"
        assert user.email == "newuser@example.com"
        assert user.phone == "0987654321"
        assert user.is_active is True
        assert user.email_verified is False
        assert user.created_at is not None
        assert user.updated_at is not None
    
    def test_user_relationships(self, db_session, sample_user):
        """測試用戶關聯"""
        # 建立用戶檔案
        profile = UserProfile(
            user_id=sample_user.id,
            bio="測試用戶的個人簡介",
            location="台北市"
        )
        db_session.add(profile)
        
        # 建立用戶偏好
        preferences = UserPreferences(
            user_id=sample_user.id,
            theme="dark",
            language="zh-TW"
        )
        db_session.add(preferences)
        
        db_session.commit()
        
        # 測試關聯
        assert sample_user.profile is not None
        assert sample_user.profile.bio == "測試用戶的個人簡介"
        assert sample_user.preferences is not None
        assert sample_user.preferences.theme == "dark"


class TestRefreshTokenModel:
    """Refresh Token 模型測試"""
    
    def test_create_refresh_token(self, db_session, sample_user):
        """測試建立 Refresh Token"""
        expires_at = datetime.utcnow() + timedelta(days=7)
        token = RefreshToken(
            user_id=sample_user.id,
            token="test_refresh_token",
            expires_at=expires_at,
            created_ip="127.0.0.1"
        )
        db_session.add(token)
        db_session.commit()
        
        assert token.id is not None
        assert token.user_id == sample_user.id
        assert token.token == "test_refresh_token"
        assert token.is_revoked is False
        assert token.created_ip == "127.0.0.1"
    
    def test_token_expiry_check(self, db_session, sample_user):
        """測試 Token 過期檢查"""
        # 建立已過期的 token
        expired_token = RefreshToken(
            user_id=sample_user.id,
            token="expired_token",
            expires_at=datetime.utcnow() - timedelta(hours=1)
        )
        db_session.add(expired_token)
        
        # 建立有效的 token
        valid_token = RefreshToken(
            user_id=sample_user.id,
            token="valid_token",
            expires_at=datetime.utcnow() + timedelta(hours=1)
        )
        db_session.add(valid_token)
        db_session.commit()
        
        assert expired_token.is_expired is True
        assert expired_token.is_valid is False
        assert valid_token.is_expired is False
        assert valid_token.is_valid is True


class TestWorkflowModel:
    """工作流模型測試"""
    
    def test_create_workflow(self, db_session, sample_user):
        """測試建立工作流"""
        workflow = Workflow(
            user_id=sample_user.id,
            name="測試工作流",
            description="這是一個測試工作流",
            status=WorkflowStatus.DRAFT,
            category="test",
            nodes=[{"id": "node1", "type": "trigger"}],
            edges=[{"source": "node1", "target": "node2"}]
        )
        db_session.add(workflow)
        db_session.commit()
        
        assert workflow.id is not None
        assert workflow.name == "測試工作流"
        assert workflow.status == WorkflowStatus.DRAFT
        assert workflow.execution_count == 0
        assert workflow.success_count == 0
        assert workflow.failure_count == 0
    
    def test_workflow_execution(self, db_session, sample_user):
        """測試工作流執行記錄"""
        workflow = Workflow(
            user_id=sample_user.id,
            name="執行測試工作流",
            status=WorkflowStatus.ACTIVE
        )
        db_session.add(workflow)
        db_session.commit()
        
        execution = WorkflowExecution(
            workflow_id=workflow.id,
            user_id=sample_user.id,
            status=ExecutionStatus.SUCCESS,
            trigger_type="manual",
            nodes_executed=3,
            nodes_successful=3,
            duration=1.5
        )
        db_session.add(execution)
        db_session.commit()
        
        assert execution.id is not None
        assert execution.workflow_id == workflow.id
        assert execution.status == ExecutionStatus.SUCCESS
        assert execution.duration == 1.5


class TestTaiwanModels:
    """台灣特色模型測試"""
    
    def test_taiwan_payment_config(self, db_session, sample_user):
        """測試台灣金流配置"""
        config = TaiwanPaymentConfig(
            user_id=sample_user.id,
            provider=PaymentProvider.LINE_PAY,
            config_name="Line Pay 測試配置",
            merchant_id="test_merchant",
            api_key_encrypted="encrypted_api_key",
            is_sandbox=True,
            supported_methods=[PaymentMethod.CREDIT_CARD, PaymentMethod.APPLE_PAY]
        )
        db_session.add(config)
        db_session.commit()
        
        assert config.id is not None
        assert config.provider == PaymentProvider.LINE_PAY
        assert config.config_name == "Line Pay 測試配置"
        assert config.is_sandbox is True
        assert PaymentMethod.CREDIT_CARD in config.supported_methods
    
    def test_taiwan_payment_transaction(self, db_session, sample_user):
        """測試台灣金流交易"""
        config = TaiwanPaymentConfig(
            user_id=sample_user.id,
            provider=PaymentProvider.ECPAY,
            config_name="綠界測試",
            merchant_id="test_merchant",
            api_key_encrypted="encrypted_key",
            supported_methods=[PaymentMethod.CREDIT_CARD]
        )
        db_session.add(config)
        db_session.commit()
        
        transaction = TaiwanPaymentTransaction(
            config_id=config.id,
            transaction_id="TXN_001",
            merchant_order_id="ORDER_001",
            amount=10000,  # 100.00 TWD
            product_name="測試商品",
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.SUCCESS,
            buyer_name="測試買家",
            buyer_email="buyer@example.com"
        )
        db_session.add(transaction)
        db_session.commit()
        
        assert transaction.id is not None
        assert transaction.transaction_id == "TXN_001"
        assert transaction.amount == 10000
        assert transaction.status == PaymentStatus.SUCCESS
        assert transaction.config_id == config.id


class TestNodeModels:
    """節點模型測試"""
    
    def test_node_type(self, db_session):
        """測試節點類型"""
        node_type = NodeType(
            name="linePay",
            display_name="Line Pay",
            category="payment",
            description="Line Pay 金流節點",
            version="1.0.0",
            is_taiwan_service=True,
            service_provider="Line",
            supports_webhook=True
        )
        db_session.add(node_type)
        db_session.commit()
        
        assert node_type.id is not None
        assert node_type.name == "linePay"
        assert node_type.display_name == "Line Pay"
        assert node_type.is_taiwan_service is True
        assert node_type.supports_webhook is True
    
    def test_node_instance(self, db_session, sample_user):
        """測試節點實例"""
        # 建立工作流
        workflow = Workflow(
            user_id=sample_user.id,
            name="節點測試工作流",
            status=WorkflowStatus.DRAFT
        )
        db_session.add(workflow)
        
        # 建立節點類型
        node_type = NodeType(
            name="testNode",
            display_name="測試節點",
            category="test"
        )
        db_session.add(node_type)
        db_session.commit()
        
        # 建立節點實例
        node = Node(
            workflow_id=workflow.id,
            node_type_id=node_type.id,
            node_key="test_node_1",
            node_name="我的測試節點",
            position_x=100.0,
            position_y=200.0,
            configuration={"param1": "value1"}
        )
        db_session.add(node)
        db_session.commit()
        
        assert node.id is not None
        assert node.workflow_id == workflow.id
        assert node.node_key == "test_node_1"
        assert node.position_x == 100.0
        assert node.configuration["param1"] == "value1"
