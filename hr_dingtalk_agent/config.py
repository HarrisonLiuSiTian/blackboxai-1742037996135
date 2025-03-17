import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # DingTalk Configuration
    DINGTALK_APP_KEY = os.getenv('DINGTALK_APP_KEY')
    DINGTALK_APP_SECRET = os.getenv('DINGTALK_APP_SECRET')
    DINGTALK_AGENT_ID = os.getenv('DINGTALK_AGENT_ID')
    
    # Database Configuration
    DB_TYPE = os.getenv('DB_TYPE', 'sqlite')  # or mysql, postgresql
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'hr_data')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # HR Data Tables
    HR_TABLES = {
        'employees': 'employee_info',
        'attendance': 'attendance_records',
        'career': 'career_history',
        'departments': 'department_info',
        'positions': 'position_info'
    }
    
    # AI Agent Configuration
    AGENT_PROMPT_TEMPLATE = """
    你是一个专业的人力资源助手，可以帮助查询和解答HR相关问题。
    你可以访问以下数据：
    - 员工基本信息
    - 考勤记录
    - 职业发展记录
    - 部门信息
    - 岗位信息
    
    请根据用户的问题，提供准确、专业的回答。
    """
    
    @staticmethod
    def get_db_url():
        if Config.DB_TYPE == 'sqlite':
            return f'sqlite:///{Config.DB_NAME}.db'
        return f'{Config.DB_TYPE}://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}'
