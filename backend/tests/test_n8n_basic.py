"""
n8n 基礎功能測試
"""

import pytest
from app.services.n8n_service import N8nService


class TestN8nBasic:
    """n8n 基礎功能測試"""
    
    def test_n8n_service_initialization(self):
        """測試 n8n 服務初始化"""
        service = N8nService()
        
        assert service.base_url is not None
        assert "localhost:5678" in service.base_url
        assert service.client is not None
    
    def test_create_workflow_json(self):
        """測試工作流 JSON 建立"""
        service = N8nService()
        
        nodes = [
            service.create_node(
                "start",
                "Start",
                "n8n-nodes-base.manualTrigger",
                [240, 300],
                {}
            )
        ]
        
        connections = {}
        
        workflow = service.create_workflow_json(
            "測試工作流",
            nodes,
            connections
        )
        
        assert workflow["name"] == "測試工作流"
        assert len(workflow["nodes"]) == 1
        assert workflow["nodes"][0]["name"] == "Start"
        assert workflow["active"] is False
    
    def test_create_node_helper(self):
        """測試節點建立輔助方法"""
        service = N8nService()
        
        node = service.create_node(
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
    
    def test_create_connection_helper(self):
        """測試連線建立輔助方法"""
        service = N8nService()
        
        connection = service.create_connection("Source Node", "Target Node")
        
        assert connection["node"] == "Target Node"
        assert connection["type"] == "main"
        assert connection["index"] == 0
    
    def test_taiwan_workflow_structure(self):
        """測試台灣工作流結構"""
        service = N8nService()
        
        # 建立包含台灣節點的工作流
        nodes = [
            service.create_node(
                "webhook",
                "Webhook",
                "n8n-nodes-base.webhook",
                [240, 300],
                {"path": "taiwan-payment"}
            ),
            service.create_node(
                "line-pay",
                "Line Pay",
                "linePay",
                [460, 300],
                {
                    "resource": "payment",
                    "operation": "create",
                    "amount": 1000,
                    "productName": "測試商品"
                }
            ),
            service.create_node(
                "response",
                "Response",
                "n8n-nodes-base.respondToWebhook",
                [680, 300],
                {"responseBody": "Payment processed"}
            )
        ]
        
        connections = {
            "Webhook": {
                "main": [
                    [service.create_connection("Webhook", "Line Pay")]
                ]
            },
            "Line Pay": {
                "main": [
                    [service.create_connection("Line Pay", "Response")]
                ]
            }
        }
        
        workflow = service.create_workflow_json(
            "台灣金流處理工作流",
            nodes,
            connections
        )
        
        # 驗證工作流結構
        assert workflow["name"] == "台灣金流處理工作流"
        assert len(workflow["nodes"]) == 3
        
        # 驗證節點類型
        node_types = [node["type"] for node in workflow["nodes"]]
        assert "n8n-nodes-base.webhook" in node_types
        assert "linePay" in node_types
        assert "n8n-nodes-base.respondToWebhook" in node_types
        
        # 驗證連線
        assert "Webhook" in workflow["connections"]
        assert "Line Pay" in workflow["connections"]
        
        # 驗證 Line Pay 節點參數
        line_pay_node = next(node for node in workflow["nodes"] if node["type"] == "linePay")
        assert line_pay_node["parameters"]["resource"] == "payment"
        assert line_pay_node["parameters"]["operation"] == "create"
        assert line_pay_node["parameters"]["amount"] == 1000


class TestN8nNodeValidation:
    """n8n 節點驗證測試"""
    
    def test_line_pay_node_parameters(self):
        """測試 Line Pay 節點參數驗證"""
        service = N8nService()
        
        # 測試完整的 Line Pay 節點配置
        line_pay_node = service.create_node(
            "line-pay-1",
            "Line Pay Payment",
            "linePay",
            [400, 300],
            {
                "resource": "payment",
                "operation": "create",
                "orderId": "TW-ORDER-001",
                "amount": 1500,
                "productName": "台灣特產禮盒",
                "confirmUrl": "https://example.com/confirm",
                "cancelUrl": "https://example.com/cancel"
            }
        )
        
        params = line_pay_node["parameters"]
        assert params["resource"] == "payment"
        assert params["operation"] == "create"
        assert params["orderId"] == "TW-ORDER-001"
        assert params["amount"] == 1500
        assert params["productName"] == "台灣特產禮盒"
        assert params["confirmUrl"] == "https://example.com/confirm"
        assert params["cancelUrl"] == "https://example.com/cancel"
    
    def test_ecpay_node_structure(self):
        """測試綠界節點結構"""
        service = N8nService()
        
        ecpay_node = service.create_node(
            "ecpay-1",
            "ECPay Payment",
            "ecPay",
            [400, 300],
            {
                "resource": "payment",
                "operation": "create",
                "merchantTradeNo": "TW-ECPAY-001",
                "totalAmount": 2000,
                "tradeDesc": "台灣商品購買",
                "paymentType": "aio"
            }
        )
        
        assert ecpay_node["type"] == "ecPay"
        params = ecpay_node["parameters"]
        assert params["merchantTradeNo"] == "TW-ECPAY-001"
        assert params["totalAmount"] == 2000
        assert params["tradeDesc"] == "台灣商品購買"
    
    def test_taiwan_airport_node_structure(self):
        """測試桃機航班節點結構"""
        service = N8nService()
        
        airport_node = service.create_node(
            "taoyuan-airport-1",
            "Taoyuan Airport",
            "taoyuanAirport",
            [400, 300],
            {
                "resource": "flight",
                "operation": "getInfo",
                "flightNumber": "CI123",
                "date": "2024-01-01"
            }
        )
        
        assert airport_node["type"] == "taoyuanAirport"
        params = airport_node["parameters"]
        assert params["resource"] == "flight"
        assert params["operation"] == "getInfo"
        assert params["flightNumber"] == "CI123"
        assert params["date"] == "2024-01-01"


class TestN8nWorkflowTemplates:
    """n8n 工作流模板測試"""
    
    def test_simple_taiwan_payment_template(self):
        """測試簡單台灣金流模板"""
        service = N8nService()
        
        # 建立簡單的台灣金流工作流模板
        template = service.create_workflow_json(
            "台灣金流模板",
            [
                service.create_node(
                    "trigger",
                    "Manual Trigger",
                    "n8n-nodes-base.manualTrigger",
                    [200, 300],
                    {}
                ),
                service.create_node(
                    "payment",
                    "Taiwan Payment",
                    "linePay",
                    [400, 300],
                    {
                        "resource": "payment",
                        "operation": "create",
                        "amount": "={{ $json.amount }}",
                        "productName": "={{ $json.productName }}",
                        "orderId": "={{ $json.orderId }}"
                    }
                ),
                service.create_node(
                    "notify",
                    "Send Notification",
                    "n8n-nodes-base.httpRequest",
                    [600, 300],
                    {
                        "method": "POST",
                        "url": "https://notify-api.line.me/api/notify",
                        "body": {
                            "message": "付款處理完成: {{ $json.orderId }}"
                        }
                    }
                )
            ],
            {
                "Manual Trigger": {
                    "main": [
                        [service.create_connection("Manual Trigger", "Taiwan Payment")]
                    ]
                },
                "Taiwan Payment": {
                    "main": [
                        [service.create_connection("Taiwan Payment", "Send Notification")]
                    ]
                }
            }
        )
        
        # 驗證模板結構
        assert template["name"] == "台灣金流模板"
        assert len(template["nodes"]) == 3
        assert len(template["connections"]) == 2
        
        # 驗證節點順序和類型
        node_names = [node["name"] for node in template["nodes"]]
        assert "Manual Trigger" in node_names
        assert "Taiwan Payment" in node_names
        assert "Send Notification" in node_names
        
        # 驗證動態參數設定
        payment_node = next(node for node in template["nodes"] if node["name"] == "Taiwan Payment")
        assert "={{ $json.amount }}" in payment_node["parameters"]["amount"]
        assert "={{ $json.productName }}" in payment_node["parameters"]["productName"]
