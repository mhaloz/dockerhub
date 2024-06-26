pipeline {
    environment {
        IMAGEN = "mhaloz785/docker"
        USUARIO = 'USER_DOCKERHUB'
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
                    newApp = docker.build "$IMAGEN:$BUILD_NUMBER"
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    docker.image("$IMAGEN:$BUILD_NUMBER").inside('-u root') {
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
                        if ! command -v trivy &> /dev/null
                        then
                            curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh
                        fi
                    '''
                    // Scan the Docker image
                    sh "trivy image $IMAGEN:$BUILD_NUMBER"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    docker.withRegistry( '', USUARIO ) {
                        newApp.push()
                    }
                }
            }
        }

        stage('Clean Up') {
            steps {
                sh "docker rmi $IMAGEN:$BUILD_NUMBER"
            }
        }
    }
}
