from fastapi import FastAPI
from fastapi_redis_cache import FastApiRedisCache

from gnc_todo.apps.auth import router_auth
from gnc_todo.apps.todo import router_todo
from gnc_todo.apps.users import router_users

app = FastAPI()
rd = FastApiRedisCache()

app.include_router(router=router_auth)
app.include_router(router=router_users)
app.include_router(router=router_todo)

rd.init(
    host_url="redis://127.0.0.1:3306"
)
