def mensagemResult = ''
def tagName = 'betonr/worker-finance:build-' + currentBuild.number

env.tagName = tagName

def checkoutProject() {
    stage('checkout') {
        checkout([
            $class: 'GitSCM',
            branches: [[name: '${ghprbActualCommit}']],
            doGenerateSubmoduleConfigurations: false,
            extensions: [],
            gitTool: 'Default',
            submoduleCfg: [],
            userRemoteConfigs: [[
                name: 'origin',
                refspec: '+refs/pull/*:refs/remotes/origin/pr/*',
                url: 'https://github.com/betonr/api-lucas.git'
            ]]
        ])
    }
}

def prepareEnvironment() {
    stage('prepare-environment') {
        sh 'docker run --name postgres-test -p 5432:5432 -d -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres mdillon/postgis'
        sh 'docker build --tag ${tagName} -f docker/Dockerfile .'
    }
}

def unittest() {
    stage('unittest') {
        sh 'docker run --rm -i -v $(pwd):/app --name api_lucas_test --net host ${tagName} bash -c ./run-test.sh'
    }
}

def notifySlack(String buildStatus = 'STARTED', String mensagem = '') {
    buildStatus = buildStatus ?: 'SUCCESS'

    def color

    if (buildStatus == 'STARTED') {
        color = '#D4DADF'
        mensagem = mensagem ?: 'Iniciado'
    } else if (buildStatus == 'SUCCESS') {
        color = '#BDFFC3'
        mensagem = mensagem ?: 'Finalizado'
    } else if (buildStatus == 'UNSTABLE') {
        color = '#FFFE89'
        mensagem = mensagem ?: 'Travado'
    } else {
        color = '#FF9FA1'
        mensagem = mensagem ?: 'Erro'
    }

    def msg = "${buildStatus}: `${env.JOB_NAME}` #${env.BUILD_NUMBER}:\n${env.BUILD_URL}\n${mensagem}"

    echo "${env}"

    slackSend(color: color, message: msg)
}

def cleanEnvironment() {
    sh 'docker stop postgres-test'
    sh 'docker rm postgres-test'
    sh 'docker rmi ${tagName} || exit 0'
}

node("ubuntu-16.04"){
    try {
        checkoutProject()
        notifySlack()

        prepareEnvironment()

        unittest()

    } catch (e) {
        currentBuild.result = 'FAILURE'
        mensagemResult = e.toString()
        throw e
    } finally {
        notifySlack(currentBuild.result, mensagemResult)
        cleanEnvironment()
    }
}