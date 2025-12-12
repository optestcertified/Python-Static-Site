# Python-Static-Site 
## CI/CD Pipeline with Jenkins & DigitalOcean

## Overview
This project automates the deployment of a Flask static site to a DigitalOcean Droplet using Jenkins.  
Every code push to GitHub triggers an automatic build and redeployment.

## Tech Stack
- Python (Flask)
- Jenkins
- GitHub Webhook
- DigitalOcean Droplet (Ubuntu 22.04)

## Pipeline Flow
1. Developer pushes code to GitHub.
2. GitHub Webhook notifies Jenkins.
3. Jenkins pulls code, installs dependencies, tests syntax.
4. Jenkins SSHs into Droplet, deploys, and restarts the app.

## Setup Steps
1. Clone this repository.
2. Create a DigitalOcean Droplet.
3. Install Jenkins and add SSH credentials.
4. Add GitHub webhook → `http://<JENKINS_IP>:8080/github-webhook/`
5. Configure pipeline using the `Jenkinsfile`.
6. Push code to trigger automatic deployment.

## Access
Visit:  
`http://<DROPLET_IP>:3000`

