#!/usr/bin/env groovy

"""
.. module:: Testing
     :platform: Jenkins
     :synopsis: Trigger tests.
.. moduleauthor::
     :Nickname: nebul4ck
     :mail: a.gonzalezmesas@gmail.com
     :Web : https://github.com/nebul4ck/devops-engineer/tree/master/jenkins
"""

def call(Map pipelineParams) {
        
      ''' Main build method '''

      def FILE = new File("${JENKINS_HOME}" + "/workspace/" + "${env.JOB_BASE_NAME}" + "/testing.sh")
      LIST = new String[2]
      date = "${pipelineParams.date}"

      if (FILE.exists()) {
          println '################### STARTING TESTS #######################'
          testing_status = """${sh(
                          returnStatus: true,
                          script: "./testing.sh ${date}")}"""  
          LIST[0] = 'Success'  
      } else {
          println '****This project have not tests for Jenkins****'
          LIST[0] = 'No tests'
          testing_status = "0"
      }
                      
      if (testing_status != "0") {
              currentBuild.result = 'FAILURE'
              /* TODO: test report history */
              BOOL = new File("${env.JENKINS_HOME}" + "/workspace/" + "${env.JOB_BASE_NAME}" + \
                                "/results/Reports" + "${date}" + "/html/overview-summary.html").exists()

      } else {
              currentBuild.result = 'SUCCESS'
              BOOL = new File("${env.JENKINS_HOME}" + "/workspace/" + "${env.JOB_BASE_NAME}" + \
                                "/results/Reports" + "${date}" + "/html/overview-summary.html").exists()                
      }
      // workaround to fix toString class doesn't works in Jenkins
      if (BOOL==true) {
        LIST[1]='true'          
      } else {
        LIST[1]='false'
      }
      return LIST
  }
return this
