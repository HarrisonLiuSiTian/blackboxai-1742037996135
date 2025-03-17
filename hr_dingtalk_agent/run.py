import uvicorn
import os
from dotenv import load_dotenv

def main():
    """
    应用程序入口点
    加载环境变量并启动FastAPI服务器
    """
    # 加载环境变量
    load_dotenv()
    
    # 检查必要的环境变量
    required_env_vars = [
        'DINGTALK_APP_KEY',
        'DINGTALK_APP_SECRET',
        'DINGTALK_AGENT_ID',
        'OPENAI_API_KEY'
    ]
    
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        print("错误: 缺少必要的环境变量:")
        for var in missing_vars:
            print(f"- {var}")
        return
    
    # 启动FastAPI应用
    print("正在启动HR DingTalk AI Agent...")
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
