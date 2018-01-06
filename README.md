# fund-planner
Add expected and recurring payments, income, and transfers to see how the money in your bank accounts will grow and shrink through the upcoming months.

# What does it do?
Right now there is a database holding accounts and account adjustments. The main.py file adds sample data and outputs the adjustments for February and November as examples.

Adjustments are transactions that will add or remove money from your bank account. They can be one-time adjustments or monthly or yearly. An example of a one-time adjustment would be a trip that you'll be taking that you think will cost $500, so you'd create an AccountAdjustment with -500 for the amount. Examples of monthly recurring adjustments would be rent and income, and yearly might be taxes.

Right now the code simply displays this data, but next up will be showing how much money you'll have in your bank accounts as these transactions happen. This will give you a better idea of how you gain and spend money throughout the month and help you avoid forgetting upcoming auto-payments and overspending.

Note: If you put the AccountAdjustment day as 31 or anything more than that, the code will automatically adjust this to be the last day of the month when you make a query for a specific month.

# Setup
sudo python install -r requirements.txt
./main.py
