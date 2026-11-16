pipeline {
    agent any

    environment {
        IMAGE_NAME = "clubsphere"
        DOCKERHUB_USERNAME = "mallikarjunbaddi"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Python') {
            steps {
                bat 'python --version'
                bat 'python -m py_compile app.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %DOCKERHUB_USERNAME%/%IMAGE_NAME%:%BUILD_NUMBER% .'
                bat 'docker tag %DOCKERHUB_USERNAME%/%IMAGE_NAME%:%BUILD_NUMBER% %DOCKERHUB_USERNAME%/%IMAGE_NAME%:latest'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat 'echo %DOCKER_PASS%| docker login -u %DOCKER_USER% --password-stdin'
                    bat 'docker push %DOCKERHUB_USERNAME%/%IMAGE_NAME%:%BUILD_NUMBER%'
                    bat 'docker push %DOCKERHUB_USERNAME%/%IMAGE_NAME%:latest'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(
                    credentialsId: 'kubeconfig',
                    variable: 'KUBECONFIG'
                )]) {
                    bat 'kubectl apply -f deployment.yaml'
                    bat 'kubectl set image deployment/clubsphere-deployment clubsphere=%DOCKERHUB_USERNAME%/%IMAGE_NAME%:%BUILD_NUMBER%'
                    bat 'kubectl apply -f service.yaml'
                    bat 'kubectl rollout status deployment/clubsphere-deployment'
                }
            }
        }
    }

    post {
        always {
            bat 'docker logout'
        }
        success {
            echo 'ClubSphere CI/CD pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the console output for details.'
        }
    }
}
