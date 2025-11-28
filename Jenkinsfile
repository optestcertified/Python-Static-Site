pipeline {
    agent any

    environment {
        DROPLET_USER = "root"
        DROPLET_IP = "209.38.37.241"
        SSH_KEY_ID = "droplets-ssh-key"   // Jenkins credentials ID
        REPO_URL = "https://github.com/optestcertified/python-static-site.git"
        BRANCH = "main"
    }

    triggers {
        githubPush()   // Listen for GitHub webhook
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
                sudo apt update -y
                sudo apt install -y python3 python3-pip python3-venv git

                # Create Python virtual environment
                python3 -m venv venv
                . venv/bin/activate

                pip install --upgrade pip

                # Install requirements inside venv
                pip install -r requirements.txt
                '''
            }
        }

        stage('Syntax Test') {
            steps {
                sh '''
                . venv/bin/activate
                python -m py_compile app.py
                '''
            }
        }

        stage('Deploy to Droplet') {
            steps {
                sshagent(credentials: [env.SSH_KEY_ID]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ${DROPLET_USER}@${DROPLET_IP} << 'EOF'
                        set -e

                        echo "🔹 Installing Python & Git..."
                        apt update -y
                        apt install -y python3 python3-pip python3-venv git

                        echo "🔹 Stopping old app..."
                        pkill -f app.py || true

                        echo "🔹 Pulling latest code..."
                        rm -rf python-static-site
                        git clone ${REPO_URL}
                        cd python-static-site

                        echo "🔹 Creating Python venv..."
                        python3 -m venv venv
                        . venv/bin/activate

                        echo "🔹 Installing dependencies..."
                        pip install -r requirements.txt

                        echo "🔹 Starting app..."
                        nohup python3 app.py > app.log 2>&1 &
                        echo "🎉 App deployed successfully!"
                    EOF
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful to DigitalOcean Droplet!"
        }
        failure {
            echo "❌ Deployment failed. Please check Jenkins console output."
        }
    }
}
