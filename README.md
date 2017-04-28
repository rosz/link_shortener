# link_shortener
A link shortener / Tornado framework / MongoDB

* post() method receives an original link and number of days to expire (max 7), returns a shortcode
* get() method receives the shortcode and redirects to the original link if valid and actual
