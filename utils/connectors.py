from cogs.error import ResponseStatusError

async def fetch(session, url: str, timeout: float = None, raise_over: int = 300, body: str = 'json'):
    async with session.get(url, timeout=timeout) as resp:
        if resp.status >= raise_over:
            raise ResponseStatusError(resp.status, resp.reason, url)
        cont = getattr(resp, body)
        return await cont()
