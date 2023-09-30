const WETH = artifacts.require("WrappedETH")
const TMToken = artifacts.require("TestMyToken")
const TMT = artifacts.require('TestMyTokenFactory');

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
        const accounts = await web3.eth.getAccounts()
        const token = await TMToken.deployed()

        await token.approve(tmt.address, 500, {from: accounts[0]})

        await tmt.sell(250, {
            from: accounts[0]
        })

        const balance = await tmt.tokenBalance(accounts[0])

        assert.equal(balance.toNumber(), 250)
    })
})