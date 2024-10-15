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

### 5. name - `{fast_food_place}/location/{location_id}` (GET)

  given wrong fast_food_place or location_id ...  

**Request**

```json

[
  {
    "Something": "string"
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

### 6. name - `choose path from previous ones` (GET)

  description start

**Request**

```json

[
  {
    "Something": "string"
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

### 7. name - `choose path from previous ones` (GET)

  description start

**Request**

```json

[
  {
    "Something": "string"
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

### 8. name - `choose path from previous ones` (GET)

  description start

**Request**

```json

[
  {
    "Something": "string"
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



