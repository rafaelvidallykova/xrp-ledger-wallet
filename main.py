"""
XRP Ledger Wallet CLI Tool
Author: Rafael Vidal Lykova
Description: Create, manage, and delete XRP Ledger accounts from the terminal.
"""

import xrpl
from os import system, name

mainnet_url = 'https://xrplcluster.com/'

def cls():
    if (name == 'nt'):
        system('cls')

    else:
        system('clear')

def create_account():
    new_wallet = xrpl.wallet.Wallet.create()

    secret = new_wallet.seed
    public_key = new_wallet.public_key
    private_key = new_wallet.private_key
    classic_address = new_wallet.classic_address

    return new_wallet, secret, public_key, private_key, classic_address

def get_account_info(address):
    try:
        client = xrpl.clients.JsonRpcClient(mainnet_url)
        acct_info = xrpl.models.requests.account_info.AccountInfo(
            account=address,
            ledger_index="validated"
        )
        response = client.request(acct_info)
        return response
    except Exception as e:
        return f"Error: {e}"

def send_xrp(seed, amount, destination, tag=None):
    try:
        sending_wallet = xrpl.wallet.Wallet.from_seed(seed)

        client = xrpl.clients.JsonRpcClient(mainnet_url)

        payment_data = {
            "account": sending_wallet.classic_address,
            "amount": xrpl.utils.xrp_to_drops(amount),
            "destination": destination,
        }
        if tag is not None:
            payment_data["destination_tag"] = tag

        payment = xrpl.models.transactions.Payment(**payment_data)

        try:
            response = xrpl.transaction.submit_and_wait(payment, client, sending_wallet)

        except Exception as e:
            response = f"Submit failed: {e}"

        return response
    except Exception as e:
        return f"Error: {e}"

def delete_wallet(seed, destination, destination_tag):
    try:
        sending_wallet = xrpl.wallet.Wallet.from_seed(seed)
        client = xrpl.clients.JsonRpcClient(mainnet_url)

        account_delete = xrpl.models.transactions.AccountDelete(
            account=sending_wallet.classic_address,
            destination=destination,
            destination_tag=destination_tag,
        )

        prepared_transaction = xrpl.transaction.autofill(account_delete, client)
        signed_transaction = xrpl.transaction.sign(prepared_transaction, sending_wallet)
        response = xrpl.transaction.submit_and_wait(signed_transaction, client)

        return response.result
    except Exception as e:
        return f"AccountDelete failed: {e}"

def main():
    cls()
    print('--- XRP LEDGER WALLET ---\n')
    print('1 - Create New Wallet')
    print('2 - Check Wallet Information')
    print('3 - Send XRP From A Wallet')
    print('4 - Delete Account And Send Funds To An Other Address\n')

    try:
        option = input('User => ').strip()

        if (option == '1'):
            cls()
            wallet = create_account()
            print('--- ACCOUNT CREATED ---')
            print(f'SEED PHRASE: {wallet[1]}')
            print(f'PUBLIC KEY: {wallet[2]}')
            print(f'PRIVATE KEY: {wallet[3]}')
            print(f'CLASSIC ADDRESS: {wallet[4]}')
            print('--- SAVE ALL OF THIS DATA OR ELSE YOU WON\'T BE ABLE TO INTERACT WITH THE WALLET ---')
            input('Press enter to continue')

        elif (option == '2'):
            cls()
            address = input('Enter wallet CLASSIC ADDRESS: ')
            cls()
            data = get_account_info(address)
            print('--- WALLET INFORMATION ---')
            print(data)
            input('Press enter to continue')

        elif (option == '3'):
            cls()
            print('--- SEND XRP ---')
            seed = input('Enter Wallet SEED: ')
            try:
                amount = float(input('Enter XRP Amount To Send: '))
            except ValueError:
                print("Invalid amount.")
                return
            destination = input('Enter Destination Address: ')
            use_tag = input('Would you like to add a TAG Y/N: ')
            if (use_tag == 'Y') or (use_tag == 'y'):
                tag = int(input('Enter Destination Tag: '))
            else:
                tag = None
                print('Caution: Only send transactions without a tag to unique wallets, else your funds may be lost')
                
            input('Press enter to proceed, or CTRL+C to exit the wallet and retry')

            transaction = send_xrp(seed, amount, destination, tag)
            print(f'\nTransaction Results: {transaction}')
            input('Press enter to continue')

        elif (option == '4'):
            cls()
            print('--- DELETE ACCOUNT ---')
            seed = input('Enter Wallet SEED: ')
            destination = input('Enter Destination Address: ')
            use_tag = input('Would you like to add a TAG Y/N: ')
            if (use_tag == 'Y') or (use_tag == 'y'):
                tag = int(input('Enter Destination Tag: '))
            else:
                tag = None
                print('Caution: Only send transactions without a tag to unique wallets, else your funds may be lost')

            input('Press enter to proceed, or CTRL+C to exit the wallet and retry')

            transaction = delete_wallet(seed, destination, tag)
            print(f'\nTransaction Results: {transaction}')
            input('Press enter to continue')
    except Exception as e:
        print(f"Unexpected error: {e}")
        input("Press enter to continue.")

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("\nExiting wallet.")

