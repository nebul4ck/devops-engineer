
''' Main Pipeline method '''

def call(Map pipelineParams) {

    /* Saturn Pipeline */
    pipeline {
        agent any

        /* parameters {
            booleanParam(defaultValue: true, description: '', name: 'booleanExample')
            string(defaultValue: "TEST", description: 'What environment?', name: 'stringExample')
            text(defaultValue: "This is a multiline\n text", description: "Multiline Text", name: "textExample")
            choice(choices: 'US-EAST-1\nUS-WEST-2', description: 'What AWS region?', name: 'choiceExample')
            password(defaultValue: "Password", description: "Password Parameter", name: "passwordExample")
        }*/

        /* Use input to stop de workflow and wait to approval
        timeout(time:5, unit:'DAYS') {
            input message:'Approve deployment?', submitter: 'it-ops'
        }*/

        environment {
            PATH="/home/buanarepo/bin:/home/buanarepo/.local/bin:\
            /usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:\
            /snap/bin:/usr/lib/jvm/java-8-oracle/bin:\
            /usr/lib/jvm/java-8-oracle/db/bin:/usr/lib/jvm/java-8-oracle/jre/bin:\
            /home/buanarepo/.nvm/versions/node/${pipelineParams.language_version}/bin/"

            /* Committer */
            GIT_COMMITTER = """${sh(
                                    returnStdout: true,
                                    script: "git --no-pager show -s --format='%an' ${GIT_COMMIT}")
                                    .trim()}"""

            MAINTAINER = "${pipelineParams.git_maintainer}"

            /* Committer e-mail */
            GIT_EMAIL = """${sh(
                                returnStdout: true,
                                script: "git --no-pager show -s --format='%ae' ${GIT_COMMIT}")
                                .trim()}"""

            /* Useful Git commands:
                Commit msg: git log --format=format:%s -1 ${GIT_COMMIT}
                Full info: git log --format=fuller -1
                Body: git log --format=format:%b -1
            */

            RUNTIMESTAMP = """${sh(
                                returnStdout: true,
                                script: "date +%d%m%Y_%H%m")
                                .trim()}"""

            GIT_COMMIT_MESSAGE = """${sh(
                                        returnStdout: true,
                                        script: "git log --format=format:%s -1")
                                        .trim()}"""
            
            /* Slack Messages (Header definition) */
            SLACK_HEADER = """\
                                repository: ${env.JOB_BASE_NAME}
                                maintainer: ${env.MAINTAINER}
                                committer: ${env.GIT_COMMITTER} <${env.GIT_EMAIL}>
                                branch: ${env.GIT_BRANCH}
                                build: ${env.BUILD_ID}
                                build timestamp: ${env.BUILD_TIMESTAMP}
                                commit: ${env.GIT_COMMIT}
                                previous successful commit: ${env.GIT_PREVIOUS_SUCCESSFUL_COMMIT}  
                            """.stripIndent()
        }
        /* Jenkins Stages */
        stages {
            stage('Check Up stage') {

                steps {
                    println '@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
                    println '@ Pipeline checkup  stage  @'
                    println '@@@@@@@@@@@@@@@@@@@@@@@@@@@@'

                    /* Send initial Slack message */
                    slackSend color: '#000000', message:
                    "Pipeline *${env.JOB_BASE_NAME}* info:\n${env.SLACK_HEADER}"

                    script {
                        // check requirements
                        globalize = checkup(
                                        repository: "${env.JOB_BASE_NAME}",
                                        git_commit_message: "${env.GIT_COMMIT_MESSAGE}"
                        )
                        
                        /* Global vars */

                        env.BUILD_DOCUMENTATION = globalize.build_documentation
                        env.LAUNCH_TESTS = globalize.launch_tests
                        env.BUILD_NEW_PACKAGE = globalize.build_package
                        env.UPDATE_VERSION = globalize.update_version
                        env.EVOLUTIVE = globalize.evolutive
                        env.TAGGER_STATUS = ''
                        env.NEW_RELEASE = ''
                        env.TESTMSG = 'Not there tests in test folder'
                        env.JUNIT_REPORT_URL = 'Not junit report'
                        env.BUILT_DOC_STATUS = ''
                        env.PRO_BUILD_STATUS = 'No package ready for production'
                        env.NEW_RELEASE = ''
                        env.DEPLOY_PRO_STATUS = ''
                        /* Workaround for pandora tests folder issue */
                        env.TESTS_OK = 'True'
                    }
                }
            }
            stage('Deployment stage in development environment') {
                when { 
                    environment name: 'BUILD_NEW_PACKAGE', value: 'True'
                }
                options {
                    timeout(time: "${pipelineParams.build_timeout}", unit: 'MINUTES')
                }

                steps {
                    println '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
                    println '@ Deployment stage in development environment @'
                    println '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'

                    script {

                        println "Building from develop branch"

                        /* git sync */
                        sh "git checkout develop && git pull"

                        /*TODO - sh "git branch -D ${BRANCH_NAME} && git checkout ${BRANCH_NAME} 
                        && git pull".
                        sustituir lo anterior por el step  deleteDir(). Para eliminar un directorio
                        concreto usar dir() para movernos al que queramos.
                        */

                        /* Call Build() */
                        build = builder(
                            repository: "${env.JOB_BASE_NAME}",
                            branch: "develop",
                            buanaclient_cmd: "${pipelineParams.build_command}",
                            third_party: "${pipelineParams.third_party}",
                            language: "${pipelineParams.language}",
                            language_version: "${pipelineParams.language_version}",
                            syncs_repositories: 'False'
                        )

                        /* Set build status */
                        env.DEV_BUILD_STATUS = build.status

                        if (currentBuild.result == 'FAILURE' ||
                            currentBuild.result == 'ABORTED') {
                            println " => Development, Build status: ${env.DEV_BUILD_STATUS}"
                            //sh 'exit 1'
                        } else {

                            if ("${pipelineParams.auto_deploy_dev}" == 'True') {
                                /* Call Deployer() */
                                deploy = deployer(
                                                  repository: "${env.JOB_BASE_NAME}",
                                                  environment: 'development'
                                        )

                                /* Set deploy status */
                                env.DEPLOY_DEV_STATUS = deploy.status
                            } else {
                                env.DEPLOY_DEV_STATUS = '*ATTENTION*: you need to deploy manually!'
                            }

                            if (currentBuild.result == 'FAILURE' ||
                                currentBuild.result == 'ABORTED') {
                                println " => Development, Build status: ${env.DEV_BUILD_STATUS}"
                                println " => Development, Deploy status: ${env.DEPLOY_DEV_STATUS}"
                                //sh 'exit 1'
                            } else {
                                println " => Development, Build status: ${env.DEV_BUILD_STATUS}"
                                println " => Development, Deploy status: ${env.DEPLOY_DEV_STATUS}"                               
                            }
                        }
                    }
                }
            }
            stage('Testing stage') {
                when {
                    allOf { 
                        environment name: 'LAUNCH_TESTS', value: 'True'
                        environment name: 'DEPLOY_DEV_STATUS', value: 'Success'
                    }
                }

                steps {
                    println '@@@@@@@@@@@@@@@@@'
                    println '@ Testing stage @'
                    println '@@@@@@@@@@@@@@@@@'

                    script {

                        /* git sync */
                        sh "git checkout develop && git pull"

                        /* call tests */
                        env.JUNIT_REPORT_URL = "${env.JENKINS_URL}job/${env.JOB_NAME}/lastBuild/execution/node/3/ws/results/"
                        env.JUNIT_REPORT_URL = env.JUNIT_REPORT_URL+"Reports${env.RUNTIMESTAMP}/html/overview-summary.html"
                        def VARS = new String[2]
                        VARS = testing(
                                       date: "${env.RUNTIMESTAMP}"
                                       )
                        env.TESTMSG = VARS[0]
                        env.EXIST_REPORT = VARS[1]
                                                
                        if (currentBuild.result == 'FAILURE' ||
                            currentBuild.result == 'ABORTED') {
                            env.TESTMSG = 'Failed'
                            println " => Results tests: ${env.TESTMSG}"
                            env.TESTS_OK = 'False'                                        
                        } else {
                            println " => Results tests: ${env.TESTMSG}"
                            env.TESTS_OK = 'True'
                        }
                        if (env.EXIST_REPORT != 'true') {
                            env.JUNIT_REPORT_URL = 'Without report'
                        }
                        
                    }
                }
            }
            stage('Tag/Release stage') {
                // only if test stage is OK
                when { 
                    allOf {
                        environment name: 'UPDATE_VERSION', value: 'True'
                        environment name: 'TESTS_OK', value: 'True'
                    }
                }

                steps {
                    println '@@@@@@@@@@@@@@@@@@@@@'
                    println '@ Tag/Release stage @'
                    println '@@@@@@@@@@@@@@@@@@@@@'

                    script {

                        /* git sync */
                        sh "git checkout develop && git pull"

                        /* Call taggerRelease(): bumpversion */
                        tagger_bump = taggerRelease(
                                    action: 'update_version',
                                    branch_name: 'develop',
                                    evolutive: "${env.EVOLUTIVE}",
                                    repository: "${env.JOB_BASE_NAME}"
                        )

                        /* Set tagger bump status */
                        env.TAGGER_STATUS = tagger_bump.status

                        if (currentBuild.result == 'FAILURE' ||
                            currentBuild.result == 'ABORTED') {
                            println " => Bumpversion: ${env.TAGGER_STATUS}"
                            //sh 'exit 1'
                        } else {
                            /* Call Discover Release */
                            env.NEW_RELEASE = discoverRelease()

                            /* Call taggerRelease(): newRelease */
                            tagger_release = taggerRelease(
                                        action: 'releasing',
                                        branch_name: 'master',
                                        new_release: "${env.NEW_RELEASE}"
                            )                                    

                            /* Set tagger release status */
                            env.TAGGER_STATUS = tagger_release.status

                            if (currentBuild.result == 'FAILURE' ||
                                currentBuild.result == 'ABORTED') {
                                println " => Bumpversion: ${env.TAGGER_STATUS}"
                                println " => Releasing: ${env.TAGGER_STATUS}"
                                //sh 'exit 1'
                            } else {
                                /* Make latest package version */
                                build = builder(
                                    repository: "${env.JOB_BASE_NAME}",
                                    branch: "develop",
                                    buanaclient_cmd: "${pipelineParams.build_command}",
                                    third_party: "${pipelineParams.third_party}",
                                    language: "${pipelineParams.language}",
                                    language_version: "${pipelineParams.language_version}",
                                    syncs_repositories: 'True'
                                )

                                /* Set build status */
                                env.PRO_BUILD_STATUS = build.status

                                if (currentBuild.result == 'FAILURE' ||
                                    currentBuild.result == 'ABORTED') {
                                    println " => Bumpversion: ${env.TAGGER_STATUS}"
                                    println " => Releasing: ${env.TAGGER_STATUS}"
                                    println " => Production, Build status: ${env.PRO_BUILD_STATUS}"
                                    //sh 'exit 1'
                                } else {
                                    println " => Bumpversion: ${env.TAGGER_STATUS}"
                                    println " => Releasing: ${env.TAGGER_STATUS}"
                                    println " => Production, Build status: ${env.PRO_BUILD_STATUS}"
                                    env.READY_FOR_PRO = 'True'
                                }
                            }
                        }
                    }
                }
            }
            stage('Build Doc stage') {
                when { 
                    allOf {
                        environment name: 'BUILD_DOCUMENTATION', value: 'True'
                        environment name: 'UPDATE_VERSION', value: 'True'
                        environment name: 'TAGGER_STATUS', value: 'Success'
                    }         
                }

                steps {
                    println '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
                    println '@ Build documentation stage @'
                    println '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'

                    script {

                        /* git sync */
                        sh "git checkout develop && git pull"

                        build_doc = """${sh(
                                    returnStatus: true,
                                    script: "curl localhost:8000/\
                                    updatedoc?repo=${env.JOB_BASE_NAME}")}"""

                        println "El resultado de build_doc es : ${build_doc}"

                        if (build_doc != "0") {
                            // Any failure to compile documentation can not stop the pipeline
                            currentBuild.result = 'SUCCESS'
                            env.BUILT_DOC_STATUS = 'Failed'
                            println " => Documentation: ${env.BUILT_DOC}"
                        } else {
                            currentBuild.result = 'SUCCESS'
                            env.BUILT_DOC_STATUS = 'Success'
                            println " => Documentation: ${env.BUILT_DOC}"
                        }
                    }
                }  
            }
            stage('Deployment stage in production environment') {
                when { 
                    environment name: 'READY_FOR_PRO', value: 'True'
                }

                steps {
                    println '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
                    println '@ Deployment stage in production environment @'
                    println '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'

                    script {

                        println "Deploying in production environment"

                        /* git sync */
                        sh "git checkout master && git pull"

                        if ("${pipelineParams.auto_deploy_pro}" == 'True') {
                            /* Call Deployer() */
                            deploy = deployer(
                                              repository: "${env.JOB_BASE_NAME}",
                                              environment: 'production'
                                    )

                            /* Set deploy status */
                            env.DEPLOY_PRO_STATUS = deploy.status
                        } else {
                            env.DEPLOY_PRO_STATUS = '*ATTENTION*: you need to deploy manually!'
                        }

                        if (currentBuild.result == 'FAILURE' ||
                            currentBuild.result == 'ABORTED') {
                            println " => Production, deploy status: ${env.DEPLOY_PRO_STATUS}"
                            //sh 'exit 1'
                        } else {
                            println " => Production, deploy status: ${env.DEPLOY_PRO_STATUS}"
                        }
                    }                       
                }
            }
        }
        post {
            success {
                // send stages_results
                slackSend color: 'good', message: """\
                        *Stages results:*
                          repository: ${env.JOB_BASE_NAME}
                          build: ${env.BUILD_ID}
                          build timestamp: ${env.BUILD_TIMESTAMP}
                        *Deployment stage in development environment*:
                          Built package: ${env.DEV_BUILD_STATUS}
                          Auto deploy: ${pipelineParams.auto_deploy_dev}
                          Deploy status: ${env.DEPLOY_DEV_STATUS}
                        *Testing stage*:
                          Environment: development
                          Need to be tested: ${env.LAUNCH_TESTS}
                          Tests results: ${env.TESTMSG}
                          Report: ${env.JUNIT_REPORT_URL}
                        *Tag/Release stage*:
                          New release: ${env.UPDATE_VERSION}
                          Tagged: ${env.TAGGER_STATUS}
                          Evolutive: ${env.EVOLUTIVE}
                          Version: ${env.NEW_RELEASE}
                        *Build Doc stage*:
                          Build the documentation: ${env.BUILD_DOCUMENTATION}
                          Build doc status: ${env.BUILT_DOC_STATUS}
                        *Deployment stage in production environment*:
                          Built package: ${env.PRO_BUILD_STATUS}
                          Release: ${env.NEW_RELEASE}
                          Auto deploy: ${pipelineParams.auto_deploy_pro}
                          Deploy status: ${env.DEPLOY_PRO_STATUS}
                        """.stripIndent()
            }
            failure {
                // send stages_results
                slackSend color: '#ff0000', message: """\
                        *Stages results:*
                          repository: ${env.JOB_BASE_NAME}
                          build: ${env.BUILD_ID}
                          build timestamp: ${env.BUILD_TIMESTAMP}
                        *Deployment stage in development environment*:
                          Built package: ${env.DEV_BUILD_STATUS}
                          Auto deploy: ${pipelineParams.auto_deploy_dev}
                          Deploy status: ${env.DEPLOY_DEV_STATUS}
                        *Testing stage*:
                          Environment: development
                          Need to be tested: ${env.LAUNCH_TESTS}
                          Tests results: ${env.TESTMSG}
                          Report: ${env.JUNIT_REPORT_URL}
                        *Tag/Release stage*:
                          Tagged: ${env.TAGGER_STATUS}
                          New release: ${env.UPDATE_VERSION}
                          Evolutive: ${env.EVOLUTIVE}
                          Version: ${env.NEW_RELEASE}
                        *Build Doc stage*:
                          Build the documentation: ${env.BUILD_DOCUMENTATION}
                          Build doc status: ${env.BUILT_DOC_STATUS}
                        *Deployment stage in production environment*:
                          Built package: ${env.PRO_BUILD_STATUS}"
                          Release: ${env.NEW_RELEASE}
                          Auto deploy: ${pipelineParams.auto_deploy_pro}
                          Deploy status: ${env.DEPLOY_PRO_STATUS}
                        """.stripIndent()                
            }
        }
    }
}
