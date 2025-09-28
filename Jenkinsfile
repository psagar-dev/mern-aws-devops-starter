@Library('Shared') _
def mernMicroservicesHello = securityConfig("securelooper/mern-microservices-hello:${BUILD_NUMBER}",'')
def mernMicroservicesProfile = securityConfig("securelooper/mern-microservices-profile:${BUILD_NUMBER}",'')
def mernMicroservicesfrontend = securityConfig("securelooper/mern-microservices-frontend:${BUILD_NUMBER}",'')
pipeline {
    agent any

    parameters {
        choice(
            name: 'SERVICE_TO_BUILD',
            choices: ['ALL', 'frontend', 'backend-hello', 'backend-profile'],
            description: 'Select which part of the application to build and deploy.'
        )
    }

    stages {
        stage("Security Scans") {
            steps {
                script {
                    securityScan()
                }
            }
        }
    
        stage('Build Docker Images') {
            parallel {
                stage('Build Frontend') {
                    when {
                        expression {
                            params.SERVICE_TO_BUILD == 'ALL' || params.SERVICE_TO_BUILD == 'frontend'
                        }
                    }
                    steps {
                        echo "Building Frontend because '${params.SERVICE_TO_BUILD}' was selected."
                        dir('frontend') {
                            script {
                                echo "Building Docker image for frontend"
                                docker.build(
                                    "${mernMicroservicesfrontend.DOCKER_IMAGE}",
                                    "--build-arg REACT_APP_API_BASE_URL_HELLO=${env.REACT_APP_API_BASE_URL_HELLO} --build-arg REACT_APP_API_BASE_URL_PROFILE=${env.REACT_APP_API_BASE_URL_PROFILE} ."
                                )
                            }
                        }
                    }
                }
                stage('Build Backend Hello') {
                    when {
                        expression {
                            params.SERVICE_TO_BUILD == 'ALL' || params.SERVICE_TO_BUILD == 'backend-hello'
                        }
                    }
                    steps {
                        echo "Building Backend Hello because '${params.SERVICE_TO_BUILD}' was selected."
                        dir('backend/helloService') {
                            script {
                                docker.build("${mernMicroservicesHello.DOCKER_IMAGE}")
                            }
                        }
                    }
                }
                stage('Build Backend Profile') {
                    when {
                        expression {
                            params.SERVICE_TO_BUILD == 'ALL' || params.SERVICE_TO_BUILD == 'backend-profile'
                        }
                    }
                    steps {
                        echo "Building Backend Profile because '${params.SERVICE_TO_BUILD}' was selected."
                        dir('backend/profileService') {
                            script {
                                docker.build("${mernMicroservicesProfile.DOCKER_IMAGE}")
                            }
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            script {
                def commitInfo = sh(script: 'git log -1 --pretty=%h', returnStdout: true).trim()
                def message = """
                {
                    "status": "SUCCESS",
                    "project": "${env.JOB_NAME}",
                    "build_number": "${BUILD_NUMBER}",
                    "url": "${env.BUILD_URL}",
                    "commit": "${commitInfo}"
                }
                """
                echo "Sending SUCCESS notification..."
                withCredentials([aws(credentialsId: 'aws-credentials')]) {
                    sh "aws sns publish --topic-arn '${env.SNS_TOPIC_ARN}' --message '${message}' --region '${env.AWS_REGION}'"
                }
            }
        }

        failure {
            script {
                def commitInfo = sh(script: 'git log -1 --pretty=%h', returnStdout: true).trim()
                def message = """
                {
                    "status": "FAILURE",
                    "project": "${env.JOB_NAME}",
                    "build_number": "${BUILD_NUMBER}",
                    "url": "${env.BUILD_URL}",
                    "commit": "${commitInfo}"
                }
                """
                echo "Sending FAILURE notification..."
                withCredentials([aws(credentialsId: 'aws-credentials')]) {
                    sh "aws sns publish --topic-arn '${env.SNS_TOPIC_ARN}' --message '${message}' --region '${env.AWS_REGION}'"
                }
            }
        }
    }
}