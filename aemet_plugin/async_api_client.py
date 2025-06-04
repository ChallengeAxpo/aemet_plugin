import aiohttp
import asyncio

class AsyncClient:
    def __init__(self, bucket_capacity = 40, refill_period = 60):
        """Initializes the AsyncClient with a token bucket for rate limiting.

        Args:
            bucket_capacity (int, optional): Maximum number of tokens in the bucket. Defaults to 40.
            refill_period (int, optional): Time in seconds to fully refill the bucket. Defaults to 60.
        """
        self.bucket_capacity = bucket_capacity
        self.refill_period = refill_period
        self.bucket_level = asyncio.Queue(maxsize = bucket_capacity)
        self.token_refill_task = asyncio.create_task(self.refill_tokens())

    async def refill_tokens(self):
        """Refills the token bucket at bucket_capacity every refill_period seconds

        Runs in the background and periodically adds tokens to the bucket,
        ensuring the rate limit is maintained. Defaults to 40 tokens every 60 seconds.
        """
        while True:
            tokens_to_refill = self.bucket_capacity - self.bucket_level.qsize() 
            for tokens in range(tokens_to_refill):
                await self.bucket_level.put(None)
            await asyncio.sleep(self.refill_period)

    async def fetch(self, url):
        """Fetches the content of a URL, according to token availability in the bucket.

        Args:
            url (str): The URL to fetch.

        Returns:
            bytes: The response content of the body.

        Raises:
            aiohttp.ClientResponseError: If the HTTP response status is an error (codes 5XX, 4XX).
        """
        await self.bucket_level.get() # Wait for a token to be available before making the request
        async with aiohttp.ClientSession() as session: # Create a session for making requests
            async with session.get(url) as response: 
                response.raise_for_status() # Raise an error for bad responses
                return await response.read()

    async def fetch_multiple(self, urls):
        """Fetches multiple URLs concurrently, respecting the rate limit.

        Args:
            urls (list of str): List of URLs to fetch.

        Returns:
            list: List of response contents for each URL.
        """
        tasks = [self.fetch(url) for url in urls] #create a list of tasks for each URL
        return await asyncio.gather(*tasks) 

    async def close(self):
        """Stops the token refill task in the background"""
        self.token_refill_task.cancel()