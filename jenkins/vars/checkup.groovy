#!/usr/bin/env groovy

"""
.. module:: Checkup
     :platform: Jenkins
     :synopsis: Trigger Pipeline Check up.
.. moduleauthor::
     :Nickname: nebul4ck
     :mail: a.gonzalezmesas@gmail.com
     :Web : https://github.com/nebul4ck/devops-engineer/tree/master/jenkins
"""

/* Checkup */
def call(Map pipelineParams) {
        
    ''' Main Checkup method '''

    // Local Vars
    def repository = "${pipelineParams.repository}"
    def git_commit_message = "${pipelineParams.git_commit_message}"
    def base_name_repository = "${env.JENKINS_HOME}/workspace/${repository}"
    def dirDoc = new File("${base_name_repository}/docs")
    def dirTest = new File("${base_name_repository}/tests")
    def defaultBuildDirectories = ["${base_name_repository}/${repository}", \
                                "${base_name_repository}/deb_packages"]

    /* Default Settings */
    globalize = [:]
    globalize['build_documentation'] = 'False'
    globalize['launch_tests'] = 'False'
    globalize['build_package'] = 'False'
    globalize['update_version'] = 'False'
    globalize['evolutive'] = ''

    // does it need to build a new package?
    defaultBuildDirectories.each {
        def build_directory = new File("$it")
        if (build_directory.exists()) {
            globalize.put('build_package', 'True')
        }
    }

    // does it need to run testing?
    if (dirTest.exists()) {
        globalize.put('launch_tests', 'True')
    /* Workaround for pass without tests in pandora */
    } else {
        globalize.put('launch_tests', 'True')
    }

    // does it need to update version?
    if ("${git_commit_message}" =~ /release\((major|minor|patch)\):/) {
        def evolutive = ("${git_commit_message}" =~ /[^release(]\w+/)
        globalize.put('evolutive', "${evolutive[0]}")
        globalize.put('update_version', 'True')

        // does it need to build documentation?
        if (dirDoc.exists()) {
            globalize.put('build_documentation', 'True')
        }

    }
    return globalize
}
return this
