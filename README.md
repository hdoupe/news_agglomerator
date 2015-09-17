# news_agglomerator

Ever find yourself busy checking many sites for your news? Or even worse checking sites to find that there are not any new articles? Assuming that you consume as much news as I do, you probably encounter this problem fairly often.  Here is my attempt at the solution.

Currently, it only pulls articles from fivethirtyeight, but I plan to add more news sites such as The Atlantic, The Economist, RealClearPolitics, etc...  In the future, I would like to pull not only names of articles and links, but also information such as new polls or financial information like DOW averages or S&P 500 average.  From this point forward, I plan to write a separate class for each news site with its own parse method unless it can be handled by the generic parse method I defined in the Article_Getter class.  

The output of this program is an email from a gmail account to your account.  I am not making any promises about the securtiy of my email class. I hastily implemented the python email module to do this work.  

I would appreciate any suggestions or the addition of any sites to the article_getter.py file.

Enjoy.
