# Before the start
In postman create py request from curl request. Put
```
curl -H 'Authorization: ************** \ #AuthorizationKeyHere
     -H 'Content-Type: application/json'\
     -v -X GET "http://kibana.***link_to_report_here/_search?size=1000" \ #change link
     -d'{}' #put query here
```
