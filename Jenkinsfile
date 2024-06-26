pipeline {
    environment {
        IMAGEN = "mhaloz785/docker"
        USUARIO = 'USER_DOCKERHUB'  // Credential ID for Docker Hub
    }
    agent any
    stages {
        stage('Clone') {
            steps {
                git branch: "main", url: 'https://github.com/mhaloz/dockerhub/'
            }
        }
        stage('Build') {
            steps {
                script {
                    newApp = docker.build("${IMAGEN}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    docker.image("${IMAGEN}:${BUILD_NUMBER}").inside('-u root') {
                        sh 'apache2ctl -v'
                    }
                }
            }
        }

        stage('Scan Image') {
            steps {
                script {
                    // Install Trivy if not installed
                    sh '''
                        if ! command -v trivy &> /dev/null; then
                            echo "Installing Trivy..."
                            wget -qO- https://github.com/aquasecurity/trivy/releases/latest/download/trivy_0.41.0_Linux-64bit.tar.gz | tar zxvf - -C /usr/local/bin/
                        fi
                    '''
                    // Scan the Docker image
                    sh "trivy image ${IMAGEN}:${BUILD_NUMBER}"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    docker.withRegistry('', USUARIO) {
                        newApp.push()
                    }
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    // Clean up Docker images
                    sh "docker rmi ${IMAGEN}:${BUILD_NUMBER} || true"
                }
            }
        }
    }
    post {
        always {
            cleanWs() // Clean workspace after build
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
