# Virtual Assistant

Virtual Assistant is build using following open source components.

- Angular Ui - To build, train and deploy a chat bot project
- Python API gateway - connecting to rasa for deploying and persisting training data
- Mongodb - for storing training data and editing training data

### How To Get Started

1. Use below commands to clone the github repo to local machine or server.
    
    git clone https://github.com/navigateconsulting/va-grievance-redressal.git
    cd va-grievance-redressal
    docker-compose build
    docker-compose up
    
Docker containers would be using ports 5055, 5005, 27017, 8080 for VA components. Ensure these ports are free.

2. Once the application is made available on http://localhost:8080/home/grievance-app , on the header you will find an option for Deploy once you click the menu button. Follow the screenshots attached below:

<div align="center" >
  <img src="/docs/assets/grievance_deploy_1.png">
</div>
<br />
<div align="center" >
  <img src="/docs/assets/grievance_deploy_2.png">
</div>
<br />
<div align="center" >
  <img src="/docs/assets/grievance_deploy_3.png">
</div>
<br />
<div align="center" >
  <img src="/docs/assets/grievance_deploy_4.png">
</div>
<br />
<div align="center" >
  <img src="/docs/assets/grievance_deploy_5.png">
</div>
