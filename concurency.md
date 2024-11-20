### Case #1: Duplicate Users
![image](https://github.com/user-attachments/assets/32a67bca-81ff-4272-b2df-871d0a086e14)
  
&ensp; This problem is known as a "Write Skew" since 2 users are trying to add themselves at the same time, so they both pass the requirment of their username not being a duplicate.
However this then leads to duplicate usernames being in the database, which is bypassing the requirments of creating a user. This could be solved by setting uniqueness on names in the database.


### Case #2: Incorrect Top Locations, Dirty Read
![image](https://github.com/user-attachments/assets/88415bf7-d501-41e7-bceb-f69c563c7b91)
&ensp; This problem is known as a "Dirty Read" since the best locations that the user is trying to get includes a review with invalid ratings values, like -1000 in cleanliness when its only a range between 0-10. So this heavily sku a location's avg ratings preventing it from showing up in the "best locations" response due to one bad review that broke the rules. Ths can be fixed by checking for parameters before inserting a review or preventing the "best_locations" API from reading uncommited insertions.


### Case #3: Lost Review from Deleted User

&ensp; The problem here is known as a "Phantom Read" since as someone is adding a review, Another deletes their account in the middle of adding the review. 
Since deleting a user also deletes all the reviews and the user adding the review passed the check to see if the user existed, The review gets added with a user that doesn't exist.
This lead to an incorrect database as it takes reviews from users that don't exist even when they can never be accessed by anyone.

