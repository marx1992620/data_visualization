from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.templating import Jinja2Templates

app = FastAPI()

# 配置跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名进行跨域请求
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# 设置静态文件夹，用于提供HTML文件和JavaScript代码
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# 首页路由，提供HTML文件
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("board.html", {"request": request})

# POST路由，用于接收前端发送的数据
# @app.post("/api/data")
# async def get_data():
#     response_data = {
#         'labels': ['红色', '蓝色', '黄色', '绿色', '紫色'],
#         'data': [12, 19, 3, 5, 2]
#     }
#     return response_data