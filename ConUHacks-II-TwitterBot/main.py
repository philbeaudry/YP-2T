import tweepy
from monkeylearn import MonkeyLearn
import time
import requests

# Monkey Learn Credentials
ml = MonkeyLearn('47dde3e5ab73adb5379ca8b71d1f47d03befa89f')
module_id = 'ex_y7BPYzNG'

# Tweepy Credentials
auth = tweepy.OAuthHandler("2Uxy8KpZzRvGtuAPvrSN4TZDs", "irNuDUG1IZvYztcGAWY9XfDq6RPAjXS75djdaOBJYPKbbYPc5v")
auth.set_access_token("822933243880243200-6VQTFBUab7mjgAlQKfXAb4gYZJnHR1X", "jqr7fHhHS7xPtOzr4QCKfQO7BlT6vXvAj2cIYx87esfbI")

JSONrequest = "http://api.sandbox.yellowapi.com/FindBusiness/?what=%s&where=Montreal&pgLen=1&pg=1&dist=1&fmt=JSON&lang=en&UID=172.31.109.198&apikey=tst3bbg2kzkdgnscystpbk6j"

# File containing tweets already replied to
already_replied_file = open('already_replied.txt', 'a+')

# Create Tweepy Object
api = tweepy.API(auth)

def find_business(sentence):
  sentence = requests.get(JSONrequest % sentence)
  sentence = sentence.json()
  try:
    sentence = "http://www.yellowpages.ca/bus/Quebec/Montreal/Yellow-Pages/%s.html Checkout %s at %s!" % (sentence['listings'][0]['id'], sentence['listings'][0]['name'], sentence['listings'][0]['address']['street'])
  except:
    sentence = "Couldn't find anything on Yellow Pages!"
  return sentence

def have_replied(tweet_id):
  already_replied_file.seek(0)
  replied_tweet_ids = already_replied_file.readlines()
  return replied_tweet_ids.count("%s\n" % tweet_id) != 0

def find_keyword(sentence):
  sentence = [sentence]
  try:
    res = ml.extractors.extract(module_id, sentence)
    res = res.result[0][0]['keyword']
  except:
    res = "jrioeht43hr4u3chru34ty8349"
  return res

def cut_to_140_chars(sentence):
  if len(sentence) > 140:
    sentence = sentence[0:139] + '…'
  return sentence

def reference_author(author, sentence):
  sentence = '@%s %s' % (author, sentence)
  return sentence

def is_a_reply(sentence):
  return sentence.find('@') != -1

def remove_tags(sentence):
  sentence = sentence.split(' ')
  try:
    sentence = sentence.remove('')
  except:
    pass
  indexes_to_delete = []
  for word in sentence:
    # Detect indexes to delete
    if word[0] == '#':
      indexes_to_delete.append(sentence.index(word))
  count = 0
  for index in indexes_to_delete:
    del sentence[index - count]
    count = count + 1
  sentence = ' '.join(sentence)
  return sentence

def check_tweets():
  # Search tweets with the keyword
  public_tweets = api.search("#askYP", rpp=100, since_id=822903540108722178)

  for tweet in public_tweets:
    # Skip if this is a reply tweet
    if is_a_reply(tweet.text) or have_replied(tweet.id):
      continue

    print("Replying to %s (%s): " % (tweet.text, tweet.id_str))

    reply_text = tweet.text
    reply_text = remove_tags(reply_text)
    reply_text = find_keyword(reply_text)
    print("Detected keywords: %s" % reply_text)
    reply_text = find_business(reply_text)
    reply_text = reference_author(tweet.author.screen_name, reply_text)
    # reply_text = cut_to_140_chars(reply_text)

    print(reply_text)

    try:
      api.update_status(reply_text, tweet.id)
      # Add tweet id to list of replied tweets
      already_replied_file.write("%s\n" % tweet.id)
      already_replied_file.flush()
    except:
      try:
        # Add tweet id to list of replied tweets
        already_replied_file.write("%s\n" % tweet.id)
        already_replied_file.flush()
      except:
        print("Error: Failed to list tweet.")
      print("Error: Failed to reply to tweet.")

    time.sleep(3)


while(True):
  check_tweets()
  time.sleep(30)


