# SmartContract Lottery

This is a repo to work with and create a truely random smart contract lottery in a python environment. If you're brand new to solidity, be sure to check out [FreeCodeCamp](https://www.freecodecamp.org/news/tag/solidity/). If you're new to brownie, check out the [Brownie](https://eth-brownie.readthedocs.io/en/stable/) documentation.  If you're brand new to Chainlink, check out the beginner walkthroughs in remix to [learn the basics.](https://docs.chain.link/docs/beginners-tutorial)

- [SmartContract Lottery](#smartcontract-lottery)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Testnet Development](#testnet-development)
    - [With environment variables](#with-environment-variables)
    - [Without environment variables](#without-environment-variables)
  - [Local Development](#local-development)
  - [Deploy to a testnet / Scripts](#deploy-to-a-testnet--scripts)
  - [Testing](#testing)
    - [To test development / local](#to-test-development--local)
    - [To test mainnet-fork](#to-test-mainnet-fork)
    - [To test a testnet](#to-test-a-testnet)
  - [Adding additional Chains](#adding-additional-chains)
  - [Linting](#linting)
  - [Resources](#resources)
  - [License](#license)

## Prerequisites

Please install or have installed the following:

- [nodejs and npm](https://nodejs.org/en/download/)
- [python](https://www.python.org/downloads/)
## Installation

1. [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html), if you haven't already. Here is a simple way to install brownie.


```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
# restart your terminal
pipx install eth-brownie
```
Or, if that doesn't work, via pip
```bash
pip install eth-brownie
```

2. Download the mix and install dependancies. 

```bash
brownie bake chainlink-mix
cd chainlink-mix
pip install -r requirements.txt
```

This will open up a new Chainlink project. Or, you can clone from source:

```bash
git clone https://github.com/PatrickAlphaC/chainlink-mix
cd chainlink-mix 
```

## Testnet Development
If you want to be able to deploy to testnets, do the following. 

### With environment variables

Set your `WEB3_INFURA_PROJECT_ID`, and `PRIVATE_KEY` [environment variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html). 

You can get a `WEB3_INFURA_PROJECT_ID` by getting a free trial of [Infura](https://infura.io/). At the moment, it does need to be infura with brownie. If you get lost, you can [follow this guide](https://ethereumico.io/knowledge-base/infura-api-key-guide/) to getting a project key. You can find your `PRIVATE_KEY` from your ethereum wallet like [metamask](https://metamask.io/). 

You'll also need testnet rinkeby ETH and LINK. You can get LINK and ETH into your wallet by using the [rinkeby faucets located here](https://docs.chain.link/docs/link-token-contracts#rinkeby). If you're new to this, [watch this video.](https://www.youtube.com/watch?v=P7FX_1PePX0)

You can add your environment variables to the `.env` file:

```
export WEB3_INFURA_PROJECT_ID=<PROJECT_ID>
export PRIVATE_KEY=<PRIVATE_KEY>
```

AND THEN RUN `source .env` TO ACTIVATE THE ENV VARIABLES
(You'll need to do this everytime you open a new terminal, or [learn how to set them easier](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html))

> DO NOT SEND YOUR PRIVATE KEY WITH FUNDS IN IT ONTO GITHUB

### Without environment variables

Add your account by doing the following:
```
brownie accounts new <some_name_you_decide>
```
You'll be prompted to add your private key, and a password. 
Then, in your code, you'll want to use `load` instead of add when getting an account.
```python
account = accounts.load("some_name_you_decide")
```
Then you'll want to add your RPC_URL to the network of choice. For example:
```bash
brownie networks modify rinkeby host=https://your_url_here
```
If the network you want doesn't already exist, see [the below section](#adding-additional-chains)

Otherwise, you can build, test, and deploy on your local environment. 

## Local Development

For local testing [install ganache-cli](https://www.npmjs.com/package/ganache-cli)
```bash
npm install -g ganache-cli
```
or
```bash
yarn add global ganache-cli
```

All the scripts are designed to work locally or on a testnet. You can add a ganache-cli or ganache UI chain like so: 
```
brownie networks add Ethereum ganache host=http://localhost:8545 chainid=1337
```
And update the brownie config accordingly. There is a `deploy_mocks` script that will launch and deploy mock Oracles, VRFCoordinators, Link Tokens, and Price Feeds on a Local Blockchain. 


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
autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r .
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
