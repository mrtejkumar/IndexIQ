# core/news.py

from datetime import datetime

def get_latest_news():
    # Replace with actual API integration (NewsAPI, NewsCatcher, etc.)
    return [
        {
            "title": "Nifty gains 150 points as IT, Banking stocks rally",
            "summary": "Indian equity markets opened higher led by gains in IT and private banks as global cues turned positive.",
            "url": "https://example.com/nifty-gains",
            "source": "MoneyControl",
            "published": datetime.now().strftime("%Y-%m-%d %H:%M")
        },
        {
            "title": "RBI keeps repo rate unchanged at 6.5%",
            "summary": "The Reserve Bank of India decided to maintain the key interest rate citing inflation concerns and global uncertainty.",
            "url": "https://example.com/rbi-hold",
            "source": "Economic Times",
            "published": datetime.now().strftime("%Y-%m-%d %H:%M")
        },
        {
            "title": "Reliance announces Q1 results, profit up 10%",
            "summary": "Reliance Industries reported a 10% increase in quarterly profits driven by strong retail and energy performance.",
            "url": "https://example.com/reliance-q1",
            "source": "Business Standard",
            "published": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    ]
