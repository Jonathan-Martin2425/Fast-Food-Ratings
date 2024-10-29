# Example workflow
Karen Willoughby comes to our website because she had an awful experience at McDonald's today and wishes to warn others of that bad location. First Karen opens the website by calling GET "/" and 
the URL where she is greeted by all the different fast food locations on the website. Eventually, she finds Mcdonald's and she clicks on it calling GET "/Mcdonalds/" where she finds all locations on the website
and by putting her zip code she finds the location she visited.

After clicking on said location Karen calls GET "/Mcdonalds/locations/176" and scrolls past previous reviews of that location to an area where she can type her review and rate different aspects of the location. 
Once Karen has finished her response she presses submit calling POST "/Mcdonalds/locations/176" and receives a message telling her that the review was submitted.

Then Karen goes on about her day knowing fewer people, like her, will be going to that McDonald's again

# Testing results
1. [the curl statement inputed]
2. [response received after executing the curl statement.]
