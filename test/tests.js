const WETH = artifacts.require("WrappedETH")
const TMToken = artifacts.require("TestMyToken")
const TMT = artifacts.require('TestMyTokenFactory')
const LiquidityPool = artifacts.require('LiquidityPool');

contract("WrappedETH Test", async () => {
    it("Wrap ethers", async () => {
        const weth = await WETH.deployed()
        const accounts = await web3.eth.getAccounts()

        await weth.deposit({
            from: accounts[0],
            value: '1000000'
        })

        const balance = await weth.balanceOf(accounts[0])

        assert.equal(balance.toNumber(), 1000000)
    })

    it("Withdraw ethers", async () => {
        const weth = await WETH.deployed()
        const accounts = await web3.eth.getAccounts()

        await weth.withdraw(1000000, {
            from: accounts[0]
        })

        const balance = await weth.balanceOf(accounts[0])

        assert.equal(balance.toNumber(), 0)
    })
})

contract("MyToken Test", async () => {
    it("Buying tokens", async () => {
        const tmt = await TMT.deployed()
        const accounts = await web3.eth.getAccounts()

        await tmt.sendTransaction({
            from: accounts[0],
            value: 500
        })

        const balance = await tmt.tokenBalance({from: accounts[0]})

        assert.equal(balance.toNumber(), 500)
    })

    it("Selling tokens", async () => {
        const tmt = await TMT.deployed()
        const tokenInstance = await tmt.token()
            .then((token) => {return TMToken.at(token)})
        const accounts = await web3.eth.getAccounts()
        
        await tokenInstance.approve(tmt.address, 250, {from: accounts[0]})
        await tmt.sell(250, {from: accounts[0]})
        
        const balance = await tokenInstance.balanceOf(accounts[0]).then((balance) => {return balance.toNumber()})
        
        assert.equal(balance, 250)
    })
})

contract("Liquidity Pool", async () => {
    it("Create deposit", async () => {
        const pool = await LiquidityPool.deployed()
        const tokenInstance = await TMT.deployed()
            .then((tmt) => {return tmt.token()})
            .then((token) => {return TMToken.at(token)})
        const accounts = await web3.eth.getAccounts()

        await TMT.deployed().then((tmt) => {
            tmt.sendTransaction({
                from: accounts[0],
                value: 500
            })
        })

        await tokenInstance.approve(pool.address, 100, {from: accounts[0]})
        const createdPool = await pool.createDeposit.call(tokenInstance.address, 100, {from: accounts[0]})
        
        assert.isTrue(createdPool)
    })
})