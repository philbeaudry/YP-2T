## Inspiration
The YellowPages API Challenge!

## What it does
YP-2T searches tweets containing the #askYP hashtag. It parses the tweet and inputs it to a machine learning platform called MonkeyLearn. This platform detects keywords in the tweet. The keywords are then passed to the YellowPages API, which returns a business in Montreal related to these words. YP-2T then marks that the tweet was already responded to in a text file. This ensures that it doesn't provide an answer to a tweet twice, as well as ensuring that we don't surpass the Twitter API limits.

## How we built it
We wrote a python script that runs on a server that periodically checks Twitter search for updates using the Twitter REST API. This script uses the MonkeyLearn machine learning platform to extract keywords from the tweet. These keywords are inputted into the YellowPages API, and the result is returned via a Twitter reply on the initial tweet.

## Challenges we ran into
* Learning the different APIs. We used a total of three for this project (YellowPages, MonkeyLearn and Twitter REST). We ran into many bugs before getting these platforms working.
* The 140 character tweet limit. Ensuring not to pass this limit and parsing accordingly.
* Our twitter account got blocked twice because we were sending too many requests.
* One of the team members fell sick with the flu.

## Accomplishments that we're proud of
This is our second hackathon. Last time, we didn't submit a project, so we're very proud of our submission this time around. We're very confident in our project.

## What we learned
* How to write better Python code (we only knew the very basic fundamentals prior to the hackathon).
* How to use three different APIs. We knew nothing about these before the hackathon.
* Working as a team and splitting tasks.
* Better appreciation for Git, the version control software. We used this to manage our project.


## What's next for YP-2T
YP-2T is complete. The software can be further improved by making it more stable and testing corner cases. Furthermore, we would also like to refactor the code to make it more clean and readable.
