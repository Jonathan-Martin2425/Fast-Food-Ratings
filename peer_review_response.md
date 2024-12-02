
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

## Code Review Response

## Test Results Response

## Product Ideas Response