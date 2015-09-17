Instructions:
Simply type run.sh in your command line and check the results file.

Understanding:
1. The function here is based on that the listing title would contain the product manufacture, model and/or family,
so I just generate a regex of those three and check in lisitng title.
2. I've tried several ways and I believe that this is the best way though it may takes little longer about O(n) of the listing numbers
based on that the product number would be much less than listings, but it doesn't have any miss or wrong match.
