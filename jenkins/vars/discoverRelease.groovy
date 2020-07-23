#!/usr/bin/env groovy

"""
.. module:: Discover release
     :platform: Jenkins
     :synopsis: Discover release.
.. moduleauthor::
     :Nickname: nebul4ck
     :mail: a.gonzalezmesas@gmail.com
     :Web : https://github.com/nebul4ck/devops-engineer/tree/master/jenkins
"""

/* Discover release */
def call(Map pipelineParams) {
        
    ''' Main discover release method '''

    release = [:]
    release['new_release'] = ''

    //sh 'git checkout develop && git pull'

    def version_file = new File("${env.WORKSPACE}/VERSION").readLines()[0]

    //sh 'git checkout develop && git pull'

    if ("${version_file}" =~ /\d+.\d+.\d+/) {
        def new_release = ("${version_file}" =~ /\d+.\d+.\d+/)
        release.put('new_release', "${new_release[0]}")
    }
    return release.new_release
}
return this
