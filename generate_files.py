import json
from datetime import datetime
from tokenize_uk import tokenize_words


with open('messages.json') as data_file:    
    data = json.load(data_file)


# Define the start and end dates for filtering
start_date = datetime(2022, 2, 1)
end_date = datetime(2023, 8, 31)

# Create a list of lists to store posts by month
posts_by_month = [[] for _ in range(19)]

# Iterate through the data and filter posts by date
for key, post_data in data.items():

    post_date = datetime.strptime(post_data[0]['date'], "%Y-%m-%d %H:%M:%S")
    if start_date <= post_date <= end_date:
        month_index = (post_date.year - 2022) * 12 + post_date.month - 2
        posts_by_month[month_index].append({key: post_data})

w = []

# Save posts to separate JSON files
for i, posts in enumerate(posts_by_month):
    month = start_date.month + i
    year = start_date.year + (month - 1) // 12
    month = (month - 1) % 12 + 1
    file_name = f"{year}-{month:02}.txt"

    for post in posts:

        for val in post.values():
            
            words = tokenize_words(val[1]['post'])

            w.append(len(words))

            if len(words) > 50:
                with open(f'long/{file_name}', "a", encoding="utf-8") as long_posts:
                    long_posts.write(f'{val[0]["date"]}\n')
                    long_posts.write(f'{val[1]["post"].strip()}\n')
                    long_posts.write('\n') 

            else:
                with open(f'short/{file_name}', "a", encoding="utf-8") as short_posts:
                    short_posts.write(f'{val[0]["date"]}\n')
                    short_posts.write(f'{val[1]["post"].strip()}\n')
                    short_posts.write('\n') 



print(sum(w))