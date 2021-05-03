# AppCubo - App Info Collector
- This is a web app made in Django and Postgres.<br>
- It collects all information(Name, Publisher, Icon, etc.) about an app from all major app stores (Google Play, Apple App Store, Windows/Microsoft Store) by web scraping using beautifulsoup4.<br>
- There is a REST API that returns search results and app info from a URL endpoint to the user using Django REST Framework.<br>
- Made for ollecting users' feedback, suggestions, and bugs reports for a specific app.<br>

Some of the work is continued on this repo: https://github.com/rkwap/appdex

The web app is also hosted on heroku:- https://rkwap.herokuapp.com/

## Screenshots
Here are some screenshots of the app demonstrating some core features.

<h3>Member Login</h3><br>
<img src="https://i.imgur.com/Bflx1P8.png">
<br>

<h3>Selecting store</h3>
Here for adding post, user have to choose an app from a particular store. (here only google play store and apple store are present. Others are not coded in frontend yet)<br>
<img src="https://i.imgur.com/wai5WMG.png">
<br>

<h3>Searching App</h3>
<h4>Play Store</h4>
<img src="https://i.imgur.com/5scXcmC.png">
<br>
<h4>Apple Store</h4>
<img src="https://i.imgur.com/OmVvYV5.png">
<br>


<h3>Add feed for an app</h3>
<h4>Play Store</h4>
<img src="https://i.imgur.com/Z48qmRS.png">
<br>
<h4>Apple Store</h4>
<img src="https://i.imgur.com/wsdSLUh.png">
<br>

<h3>Pending feeds for approval</h3><br>
<img src="https://i.imgur.com/ud4Im62.png">
<br>

<h3>Accept/Reject a feed</h3><br>
<img src="https://i.imgur.com/Twr7xw1.png">
<br>
