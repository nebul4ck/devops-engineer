#!/usr/bin/env groovy

"""
.. module:: Deployer
     :platform: Jenkins
     :synopsis: Launch Deployer.
.. moduleauthor::
     :Nickname: nebul4ck
     :mail: a.gonzalezmesas@gmail.com
     :Web : https://github.com/nebul4ck/devops-engineer/tree/master/jenkins
"""

def deployEnv(Map pipelineParams) {
  ''' Main environments deployer method '''

  environment = "${pipelineParams.environment}"
  repository = "${pipelineParams.repository}"

  /* At this moment jenkins is in the ./proyect@2 directory, then, we move to ./repository
  in the next step */
  dir("../${repository}") {
    set_environment = """${sh(
                              returnStatus: true,
                              script: ". ansible/ANSIBLE-ENVIRONMENT.sh")}"""
    deploy_status = """${sh(
                            returnStatus: true,
                            script: "ansible-playbook -i ansible/${environment}-hosts\
                             ansible/${repository}.yml")}"""
  }

  if (deploy_status != "0") {
    currentBuild.result = 'FAILURE'
    deploy.put('status', 'Failed')
  } else {
    currentBuild.result = 'SUCCESS'
    deploy.put('status', 'Success')
  }
}

def call(Map pipelineParams) {

    ''' Main deployer method '''

	environment = "${pipelineParams.environment}"
  repository = "${pipelineParams.repository}"
  deploy = [:]

	deployEnv(
            environment: "${environment}",
            repository: "${repository}"
  )
    return deploy   
}
return this
