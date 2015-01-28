# Project Descripton

This project gives a solutions to the SF Food trucks challenge.  It is a full stack solution to displaying the data received from sfdata about mobile food trucks in an elegant manner. I have hosted it using Google Developer Cloud and can be found [here](http://23.251.159.86/)

# Technical Stack
## Backend Stack
The stack used on the backend is as follows:
###Database
The database chosen for this application was Postgresql with the PostGIS extension.  The reasoning behind this is it allows for geospacial queries. This makes showing the appropriate food trucks within an area (like San Francisco) a breeze.

##### Thoughts
I think this was the appropriate database for this solution.  This was my first time working with geospacial queries so there was a bit of a learning curve. However, once it was up and running, it was really easy to make queries based on location.  

### Backend
The backend was written in the Python microframework Flask.  Flask was chosen to stay as close to Uber's stack as possible.  To manage the database, SQLAlchemy was chosen as an extension. 

#####Thoughts
After working in Ruby on Rails for the past couple years, writing something in Flask was a cool experience. It felt almost like taking the training wheels off a Rails stack and leaving only the important parts.  It made things extremely lightweight and easy to build out new features.  Some of the shortcomings I saw (disclaimer: these could simply be a lack of experience with the framework) were handling assets was somewhat difficult.  For instance, having template html/haml files was somewhat difficult to incorporate.  Also, I think security may be somewhat difficult to implement. If I ever wanted to add a layer of OAuth and perform two and three legged requests, I could see it being difficult to implement.

I will say though that writing tests for Flask is extremely easy ( much preferred over rspec).  Also, I'm really happy HAML has carried over to python.  It's the one thing I brought from the ruby world and I think it makes writing HTML significantly easier.

### Frontend
For the frontend Backbone.js was chosen along with the Google Maps JS API.  I chose backbone because it's an extremely lightweight framework that would easily help keep track of large quantities of data (like 600+ food trucks).  

#####Thoughts
Having used Backbone before, it was nice to get back into it and I think the code looks really clean.  I was also fortunate enough to find an open source backbone library for models of the Google API.  This library was good enough for this project, but if this was ever to be extended further I would rewrite it (or simply merge it).  I didn't take the time to implement a css framework as the css involved in this project was pretty minimal, but adding something like Bootstrap could allow for a really nice looking UI with search and other niceties that aren't included (yet).

###Future
Some of the improvements I'd like to make in the future:

Backend:
  - Adding versioning to the api calls, espcially when there become multiple
  - Adding an API for searching by truck description instead of by location
  - Add an API that hits the sfdata end point for mobile truck schedules and adding that to the Model
    
Frontend:
  - Add bootstrap for controlling CSS
  - Abstract Backbone templates into JST files
  - Add a search to the top for food trucks
  - Add a toggle to turn food trucks on/off by neighborhood in addition to just by truck owner
  - Adding schedule to the infowindow displayed when a truck is clicked on
 
Other:
  - Set up a chef recipe to deploy using a continuous deploy/integration system
