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

        stage('Check and Display API Docs Files') {
            steps {
                script {
                     def txtPath  = 'out/api_docs.txt'
                     def htmlPath = 'out/api_docs.html'

                    def txtExists  = fileExists(txtPath)
                    def htmlExists = fileExists(htmlPath)

                    if (txtExists && htmlExists) {
                    echo "Both api_docs.txt and api_docs.html were found in the out folder."
                    echo "===== api_docs.txt ====="
                    echo readFile(txtPath)
                    echo "===== api_docs.html ====="
                    echo readFile(htmlPath)
                      } else {
                        if (!txtExists)  { echo "api_docs.txt is missing in the out folder." }
                        if (!htmlExists) { echo "api_docs.html is missing in the out folder." }
                        error('Required API docs files missing!') // Fail the pipeline if any file is missing
              }
            }
          }
        }

        
        // stage("Check 'out' Folder Files") {
        //     steps {
        //         script {
        //             sh 'pwd'
        //             sh 'cd /Users/nidhishreebh/.jenkins/workspace/docflow-poc-2/out'
        //             //sh 'cd out'
        //             sh 'ls -ltr'
        //         }
        //     }
        // }

        stage('Read files') {
            steps {
                script {
                    sh 'ls -ltr /Users/nidhishreebh/.jenkins/workspace/docflow-poc-2/out | awk '{print $9}'| grep api | xargs cat'
                }
            }
        }
    }
}
