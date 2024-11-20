### Case #1: Duplicate Users
![image](https://github.com/user-attachments/assets/32a67bca-81ff-4272-b2df-871d0a086e14)
  
&ensp; This problem is known as a "Write Skew" since 2 users are trying to add themselves at the same time, so they both pass the requirment of their username not being a duplicate.
However this then leads to duplicate usernames being in the database, which is bypassing the requirments of creating a user. This could be solved by setting uniqueness on names in the database.


### Case #2: Duplicate Reviews

### Case #3: Lost Review Update

