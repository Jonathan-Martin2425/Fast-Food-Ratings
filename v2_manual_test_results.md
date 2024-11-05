### Example Workflow 2

  One day Randy Jr, curious about whether ordering from the Domino's closest to him is worth the price, visits our website to check out some reviews. 
First Randy opens the website calling GET "/" and sees an assortment of different fast food places, eventually finding Domino's
When Randy clicks on Domino's he calls GET "/Dominos/" where he finds many different locations, so he puts in his zip code and finds the nearest location

After clicking on the location Randy calls GET "/Dominos/location/42" where he finds an assortment of different reviews praising the location for fast and quality service.

Pleased, Randy decides to order from the location and enjoys his pizza when it arrives in less than 30 min.

## Testing results


# Get root

1. curl -X 'GET' \
  'http://127.0.0.1:3000/' \
  -H 'accept: application/json'
2. 
```json
[
  {
    "message": "Welcome to Fast-Food-Ratings, for all your fast food needs."
  },
  {
    "brand": "McDonalds",
    "addresses": [
      "275 Madonna Rd, San Luis Obispo, CA 93401",
      "123 Bob Dr, Tustin, CA 92780"
    ]
  },
  {
    "brand": "Del Taco",
    "addresses": [
      "13742 Red Hill Ave, Tustin, CA 92780"
    ]
  },
  {
    "brand": "Dominos",
    "addresses": [
      "866 Foothill Blvd, San Luis Obispo, CA 93405"
    ]
  },
  {
    "brand": "Five Guys",
    "addresses": [
      "763 Foothill Blvd, San Luis Obispo, CA 93405"
    ]
  }
]
```


# Get locations

1. curl -X 'GET' \
  'http://127.0.0.1:3000/brands/3/' \
  -H 'accept: application/json' \
  -H 'access_token: [API_KEY]'
2. 
```json
[
  {
    "address": "866 Foothill Blvd, San Luis Obispo, CA 93405",
    "brand": "Dominos"
  }
]
```

# Get Reviews

1. curl -X 'GET' \
  'http://127.0.0.1:3000/brands/3/location/4' \
  -H 'accept: application/json' \
  -H 'access_token: [API_KEY]'
2. 
```json
[
  {
    "brand": "Dominos",
    "address": "866 Foothill Blvd, San Luis Obispo, CA 93405"
  },
  {
    "publisher": "Anonymous",
    "description": "Best Dominos Ever. took less than 10 min from ordering to get food, it was somehow better than other dominos I have gone too AND was spotless down to the area behind the drinks.",
    "ratings (S, Q, C)": [
      10,
      10,
      10
    ],
    "date_published": "2024-11-05T17:59:59.888767+00:00"
  }
]
```



### Example Workflow 3

 A person who's into fitness cares a lot about what they eat/consume throughout the day. They decide that cooking is not an option today after a long day at work and gym. Visitng our fast food ratings website gives them a spectrum of options to chose from and they are indecisive about eating fast food when they really shouldn't. That's when we recommend a full course meal at Five Guys because they spent a long period of time hovering over cheeseburger reviews while on our website.

They are now set to go an enjoy their meal. To do such influence:
  - Person begins by looking at reviews in the /front_page
  - then /reviews/location/menu_items/10 and they remain
  - finally we recommend a cheeseburger based on the activity/data
It was a really good meal.
