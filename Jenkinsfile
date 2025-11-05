pipeline {
    agent any

    environment {
        PATH = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Applications/Docker.app/Contents/Resources/bin:${env.PATH}"
        GEMINI_API_KEY = credentials('gemini-api-key') // Store your API key securely in Jenkins Credentials
    }

    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/Patel-Phaneendra/autodocs-hackathon.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'pwd'
                    sh 'printenv'
                    sh 'whoami'
                    //sh 'export PATH=/usr/local/bin:$PATH'
                    sh 'echo $PATH'
                    sh 'docker build -t autodocflow:python-doc-api-gemini-jenkins .'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sh 'docker run --rm -v $PWD:/app -e GEMINI_API_KEY=${GEMINI_API_KEY} autodocflow:python-doc-api-gemini-jenkins'
                }
            }
        }

        stage("Check 'out' Folder Files") {
            steps {
                script {
                    def outDir = "${env.WORKSPACE}/out"
                    sh "[ -d ${outDir} ] && ls -l ${outDir} || echo 'out directory does not exist'"
                }
            }
        }

        stage("Read and Show Contents of 'out' Folder Files") {
            steps {
                script {
                    def outDir = "${env.WORKSPACE}/out"
                    sh '''
                        if [ -d '${outDir}' ]; then
                            for f in ${outDir}/*; do
                                echo "=== $f ==="
                                cat "$f"
                            done
                        else
                            echo "No 'out' directory found."
                        fi
                    '''
                }
            }
        }
    }
}
