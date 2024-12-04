
## 1. User Management

### 1.1. Get Users - `/users/` (GET)

  Retrieves a list of all users.

**Response**

```json
[
  {
    "name": "string",
    "id": "integer"
  },
  {
    "name": "string",
    "id": "integer"
  }
]
```

### 1.2. Get User Reviews - `/users/{username}` (GET)

  Retrieves all reviews written by a specific user.

**Response**

```json
[
  {
    "publisher": "string",
    "description": "string",
    "ratings (S, Q, C)": ["integer", "integer", "integer"],
    "date_published": "string",
    "publisher_id": "integer"
  },
  {
    "publisher": "string",
    "description": "string",
    "ratings (S, Q, C)": ["integer", "integer", "integer"],
    "date_published": "string",
    "publisher_id": "integer"
  }
]
```

### 1.3. Create User - `/users/signup` (POST)

  Adds a new user to the database.

**Request**

```json
{
  "username": "string",
  "password": "string"
}
```

**Response**

```json
{
  "id": "integer"
}
```

### 1.4. Delete User - `/users/` (DELETE)

  Deletes a user and their associated data.

**Request**

```json
{
  "username": "string",
  "password": "string"
}
```

**Response**

```json
{
  "message": "string"
}
```
## 2. Reviews

### 2.1. Get Reviews by Location - `/reviews/{location_id}` (GET)

  Retrieves all reviews for a specific location.

**Response**

```json
[
  {
    "brand": "string",
    "brand_id": "integer",
    "address": "string",
    "address_id": "integer"
  },
  {
    "description": "string",
    "ratings (S, Q, C)": ["integer", "integer", "integer"],
    "date_published": "string",
    "publisher": "string",
    "publisher_id": "integer",
    "review_id": "integer"
  }
]
```

### 2.2. Submit Review - `/reviews/` (POST)

  Adds a new review for a specific location.

**Request**

```json
{
  "brand_id": "integer",
  "location_id": "integer",
  "publisher_id": "integer",
  "description": "string",
  "service": "integer",
  "quality": "integer",
  "cleanliness": "integer"
}
```

**Response**

```json
[
  {
    "publisher": "string",
    "brand": "string",
    "address": "string",
    "description": "string",
    "ratings (Service, Quality, Cleanliness)": ["integer", "integer", "integer"],
    "r_id": "integer"
  }
]
```

### 2.3. Delete Review - `/reviews/` (DELETE)

  Deletes a specific review by ID and username.

**Request**

```json
{
  "username": "string",
  "r_id": "integer"
}
```

**Response**

```json
[]
```

### 2.4. Update Review - `/reviews/{r_id}/user/{username}` (PATCH)

  Updates a specific review's details.

**Request**

```json
{
  "description": "string",
  "service": "integer",
  "quality": "integer",
  "cleanliness": "integer"
}
```

**Response**

```json
{
  "description": "string",
  "s_rating": "integer",
  "q_rating": "integer",
  "c_rating": "integer",
  "u_id": "integer",
  "r_id": "integer"
}
```
## 3. Brands

### 3.1. Get All Brands - `/brands/` (GET)

  Retrieves all brands with their locations.

**Response**

```json
[
  {
    "brand": "string",
    "brand_id": "integer",
    "addresses": [
      {
        "address": "string",
        "address_id": "integer"
      }
    ]
  }
]
```

### 3.2. Get Top Locations - `/brands/{brand_id}/top_locations` (GET)

  Retrieves the top-rated locations for a specific brand.

**Response**

```json
[
  {
    "type": "Best Overall",
    "Overall Score": "float",
    "Cleanliness": "float",
    "Quality": "float",
    "Service": "float",
    "address": "string",
    "location_id": "integer",
    "brand_id": "integer"
  }
]
```
## 4. Ingredients

### 4.1. Get All Ingredients - `/ingredients/` (GET)

  Retrieves a list of all ingredients.

**Response**

```json
[
  {
    "id": "integer",
    "name": "string"
  }
]
```

### 4.2. Get Brand Ingredients - `/ingredients/{brand_id}/all_ingredients` (GET)

  Retrieves all ingredients for a specific brand.

**Response**

```json
{
  "brand_id": "integer",
  "brand_name": "string",
  "ingredients": ["string", "string"]
}
```

### 4.3. Get Food Ingredients - `/ingredients/{food_id}` (GET)

  Retrieves all ingredients for a specific food item.

**Response**

```json
{
  "food_id": "integer",
  "food": "string",
  "ingredients": ["string", "string"]
}
```
