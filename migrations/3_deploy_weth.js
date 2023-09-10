const WETHFactory = artifacts.require('WETHFactory');

module.exports = (deployer) => {
    deployer.deploy(WETHFactory);
};