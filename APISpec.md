### 1. Get Root - `/` (GET)

  Loads the front page of the website, which will include a list of
All fast food places available to rate with better formatting and
buttons to lead to their different locations

**Response**

```json

[
  {
    "fast food": "string",
    "...": "..."
  },

  {"...": "..."},

  {
    "fast food": "string"
    "...": "..."
  }
]
```

### 2. Get Fast Food Place - `/{fast_food_place}` (GET)

  Given the name of a fast_food_place, like "KFC" or "Taco_Bell", returns
the page for that specific place, the details of different locations leading to their page
and ratings of specific foods shared between locations.

**Response**

```json
[
  {
    "location_id": "int"
    "address": "string"
    "...": "..."
  },

  {"...": "..."},

  {
    "location_id": "int"
    "address": "string"
    "...": "..."
  }
]
```

### 3. Get Location - `{fast_food_place}/location/{location_id}` (GET)

  Given a correct fast_food_place and location_id returns the list of interviews
related to that location and an area to write a review with a button to submit

**Response**

```json

[
  {
    "interview_id": "int"
    "review_text": "string"
    "food_ratings": "List"
    "...": "..."
  },

  {"...": "..."},

  {
    "interview_id": "int"
    "review_text": "string"
    "food_ratings": "List"
    "...": "..."
  }
]
```

### 4. Submit Review - `{fast_food_place}/location/{location_id}` (POST)

  given a correctly formatted JSON request from the given review UI
returns a success message and adds it to the reviews of the location

**Request**

```json

[
  {
    "interview_id": "int"
    "review_text": "string"
    "food_ratings": "List"
    "...": "..."
  }
]
```

**Response**

```json

[
  {
    "response": "string"
  }
]
```

### 5. Handling - `{fast_food_place}/location/{location_id}` (GET)

  Given wrong fast_food_place or location_id we would have catch statements to compensate for some oversight. This will also help us improve the user experience if we see this happening a lot on our end.

**Request**

```json

[
  {
    "location": "string"
    "location_id": "integer"
  }
]
```

**Response**

```json

[
  {
    "response": "string"
    "error_message": "boolean"
  }
]
```

### 6. Recommendations - `{location_id}/recommend/` (GET)

  Person accessing our website will be able to see our recommendations for them based on their information and passed searches.

**Request**

```json

[
  {
    "location": "string"
    "reviews": "string"
    "prices": "number"
    "quality": "string"
  }
]
```

**Response**

```json

[
  {
    "recommend": "string"
    "stats": "integer"
  }
]
```

### 7. Update to see new reviews - `{fast_food_place}/updates/qualities` (GET)

  Update the information shown on the website live to allow our users to have the most up to date and relevant ratings. This will help with their last minute decision making if they spot interesting reviews.

**Request**

```json

[
  {
    "live_input": "string"
    "reviews": "string"
    "time": "number"
  }
]
```

**Response**

```json

[
  {
    "Something": "string"
  }
]
```

### 8. Notifications - `{fast_food_place}/users/person` (GET)

  Send notifications to all of our users on our website to let them know of changes. A person may have interacted with their posting or we are just saying hello to encourage engagement.

**Request**

```json

[
  {
    "posting": "string"
    "deals": "string"
    "prices": "integer"
  }
]
```

**Response**

```json

[
  {
    "notification": "string"
  }
]
```

### 9. top_locaions - `/brands/{brand_id}/top_locations` (GET)

  Gives detail on the best locations of a given brand from all reviews relates to those locations and their scores

**Request**

```json

[]
```

**Response**

```json

[
  {
    "type": "Best Overall",
    "Overall Score": float,
    "Cleanliness": float,
    "Quality": float,
    "Service": float,
    "address": str,
    "location_id": int
  },
  {
    "type": "Best Cleanliness",
    "Overall Score": float,
    "Cleanliness": float,
    "Quality": float,
    "Service": float,
    "address": str,
    "location_id": int
  },
  {
    "type": "Best Quality",
    "Overall Score": float,
    "Cleanliness": float,
    "Quality": float,
    "Service": float,
    "address": str,
    "location_id": int
  },
  {
    "type": "Best Service",
    "Overall Score": float,
    "Cleanliness": float,
    "Quality": float,
    "Service": float,
    "address": str,
    "location_id": int
  }
]
```

