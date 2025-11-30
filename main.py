import asyncio
import logging
from config import Config
from pyrogram import Client as VJ, idle
from plugins.regix import restart_forwards

# লগিং কনফিগারেশন (অপশনাল, কিন্তু ভালো)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    # ক্লায়েন্ট ইনিশিয়েলাইজেশন
    VJBot = VJ(
        "VJ-Forward-Bot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        sleep_threshold=120,
        plugins=dict(root="plugins")
    )
    
    # মেইন ফাংশন
    async def main():
        await VJBot.start()
        bot_info = await VJBot.get_me()
        print(f"Bot Started as {bot_info.first_name} (@{bot_info.username})")
        
        # রিস্টার্ট লজিক
        await restart_forwards(VJBot)
        
        # বট চালু রাখা
        await idle()
        
        # বট বন্ধ করার সময়
        await VJBot.stop()

    # কোড রান করার সঠিক নিয়ম (Fix for DeprecationWarning)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
