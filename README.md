# RedfinDataPull
I've been wanting to do a project using real estate data for a while now, but I always had a difficult time finding a 
place where I could source my own reliable data over time without having to pay for it. I looked into Zillow's API but
found that even if I wanted to use it, I couldn't store the data I'd pull via the API. Though this could still provide a
means for some decent analysis work, there's also a limitation on the number of calls I can make, which limits the scope
of what would be possible. 

Eventually, I discovered that although Redfin doesn't have it's own API, it provides a decent amount of real estate data
for FREE. The process to get the data I'm interested in would normally involve searching a specific area for real estate
listings, scrolling to the bottom of the page, and downloading a CSV of the data which I could then browse and use to my
heart's content. There are a few issues with this however:
- This process is VERY manual
- Each CSV only provides me with data as of that day, rather than over a period of time
- Though the data includes important features like list price and sq ft, it doesn't include unlisted properties, what
each property last sold for, etc. which I was hoping to have

I fully expect this project to evolve over time, but as a starting point I plan to build an ETL pipeline to navigate to Redfin
and retrieve data for the area I'm interested in by downloading the CSV for that area, storing the data in a database,
and then deleting the CSV. This will force me to learn Selenium for Python and to learn how to create a database on my
local machine and leverage SQL with Python to explore the data, and maybe use the data for predictions of some sort down
the road. As I build this I plan to begin with Rochester, MN as a test case, however I plan to make this dynamic where the user 
can define the area to search Redfin for real estate data.
