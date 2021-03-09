### pre-requisites
1. azure devops account
2. google cloud account
3. docker hub account with public evaluationapp repository.

### Importing our repository into azure devops
login to azure devops
Create a new project by clicking the button in the top right corner.
So the first thing we need to do is create a project. To do that log in to Azure DevOps and click “Create Project” in the top right corner.

Next fill in the new project card with the proper information. Make sure to click Advanced if you want to change the version control system, or the work process, for this project.
 
![image](https://user-images.githubusercontent.com/68682617/110418948-5d285d00-80be-11eb-8177-0177bed225c6.png)





The New Project Card. Enter the relevant information to create a new Azure DevOps Project.
Once your project has been created you will be taken to the project summary page. Here you can see project members, the readme, and some stats about your repos (but you don’t have one yet… so now let’s import from GitHub).

Importing your GitHub repo
Now that we have a project we can navigate to the repo’s section of our project and import our existing GitHub repo.

![image](https://user-images.githubusercontent.com/68682617/110419014-8943de00-80be-11eb-8acd-eb23b3d1299d.png)


Initial Repo page with no files.
On this screen we can click on the Import button about half way down the page. That will trigger a popup that asks where the source repo is located. From here you should select “git” as the source type, and paste in your clone URL from GitHub. If it’s a private GitHub repo you will need to check the authorization box ad enter your credentials.

 ![image](https://user-images.githubusercontent.com/68682617/110419049-93fe7300-80be-11eb-95d2-6ae97c2b98cd.png)

Import Popup – Enter your source type and your clone URL
Click Import to start the process. 
Import will complete, and it only took a minute or so.

Creating a service connection for docker hub registry.
Click on the project evaluationapp then click on project settings at the bottom left corner.
Select service connections and Create a new service connection for docker registry. 

 ![image](https://user-images.githubusercontent.com/68682617/110419076-9cef4480-80be-11eb-886c-f1e4fd3b6844.png)


When popup comes look for docker registry and select it.
Select the docker hub and provide credentials.
Under service connection name give docker2 and click on verify and save.

Creating and building the pipeline
Here we are creating pipeline for building the docker image for the application and pushing the image to the dockerhub registry.
Steps:
Go to the evaluationapp project.
Click on pipelines and select create a new pipeline
Select azure repo git yaml -> evaluationapp repo -> starter pipeline.
Delete the existing content poped up and add the following code
```
name : Docker-CI
trigger:
  branches:
    include:
      - main
 
pool:
  vmImage: 'ubuntu-latest'
 
variables:
  ImageName: 'kushalreddy/evaluationapp:$(Build.BuildId)'
 
stages:
- stage: Build
  displayName: Build image
  jobs:  
  - job: Build
    displayName: Build and push Docker image
    steps:
    - task: Docker@1
      displayName: 'Build the Docker image'
      inputs:
        containerregistrytype: 'Container Registry'
        dockerRegistryEndpoint: 'docker2'
        command: 'Build an image'
        dockerFile: '**/Dockerfile'
        imageName: '$(ImageName)'
        includeLatestTag: true
        useDefaultContext: false
        buildContext: '.'
     
    - task: Docker@1
      displayName: 'Push the Docker image to Dockerhub'
      inputs:
        containerregistrytype: 'Container Registry'
        dockerRegistryEndpoint: 'docker2'
        command: 'Push an image'
        imageName: '$(ImageName)'
      condition: and(succeeded(), ne(variables['Build.Reason'], 'PullRequest'))
 ```

click on save and run.
Now our pipeline is running and building.
After the build our docker image will create and been pushed to docker registry under the repository name evaluation app.

Deploying the application into google cloud
Login into your google cloud account
Search for kubernetes engine and select it.
Now click on create to create a new cluster.

 ![image](https://user-images.githubusercontent.com/68682617/110419111-ac6e8d80-80be-11eb-8dfe-03d84b7584ef.png)


Select standard and go with the default settings and click create.
It will take 5 – 6 minutes to create the cluster.
Till then click cloudshell icon in the top rightside.
Go to the cluster and click on  connect

 ![image](https://user-images.githubusercontent.com/68682617/110419124-b42e3200-80be-11eb-86d7-a63bef99244d.png)


Now copy the command and execute it in the cloud shell.
Command looks like as follows
gcloud container clusters get-credentials cluster-1 --zone us-central1-c --project < your project id>
now execute the following commands in the cloud shell.
1.	docker login -u <username> -p <password>
1.	docker pull <username>/evaluationapp:<recent tag>
1.	gcloud services enable containerregistry.googleapis.com --project <projectId>
1.	docker tag <username>/evaluationapp:<recent tag> gcr.io/<ProjectId>/<username>/evaluationapp:<recent tag>
1.	docker push gcr.io/<ProjectID>/username/evaluationapp:<tag>
6.	nano deployment.yaml
paste the following content and edit accordingly.
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: evaluationapp
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      name: evaluationapp
  template:
    metadata:
      labels:
        name: evaluationapp
    spec:
      containers:
      - name: evaluationapp
        image: <username>/evaluationapp:<tag>
```
7.	ctrl+X, type y and hit enter to save changes
8.	kubectl apply -f deployment.yaml
9.	kubectl expose deployment evaluationapp --type=LoadBalancer --name=my-service --port=80 --target-port=5009

Now go to the google cloud -> Kubernetes Engine -> Services and Ingress.
Under service and ingress, You will find an IPaddress under endpoint.
Copy the end point and edit it as following :
 http://<IPaddress>:80/calculas?input_standard=celsius&input1=89&output_standard=fahrenheit&output_given=95
you will see the output as wrong convertion.

