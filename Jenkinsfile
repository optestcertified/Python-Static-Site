pipeline {
    agent any

    environment {
        DROPLET_USER = "root"
        DROPLET_IP = "209.38.37.241"
        SSH_KEY_ID = "droplets-ssh-key" // Jenkins credential ID
        REPO_URL = "https://github.com/optestcertified/python-static-site.git"
        BRANCH = "main"
    }

    triggers {
        githubPush()  // Trigger on GitHub push event
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: "${env.BRANCH}", url: "${env.REPO_URL}"
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python -m venv venv
                . venv/bin/activate
                pip3 install -r requirements.txt
                '''
            }
        }

        stage('Syntax Test') {
            steps {
                echo 'Running basic Python syntax test...'
                sh 'python3 -m py_compile app.py'
            }
        }

        stage('Deploy to Droplet') {
            steps {
                echo 'Deploying to DigitalOcean Droplet...'
                sshagent(credentials: [env.SSH_KEY_ID]) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ${DROPLET_USER}@${DROPLET_IP} '
                        echo "Stopping any existing app process..."
                        pkill -f app.py || true

                        echo "Updating code..."
                        rm -rf python-static-site
                        git clone ${REPO_URL}
                        cd python-static-site
                        pip3 install -r requirements.txt

                        echo "Starting app..."
                        nohup python3 app.py > app.log 2>&1 &
                        echo "App deployed successfully!"
                    '
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful to DigitalOcean Droplet!"
        }
        failure {
            echo "❌ Deployment failed. Check Jenkins logs."
        }
    }
}
