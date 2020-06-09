# COVID-19-Australia-Cases-Data
This is a COVID-19 Australian Cases API

API end points

/records/<int:records>
return nth 20 cases based on date
/records/1 will return 1 to 20 cases (earliest)
/records/2 will return 21 to 40 cases

/search?postcode=2000
return all cases in 2000
  
/author
return author information

Demo url: 
https://covid-19-australia-api.herokuapp.com/author
https://covid-19-australia-api.herokuapp.com/records/1
https://covid-19-australia-api.herokuapp.com/search?postcode=2000
