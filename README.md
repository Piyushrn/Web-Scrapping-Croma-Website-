# Web-Scrapping-Croma-Website-
Gathering the data from the Croma website using selenium and beautifulsoup.

I have used python language for web scrapping using libraries like Selenium, and BeautifulSoup. 

The webpage is dynamically coded with javascript so Selenium was the best and easiest way to scrap it as beautiful soup has its limitation

The HTML tree is quite complex.

The Webpage has a view more button, which doesn't change the URL as it is dynamically coded with javascript.

The Croma TV webpage had about 154 products.

The attached CSV file consists of the information of each product from the webpage, It has 154 rows and 10 columns indicating

- Listing position (the first product visible will have listing position 1, subsequently increment the listing position by 1 for each
	successive product)
- Title
- Brand
- MRP
- Price
- Count of Ratings
- Count of Reviews
- Average Rating Score
- Product URL
- Image URL


Some of the information was able to be extracts directly from the page with multiple products and For some info, each products link had to hit to get it. 



