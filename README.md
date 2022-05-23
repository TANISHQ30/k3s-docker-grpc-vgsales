All the microservices, including new and old ones from assignment 1 are moved to the kubernetes environment.

The application is extended by adding another data source (new microservices for streaming and analysis). To accommodate the new dataset, I created different application pods and two new repositories. They are below,

1. vgreview_client: Responsible to read the dataset and send 2 records per second
2. vgreview_server: Responsible for finding the game with the highest number of user ratings. The second dataset consists of game titles, game info and user reviews.

The application is scaled horizontally. The application scaling and update strategy is defined in the yml file. I choose to keep the replica set for all the deployments to 1. The decision was made considering the hardware resources constraints. The application in real world would be scaled with various replica set values. If I had the resources needed for scaling, I would assign higher replica sets to weblog and server deployments.

The application also includes testing and monitoring the resources and data analysed by the kubernetes clusters.

Unit test using unittest package in python is used to ensure application is working as expected. An endpoint was created to view and verify the metrics computed by the server. The test is automated by using postman and getting requests from the weblog server. The request is made by postman to the weblog server and the server returns a json response containing the metric keys and values.

The monitor is created using Prometheus and Grafana. Prometheus is responsible for collecting metrics related to kubernetes services and grafana pulls these metrics to create visualization of the data. Helm was used to install Prometheus and Grafana on k3s. The monitoring consists of cluster resource usage, systems processes and their usuage, and pod resource and memory usage.

The application also uses a reference kubeless function that could be integrated within the main application in the later updates.
