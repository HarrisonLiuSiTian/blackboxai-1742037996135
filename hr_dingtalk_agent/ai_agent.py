from typing import Dict, List, Optional
import openai
from datetime import datetime, timedelta
from config import Config
from db_handler import HRDatabaseHandler

class HRAIAgent:
    def __init__(self):
        self.db = HRDatabaseHandler()
        openai.api_key = Config.OPENAI_API_KEY
        self.context = Config.AGENT_PROMPT_TEMPLATE

    def _extract_date_range(self, query: str) -> tuple:
        """从查询中提取日期范围"""
        # 默认查询最近一个月
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # TODO: 使用NLP提取具体的日期范围
        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

    def _extract_employee_info(self, query: str) -> tuple:
        """从查询中提取员工信息"""
        # TODO: 使用NLP提取员工ID或姓名
        return None, None

    def process_query(self, query: str) -> Dict:
        """处理用户查询并返回响应"""
        try:
            # 使用OpenAI分析查询意图
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.context},
                    {"role": "user", "content": query}
                ]
            )
            
            # 解析意图和所需信息
            intent = self._analyze_intent(query)
            
            if "个人信息" in intent or "基本信息" in intent:
                employee_id, name = self._extract_employee_info(query)
                result = self.db.get_employee_info(employee_id, name)
                return self._format_employee_info_response(result)
                
            elif "考勤" in intent or "出勤" in intent:
                employee_id, _ = self._extract_employee_info(query)
                start_date, end_date = self._extract_date_range(query)
                result = self.db.get_attendance_records(employee_id, start_date, end_date)
                return self._format_attendance_response(result)
                
            elif "履历" in intent or "经历" in intent or "职业发展" in intent:
                employee_id, _ = self._extract_employee_info(query)
                result = self.db.get_career_history(employee_id)
                return self._format_career_response(result)
                
            elif "部门" in intent:
                result = self.db.get_department_info()
                return self._format_department_response(result)
                
            elif "搜索" in intent:
                result = self.db.search_employees(query)
                return self._format_search_response(result)
                
            else:
                return {
                    "type": "text",
                    "content": "抱歉，我没有理解您的问题。请尝试用更明确的方式描述您的需求。"
                }
                
        except Exception as e:
            return {
                "type": "text",
                "content": f"处理查询时发生错误: {str(e)}"
            }

    def _analyze_intent(self, query: str) -> str:
        """分析查询意图"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "请分析以下人力资源相关查询的意图，可能的意图包括：个人信息查询、考勤查询、履历查询、部门查询、搜索员工"},
                    {"role": "user", "content": query}
                ]
            )
            return response.choices[0].message.content
        except Exception:
            # 如果API调用失败，使用简单的关键词匹配
            intents = {
                "个人信息": ["个人", "信息", "基本"],
                "考勤": ["考勤", "出勤", "打卡"],
                "履历": ["履历", "经历", "职业", "发展"],
                "部门": ["部门", "团队"],
                "搜索": ["搜索", "查找", "查询"]
            }
            
            for intent, keywords in intents.items():
                if any(keyword in query for keyword in keywords):
                    return intent
            return "未知"

    def _format_employee_info_response(self, data: List[Dict]) -> Dict:
        """格式化员工信息响应"""
        if not data:
            return {"type": "text", "content": "未找到相关员工信息"}
        
        if isinstance(data, dict) and 'error' in data:
            return {"type": "text", "content": data['error']}
            
        response = "员工信息如下：\n\n"
        for employee in data:
            response += f"姓名：{employee.get('name', 'N/A')}\n"
            response += f"工号：{employee.get('employee_id', 'N/A')}\n"
            response += f"部门：{employee.get('department_name', 'N/A')}\n"
            response += f"职位：{employee.get('position_name', 'N/A')}\n"
            response += f"邮箱：{employee.get('email', 'N/A')}\n"
            response += "-------------------\n"
            
        return {"type": "text", "content": response.strip()}

    def _format_attendance_response(self, data: List[Dict]) -> Dict:
        """格式化考勤记录响应"""
        if not data:
            return {"type": "text", "content": "未找到相关考勤记录"}
            
        if isinstance(data, dict) and 'error' in data:
            return {"type": "text", "content": data['error']}
            
        response = "考勤记录如下：\n\n"
        for record in data:
            response += f"日期：{record.get('date', 'N/A')}\n"
            response += f"签到时间：{record.get('check_in', 'N/A')}\n"
            response += f"签退时间：{record.get('check_out', 'N/A')}\n"
            response += f"状态：{record.get('status', 'N/A')}\n"
            response += "-------------------\n"
            
        return {"type": "text", "content": response.strip()}

    def _format_career_response(self, data: List[Dict]) -> Dict:
        """格式化职业发展历程响应"""
        if not data:
            return {"type": "text", "content": "未找到相关职业发展记录"}
            
        if isinstance(data, dict) and 'error' in data:
            return {"type": "text", "content": data['error']}
            
        response = "职业发展历程如下：\n\n"
        for record in data:
            response += f"时间段：{record.get('start_date', 'N/A')} 至 {record.get('end_date', 'N/A')}\n"
            response += f"部门：{record.get('department_name', 'N/A')}\n"
            response += f"职位：{record.get('position_name', 'N/A')}\n"
            response += f"职责：{record.get('responsibilities', 'N/A')}\n"
            response += "-------------------\n"
            
        return {"type": "text", "content": response.strip()}

    def _format_department_response(self, data: List[Dict]) -> Dict:
        """格式化部门信息响应"""
        if not data:
            return {"type": "text", "content": "未找到相关部门信息"}
            
        if isinstance(data, dict) and 'error' in data:
            return {"type": "text", "content": data['error']}
            
        response = "部门信息如下：\n\n"
        for dept in data:
            response += f"部门名称：{dept.get('department_name', 'N/A')}\n"
            response += f"部门主管：{dept.get('manager_name', 'N/A')}\n"
            response += f"部门描述：{dept.get('description', 'N/A')}\n"
            response += "-------------------\n"
            
        return {"type": "text", "content": response.strip()}

    def _format_search_response(self, data: List[Dict]) -> Dict:
        """格式化搜索结果响应"""
        if not data:
            return {"type": "text", "content": "未找到匹配的员工信息"}
            
        if isinstance(data, dict) and 'error' in data:
            return {"type": "text", "content": data['error']}
            
        response = "搜索结果如下：\n\n"
        for employee in data:
            response += f"姓名：{employee.get('name', 'N/A')}\n"
            response += f"工号：{employee.get('employee_id', 'N/A')}\n"
            response += f"部门：{employee.get('department_name', 'N/A')}\n"
            response += f"职位：{employee.get('position_name', 'N/A')}\n"
            response += "-------------------\n"
            
        return {"type": "text", "content": response.strip()}

    def close(self):
        """关闭数据库连接"""
        self.db.close()
