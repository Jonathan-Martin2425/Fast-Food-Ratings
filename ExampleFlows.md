### 1. Creating a Review Example Flow
 
  Karen Willoughby comes to our website because she had an awful experience at McDonald's today and wishes to warn others of that bad location.
First Karen opens the website by calling GET "/" and the URL where she is greeted by all the different fast food locations on the website.
Eventually, she finds Mcdonald's and she clicks on it calling GET "/Mcdonalds/" where she finds all locations on the website and by putting her zip code she finds the location she visited.

  After clicking on said location Karen calls GET "/Mcdonalds/locations/176" and scrolls past previous reviews of that location to an area where she can type her review and rate different aspects of the location.
Once Karen has finished her response she presses submit calling POST "/Mcdonalds/locations/176" and receives a message telling her that the review was submitted.

Then Karen goes on about her day knowing fewer people, like her, will be going to that McDonald's again

### 2. Viewing Specific Location Reviews Example Flow

  One day Randy Jr, curious about whether ordering from the Domino's closest to him is worth the price, visits our website to check out some reviews. 
First Randy opens the website calling GET "/" and sees an assortment of different fast food places, eventually finding Domino's
When Randy clicks on Domino's he calls GET "/Dominos/" where he finds many different locations, so he puts in his zip code and finds the nearest location

After clicking on the location Randy calls GET "/Dominos/location/42" where he finds an assortment of different reviews praising the location for fast and quality service.

Pleased, Randy decides to order from the location and enjoys his pizza when it arrives in less than 30 min.

### 3. Recommendations based on time spent 

 A person who's into fitness cares a lot about what they eat/consume throughout the day. They decide that cooking is not an option today after a long day at work and gym. Visitng our fast food ratings website gives them a spectrum of options to chose from and they are indecisive about eating fast food when they really shouldn't. That's when we recommend a full course meal at Five Guys because they spent a long period of time hovering over cheeseburger reviews while on our website.

They are now set to go an enjoy their meal. To do such influence:
  - Person begins by looking at reviews in the /front_page
  - then /reviews/location/menu_items/10 and they remain
  - finally we recommend a cheeseburger based on the activity/data
It was a really good meal.
