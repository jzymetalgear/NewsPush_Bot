import requests
import config
import telegram
import asyncio

MAX_MESSAGE_LENGTH = 4096  # Maximum length of a Telegram message
MAX_ARTICLES = 10  # Maximum number of articles to display

async def send_message(content):
    bot = telegram.Bot(token=config.TELEGRAM_BOT_TOKEN)
    chat_id = config.TELEGRAM_CHAT_ID
    await bot.send_message(chat_id=chat_id, text=content)

def fetch_financial_news():
    # Replace 'YOUR_API_KEY' with your actual NewsAPI key
    api_key = config.NEWSAPI_KEY_ID
    url = f'https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get('articles', [])
        
        news_info = []
        for i, article in enumerate(articles[:MAX_ARTICLES], start=1):
            source = article.get('source', {}).get('name', '')
            title = article.get('title', '')
            description = article.get('description', '')
            url = article.get('url', '')
            
            news_info.append(f"{i}. {title}\nSource: {source}\nDescription: {description}\nRead more: {url}\n")
        
        return '\n'.join(news_info)
    else:
        print(f"Failed to fetch financial news. Error: {response.status_code}")

async def push_daily_financial_news():
    while True:
        daily_financial_news = fetch_financial_news()

        if daily_financial_news:
            message = f"Good morning! Here are today's top {MAX_ARTICLES} financial news articles:\n\n{daily_financial_news}"
            if len(message) > MAX_MESSAGE_LENGTH:
                message = message[:MAX_MESSAGE_LENGTH]
            await send_message(message)
        else:
            print("No financial news articles found.")
        
        # Sleep for 6 hours
        await asyncio.sleep(6 * 60 * 60)

asyncio.run(push_daily_financial_news())
