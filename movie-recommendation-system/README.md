# group-project-f22-cereal-killers ![image](https://user-images.githubusercontent.com/29851745/191648956-01a63b53-3c0a-4cd8-a966-20c01702f01d.png)
group-project-f22-cereal-killers created by GitHub Classroom

**Cereal Killers : Movie Recommendations** is a recommendation service for the scenario of movie streaming. This scenario consists of a streaming service with about 1 million customers and 27,000 movies (for comparison, Netflix has about 180 million subscribers and over 300 million estimated users worldwide and about 13,000 titles worldwide). 

**Data Cleaning**
1. v1: read all kafka log and manipulate with pandas dataframe
2. v2: process kafka log as stream (parse each line)

**How to run?**

1. Activate the pyenv virtual environment by running the activate binary file using 

`source server/env/myenv/bin/activate`

2. Install the dependencies using 

`pip install server/req.txt`

3. Run the server using 

`python3 server/app.py`

4. Observe the logs for incoming requests to the server
