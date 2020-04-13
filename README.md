# COVID.txt

A Dash application to explore the [COVID-19 Open Research Dataset (CORD-19)](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge).

Deployed as a Dash app using Docker on AWS's Elastic Container Service (ECS) using AWS FARGATE. 

Download the dataset from kaggle here [COVID-19 Open Research Dataset (CORD-19)](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge).

## Local development

1. Create a Python venv with a >=3.6 interpreter.

2. Activate venv (`source <venv path>/bin/activate`).

3. Install Python dependencies using `pip3 install -r requirements.txt`.

4. Run the server using `python3 wsgi.py`.


## Running locally

To run a local instance, the easiest way is to build the Docker image:

1. Build the image using `docker build -t covid-txt .`. 

2. Run the image using `docker run -p 80:8080 covid-txt:latest`.

3. Use your browser to navigate to `127.0.0.1:8080` to view the application.

## Deploying onto AWS FARGATE

When making changes, you need to rebuild the Docker image and push it to AWS
ECR, then re-deploy.

1. Run `$(aws ecr get-login --no-include-email --region eu-west-2)` 
to authenticate your shell.

2. Build the image using `docker build -t covid-txt .`.

3. Tag the image using `docker tag covid-txt:latest <your account id>.dkr.ecr.<your AWS region>.amazonaws.com/covid-txt:latest`.

4. Push the image to AWS ECR using `docker push <your account id>.dkr.ecr.<your AWS region>.amazonaws.com/covid-txt:latest`.

5. Create a new FARGATE instance or update the running FARGATE instance 
with the Update button at the Dash ECS page.

---------

When deploying onto a new server, 1 vCPU and 2GB memory are the absolute
 minimum necessary for decent operation. More is better, as quite a bit
 of data related calculations are run in the background.
