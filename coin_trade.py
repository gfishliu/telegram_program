from web3 import Web3
import requests, json
import time
import random
from decimal import Decimal, DecimalException


panabi = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))

bscAPIkey="AE34ZSB5AWK6TZ99RRP1NGDU3P9GGURUKH"
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

address = {
'bnb' : '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c',
'busd': '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56'
}

bnb_pool_addr = web3.toChecksumAddress("0x58f876857a02d6762e0101bb5c46a8c1ed44dc16")
contract_bnb_bsc = web3.eth.contract(address = address['bnb'], abi = GetABI(address['bnb'])) #绑定合约地址
contract_busd_bsc = web3.eth.contract(address = address['busd'], abi = GetABI(address['busd'])) #绑定合约地址

def get_bnb_price():
	bnb_amount=contract_bnb_bsc.functions.balanceOf(web3.toChecksumAddress(bnb_pool_addr)).call() #查询指定地址的token数量
	busd_amount=contract_busd_bsc.functions.balanceOf(web3.toChecksumAddress(bnb_pool_addr)).call() #查询指定地址的token数量

	bnb_price = Decimal(busd_amount) / Decimal(bnb_amount)
	return bnb_price

def get_token_price(token_addr, token_pool_addr):
	contract_token_bsc=web3.eth.contract(address = web3.toChecksumAddress(token_addr), abi = GetABI(token_addr))

	token_pool_bnb_amount= contract_bnb_bsc.functions.balanceOf(web3.toChecksumAddress(token_pool_addr)).call()
	token_pool_token_amount= contract_token_bsc.functions.balanceOf(web3.toChecksumAddress(token_pool_addr)).call()
	token_price = Decimal(token_pool_bnb_amount) / Decimal(token_pool_token_amount) * bnb_price
	return token_price

def buy_token(sender_address, private_key, token_addr, buy_amount):
	panRouterContractAddress = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
	pancake_contract = web3.eth.contract(address=panRouterContractAddress, abi=panabi)
	nonce = web3.eth.get_transaction_count(sender_address)
	token_addr = web3.toChecksumAddress(token_addr)  #wbnb contract
	bnb_addr = web3.toChecksumAddress("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")  #wbnb contract
	pancakeswap2_txn = pancake_contract.functions.swapExactETHForTokens(
		10000000000, # set to 0, or specify minimum amount of tokeny you want to receive - consider decimals!!!
		[bnb_addr,token_addr],
		sender_address,
		(int(time.time()) + 10000)
		).buildTransaction({
		'from': sender_address,
		'value': web3.toWei(buy_amount,'ether'),#This is the Token(BNB) amount you want to Swap from
		'gas': 1500000,
		'gasPrice': web3.toWei('5','gwei'),
		'nonce': nonce,
	})
    
	signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=private_key)
	tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_token
	#print("购买者，数量, 哈希：", sender_address, buy_amount, web3.toHex(tx_token))


def sell_token(sender_address, private_key, token_addr, sell_ratio):
	bnb_addr = web3.toChecksumAddress("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")  #wbnb contract
	panRouterContractAddress = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
	pancake_contract = web3.eth.contract(address=panRouterContractAddress, abi=panabi)
	token_addr = web3.toChecksumAddress(token_addr)  

	#Create token Instance for Token
	contract_token_bsc=web3.eth.contract(address = web3.toChecksumAddress(token_addr), abi = GetABI(token_addr))
	#Get Token Balance
	token_amount = contract_token_bsc.functions.balanceOf(web3.toChecksumAddress(sender_address)).call()
	#print(web3.fromWei(balance,'ether'))

	#Enter amount of token to sell
	token_amount = int(token_amount/10*sell_ratio)
	"""
	#Approve Token before Selling
	tokenValue2 = web3.fromWei(token_amount, 'ether')
	start = time.time()
	approve = contract_token_bsc.functions.approve(panRouterContractAddress, token_amount).buildTransaction({
		    'from': sender_address,
		    'gasPrice': web3.toWei('5','gwei'),
		    'nonce': web3.eth.get_transaction_count(sender_address),
		    })

	signed_txn = web3.eth.account.sign_transaction(approve, private_key=private_key)
	tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
	print("Approved: " + web3.toHex(tx_token))

	#Wait after approve 10 seconds before sending transaction
	time.sleep(10)
	print(f"Swapping {tokenValue2} {symbol} for BNB")
	#Swaping exact Token for ETH 
	"""

	pancakeswap2_txn = pancake_contract.functions.swapExactTokensForETH(
		    token_amount,0, 
		    [token_addr, bnb_addr],
		    sender_address,
		    (int(time.time()) + 1000000)

		    ).buildTransaction({
		    'from': sender_address,
		    'gasPrice': web3.toWei('5','gwei'),
		    'nonce': web3.eth.get_transaction_count(sender_address),
		    })
	    
	signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=private_key)
	tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_token

