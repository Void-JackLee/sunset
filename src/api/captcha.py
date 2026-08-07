from fastapi import APIRouter, Request
import redis
import uuid
from captcha.image import ImageCaptcha
from fastapi.responses import StreamingResponse

app = APIRouter()
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def verifyCode(code: str, request: Request):
    captcha_id = request.cookies.get("captcha-id")
    if not captcha_id:
        return False
    _code = r.get(f"captcha:{captcha_id}")
    r.delete(f"captcha:{captcha_id}")
    print(f'_code={_code}, code={code}')
    if _code and code and _code.lower() == code.lower():
        return True
    return False

# 使用redis + captcha防止爬虫
# 生成图片验证码
@app.get("/captcha")
def get_captcha():
    image = ImageCaptcha()
    captcha_text = str(uuid.uuid4())[:4]  # 生成4位验证码
    data = image.generate(captcha_text)
    captcha_id = str(uuid.uuid4())
    # 存储到 Redis，过期时间5分钟
    r.setex(f"captcha:{captcha_id}", 300, captcha_text.lower())
    # 返回图片和captcha_id
    response = StreamingResponse(data, media_type="image/png")
    response.set_cookie(key="captcha-id", value=captcha_id, httponly=True, path="/", expires=60*5)
    return response
