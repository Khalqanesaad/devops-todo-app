pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
        IMAGE_NAME = 'khalqanesaad/todo-app'
    }

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Running unit tests for Python application...'
                // يمكنك إضافة أوامر تشغيل الاختبارات هنا لاحقاً مثل pytest
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    appImage = docker.build("${env.IMAGE_NAME}:${env.BUILD_ID}")
                    appImage.tag("latest")
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', "${env.DOCKER_CREDENTIALS_ID}") {
                        appImage.push("${env.BUILD_ID}")
                        appImage.push("latest")
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/deployment.yaml'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully and application deployed!'
        }
        failure {
            echo 'Pipeline failed during execution.'
        }
    }
}