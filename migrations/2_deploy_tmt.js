const TMTFactory = artifacts.require('TestMyTokenFactory');

module.exports = (deployer) => {
    deployer.deploy(TMTFactory);
};