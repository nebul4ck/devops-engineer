#!/usr/bin/env groovy

"""
.. module:: Builder
     :platform: Jenkins
     :synopsis: Trigger Builder.
.. moduleauthor::
     :Nickname: nebul4ck
     :mail: a.gonzalezmesas@gmail.com
     :Web : https://github.com/nebul4ck/devops-engineer/tree/master/jenkins
"""

/* Sync dev and pro repositories */
def syncsRepositories(Map pipelineParams) {
    repository = "${pipelineParams.repository}"
    branch = "${pipelineParams.branch}"
    buanaclient_cmd = "${pipelineParams.buanaclient_cmd}"

    syncs_repositories_status = """${sh(
                                    returnStatus: true,
                                    script: "${buanaclient_cmd} ${repository} ${branch}")}"""

    return syncs_repositories_status
}

/* Make package */
def makePackage(Map pipelineParams) {
    language_version = "${pipelineParams.language_version}"
    repository = "${pipelineParams.repository}"
    // Workaround for https://issues.jenkins-ci.org/browse/JENKINS-46988 BUG
    make_package_status = """${sh(
                            returnStatus: true,
                            script: "./make_package.sh ${language_version} jenkins \
                            ${repository}")}"""

    return make_package_status
}

/* Buanaclient */
def buanaClient(Map pipelineParams) {
    buanaclient_cmd = "${pipelineParams.buanaclient_cmd}"
    repository = "${pipelineParams.repository}"
    branch = "${pipelineParams.branch}"
    language = "${pipelineParams.language}"

    buanaclient_status = """${sh(
                            returnStatus: true,
                            script: "${buanaclient_cmd} ${repository} \
                                    ${branch} ${language}")}"""

    return buanaclient_status
}

/* Builder */
def call(Map pipelineParams) {
        
    ''' Main build method '''

    syncs_repositories = "${pipelineParams.syncs_repositories}"
    branch = "${pipelineParams.branch}"
    repository = "${pipelineParams.repository}"
    build = [:]

    if ("${pipelineParams.third_party}" == 'False') {

        //sh "git checkout ${branch} && git pull"

        make_package_status = makePackage(
                                        language_version: "${pipelineParams.language_version}",
                                        repository: "${repository}"
                            )

        if (make_package_status != "0") {
            currentBuild.result = 'FAILURE'
            build.put('status', 'Failed')
        } else {
            buanaclient_status = buanaClient(
                                            buanaclient_cmd: "${pipelineParams.buanaclient_cmd}",
                                            repository: "${repository}",
                                            branch: "${pipelineParams.branch}",
                                            language: "${pipelineParams.language}"
                                )

            if (buanaclient_status != "0") {
                currentBuild.result = 'FAILURE'
                build.put('status', 'Failed')
            } else {

                if (syncs_repositories == 'True') {
                    syncs_repositories_status = syncsRepositories(
                                                        branch: 'master',
                                                        repository: "${repository}",
                                                        buanaclient_cmd: "buanaclient sync"
                                            )

                    if (syncs_repositories_status != "0") {
                        currentBuild.result = 'FAILURE'
                        build.put('status', 'Error: The repositories could not be synchronized')
                    } else {
                        currentBuild.result = 'SUCCESS'
                        build.put('status', 'Success')
                    }
                } else {
                    build.put('status', 'Success')
                }
                
            }
        }        
    } else if ("${pipelineParams.third_party}" == 'True') {
            buanaclient_status = buanaClient(
                                            buanaclient_cmd: "${pipelineParams.buanaclient_cmd}",
                                            repository: "${repository}",
                                            branch: "${pipelineParams.branch}",
                                            language: "${pipelineParams.language}"
                                )

            if (buanaclient_status != "0") {
                currentBuild.result = 'FAILURE'
                build.put('status', 'Failed')
            } else {
                currentBuild.result = 'SUCCESS'
                build.put('status', 'Success')
            }        
    } else {
        build['status'] = 'The third_party parameter in Jenkisfile *must* be True or False'
        currentBuild.result = 'FAILURE'
    }
    return build   
}
return this
