# Example Pydantic

This is a repository for experimenting with Pydantic.

Example includes NASA - DONKI - Notifications API. So to regenerate the sample results:

Include a `.env` file in the root directory, with `API_KEY=<YOUR_NASA_API_KEY>` in it, then:

```
pipenv install && pipenv shell
```

Then spin up a local MongoDB (Docker deamon must be running):

```
docker-compose up
```

Lastly:

```
python notification_ingestor.py 2020-10-01 2020-10-05
```

Example returned query results in MongoDB when the script successfully runs:

```
{ 
    "_id" : ObjectId("5fd7d2dc3427dc78d2a11757"), 
    "insertion_date" : ISODate("2020-12-14T22:02:19.263+0000"), 
    "message_type_abbreviation" : "RBE", 
    "message_url" : "https://kauai.ccmc.gsfc.nasa.gov/DONKI/view/Alert/15911/1", 
    "message_type" : "Space Weather Notification - Continued Radiation Belt Enhancement", 
    "message_issue_date" : ISODate("2020-10-04T12:09:11.000+0000"), 
    "message_id" : "20201004-AL-001", 
    "disclaimer" : "NOAA's Space Weather Prediction Center (http://swpc.noaa.gov) is the...", 
    "summary" : "Significantly elevated energetic electron fluxes...", 
    "notes" : "NASA Community Coordinated Modeling Center/Space Weather..."
}
{ 
    "_id" : ObjectId("5fd7d2dc3427dc78d2a11758"), 
    "insertion_date" : ISODate("2020-12-14T22:02:19.263+0000"), 
    "message_type_abbreviation" : "RBE", 
    "message_url" : "https://kauai.ccmc.gsfc.nasa.gov/DONKI/view/Alert/15908/1", 
    "message_type" : "Space Weather Notification - Continued Radiation Belt Enhancement", 
    "message_issue_date" : ISODate("2020-10-02T13:19:14.000+0000"), 
    "message_id" : "20201002-AL-001", 
    "disclaimer" : "NOAA's Space Weather Prediction Center (http://swpc.noaa.gov) is...", 
    "summary" : "Significantly elevated energetic electron fluxes in the...", 
    "notes" : "NASA Community Coordinated Modeling Center/Space Weather Research Center..."
}
```
