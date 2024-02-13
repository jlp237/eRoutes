# eRoutes

![image](https://github.com/jlp-ue/eRoutes/assets/54306210/d382169c-cd3b-4924-a281-e35bf012dbd1)

## Background
In 2017 planning long-distance trips with an electric vehicle was a time-consuming process. The network of charging stations for electric vehicles was still sparse and the range of electric cars was limited. To avoid getting stuck on the road with an empty battery and no charging station in sight, a lot of planning was necessary in advance. Drivers had to do their research to find out whether there were enough charging stations along the planned route and whether they could be reached with their electric car. To make things even more complicated, the plug type of the car also had to be compatible with the charging station.

eRoutes was created to automate route planning and make long-distance journeys with electric vehicles straightforward. The aim was to calculate the optimal route to the destination while showing the driver the best locations to charge the car.

## Challenge
To find the optimal locations of the charging stations, the first challenge was to calculate the expected range of the vehicle. Since the range of an electric vehicle not only varies from model to model but also depends on many other factors such as the driving style and the weather conditions, these factors must be taken into consideration. Another challenge was to collect data for all charging stations from different providers and process the data for consistency and duplicates. Furthermore, a routing algorithm had to be developed to find the best route taking into account all available charging stations.

## Development
The first step of this project was to collect a dataset of all charging stations in Europe from public sources through a combination of web scraping and APIs. To make the route planner more user-friendly and to ensure the compatibility of the plug type of the electric vehicle and the charging station, the next step was to collect data of each electric car that was released during this time. After all necessary data was collected, the routing algorithm was developed using Geolocation and Geospatial APIs from HERE Maps and Google Maps. In the last step, the web application was developed. The main focus was to provide an excellent user experience by keeping the application simple, while still allowing the user to change important input variables.

## Result
The user can first select his specific vehicle and choose between 3 driving styles and the current battery status of the vehicle. Based on the calculated range, the algorithm calculates the best route, as well as the expected driving and charging time and the estimated charging price. The user can then comfortably send the route to his smartphone and navigate with Google Maps.

