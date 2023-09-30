const LiquidityPool = artifacts.require('LiquidityPool');
const TMTFactory = artifacts.require('TestMyTokenFactory');
const WETH = artifacts.require('WrappedETH');

module.exports = async (deployer) => {
    const weth = await WETH.deployed().then((weth) => {return weth})
    const tmt = await TMTFactory.deployed().then((tmt) => {return tmt})
    await deployer.deploy(LiquidityPool, weth.address, tmt.token());
};