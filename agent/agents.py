import json
from swarm import Agent
from cdp import *
from typing import List, Dict, Any
import os
from openai import OpenAI
from decimal import Decimal
from typing import Union
from web3 import Web3
from web3.exceptions import ContractLogicError
from cdp.errors import ApiError, UnsupportedAssetError
import requests
from twitter_utils import TwitterBot

# Get configuration from environment variables
API_KEY_NAME = os.environ.get("CDP_API_KEY_NAME")
PRIVATE_KEY = os.environ.get("CDP_PRIVATE_KEY", "").replace('\\n', '\n')
MORALIS_API_KEY = os.environ.get("MORALIS_API_KEY")
TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")

# Configure CDP with environment variables
Cdp.configure(API_KEY_NAME, PRIVATE_KEY)

# Create a new wallet on the Base Sepolia testnet
# You could make this a function for the agent to create a wallet on any network
# If you want to use Base Mainnet, change Wallet.create() to Wallet.create(network_id="base-mainnet")
# see https://docs.cdp.coinbase.com/mpc-wallet/docs/wallets for more information
agent_wallet = Wallet.create()

# NOTE: the wallet is not currently persisted, meaning that it will be deleted after the agent is stopped. To persist the wallet, see https://docs.cdp.coinbase.com/mpc-wallet/docs/wallets#developer-managed-wallets
# Here's an example of how to persist the wallet:
# WARNING: This is for development only - implement secure storage in production!

# # Export wallet data (contains seed and wallet ID)
# wallet_data = agent_wallet.export_data()
# wallet_dict = wallet_data.to_dict()

# # Example of saving to encrypted local file
# file_path = "wallet_seed.json"
# agent_wallet.save_seed(file_path, encrypt=True)
# print(f"Seed for wallet {agent_wallet.id} saved to {file_path}")

# # Example of loading a saved wallet:
# # 1. Fetch the wallet by ID
# fetched_wallet = Wallet.fetch(wallet_id)
# # 2. Load the saved seed
# fetched_wallet.load_seed("wallet_seed.json")

# Example of importing previously exported wallet data:
# imported_wallet = Wallet.import_data(wallet_dict)

# Request funds from the faucet (only works on testnet)
faucet = agent_wallet.faucet()
print(f"Faucet transaction: {faucet}")
print(f"Agent wallet address: {agent_wallet.default_address.address_id}")


# Function to create a new ERC-20 token
def create_token(name, symbol, initial_supply):
    """
    Create a new ERC-20 token.
    
    Args:
        name (str): The name of the token
        symbol (str): The symbol of the token
        initial_supply (int): The initial supply of tokens
    
    Returns:
        str: A message confirming the token creation with details
    """
    deployed_contract = agent_wallet.deploy_token(name, symbol, initial_supply)
    deployed_contract.wait()
    return f"Token {name} ({symbol}) created with initial supply of {initial_supply} and contract address {deployed_contract.contract_address}"


# Function to transfer assets
def transfer_asset(amount, asset_id, destination_address):
    """
    Transfer an asset to a specific address.
    
    Args:
        amount (Union[int, float, Decimal]): Amount to transfer
        asset_id (str): Asset identifier ("eth", "usdc") or contract address of an ERC-20 token
        destination_address (str): Recipient's address
    
    Returns:
        str: A message confirming the transfer or describing an error
    """
    try:
        # Check if we're on Base Mainnet and the asset is USDC for gasless transfer
        is_mainnet = agent_wallet.network_id == "base-mainnet"
        is_usdc = asset_id.lower() == "usdc"
        gasless = is_mainnet and is_usdc

        # For ETH and USDC, we can transfer directly without checking balance
        if asset_id.lower() in ["eth", "usdc"]:
            transfer = agent_wallet.transfer(amount,
                                             asset_id,
                                             destination_address,
                                             gasless=gasless)
            transfer.wait()
            gasless_msg = " (gasless)" if gasless else ""
            return f"Transferred {amount} {asset_id}{gasless_msg} to {destination_address}"

        # For other assets, check balance first
        try:
            balance = agent_wallet.balance(asset_id)
        except UnsupportedAssetError:
            return f"Error: The asset {asset_id} is not supported on this network. It may have been recently deployed. Please try again in about 30 minutes."

        if balance < amount:
            return f"Insufficient balance. You have {balance} {asset_id}, but tried to transfer {amount}."

        transfer = agent_wallet.transfer(amount, asset_id, destination_address)
        transfer.wait()
        return f"Transferred {amount} {asset_id} to {destination_address}"
    except Exception as e:
        return f"Error transferring asset: {str(e)}. If this is a custom token, it may have been recently deployed. Please try again in about 30 minutes, as it needs to be indexed by CDP first."


# Function to get the balance of a specific asset
def get_balance(asset_id):
    """
    Get the balance of a specific asset in the agent's wallet.
    
    Args:
        asset_id (str): Asset identifier ("eth", "usdc") or contract address of an ERC-20 token
    
    Returns:
        str: A message showing the current balance of the specified asset
    """
    balance = agent_wallet.balance(asset_id)
    return f"Current balance of {asset_id}: {balance}"


# Function to request ETH from the faucet (testnet only)
def request_eth_from_faucet():
    """
    Request ETH from the Base Sepolia testnet faucet.
    
    Returns:
        str: Status message about the faucet request
    """
    if agent_wallet.network_id == "base-mainnet":
        return "Error: The faucet is only available on Base Sepolia testnet."

    faucet_tx = agent_wallet.faucet()
    return f"Requested ETH from faucet. Transaction: {faucet_tx}"


# Contract addresses for Basenames
BASENAMES_REGISTRAR_CONTROLLER_ADDRESS_MAINNET = "0x4cCb0BB02FCABA27e82a56646E81d8c5bC4119a5"
BASENAMES_REGISTRAR_CONTROLLER_ADDRESS_TESTNET = "0x49aE3cC2e3AA768B1e5654f5D3C6002144A59581"
L2_RESOLVER_ADDRESS_MAINNET = "0xC6d566A56A1aFf6508b41f6c90ff131615583BCD"
L2_RESOLVER_ADDRESS_TESTNET = "0x6533C94869D28fAA8dF77cc63f9e2b2D6Cf77eBA"


# Function to create registration arguments for Basenames
def create_register_contract_method_args(base_name: str, address_id: str,
                                         is_mainnet: bool) -> dict:
    """
    Create registration arguments for Basenames.
    
    Args:
        base_name (str): The Basename (e.g., "example.base.eth" or "example.basetest.eth")
        address_id (str): The Ethereum address
        is_mainnet (bool): True if on mainnet, False if on testnet
    
    Returns:
        dict: Formatted arguments for the register contract method
    """
    w3 = Web3()

    resolver_contract = w3.eth.contract(abi=l2_resolver_abi)

    name_hash = w3.ens.namehash(base_name)

    address_data = resolver_contract.encode_abi("setAddr",
                                                args=[name_hash, address_id])

    name_data = resolver_contract.encode_abi("setName",
                                             args=[name_hash, base_name])

    register_args = {
        "request": [
            base_name.replace(".base.eth" if is_mainnet else ".basetest.eth",
                              ""),
            address_id,
            "31557600",  # 1 year in seconds
            L2_RESOLVER_ADDRESS_MAINNET
            if is_mainnet else L2_RESOLVER_ADDRESS_TESTNET,
            [address_data, name_data],
            True
        ]
    }

    return register_args


# Function to register a basename
def register_basename(basename: str, amount: float = 0.002):
    """
    Register a basename for the agent's wallet.
    
    Args:
        basename (str): The basename to register (e.g. "myname.base.eth" or "myname.basetest.eth")
        amount (float): Amount of ETH to pay for registration (default 0.002)
    
    Returns:
        str: Status message about the basename registration
    """
    address_id = agent_wallet.default_address.address_id
    is_mainnet = agent_wallet.network_id == "base-mainnet"

    suffix = ".base.eth" if is_mainnet else ".basetest.eth"
    if not basename.endswith(suffix):
        basename += suffix

    register_args = create_register_contract_method_args(
        basename, address_id, is_mainnet)

    try:
        contract_address = (BASENAMES_REGISTRAR_CONTROLLER_ADDRESS_MAINNET
                            if is_mainnet else
                            BASENAMES_REGISTRAR_CONTROLLER_ADDRESS_TESTNET)

        invocation = agent_wallet.invoke_contract(
            contract_address=contract_address,
            method="register",
            args=register_args,
            abi=registrar_abi,
            amount=amount,
            asset_id="eth",
        )
        invocation.wait()
        return f"Successfully registered basename {basename} for address {address_id}"
    except ContractLogicError as e:
        return f"Error registering basename: {str(e)}"
    except Exception as e:
        return f"Unexpected error registering basename: {str(e)}"

def get_token_metadata(token_address: str) -> str:
    """
    Fetch metadata for an ERC-20 token using the Moralis API.
    Automatically determines if the network is mainnet or testnet.

    Args:
        token_address (str): The address of the ERC-20 token

    Returns:
        str: A message with the token metadata or an error message if unsuccessful
    """
    # Read the Moralis API key from the environment
    if not MORALIS_API_KEY:
        return "Error: Moralis API key is missing. Please set the MORALIS_API_KEY environment variable."

    # Determine the network dynamically based on the agent's current network ID
    is_mainnet = agent_wallet.network_id in ["base", "base-mainnet"]
    chain = "base" if is_mainnet else "base sepolia"

    # API endpoint and headers
    url = "https://solana-gateway.moralis.io/token/mainnet/"+token_address+"/metadata"
    headers = {
        "accept": "application/json",
        "X-API-Key": MORALIS_API_KEY
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        metadata = response.json()

        if metadata:
            return (
                f"Token Name: {metadata.get('name')}\n"
                f"Symbol: {metadata.get('symbol')}\n"
                f"Decimals: {metadata.get('decimals')}\n"
            )
        else:
            return "No metadata found for the provided token address."

    except requests.exceptions.RequestException as e:
        return f"Error fetching token metadata: {str(e)}"


def post_to_twitter(content: str):
    """
    Post a message to Twitter.

    Args:
        content (str): The content to tweet

    Returns:
        str: Status message about the tweet
    """
    return twitter_bot.post_tweet(content)

def get_tweets():
    """
    Get tweets.

    Returns:
        str: Formatted string of matching tweets
    """
    tweets = twitter_bot.get_tweets()
    if not tweets:
        return "No tweets found"

    result = f"Tweets:\n"
    for tweet in tweets:
        if 'error' in tweet:
            return f"Error searching tweets: {tweet['error']}"
        result += f"- {tweet['text']}\n"
    return result

# Create the Based Agent with all available functions
based_agent = Agent(
    name="Based Agent",
    instructions=
    "You are a helpful agent that can interact onchain on the Base Layer 2 using the Coinbase Developer Platform SDK. You can create tokens, transfer assets, generate art, deploy NFTs, mint NFTs, register basenames, and swap assets (on mainnet only). If you ever need to know your address, it is {agent_wallet.default_address.address_id}. If you ever need funds, you can request them from the faucet. You can also deploy your own ERC-20 tokens, NFTs, and interact with them. If someone asks you to do something you can't do, you can say so, and encourage them to implement it themselves using the CDP SDK, recommend they go to docs.cdp.coinbase.com for more informaton. You can also offer to help them implement it by writing the function and telling them to add it to the agents.py file and within your list of callable functions.",
    functions=[
        create_token,
        transfer_asset,
        get_balance,
        request_eth_from_faucet,
        register_basename,
        get_token_metadata,
        post_to_twitter,
        get_tweets
    ],
)

# add the following import to the top of the file, add the code below it, and add the new functions to the based_agent.functions list

# from twitter_utils import TwitterBot

# Initialize TwitterBot with your credentials
twitter_bot = TwitterBot(
    api_key=TWITTER_API_KEY,
    api_secret=TWITTER_API_SECRET,
    access_token=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
    bearer_token=TWITTER_BEARER_TOKEN
)

# ABIs for smart contracts (used in basename registration)
l2_resolver_abi = [{
    "inputs": [{
        "internalType": "bytes32",
        "name": "node",
        "type": "bytes32"
    }, {
        "internalType": "address",
        "name": "a",
        "type": "address"
    }],
    "name":
    "setAddr",
    "outputs": [],
    "stateMutability":
    "nonpayable",
    "type":
    "function"
}, {
    "inputs": [{
        "internalType": "bytes32",
        "name": "node",
        "type": "bytes32"
    }, {
        "internalType": "string",
        "name": "newName",
        "type": "string"
    }],
    "name":
    "setName",
    "outputs": [],
    "stateMutability":
    "nonpayable",
    "type":
    "function"
}]

registrar_abi = [{
    "inputs": [{
        "components": [{
            "internalType": "string",
            "name": "name",
            "type": "string"
        }, {
            "internalType": "address",
            "name": "owner",
            "type": "address"
        }, {
            "internalType": "uint256",
            "name": "duration",
            "type": "uint256"
        }, {
            "internalType": "address",
            "name": "resolver",
            "type": "address"
        }, {
            "internalType": "bytes[]",
            "name": "data",
            "type": "bytes[]"
        }, {
            "internalType": "bool",
            "name": "reverseRecord",
            "type": "bool"
        }],
        "internalType":
        "struct RegistrarController.RegisterRequest",
        "name":
        "request",
        "type":
        "tuple"
    }],
    "name":
    "register",
    "outputs": [],
    "stateMutability":
    "payable",
    "type":
    "function"
}]
