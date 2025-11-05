# autodocs-hackathon
This repo contains the code that is used for a POC of automating the process of documentations 



# **api_doc_template.html**
This template is a Jinja2 template used to generate an HTML page that documents an API. It iterates over a collection called "routes" using a for loop. For each route in the routes collection, it outputs the route's name and programming language as a section header, followed by the route's path and a description (documentation) of the route. Essentially, it dynamically creates an API documentation page listing all routes with their details by looping through the provided routes data. The template is structured to create a heading and paragraphs for each route entry on the page.
