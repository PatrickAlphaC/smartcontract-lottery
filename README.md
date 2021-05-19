# SmartContract Lottery

This is a repo to work with and create a truely random smart contract lottery in a python environment. If you're brand new to solidity, be sure to check out [FreeCodeCamp](https://www.freecodecamp.org/news/tag/solidity/). If you're new to brownie, check out the [Brownie](https://eth-brownie.readthedocs.io/en/stable/) documentation.  If you're brand new to Chainlink, check out the beginner walkthroughs in remix to [learn the basics.](https://docs.chain.link/docs/beginners-tutorial)

## Prerequisites

Please install or have installed the following:

- [nodejs and npm](https://nodejs.org/en/download/)
- [python](https://www.python.org/downloads/)

## Installation

1. [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html), if you haven't already. Here is a simple way to install brownie.

```bash
pip install eth-brownie
```
Or, if that doesn't work, via pipx
```bash
pip install --user pipx
pipx ensurepath
# restart your terminal
pipx install eth-brownie
```

2. [Install ganache-cli](https://www.npmjs.com/package/ganache-cli)

```bash
npm install -g ganache-cli
```

3. Download the mix and install dependancies. 

```bash
git clone https://github.com/PatrickAlphaC/smartcontract-lottery
cd smartcontract-lottery
pip install -r requirements.txt
```

### Environment Variables

If you want to be able to deploy to testnets, set the following environment variables. You can [learn more about setting environment variables from this linked Twilio blog.](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html) 

- `WEB3_INFURA_PROJECT_ID`: Your project ID from [Infura](https://infura.io/). You can signup to get a free key. You can [follow this guide](https://ethereumico.io/knowledge-base/infura-api-key-guide/) to getting a project key.
- `PRIVATE_KEY`: From your ethereum wallet like [metamask](https://metamask.io/). You can follow [this guide](https://metamask.zendesk.com/hc/en-us/articles/360015289632-How-to-Export-an-Account-Private-Key) to get your private key. Just note, if pulling from metamask, you will have to append an `0x` to the start, like so: `0xasfasdfasdfasfsa`

You can add your environment variables to the `.env` file:

```
export WEB3_INFURA_PROJECT_ID=<PROJECT_ID>
export PRIVATE_KEY=<PRIVATE_KEY>
```

AND THEN RUN `source .env` to activate them. 
You'll need to do this everytime you open a new terminal, or [learn how to set them easier](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html)


Otherwise, you can build, test, and deploy on your local environment. 

## Deploy to a testnet / Scripts

```
brownie run scripts/1_deploy_lottery.py
brownie run scripts/2_start_lottery.py
brownie run scripts/3_enter_lottery.py
brownie run scripts/4_end_lottery.py
```
This will deploy your lottery, fund it with LINK, start your lottery, you'll enter it, and then end your lottery. You can also work with the console to do these. 

You can deploy and work with a local network by deploying mocks. 
## Testing

There are 2 types of tests in this project. 

- unit tests, which run on a local blockchain.
- integration tests, which run on a testnet

To run the unit tests:
```
brownie test
```
integration tests:
```
brownie test --network <network>
```

For more information on effective testing with Chainlink, check out [Testing Smart Contracts](https://blog.chain.link/testing-chainlink-smart-contracts/)

Tests are really robust here! They work for local development and testnets. There are a few key differences between the testnets and the local networks. We utilize mocks so we can work with fake oracles on our testnets. 

### To test development / local
```bash
brownie test
```
### To test mainnet-fork
This will test the same way as local testing, but you will need a connection to a mainnet blockchain (like with the infura environment variable.)
```bash
brownie test --network mainnet-fork
```
### To test a testnet
Kovan and Rinkeby are currently supported
```bash
brownie test --network kovan
```

## Adding additional Chains

If the blockchain is EVM Compatible, adding new chains can be accomplished by something like:

```
brownie networks add Ethereum binance-smart-chain host=https://bsc-dataseed1.binance.org chainid=56
```
or, for a fork: 

```
brownie networks add development binance-fork cmd=ganache-cli host=http://127.0.0.1 fork=https://bsc-dataseed1.binance.org accounts=10 mnemonic=brownie port=8545
```

## Linting

```
pip install black 
pip install autoflake
autoflake --in-place --remove-unused-variables -r .
black .
```

## Resources

To get started with Brownie:

* [Chainlink Documentation](https://docs.chain.link/docs)
* Check out the [Chainlink documentation](https://docs.chain.link/docs) to get started from any level of smart contract engineering. 
* Check out the other [Brownie mixes](https://github.com/brownie-mix/) that can be used as a starting point for your own contracts. They also provide example code to help you get started.
* ["Getting Started with Brownie"](https://medium.com/@iamdefinitelyahuman/getting-started-with-brownie-part-1-9b2181f4cb99) is a good tutorial to help you familiarize yourself with Brownie.
* For more in-depth information, read the [Brownie documentation](https://eth-brownie.readthedocs.io/en/stable/).


Any questions? Join our [Discord](https://discord.gg/2YHSAey)

## License

This project is licensed under the [MIT license](LICENSE).
