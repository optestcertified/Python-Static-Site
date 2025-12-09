pipeline {
    agent any

    environment {
        DROPLET_USER = "root"
        DROPLET_IP = "138.68.31.248"
        SSH_KEY_ID = "droplets-ssh-key"
        REPO_URL = "https://github.com/optestcertified/python-static-site.git"
        BRANCH = "main"
        REMOTE_DIR = "/var/www/python-static-site"
    }

    triggers {
        githubPush()
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: "${BRANCH}", url: "${REPO_URL}"
            }
        }

        stage('Install Dependencies (Local Jenkins)') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate

                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Syntax Test') {
            steps {
                sh '''
                . venv/bin/activate
                python3 -m py_compile app.py
                '''
            }
        }

        stage('Deploy to DigitalOcean Droplet') {
            steps {
                sshagent(credentials: [SSH_KEY_ID]) {
                    sh """
                    # Create folder on Droplet
                    ssh -o StrictHostKeyChecking=no ${DROPLET_USER}@${DROPLET_IP} "mkdir -p ${REMOTE_DIR}"

                    # Copy project files to Droplet securely
