import asyncio
import aiohttp
import time
NUMBERS = range(12)
URL = 'http://httpbin.org/get?a={}'
sema = asyncio.Semaphore(3)


async def fetch_async(a):
    async with aiohttp.request('GET',URL.format(a)) as r:
        data = await r.json()
        print('+++++++++from ',data)
        await asyncio.sleep(3)               #一共停3*(12%3)s 因为锁住了 每次只能进3个
        #time.sleep(3)                       #一共停30s
    return data['args']['a']

async def print_result(a):
    with await(sema):
        r = await fetch_async(a)                                     #相当于yield from
        print('------from ',r)
        print('fetch{}={}'.format(a,r))


loop = asyncio.get_event_loop()
f = asyncio.wait([print_result(x) for x in NUMBERS])                 #创建一个协同的执行同步任务的对象
loop.run_until_complete(f)