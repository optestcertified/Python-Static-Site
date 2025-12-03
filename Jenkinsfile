pipeline {
    agent any

    environment {
        DROPLET_USER = "root"
        DROPLET_IP = "138.197.37.221"
        SSH_KEY_ID = "droplet-ssh-key"
        REPO_URL = "https://github.com/optestcertified/python-static-site.git"
        BRANCH = "main"
    }

    triggers {
        githubPush()   // GitHub webhook trigger
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: "${env.BRANCH}", url: "${env.REPO_URL}"
            }
        }

        stage('Install Dependencies (Jenkins Node)') {
            steps {
                sh '''
                sudo apt-get update -y
                sudo apt-get install -y python3 python3-pip python3-venv git

                python3 -m venv venv
                . venv/bin/activate

                pip install --upgrade pip
                pip install -r requirements.txt || true
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
                sshagent(credentials: [env.SSH_KEY_ID]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ${DROPLET_USER}@${DROPLET_IP} << 'EOF'

                        set -e

                        echo "🔹 Updating system..."
                        apt-get update -y
                        apt-get install -y python3 python3-pip python3-venv git

                        echo "🔹 Stopping existing app (if running)..."
                        pkill -f app.py || true

                        echo "🔹 Fetching latest application code..."
                        rm -rf python-static-site
                        git clone ${REPO_URL}

                        cd python-static-site

                        echo "🔹 Creating Python virtual environment..."
                        python3 -m venv venv

                        echo "🔹 Installing dependencies..."
                        ./venv/bin/pip install --upgrade pip
                        ./venv/bin/pip install -r requirements.txt

                        echo "🔹 Starting application..."
                        nohup ./venv/bin/python3 app.py > app.log 2>&1 &

                        echo "🎉 Application deployed successfully!"
                    EOF
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful!"
        }
        failure {
            echo "❌ Deployment failed — check Jenkins logs."
        }
    }
}
