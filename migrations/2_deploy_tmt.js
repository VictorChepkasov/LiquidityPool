const TMTFactory = artifacts.require('TestMyTokenFactory')
const TMToken = artifacts.require("TestMyToken")

module.exports = (deployer) => {
    deployer.deploy(TMTFactory)
    deployer.deploy(TMToken, TMTFactory.deployed().then((tmt) => { return tmt.address }))
};