## Example workflow
Karen Willoughby comes to our website because she had an awful experience at McDonald's today and wishes to warn others of that bad location. First Karen opens the website by calling GET "/" and 
the URL where she is greeted by all the different fast food locations on the website. Eventually, she finds Mcdonald's and she clicks on it calling GET "/Mcdonalds/" where she finds all locations on the website
and by putting her zip code she finds the location she visited.

After clicking on said location Karen calls GET "/Mcdonalds/locations/176" and scrolls past previous reviews of that location to an area where she can type her review and rate different aspects of the location. 
Once Karen has finished her response she presses submit calling POST "/Mcdonalds/locations/176" and receives a message telling her that the review was submitted.

Then Karen goes on about her day knowing fewer people, like her, will be going to that McDonald's again

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


# Getting locations
1. curl -X 'GET' \
  'http://127.0.0.1:3000/brands/1/' \
  -H 'accept: application/json' \
2.
```json
[
  {
    "brand": "McDonalds",
    "address": "275 Madonna Rd, San Luis Obispo, CA 93401"
  },
  {
    "publisher": "Anonymous",
    "description": "Complete garbage, will never go here again",
    "ratings (S, Q, C)": [
      0,
      0,
      0
    ],
    "date_published": "2024-11-05T16:34:55.856497+00:00"
  }
]
```

# Get reviews

1. curl -X 'GET' \
  'http://127.0.0.1:3000/brands/1/location/1' \
  -H 'accept: application/json' \
2. 
```json
[
  {
    "brand": "McDonalds",
    "address": "275 Madonna Rd, San Luis Obispo, CA 93401"
  },
  {
    "publisher": "Anonymous",
    "description": "Complete garbage, will never go here again",
    "ratings (S, Q, C)": [
      0,
      0,
      0
    ],
    "date_published": "2024-11-05T16:34:55.856497+00:00"
  }
]    
```

# Post review

1. curl -X 'POST' \
  'http://127.0.0.1:3000/brands/1/location/1' \
  -H 'accept: application/json' \
  -H 'access_token: [API_KEY]' \
  -H 'Content-Type: application/json' \
  -d '{
  "publisher_id": 2,
  "description": "Horrible, just horrible. I wasn'\''t expecting much from a McDonalds but they took way too long, gave me meat that looked raw and were rude on every interaction. 
If you'\''re going to McDonald'\''s then just make sure it'\''s not this one. It was surprisingly clean though considering everything else about the place",
  "service": 0,
  "quality": 0,
  "cleanliness": 7
}'
2. 
```json
[
  {
    "publisher": "Karen Willoughby",
    "brand": "McDonalds",
    "address": "275 Madonna Rd, San Luis Obispo, CA 93401",
    "description": "Horrible just horrible. I was not expecting much from a McDonalds but they took way too long and gave me meat that looked raw and were rude on every interaction. If you are going to McDonalds then just make sure it is not this one. It was surprisingly clean though considering everything else about the place.",
    "ratings (S, Q, C)": [
      0,
      0,
      7
    ]
  }
]
```




