# HR DingTalk AI Agent

一个基于Python的HR智能助手，集成到钉钉中，用于查询公司人力资源相关信息。

## 功能特点

- 查询员工个人信息
- 查询考勤记录
- 查询职业发展履历
- 查询部门信息
- 智能分析和回答HR相关问题

## 技术栈

- Python 3.8+
- FastAPI
- SQLAlchemy
- OpenAI GPT
- DingTalk SDK
- Pandas

## 环境要求

1. Python 3.8或更高版本
2. 数据库（支持SQLite、MySQL、PostgreSQL）
3. 钉钉企业应用
4. OpenAI API密钥

## 安装步骤

1. 克隆项目并安装依赖：
```bash
git clone [repository-url]
cd hr_dingtalk_agent
pip install -r requirements.txt
```

2. 配置环境变量：
创建`.env`文件并填入以下配置：
```env
# DingTalk配置
DINGTALK_APP_KEY=your_app_key
DINGTALK_APP_SECRET=your_app_secret
DINGTALK_AGENT_ID=your_agent_id

# 数据库配置
DB_TYPE=sqlite  # 或 mysql, postgresql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=hr_data
DB_USER=root
DB_PASSWORD=your_password

# OpenAI配置
OPENAI_API_KEY=your_openai_api_key
```

3. 初始化数据库：
确保数据库中已创建必要的表结构：
- employee_info（员工信息表）
- attendance_records（考勤记录表）
- career_history（职业发展表）
- department_info（部门信息表）
- position_info（职位信息表）

## 运行应用

使用以下命令启动应用：
```bash
python run.py
```

应用将在 http://localhost:8000 启动，并提供以下接口：
- `/webhook`: 钉钉回调接口
- `/health`: 健康检查接口

## 钉钉配置

1. 在钉钉开发者后台创建企业内部应用
2. 配置应用权限范围
3. 设置消息接收回调地址为：`http://your-domain/webhook`
4. 记录应用的AppKey、AppSecret和AgentId

## 使用示例

在钉钉中，用户可以向机器人发送以下类型的消息：

1. 查询个人信息：
```
查询张三的个人信息
```

2. 查询考勤记录：
```
查询张三最近一个月的考勤记录
```

3. 查询职业发展履历：
```
查看张三的职业发展历程
```

4. 查询部门信息：
```
查询技术部的信息
```

## 注意事项

1. 确保数据库中的数据符合预期的格式和结构
2. 保护好敏感配置信息，不要将其提交到版本控制系统
3. 定期检查和更新OpenAI API密钥
4. 监控应用日志，及时处理异常情况

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

[MIT License](LICENSE)
