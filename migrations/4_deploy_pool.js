const LiquidityPool = artifacts.require('LiquidityPool');
const TMTFactory = artifacts.require('TestMyTokenFactory');
const WETHFactory = artifacts.require('WETHFactory');

module.exports = (deployer) => {
    const weth = WETHFactory.deployed().then((weth) => {return weth.token()})
    const tmt = TMTFactory.deployed().then((tmt) => {return tmt.token()})
    deployer.deploy(LiquidityPool, weth, tmt);
};