"""
工作流API測試
"""

import pytest
import uuid
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.database import get_db
from app.models.user import User
from app.models.workflow import Workflow
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate


@pytest.fixture
def client():
    """測試客戶端"""
    return TestClient(app)


@pytest.fixture
def test_user(db_session: Session):
    """建立測試用戶"""
    user = User(
        name="測試用戶",
        email="test@example.com",
        password_hash="hashed_password",
        email_verified=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_workflow(db_session: Session, test_user: User):
    """建立測試工作流"""
    workflow = Workflow(
        name="測試工作流",
        description="這是一個測試工作流",
        user_id=test_user.id,
        category="test",
        is_active=True,
        nodes=[
            {
                "id": "node1",
                "type": "trigger",
                "name": "開始",
                "position": {"x": 100, "y": 100}
            }
        ],
        edges=[],
        settings={"timeout": 300}
    )
    db_session.add(workflow)
    db_session.commit()
    db_session.refresh(workflow)
    return workflow


@pytest.fixture
def auth_headers(test_user: User):
    """認證標頭"""
    # 這裡應該生成真實的JWT token
    # 為了測試簡化，使用模擬token
    return {"Authorization": f"Bearer test_token_{test_user.id}"}


class TestWorkflowCRUD:
    """工作流CRUD API測試"""
    
    def test_get_workflows(self, client: TestClient, test_workflow: Workflow, auth_headers: dict):
        """測試取得工作流列表"""
        response = client.get("/api/v1/workflows/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # 檢查工作流資料格式
        workflow_data = data[0]
        assert "id" in workflow_data
        assert "name" in workflow_data
        assert "description" in workflow_data
        assert "user_id" in workflow_data
        assert "created_at" in workflow_data
        assert "updated_at" in workflow_data
        
        # 檢查UUID格式
        assert isinstance(workflow_data["id"], str)
        uuid.UUID(workflow_data["id"])  # 驗證UUID格式
    
    def test_create_workflow(self, client: TestClient, auth_headers: dict):
        """測試建立工作流"""
        workflow_data = {
            "name": "新工作流",
            "description": "這是一個新的工作流",
            "category": "automation",
            "tags": ["test", "automation"],
            "is_active": False,
            "nodes": [
                {
                    "id": "start",
                    "type": "trigger",
                    "name": "開始節點",
                    "position": {"x": 0, "y": 0}
                }
            ],
            "edges": [],
            "settings": {"timeout": 600}
        }
        
        response = client.post("/api/v1/workflows/", json=workflow_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # 檢查回應資料
        assert data["name"] == workflow_data["name"]
        assert data["description"] == workflow_data["description"]
        assert data["category"] == workflow_data["category"]
        assert data["tags"] == workflow_data["tags"]
        assert data["is_active"] == workflow_data["is_active"]
        assert len(data["nodes"]) == 1
        assert len(data["edges"]) == 0
        
        # 檢查UUID格式
        uuid.UUID(data["id"])
        uuid.UUID(data["user_id"])
    
    def test_get_workflow_by_id(self, client: TestClient, test_workflow: Workflow, auth_headers: dict):
        """測試取得指定工作流"""
        workflow_id = str(test_workflow.id)
        response = client.get(f"/api/v1/workflows/{workflow_id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == workflow_id
        assert data["name"] == test_workflow.name
        assert data["description"] == test_workflow.description
        assert data["category"] == test_workflow.category
    
    def test_get_workflow_invalid_uuid(self, client: TestClient, auth_headers: dict):
        """測試使用無效UUID取得工作流"""
        response = client.get("/api/v1/workflows/invalid-uuid", headers=auth_headers)
        
        assert response.status_code == 400
        assert "無效的工作流ID格式" in response.json()["detail"]
    
    def test_update_workflow(self, client: TestClient, test_workflow: Workflow, auth_headers: dict):
        """測試更新工作流"""
        workflow_id = str(test_workflow.id)
        update_data = {
            "name": "更新後的工作流",
            "description": "這是更新後的描述",
            "is_active": False
        }
        
        response = client.put(f"/api/v1/workflows/{workflow_id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"]
        assert data["is_active"] == update_data["is_active"]
    
    def test_delete_workflow(self, client: TestClient, test_workflow: Workflow, auth_headers: dict):
        """測試刪除工作流"""
        workflow_id = str(test_workflow.id)
        response = client.delete(f"/api/v1/workflows/{workflow_id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["message"] == "工作流刪除成功"
        assert data["workflow_id"] == workflow_id
        
        # 確認工作流已被刪除
        get_response = client.get(f"/api/v1/workflows/{workflow_id}", headers=auth_headers)
        assert get_response.status_code == 404


class TestWorkflowExecution:
    """工作流執行API測試"""
    
    def test_execute_workflow(self, client: TestClient, test_workflow: Workflow, auth_headers: dict):
        """測試執行工作流"""
        workflow_id = str(test_workflow.id)
        execution_data = {
            "trigger_data": {"input": "test_data"}
        }
        
        response = client.post(
            f"/api/v1/workflows/{workflow_id}/execute", 
            json=execution_data, 
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "id" in data
        assert data["workflow_id"] == workflow_id
        assert data["status"] in ["pending", "running", "success", "failed"]
        
        # 檢查UUID格式
        uuid.UUID(data["id"])
        uuid.UUID(data["workflow_id"])
        uuid.UUID(data["user_id"])
    
    def test_get_workflow_executions(self, client: TestClient, test_workflow: Workflow, auth_headers: dict):
        """測試取得工作流執行歷史"""
        workflow_id = str(test_workflow.id)
        response = client.get(f"/api/v1/workflows/{workflow_id}/executions", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_execute_inactive_workflow(self, client: TestClient, test_workflow: Workflow, auth_headers: dict):
        """測試執行已停用的工作流"""
        # 先停用工作流
        workflow_id = str(test_workflow.id)
        client.post(f"/api/v1/workflows/{workflow_id}/deactivate", headers=auth_headers)
        
        # 嘗試執行
        response = client.post(f"/api/v1/workflows/{workflow_id}/execute", headers=auth_headers)
        
        assert response.status_code == 400
        assert "工作流已停用" in response.json()["detail"]


class TestWorkflowStatus:
    """工作流狀態管理API測試"""
    
    def test_activate_workflow(self, client: TestClient, test_workflow: Workflow, auth_headers: dict):
        """測試啟用工作流"""
        workflow_id = str(test_workflow.id)
        response = client.post(f"/api/v1/workflows/{workflow_id}/activate", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "工作流已啟用"
        assert data["workflow_id"] == workflow_id
    
    def test_deactivate_workflow(self, client: TestClient, test_workflow: Workflow, auth_headers: dict):
        """測試停用工作流"""
        workflow_id = str(test_workflow.id)
        response = client.post(f"/api/v1/workflows/{workflow_id}/deactivate", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "工作流已停用"
        assert data["workflow_id"] == workflow_id


class TestWorkflowStats:
    """工作流統計API測試"""
    
    def test_get_workflow_stats(self, client: TestClient, test_workflow: Workflow, auth_headers: dict):
        """測試取得工作流統計"""
        workflow_id = str(test_workflow.id)
        response = client.get(f"/api/v1/workflows/{workflow_id}/stats", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["workflow_id"] == workflow_id
        assert "total_executions" in data
        assert "successful_executions" in data
        assert "failed_executions" in data
        assert "success_rate" in data
        assert isinstance(data["success_rate"], float)


class TestWorkflowTemplates:
    """工作流模板API測試"""
    
    def test_get_workflow_templates(self, client: TestClient):
        """測試取得工作流模板列表（不需要認證）"""
        response = client.get("/api/v1/workflows/templates/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_taiwan_featured_templates(self, client: TestClient):
        """測試取得台灣特色模板"""
        response = client.get("/api/v1/workflows/templates/?taiwan_featured=true")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestWorkflowDuplication:
    """工作流複製API測試"""
    
    def test_duplicate_workflow(self, client: TestClient, test_workflow: Workflow, auth_headers: dict):
        """測試複製工作流"""
        workflow_id = str(test_workflow.id)
        response = client.post(
            f"/api/v1/workflows/{workflow_id}/duplicate",
            json={"new_name": "複製的工作流"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["name"] == "複製的工作流"
        assert data["id"] != workflow_id  # 確保是新的ID
        assert data["is_active"] == False  # 複製的工作流預設為停用
        
        # 檢查UUID格式
        uuid.UUID(data["id"])
