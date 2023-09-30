from pytz import timezone 
import telethon
from datetime import datetime
from collections import defaultdict
from remove_extra import remove_emojis
import asyncio
import json
from telethon.errors import rpcerrorlist
from langdetect import detect, LangDetectException

TELEGRAM_CHANNEL = 'https://t.me/+OX04hwkLncZhZjI6'
api_id = '...'
api_hash = '...'
phone_number = '...'
user_name = '...'

client = telethon.TelegramClient(user_name, api_id, api_hash)

async def get_posts(channel_username, limit, offset_id):

    posts = []

    while len(posts) < limit:
        try:
            messages = await client.get_messages(channel_username,limit=100,offset_id=offset_id)
        except rpcerrorlist.FloodWaitError as e:
            # Handle FloodWaitError by waiting for the specified time
            wait_time = e.seconds
            print(f"FloodWaitError: Waiting for {wait_time} seconds before retrying...")
            await asyncio.sleep(wait_time)
            continue

        if not messages:
            break
    
        posts.extend(messages)

        offset_id = messages[-1].id

    return posts, offset_id

posts_dict = {}

async def main():
    await client.start(phone_number)
    channel_username = TELEGRAM_CHANNEL
    limit = 100
    offset_id = 0
    counter = 0

    def contains_letters(input_string):
        for char in input_string:
            if char.isalpha():
                return True
        return False

    while True:
        posts, offset_id = await get_posts(channel_username, limit, offset_id)
        if not posts:
            break

        local_tz = timezone('Europe/Kiev')

            
        for ind, post in enumerate(posts):

            if post.text != None and post.text.strip() != '' and contains_letters(post.text):
                
                try:

                    lang_detected = detect(post.text)

                    if lang_detected=='uk':

                        message = str(post.message).replace('\n', ' ').strip()
                        clean_message = remove_emojis(message)
                        entire_date = post.date.astimezone(local_tz)
                        formatted_date = entire_date.strftime("%Y-%m-%d %H:%M:%S")

                        index = f"{ind:02}"

                        posts_dict[f'{counter}{index}'] = [{"date":formatted_date}, {"post":clean_message}]

                        print(f'{counter}{index}')
                        print(formatted_date)
                        print(clean_message)
                        print('\n')
                
                except LangDetectException:
                    continue

                
        counter += 1
                
        await asyncio.sleep(5)
        
    await client.disconnect()

    with open('messages.json', 'w') as outfile:
        json.dump(posts_dict, outfile, ensure_ascii=False, indent=4)

if __name__=='__main__':
    asyncio.run(main())

