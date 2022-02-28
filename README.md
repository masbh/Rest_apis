# rest_apis
Develop a task that runs every day and downloads weather data and stores it in the database (SQLite for the purpose of this assignment)
1.	Downloads the forecast data from the url
2.	Saves the data in the csv to a Django model
3.	Create methods to 
a.	Retrieve past data
b.	Retrieve most recent data
Django Project: metdata
Dango app: my_api
Requirements.txt has all the package dependencies.
Model:
I created a Forecast model with the following attributes:
Start_date: the date the forecast was generated. This is how I identify all elements belonging to a particular forecast file
Station: The station for which there are forecasted values
Forecast_date: The date which was forecasted
Forecast_time: The time which was forecasted
Mean_precip: The mean of the 20 forecasted precipitation for a station, forecast_datetime combination
Mean_temp: The mean of the 20 forecasted temperatures for a station, forecast_datetime combination
Rationale for the Model
Mostly for ease of manipulation of data and model creation.
I figured if I can store 2 values then I can always extend the model to store additional values
Automatic Download and Scheduling:
1.	The download is automatic in the sense that the user initiates the download by inputting the api url. Once download is initiated, the data is automatically stored in the database.
2.	If data already exists in the database for the same forecast file, no data is stored as there is a check to see if forecasts already exist in the DB for that day.
3.	Data is automatically saved in database once download is initiated
4.	There is no scheduling of the download.
API Urls:
1.	API Overview: localhost:8000/my_api
2.	Save today's forecast into database: "/save-today-forecast/"
3.	List of past forecasts: "/past-forecast/"
4.	Forecast from start date to end date: "/range-forecast/<str:YYYY-MM-DD>/<str:YYYY-MM-DD>"
5.	Most recent forecast: "/recent-forecast"
Next steps/Improvements:
1.	Scheduling automatic download of the forecast file to happen daily using cron and Django-background-tasks. This can be done but is considered out of the scope for this assignment 
2.	Extending the Forecast model to the actual temperature and precipitation vectors of all 20 forecasts and not just the aggregates. This is a simple change to the code (and to the model), if needed
3.	Adding a Location model such as one below to store longitudes and latitudes of the station if we want to group forecasts by locations closest to one another.
Class Location:
	Station name
	Longitude
	Latitude 

Class Forecast
	Station = Foreign Key to Location
	…..
	…..
4.	Adding unique_together constraints for start_date, station and forecast_date, forecast_time to return unique records in the table
5.	Develop additional methods to retrieve different slices of data depending on the model, such as forecasts for all stations that lie within a certain longitude and latitude range etc.
