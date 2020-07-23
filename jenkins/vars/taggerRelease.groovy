#!/usr/bin/env groovy

"""
.. module:: Tagger
     :platform: Jenkins
     :synopsis: Launch tagger.
.. moduleauthor::
     :Nickname: nebul4ck
     :mail: a.gonzalezmesas@gmail.com
     :Web : https://github.com/nebul4ck/devops-engineer/tree/master/jenkins
"""

def runBumpversion(Map pipelineParams) {

    /* Upgrade version (control file) */
    evolutive = "${pipelineParams.evolutive}"
    branch_name = "${pipelineParams.branch_name}"
    repository = "${pipelineParams.repository}"

    /* git sync */
    sh "git checkout ${branch_name} && git pull"

    bumpversion_status = """${sh(
                                returnStatus: true,
                                script: "bumpversion ${evolutive}")}"""

    return bumpversion_status
}

def newRelease(Map pipelineParams) {

    /* Updating new release in github */
    branch_name = "${pipelineParams.branch_name}"
    new_release = "${pipelineParams.new_release}"
    repository = "${pipelineParams.repository}"

    sh "git checkout ${branch_name} && git pull"

    // no fast-forward: posibilidad de seguimiento de commit después del merge
    // You should tag the commit you actually release (merge)
    sh "git merge --no-ff --log --no-edit develop"
    sh "git push origin ${branch_name}"

    // Jenkins not listen in tags (only */develop)
    sh "git tag -a v${new_release} -m 'v${new_release}'"
    sh "git push --tags"

    def data_json = """'{\"tag_name\": \"${new_release}\",
                   | \"target_commitish\": \"master\",
                   | \"name\": \"${new_release}\",
                   | \"body\": \"merge from develop: Relasing v${new_release}\",
                   | \"draft\": false,\"prerelease\": false}'"""
                    .stripMargin().replaceAll("\n", "")

    /* Used icampos Token */
    def command = """curl -v -i -X POST -H \"Content-Type:application/json\"
                | -H \"Authorization: token 395e20b70a9bda93f5d5209a9dab9d6456727ee6\"
            | https://api.github.com/repos/nebul4ck/${repository}/releases -d ${data_json}"""
             .stripMargin().replaceAll("\n", "")

    new_release_status = """${sh(
                                returnStatus: true,
                                script: "${command}")}"""

    return new_release_status
}

def call(Map pipelineParams) {
        
    ''' Main tagger method '''

    branch_name = "${pipelineParams.branch_name}"
    action = "${pipelineParams.action}"
    repository = "${pipelineParams.repository}"
    tagger = [:]

    if (action == 'update_version') {
        evolutive = "${pipelineParams.evolutive}"
        bumpversion_status = runBumpversion(
                     evolutive: "${evolutive}",
                     branch_name: "${branch_name}",
                     repository: "${repository}"
                    )

        if (bumpversion_status != "0") {
            currentBuild.result = 'FAILURE'
            tagger.put('status', 'Error: Bumpversion failed!')
        } else {
            /* Commit version control files :after from push with commit 
            "Bump Version x.y.z -> z.y.x" Jenkins doesn't trigger a new pipeline.
            Pipeline config:
                -> Additional Behaviours: Polling ignores commits with certain messages */
            /*def pw = pwd()
            dir("${pw}") {
                sh "git push origin ${branch_name}"
            }*/

            dir("../${repository}") {
                sh 'git checkout develop && git pull'
            }
            currentBuild.result = 'SUCCESS'
            tagger.put('status', 'Success')
        }
    } else if (action == 'releasing') {
        new_release = "${pipelineParams.new_release}"
        new_release_status = newRelease(
                   branch_name: "${branch_name}",
                   new_release: "${new_release}",
                   repository: "${env.JOB_BASE_NAME}"
                   )

        if (new_release_status != "0") {
            currentBuild.result = 'FAILURE'
            tagger.put('status', 'Error: Releasing failed!')
        } else {
            currentBuild.result = 'SUCCESS'
            tagger.put('status', 'Success')
        }
    }
    return tagger
}
return this
