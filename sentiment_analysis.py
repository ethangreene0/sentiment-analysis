#Ethan Thomas Davies Greene
#251348539
#egreene4
#November 12 2023

#This file contains all the functions that are needed to complete the text analysis

# Function to read keywords and their scores from a file
def read_keywords(keyword_file_name):
    keyword_scores = {}

    try:
        with open(keyword_file_name, 'r') as file:
            for line in file:
                keyword, score = line.strip().split('\t')
                keyword_scores[keyword] = int(score)
    except FileNotFoundError:
        print(f"Could not open file '{keyword_file_name}'!")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

    return keyword_scores


# Function to clean tweet text by removing non-English letters
def clean_tweet_text(tweet_text):
    def is_english_letter(char):
        return 'a' <= char <= 'z' or 'A' <= char <= 'Z'

    cleaned_text = ''.join([char.lower() for char in tweet_text if is_english_letter(char) or char.isspace()])

    return cleaned_text


# Function to calculate sentiment score of a tweet based on keywords
def calc_sentiment(tweet_text, keyword_dict):
    words = tweet_text.split()
    sentiment_score = 0

    for word in words:
        if word in keyword_dict:
            sentiment_score += keyword_dict[word]

    return sentiment_score


# Function to classify sentiment into 'positive', 'negative', or 'neutral'
def classify(score):
    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    else:
        return "neutral"


# Function to read tweets from a file and parse them into a list of dictionaries
def read_tweets(tweet_file_name):
    tweet_list = []

    try:
        with open(tweet_file_name, 'r', errors='ignore') as file:
            for line in file:
                fields = line.strip().split(',')

                # Extracting fields from each tweet
                date, text, user, retweet, favorite, lang, country, state, city, lat, lon = fields

                # Converting some fields to appropriate types
                favorite = int(favorite)
                retweet = int(retweet)
                lat = float(lat) if lat != 'NULL' else 'NULL'
                lon = float(lon) if lon != 'NULL' else 'NULL'

                # Cleaning the tweet text
                cleaned_text = clean_tweet_text(text)

                # Creating a dictionary for each tweet and appending it to the list
                tweet_dict = {
                    'date': date,
                    'text': cleaned_text,
                    'user': user,
                    'favorite': favorite,
                    'retweet': retweet,
                    'lang': lang,
                    'country': country,
                    'state': state,
                    'city': city,
                    'lat': lat,
                    'lon': lon
                }
                tweet_list.append(tweet_dict)

    except IOError:
        print(f"Could not open file {tweet_file_name}")
        return []

    return tweet_list


# Function to generate a report based on tweet sentiments and statistics
def make_report(tweet_list, keyword_dict):
    total_sentiment = 0
    total_favorite_sentiment = 0
    total_retweet_sentiment = 0
    num_tweets = len(tweet_list)
    num_favorite = 0
    num_retweet = 0
    num_positive = 0
    num_negative = 0
    num_neutral = 0
    country_sentiments = {}

    # Analyzing each tweet in the list
    for tweet in tweet_list:
        sentiment = calc_sentiment(tweet['text'], keyword_dict)
        total_sentiment += sentiment

        # Analyzing favorite and retweet sentiments
        if tweet['favorite'] > 0:
            total_favorite_sentiment += sentiment
            num_favorite += 1

        if tweet['retweet'] > 0:
            total_retweet_sentiment += sentiment
            num_retweet += 1

        # Counting positive, negative, and neutral tweets
        if sentiment > 0:
            num_positive += 1
        elif sentiment < 0:
            num_negative += 1
        else:
            num_neutral += 1

        # Grouping sentiment scores by country
        country = tweet.get('country', 'NULL')
        if country != 'NULL':
            country_sentiments.setdefault(country, []).append(sentiment)

    # Calculating average sentiments and selecting top five countries
    avg_sentiment = round(total_sentiment / num_tweets, 2) if num_tweets > 0 else 'NAN'
    avg_favorite = round(total_favorite_sentiment / num_favorite, 2) if num_favorite > 0 else 'NAN'
    avg_retweet = round(total_retweet_sentiment / num_retweet, 2) if num_retweet > 0 else 'NAN'

    top_five_countries = sorted(
        country_sentiments.keys(),
        key=lambda c: sum(country_sentiments[c]) / len(country_sentiments[c]),
        reverse=True
    )[:5]
    top_five_str = ', '.join(top_five_countries)

    # Creating a dictionary with report statistics
    report_dict = {
        'avg_favorite': avg_favorite,
        'avg_retweet': avg_retweet,
        'avg_sentiment': avg_sentiment,
        'num_favorite': num_favorite,
        'num_negative': num_negative,
        'num_neutral': num_neutral,
        'num_positive': num_positive,
        'num_retweet': num_retweet,
        'num_tweets': num_tweets,
        'top_five': top_five_str
    }

    return report_dict


# Function to write a report to an output file
def write_report(report, output_file):
    avg_sent = report["avg_sentiment"]
    num_tweets = report["num_tweets"]
    num_positive = report["num_positive"]
    num_negative = report["num_negative"]
    num_neutral = report["num_neutral"]
    num_favorite = report["num_favorite"]
    avg_favorite = report["avg_favorite"]
    num_retweet = report["num_retweet"]
    avg_retweet = report["avg_retweet"]
    top_countries = report["top_five"]

    try:
        with open(output_file, 'w') as file:
            # Writing various statistics to the report file
            file.write(f"Average sentiment of all tweets: {avg_sent}\n")
            file.write(f"Total number of tweets: {num_tweets}\n")
            file.write(f"Number of positive tweets: {num_positive}\n")
            file.write(f"Number of negative tweets: {num_negative}\n")
            file.write(f"Number of neutral tweets: {num_neutral}\n")
            file.write(f"Number of favorited tweets: {num_favorite}\n")
            file.write(f"Average sentiment of favorited tweets: {avg_favorite}\n")
            file.write(f"Number of retweeted tweets: {num_retweet}\n")
            file.write(f"Average sentiment of retweeted tweets: {avg_retweet}\n")

            if top_countries:
                top_countries_str = top_countries
                file.write(f"Top five countries by average sentiment: {top_countries_str}\n")

    except IOError:
        return (output_file)



    


