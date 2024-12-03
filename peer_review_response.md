
Anything part of the reviews not responded to/explained were implemented/fixed directly

# Response to Professor's feedback

## brand and location id issues

&ensp; This was fixed by making every GET endpoint for brands and their locations give both their ids and names.
The same also applies to the new additions/separation of reviews and users, 
although many requesting involving user request just the username, not the id.

## database error handling and HTTPS status codes
&ensp; error handling added to root alongside appropriate HTTP error code and message. Also, every GET, PATCH and DELETE
have appropriate and separate success status codes and invalid input error handling with messages.

## file separation
&ensp; While it was not directly what you asked for in regard to having several independent queries, we did seperate 
brands, users and reviews into separate files with users and reviews having full CRUD operations. However, the 
several independent queries problem is solved by the root containing every brand and their locations, which leaves the 
GET locations endpoint redundant as it only gives the locations of a single brand.

# Response Seth Langel's Peer Review

## Schema/API Response

### 1. one to many for food and category
&ensp; the change from one-to-many to many-to-many was done, but we changed the catagory table to an ingredients table

### 2. restrictions on ratings
&ensp; the restrictions were set as error handlin the POST and PATCH reviewsinstead of in the database Schema 
for better error messages to the user.

### 3. Seperating reviews and ratings
&ensp; while not a bad idea if we wanted to change something in the future, I believe it is better
to keep it all in one table, since it would require an extra insert everytime a review is added, which
could add to slowing down the program as multiple SQL statements are being sent per endpoint

### 4. time in hours table
&ensp; implemented except for "is24Hours" since that can just be achieved by setting open time to 00:00:00
and close time to 24:00:00. Also for hours that go past midnight can be detected by checking is the open time is greater
than the close time, allowing for better implementation when the table is used.

### 5-6. visits column and table name
&ensp; 'visit' representing a location address has been changed to 'location_id' which acts as a foreign key for 
the locations table and the table has been renamed to 'user_visits' to certify its purpose of showing when a user 
creates or changes a review

### 8-9. hours table fixes
&ensp; business_id changed to location_id and added ENUM instead of string for day_of_week column

### 11. root 
&ensp; Changed root to only display opening message and moved root functionality to GET "brands/" 
where it serves its purpose more specifically

### 12. ambiguous endpoints
&ensp; 1st example is acomplished by the GET "brands/" and 
the 2nd example is implemented in reviews after changing the URI

&ensp; Recommend was changed to focus more on recommending based on excluding ingredients of food from a brand, which
goes along with our change of the 'categories' table to the 'ingredients' table.

&ensp; the last 2 endpoints were like you said, vague, so we didn't see a way of implementing them or their purpose and
removed them to the API spec while also adding all our implemented API specs.

## Code Review Response

## Test Results Response

## Product Ideas Response