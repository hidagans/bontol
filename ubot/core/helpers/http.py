import httpx
from asyncio import gather

# HTTPx Async Client
http = httpx.AsyncClient(
    http2=True,
    verify=False,
    timeout=httpx.Timeout(40),
)

async def get(url: str, *args, **kwargs):
    async with http.get(url, *args, **kwargs) as resp:
        try:
            data = resp.json()
        except httpx.HTTPStatusError:
            data = resp.text()
    return data

async def head(url: str, *args, **kwargs):
    async with http.head(url, *args, **kwargs) as resp:
        try:
            data = resp.json()
        except httpx.HTTPStatusError:
            data = resp.text()
    return data

async def post(url: str, *args, **kwargs):
    async with http.post(url, *args, **kwargs) as resp:
        try:
            data = resp.json()
        except httpx.HTTPStatusError:
            data = resp.text()
    return data

async def multiget(url: str, times: int, *args, **kwargs):
    return await gather(*[get(url, *args, **kwargs) for _ in range(times)])

async def multihead(url: str, times: int, *args, **kwargs):
    return await gather(*[head(url, *args, **kwargs) for _ in range(times)])

async def multipost(url: str, times: int, *args, **kwargs):
    return await gather(*[post(url, *args, **kwargs) for _ in range(times)])
