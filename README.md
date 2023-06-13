# tradelikenancy

This project enables you to get visibility into a House of Representative's transactions for a particular filing date or an overview of the full year. There are 2 python scripts you are able to run. 

The first python script is drill_down.py. In this script you will input a valid House of Representative's name and a given year. We will return a list of filing dates and the output generated will present you with a list of transactions. 

The second python script is overview.py. You can input a given year, wait 5 minutes, and identify broader trends in market-impacting legislature by seeing the top 5 stocks bought and sold in a particular year.

parsing.py is a custom PDF parser I built to process highly unstructured text coming from the filing transactions. It works for both drill_down.py and overview.py. Building this processor was a technical challenge and I love discussing it. 

Feel reach out to me if you have any questions!