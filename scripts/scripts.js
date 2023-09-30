const LiquidityPool = artifacts.require('LiquidityPool');
const WETHFactory = artifacts.require('WrappedETH');

module.exports = () => {
    async function createDeposit() {
        const liquidityPool = await LiquidityPool.deployed()
        const weth = await WETHFactory.deployed()
        
        let accounts = await web3.eth.getAccounts()
        console.log("Account: ", accounts[0])
        const tx = await weth.deposit({
            from: accounts[0],
            value: '1000'
        });

        let balanceFactory = await web3.eth.getBalance(weth.address)
        console.log(balanceFactory)
        let balanceAcc = await web3.eth.getBalance(accounts[0])
        console.log(balanceAcc)
        const balanceWETH = await weth.balanceOf.call(accounts[0]);
        console.log(balanceWETH.toString())

        console.log(weth)
        let res = await liquidityPool.createDeposit(weth.address, 100, {from: accounts[0]})
        console.log(res)
    }
    createDeposit()
}
