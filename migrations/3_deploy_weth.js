const WETH = artifacts.require('WrappedETH');

module.exports = (deployer) => {
    deployer.deploy(WETH);
};
