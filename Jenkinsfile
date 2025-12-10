pipeline {
    agent any

    environment {
        DROPLET_USER = "root"
        DROPLET_IP = "206.189.78.225"
        SSH_KEY_ID = "droplets-ssh-key"
        REPO_URL = "https://github.com/optestcertified/python-static-site.git"
        BRANCH = "main"
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
                sh """
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage('Syntax Test') {
            steps {
                sh """
                    . venv/bin/activate
                    python3 -m py_compile app.py
                """
            }
        }

        stage('Deploy to DigitalOcean Droplet') {
            steps {
                sshagent(["${SSH_KEY_ID}"]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${DROPLET_USER}@${DROPLET_IP} << 'EOF'
                            set -e
                            apt-get update -y
                            apt-get install -y python3 python3-pip python3-venv git

                            pkill -f app.py || true

                            rm -rf python-static-site
                            git clone ${REPO_URL}

                            cd python-static-site

                            python3 -m venv venv
                            ./venv/bin/pip install --upgrade pip
                            ./venv/bin/pip install -r requirements.txt

                            nohup ./venv/bin/python3 app.py > app.log 2>&1 &
                        EOF
                    """
                }
            }
        }
    }

    post {
        success { echo "Deployment successful!" }
        failure { echo "Deployment failed." }
    }
}
