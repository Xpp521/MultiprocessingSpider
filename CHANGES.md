# Release Note
## v1.1.1
#### Bug Fixes
- Fix "start_urls" invalidation.
___
## v1.1.0
#### Features
- Add overwrite option for "FileSpider".
- Add routing system. After overriding "router" method, you can yield a single url or a url list in your parse method.
#### Bug Fixes
- Fix retry message display error.
#### Refactor
- Optimize setter method. Now you can do this: spider.sleep_time = ' 5'.
- Will not resend request when "status_code" is not between 200 and 300.
##### a) MultiprocessingSpider
- Rename property "handled_url_table" to "handled_urls".
- Remove "parse" method, add "example_parse_method".
- "User-Agent" in "web_headers" is now generated randomly.
- Change url_table parsing order, current rule: "FIFP" (first in first parse).
##### b) FileDownloader
- Remove "add_files" method.
___
## v1.0.0
- The first version.