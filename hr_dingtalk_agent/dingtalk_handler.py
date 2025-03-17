from typing import Dict, Optional
from dingtalk import AppKeyClient
from config import Config
from ai_agent import HRAIAgent

class DingTalkHandler:
    def __init__(self):
        self.client = AppKeyClient(
            app_key=Config.DINGTALK_APP_KEY,
            app_secret=Config.DINGTALK_APP_SECRET
        )
        self.agent_id = Config.DINGTALK_AGENT_ID
        self.ai_agent = HRAIAgent()

    async def handle_message(self, message: Dict) -> Dict:
        """处理来自钉钉的消息"""
        try:
            msg_type = message.get('msgtype')
            sender_id = message.get('senderStaffId')
            
            # 获取发送者信息
            sender_info = await self.get_user_info(sender_id)
            
            if msg_type == 'text':
                content = message.get('text', {}).get('content', '')
                return await self.process_text_message(content, sender_info)
            else:
                return {
                    "msgtype": "text",
                    "text": {
                        "content": "目前只支持文本消息查询"
                    }
                }
        except Exception as e:
            return {
                "msgtype": "text",
                "text": {
                    "content": f"消息处理出错: {str(e)}"
                }
            }

    async def process_text_message(self, content: str, sender_info: Dict) -> Dict:
        """处理文本消息"""
        try:
            # 检查用户权限
            if not await self.check_user_permission(sender_info):
                return {
                    "msgtype": "text",
                    "text": {
                        "content": "抱歉，您没有权限访问此功能"
                    }
                }

            # 使用AI Agent处理查询
            response = self.ai_agent.process_query(content)
            
            # 转换为钉钉消息格式
            return self.format_dingtalk_message(response)
            
        except Exception as e:
            return {
                "msgtype": "text",
                "text": {
                    "content": f"查询处理出错: {str(e)}"
                }
            }

    async def get_user_info(self, user_id: str) -> Dict:
        """获取钉钉用户信息"""
        try:
            response = await self.client.user.get(user_id)
            return {
                'userid': response.get('userid'),
                'name': response.get('name'),
                'department': response.get('department'),
                'position': response.get('position'),
                'email': response.get('email')
            }
        except Exception as e:
            return {'error': f'获取用户信息失败: {str(e)}'}

    async def check_user_permission(self, user_info: Dict) -> bool:
        """检查用户权限"""
        try:
            # 这里可以实现具体的权限检查逻辑
            # 例如检查用户是否属于特定部门，是否有特定角色等
            return True
        except Exception:
            return False

    def format_dingtalk_message(self, response: Dict) -> Dict:
        """将AI响应格式化为钉钉消息格式"""
        if response['type'] == 'text':
            return {
                "msgtype": "text",
                "text": {
                    "content": response['content']
                }
            }
        elif response['type'] == 'markdown':
            return {
                "msgtype": "markdown",
                "markdown": {
                    "title": "HR助手回复",
                    "text": response['content']
                }
            }
        else:
            return {
                "msgtype": "text",
                "text": {
                    "content": "不支持的响应类型"
                }
            }

    async def send_message(self, user_id: str, message: Dict) -> bool:
        """发送消息给指定用户"""
        try:
            await self.client.message.send_to_conversation(
                user_id=user_id,
                msg=message,
                agent_id=self.agent_id
            )
            return True
        except Exception as e:
            print(f"发送消息失败: {str(e)}")
            return False

    def close(self):
        """关闭AI Agent连接"""
        self.ai_agent.close()
