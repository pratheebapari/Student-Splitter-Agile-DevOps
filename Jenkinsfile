pipeline {
    agent any

    parameters {
        booleanParam(name: 'PUSH_TO_DOCKERHUB', defaultValue: false,
                     description: 'Push image to Docker Hub (requires Jenkins credential dockerhub-studentsplitter-v3)')
    }

    environment {
        IMAGE_NAME = 'student-splitter'
        IMAGE_TAG = "build-${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Install Dependencies') {
            steps { bat 'python -m pip install --upgrade pip' ; bat 'python -m pip install -r requirements.txt' }
        }
        stage('Automated Tests') {
            steps { bat 'python -m pytest -v' }
        }
        stage('Build Docker Image') {
            steps { bat 'docker build -t %IMAGE_NAME%:%IMAGE_TAG% -t %IMAGE_NAME%:latest .' }
        }
        stage('Push to Docker Hub') {
            when { expression { return params.PUSH_TO_DOCKERHUB } }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-studentsplitter-v3', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_TOKEN')]){
                    bat 'powershell -NoProfile -ExecutionPolicy Bypass -Command "$env:DOCKERHUB_TOKEN | docker login -u $env:DOCKERHUB_USER --password-stdin"'
                    bat 'docker tag %IMAGE_NAME%:%IMAGE_TAG% %DOCKERHUB_USER%/%IMAGE_NAME%:%IMAGE_TAG%'
                    bat 'docker push %DOCKERHUB_USER%/%IMAGE_NAME%:%IMAGE_TAG%'
                    bat 'docker logout'
                }
            }
        }
    }
    post {
        always { echo 'Student Splitter CI pipeline finished. Check the test and build stages above.' }
        success { echo 'Tests passed and the Docker image was built successfully.' }
    }
}
