from web3 import Web3
import json
from decimal import *
import requests

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))

#connecting web3 to Ganache
if  web3.isConnected() == True:
    print("web3 connected...\n")
else :
    print("error connecting...")

bscAPIkey=""
DEBUG=False

#有bug的发送token代码
def GetABI (Address):
    if DEBUG:
        url_eth = "https://api-testnet.bscscan.com/api"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # This is chrome, you can set whatever browser you like
        API_ENDPOINT = url_eth+"?module=contract&action=getabi&address="+str(Address)+"&apikey="+bscAPIkey
        resp = requests.get(url = API_ENDPOINT, headers=headers)
    else:
        url_eth = "https://api.bscscan.com/api"
        API_ENDPOINT = url_eth+"?module=contract&action=getabi&address="+str(Address)+"&apikey="+bscAPIkey
        resp = requests.get(url = API_ENDPOINT)

    res = json.loads(resp.text)
    status = int(res['status'])
    if status:
        response = resp.json()
        abi=json.loads(response["result"])
        return abi
    else:
        return False

def send_bnb(sender, receiver, private_key, balance=0.0003):
    nonce = web3.eth.getTransactionCount(sender)
    txbnb = {
        'nonce':nonce,
        'to':receiver,
        'value':web3.toWei(balance,'ether'),
        'gas':21000,
        'gasPrice':web3.toWei('5','gwei')
    }

	#sign transaction with private key
    signed_tx = web3.eth.account.signTransaction(txbnb,private_key)

	#send Transaction
    tx_hash= web3.eth.sendRawTransaction(signed_tx.rawTransaction)
	#print("send bnb success! sender, receiver,amount:", sender, receiver, balance)
    return tx_hash


#send_bnb("0x9A5d605f", "0x25B03909B", "0xd168222d59550ded8", 0.0004)


def send_token(sender, receiver, private_key, token_addr, tx_amount):
    contract_bsc_addr = web3.toChecksumAddress(token_addr)
    contract_bsc = web3.eth.contract(address = contract_bsc_addr, abi = GetABI(contract_bsc_addr)) #绑定合约地址
    #tx_amount=100
    nonce = web3.eth.getTransactionCount(sender)
    contract_method_transferToken = contract_bsc.functions.transfer(web3.toChecksumAddress(receiver), tx_amount)
    contract_method_transferToken_build_tx = contract_method_transferToken.buildTransaction({
        'nonce': nonce,
        'gas': 40000,
        'gasPrice': web3.toWei('5', 'gwei'),
    })
    bsc_sign_tx_transferToken = web3.eth.account.signTransaction(contract_method_transferToken_build_tx, private_key = private_key)  #private指定发送人
    bscTxHash = web3.eth.sendRawTransaction(bsc_sign_tx_transferToken.rawTransaction)
    return bscTxHash

#send_token_from_contract_in_bsc(receiver4, token_gas, str(gasprice), bsc_Nonce, tx_amount)
