"""
n8n 整合測試
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch

from app.services.n8n_service import N8nService


class TestN8nIntegration:
    """n8n 整合測試類別"""
    
    @pytest.fixture
    async def n8n_service(self):
        """建立 n8n 服務實例"""
        service = N8nService()
        yield service
        await service.client.aclose()
    
    @pytest.mark.asyncio
    async def test_health_check(self, n8n_service):
        """測試 n8n 健康檢查"""
        with patch.object(n8n_service.client, 'get') as mock_get:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_get.return_value = mock_response
            
            result = await n8n_service.health_check()
            assert result is True
            mock_get.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_workflows(self, n8n_service):
        """測試取得工作流列表"""
        mock_workflows = [
            {
                "id": "1",
                "name": "測試工作流 1",
                "active": True
            },
            {
                "id": "2", 
                "name": "測試工作流 2",
                "active": False
            }
        ]
        
        with patch.object(n8n_service.client, 'get') as mock_get:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_workflows
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            result = await n8n_service.get_workflows()
            assert len(result) == 2
            assert result[0]["name"] == "測試工作流 1"
    
    @pytest.mark.asyncio
    async def test_create_workflow(self, n8n_service):
        """測試建立工作流"""
        workflow_data = {
            "name": "新測試工作流",
            "nodes": [
                {
                    "id": "start",
                    "name": "Start",
                    "type": "n8n-nodes-base.manualTrigger",
                    "position": [240, 300],
                    "parameters": {}
                }
            ],
            "connections": {}
        }
        
        mock_response_data = {
            "id": "new-workflow-id",
            "name": "新測試工作流",
            "active": False
        }
        
        with patch.object(n8n_service.client, 'post') as mock_post:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            result = await n8n_service.create_workflow(workflow_data)
            assert result["id"] == "new-workflow-id"
            assert result["name"] == "新測試工作流"
    
    @pytest.mark.asyncio
    async def test_execute_workflow(self, n8n_service):
        """測試執行工作流"""
        workflow_id = "test-workflow-id"
        input_data = {"message": "Hello World"}
        
        mock_execution_data = {
            "id": "execution-id",
            "workflowId": workflow_id,
            "status": "running"
        }
        
        with patch.object(n8n_service.client, 'post') as mock_post:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_execution_data
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            result = await n8n_service.execute_workflow(workflow_id, input_data)
            assert result["id"] == "execution-id"
            assert result["workflowId"] == workflow_id
    
    @pytest.mark.asyncio
    async def test_get_execution_status(self, n8n_service):
        """測試取得執行狀態"""
        execution_id = "test-execution-id"
        
        mock_execution_status = {
            "id": execution_id,
            "finished": True,
            "mode": "manual",
            "status": "success",
            "data": {
                "resultData": {
                    "runData": {}
                }
            }
        }
        
        with patch.object(n8n_service.client, 'get') as mock_get:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_execution_status
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            result = await n8n_service.get_execution(execution_id)
            assert result["id"] == execution_id
            assert result["finished"] is True
            assert result["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_workflow_json_creation(self, n8n_service):
        """測試工作流 JSON 建立輔助方法"""
        nodes = [
            n8n_service.create_node(
                "start",
                "Start",
                "n8n-nodes-base.manualTrigger",
                [240, 300],
                {}
            ),
            n8n_service.create_node(
                "set-data",
                "Set Data", 
                "n8n-nodes-base.set",
                [460, 300],
                {
                    "values": {
                        "string": [
                            {
                                "name": "message",
                                "value": "Hello Taiwan!"
                            }
                        ]
                    }
                }
            )
        ]
        
        connections = {
            "Start": {
                "main": [
                    [n8n_service.create_connection("Start", "Set Data")]
                ]
            }
        }
        
        workflow = n8n_service.create_workflow_json(
            "台灣測試工作流",
            nodes,
            connections
        )
        
        assert workflow["name"] == "台灣測試工作流"
        assert len(workflow["nodes"]) == 2
        assert workflow["nodes"][0]["name"] == "Start"
        assert workflow["nodes"][1]["name"] == "Set Data"
        assert "Start" in workflow["connections"]
    
    def test_create_node_helper(self, n8n_service):
        """測試節點建立輔助方法"""
        node = n8n_service.create_node(
            "test-node",
            "Test Node",
            "n8n-nodes-base.httpRequest",
            [100, 200],
            {"url": "https://api.example.com"}
        )
        
        assert node["id"] == "test-node"
        assert node["name"] == "Test Node"
        assert node["type"] == "n8n-nodes-base.httpRequest"
        assert node["position"] == [100, 200]
        assert node["parameters"]["url"] == "https://api.example.com"
    
    def test_create_connection_helper(self, n8n_service):
        """測試連線建立輔助方法"""
        connection = n8n_service.create_connection("Source Node", "Target Node")
        
        assert connection["node"] == "Target Node"
        assert connection["type"] == "main"
        assert connection["index"] == 0


class TestN8nWorkflowExecution:
    """n8n 工作流執行測試"""
    
    @pytest.fixture
    async def n8n_service(self):
        """建立 n8n 服務實例"""
        service = N8nService()
        yield service
        await service.client.aclose()
    
    @pytest.mark.asyncio
    async def test_simple_workflow_execution(self, n8n_service):
        """測試簡單工作流執行"""
        # 建立簡單的測試工作流
        nodes = [
            n8n_service.create_node(
                "start",
                "Manual Trigger",
                "n8n-nodes-base.manualTrigger",
                [240, 300],
                {}
            ),
            n8n_service.create_node(
                "set-data",
                "Set Taiwan Data",
                "n8n-nodes-base.set",
                [460, 300],
                {
                    "values": {
                        "string": [
                            {
                                "name": "country",
                                "value": "Taiwan"
                            },
                            {
                                "name": "message", 
                                "value": "Hello from Taiwan!"
                            }
                        ]
                    }
                }
            )
        ]
        
        connections = {
            "Manual Trigger": {
                "main": [
                    [n8n_service.create_connection("Manual Trigger", "Set Taiwan Data")]
                ]
            }
        }
        
        workflow_data = n8n_service.create_workflow_json(
            "台灣簡單測試工作流",
            nodes,
            connections
        )
        
        # 模擬建立和執行工作流
        with patch.object(n8n_service.client, 'post') as mock_post:
            # 模擬建立工作流回應
            create_response = AsyncMock()
            create_response.json.return_value = {
                "id": "taiwan-workflow-id",
                "name": "台灣簡單測試工作流"
            }
            create_response.raise_for_status.return_value = None
            
            # 模擬執行工作流回應
            execute_response = AsyncMock()
            execute_response.json.return_value = {
                "id": "taiwan-execution-id",
                "workflowId": "taiwan-workflow-id"
            }
            execute_response.raise_for_status.return_value = None
            
            mock_post.side_effect = [create_response, execute_response]
            
            # 建立工作流
            created_workflow = await n8n_service.create_workflow(workflow_data)
            assert created_workflow["id"] == "taiwan-workflow-id"
            
            # 執行工作流
            execution = await n8n_service.execute_workflow(
                created_workflow["id"],
                {"test": "data"}
            )
            assert execution["id"] == "taiwan-execution-id"
    
    @pytest.mark.asyncio
    async def test_taiwan_payment_workflow(self, n8n_service):
        """測試台灣金流工作流"""
        # 建立包含台灣金流節點的工作流
        nodes = [
            n8n_service.create_node(
                "webhook",
                "Webhook Trigger",
                "n8n-nodes-base.webhook",
                [240, 300],
                {
                    "path": "taiwan-payment",
                    "httpMethod": "POST"
                }
            ),
            n8n_service.create_node(
                "line-pay",
                "Line Pay",
                "linePay",  # 我們的自定義節點
                [460, 300],
                {
                    "resource": "payment",
                    "operation": "create",
                    "amount": "={{ $json.amount }}",
                    "productName": "={{ $json.productName }}",
                    "orderId": "={{ $json.orderId }}"
                }
            )
        ]
        
        connections = {
            "Webhook Trigger": {
                "main": [
                    [n8n_service.create_connection("Webhook Trigger", "Line Pay")]
                ]
            }
        }
        
        workflow_data = n8n_service.create_workflow_json(
            "台灣金流處理工作流",
            nodes,
            connections
        )
        
        # 驗證工作流結構
        assert workflow_data["name"] == "台灣金流處理工作流"
        assert len(workflow_data["nodes"]) == 2
        
        # 驗證 Line Pay 節點配置
        line_pay_node = workflow_data["nodes"][1]
        assert line_pay_node["type"] == "linePay"
        assert line_pay_node["parameters"]["resource"] == "payment"
        assert line_pay_node["parameters"]["operation"] == "create"
