from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import Dict, List, Optional
import pandas as pd
from config import Config

class HRDatabaseHandler:
    def __init__(self):
        self.engine = create_engine(Config.get_db_url())
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_employee_info(self, employee_id: str = None, name: str = None) -> Dict:
        """获取员工基本信息"""
        query = f"""
            SELECT * FROM {Config.HR_TABLES['employees']}
            WHERE 1=1
        """
        params = {}
        if employee_id:
            query += " AND employee_id = :employee_id"
            params['employee_id'] = employee_id
        if name:
            query += " AND name LIKE :name"
            params['name'] = f"%{name}%"

        try:
            result = pd.read_sql(query, self.engine, params=params)
            return result.to_dict('records')
        except Exception as e:
            return {'error': f'获取员工信息失败: {str(e)}'}

    def get_attendance_records(self, employee_id: str, start_date: str, end_date: str) -> List[Dict]:
        """获取考勤记录"""
        query = f"""
            SELECT * FROM {Config.HR_TABLES['attendance']}
            WHERE employee_id = :employee_id
            AND date BETWEEN :start_date AND :end_date
        """
        try:
            result = pd.read_sql(query, self.engine, params={
                'employee_id': employee_id,
                'start_date': start_date,
                'end_date': end_date
            })
            return result.to_dict('records')
        except Exception as e:
            return {'error': f'获取考勤记录失败: {str(e)}'}

    def get_career_history(self, employee_id: str) -> List[Dict]:
        """获取职业发展历程"""
        query = f"""
            SELECT ch.*, d.department_name, p.position_name
            FROM {Config.HR_TABLES['career']} ch
            LEFT JOIN {Config.HR_TABLES['departments']} d ON ch.department_id = d.department_id
            LEFT JOIN {Config.HR_TABLES['positions']} p ON ch.position_id = p.position_id
            WHERE ch.employee_id = :employee_id
            ORDER BY ch.start_date DESC
        """
        try:
            result = pd.read_sql(query, self.engine, params={'employee_id': employee_id})
            return result.to_dict('records')
        except Exception as e:
            return {'error': f'获取职业发展历程失败: {str(e)}'}

    def get_department_info(self, department_id: str = None) -> List[Dict]:
        """获取部门信息"""
        query = f"""
            SELECT * FROM {Config.HR_TABLES['departments']}
            WHERE 1=1
        """
        params = {}
        if department_id:
            query += " AND department_id = :department_id"
            params['department_id'] = department_id

        try:
            result = pd.read_sql(query, self.engine, params=params)
            return result.to_dict('records')
        except Exception as e:
            return {'error': f'获取部门信息失败: {str(e)}'}

    def search_employees(self, search_term: str) -> List[Dict]:
        """搜索员工信息"""
        query = f"""
            SELECT e.*, d.department_name, p.position_name
            FROM {Config.HR_TABLES['employees']} e
            LEFT JOIN {Config.HR_TABLES['departments']} d ON e.department_id = d.department_id
            LEFT JOIN {Config.HR_TABLES['positions']} p ON e.position_id = p.position_id
            WHERE e.name LIKE :search_term
            OR e.employee_id LIKE :search_term
            OR e.email LIKE :search_term
        """
        try:
            result = pd.read_sql(query, self.engine, params={'search_term': f'%{search_term}%'})
            return result.to_dict('records')
        except Exception as e:
            return {'error': f'搜索员工信息失败: {str(e)}'}

    def close(self):
        """关闭数据库连接"""
        self.session.close()
