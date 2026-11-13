pipeline {
    agent any
    environment {
        IMAGE_NAME = "careguard-health"
        IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKER_CREDENTIALS = "dockerhub-creds"
    }
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Verify Trivy') {
            steps {
                sh '''
                    command -v trivy >/dev/null 2>&1 || { echo "Trivy is not installed on this Jenkins agent."; exit 1; }
                    trivy --version
                '''
            }
        }
        stage('Dependency and Repository Scan') {
            steps {
                sh '''
                    trivy fs --scanners vuln,misconfig,secret \\
                      --severity HIGH,CRITICAL --exit-code 1 --format table .
                '''
            }
        }
        stage('Build Image') { steps { sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .' } }
        stage('Container Image Scan') {
            steps {
                sh '''
                    trivy image --severity HIGH,CRITICAL \\
                      --exit-code 1 --format table $IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }
        stage('Push Image') {
            when {
    expression {
        env.BRANCH_NAME == 'main' ||
        env.GIT_BRANCH == 'main' ||
        env.GIT_BRANCH == 'origin/main'
    }
}
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS}",
                    usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_TOKEN')]) {
                    sh '''
                        echo "$DOCKER_TOKEN" | docker login -u "$DOCKER_USER" --password-stdin
                        docker tag $IMAGE_NAME:$IMAGE_TAG $DOCKER_USER/$IMAGE_NAME:$IMAGE_TAG
                        docker push $DOCKER_USER/$IMAGE_NAME:$IMAGE_TAG
                        docker logout
                    '''
                }
            }
        }
    }
    post { always { echo 'CareGuard DevSecOps pipeline finished. Review scan output before deployment.' } }
}
