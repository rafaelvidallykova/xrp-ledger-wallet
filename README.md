# XRP Ledger Wallet
A Python CLI crypto wallet to interact with the **XRP Ledger** network.
This tool allows you to create a wallet, check the wallet information, send XRP from a wallet and delete an account, all from the CLI.

## Features
- Generate valid XRP wallets (seed, keys, address)
- Check wallet info via the XRP Ledger
- Send XRP to other accounts (with destination tag support)
- Delete accounts and recover remaining funds
- Built using the official `xrpl-py` Python SDK

## Getting Started
### Requirements
- Python 3.8+
- `xrpl-py` Python package

### Installation
1. Download the tool
`git clone https://github.com/your-username/xrp-ledger-wallet.git && cd xrp-ledger-wallet`

2. Install requirements
`pip install -r requirements.txt`

### Run the Wallet
`python3 main.py`

## Warnings
- This wallet connects to the **mainnet** by default. Use with caution.
- Always backup your seed phrase carefully as it grants total access to the wallet. **Loss of the seed means not being able to withdraw funds from the wallet.**
- Do not send XRP unless you fully understand how the XRP Ledger network works.
- Account deletion is permanent. Remaining funds are transferred to another address.

## License
MIT - see [LICENSE](LICENSE) for details.

## Author
Created by **Rafael Vidal Lykova**
Feel free to fork, use, and contribute!
