const LiquidityPool = artifacts.require('LiquidityPool');
const TMTFactory = artifacts.require('TestMyTokenFactory');
const WETHFactory = artifacts.require('WETHFactory');

module.exports = async (deployer) => {
    const weth = await WETHFactory.deployed().then((weth) => {return weth})
    const tmt = await TMTFactory.deployed().then((tmt) => {return tmt})
    await deployer.deploy(LiquidityPool, weth.token(), tmt.token());
};