from cogs.error import ResponseStatusError

async def fetch(session, url: str, headers: dict=None, timeout: float=None,
                raise_over: int=300, return_type: str='json', **kwargs):
    """A simple and dynamic way to fetch with aiohttp."""

    async with session.get(url, headers=headers, timeout=timeout, **kwargs) as resp:
        if resp.status > raise_over:
            raise ResponseStatusError(resp.status, resp.reason, url)
        cont = getattr(resp, return_type)
        return await cont()
