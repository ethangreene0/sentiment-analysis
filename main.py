#Ethan Thomas Davies Greene
#egreene4 
#251348539
#November 13th 2023
#This file takes functions from the sentiment analysis file and takes input from the user runs the functions. 

#importing the function from the sentiment analysis file
from sentiment_analysis import *

def main():
    # Try to open the keyword file
    try:
        key_words = input("Input keyword filename (.tsv file):") 
        test1 = open(key_words, 'r')
    except FileNotFoundError:
        # If the file cannot be opened, print an error message
        print("Could not open file", key_words)

    # Try to open the tweet file
    try:
        tweet = input("Input tweet filename (.csv file):")
        test2 = open(tweet, 'r')
    except FileNotFoundError:
        # If the file cannot be opened, print an error message
        print("Could not open file", test2)

    # Try to open the output file for the report
    try:
        input_file = input("Input filename to output report in (.txt file):")
        test3 = open(input_file, 'r')
    except FileNotFoundError:
        # If the file cannot be opened, print an error message
        print("Could not open file", input_file)

    # Print a message indicating where the report will be written
    print("Wrote report to: ", input_file)

    # Read keywords from the keyword file
    key_words_file = read_keywords(key_words)

    # Read tweets from the tweet file and generate a report based on keywords
    report = make_report(read_tweets(tweet), key_words_file)

    # Write the report to the specified output file
    write_report_file = write_report(report, input_file)

# Call the main function to execute the code
main()
