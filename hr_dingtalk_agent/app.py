from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from dingtalk_handler import DingTalkHandler
import uvicorn
import json
import hmac
import base64
import time
from config import Config

app = FastAPI(title="HR DingTalk AI Agent")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建DingTalk处理器实例
dingtalk_handler = DingTalkHandler()

def verify_signature(timestamp: str, signature: str, request_body: bytes) -> bool:
    """验证钉钉请求签名"""
    app_secret = Config.DINGTALK_APP_SECRET
    string_to_sign = f"{timestamp}\n{app_secret}"
    hmac_code = hmac.new(
        app_secret.encode('utf-8'),
        string_to_sign.encode('utf-8'),
        digestmod='SHA256'
    ).digest()
    
    calculated_signature = base64.b64encode(hmac_code).decode('utf-8')
    return calculated_signature == signature

@app.post("/webhook")
async def handle_webhook(request: Request):
    """处理钉钉回调请求"""
    try:
        # 获取钉钉的签名信息
        timestamp = request.headers.get("timestamp")
        signature = request.headers.get("sign")
        
        # 读取请求体
        body = await request.body()
        
        # 验证签名
        if not verify_signature(timestamp, signature, body):
            raise HTTPException(status_code=401, detail="签名验证失败")
        
        # 解析请求数据
        data = json.loads(body)
        
        # 处理回调数据
        if data.get("type") == "message":
            response = await dingtalk_handler.handle_message(data.get("message", {}))
            return response
            
        return {"message": "success"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"}

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的清理工作"""
    dingtalk_handler.close()

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
