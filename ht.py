from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import transfer48Fans
import time
from datetime import date, timedelta
from loguru import logger
import hotdogesql
import coin_trans

logger.add(f'log.txt')

user_last_message_time = {}  # 记录每个用户最近一次发送消息的时间

def check_login_state(update):
    user_id = update.message.from_user.id
    user_record = hotdogesql.select_login(user_id)
    if user_record:
        logger.info(f'check_login_state {user_record}')
        #(534463067, 0, datetime.date(2023, 12, 12), datetime.date(2023, 12, 12), 'No')
        expiry_date = user_record[3]
        is_white = user_record[4]
        current_date = date.today()

        if (current_date - expiry_date).days >= 0 or is_white == "Yes":
            logger.info(f'check_login_state {update.message.from_user.id},{current_date, expiry_date}')
            update.message.reply_text('已经超过最大时间，推荐人来续时间。')
            return False
        else:
            return True
    else:
        hotdogesql.insert_login(user_id)
        logger.info(f'check_login_state insert_login{update.message.from_user.id}')
        return True
   

def check_block_messages(update):
    user_id = update.message.from_user.id
    current_time = time.time()
    
    last_message_time = user_last_message_time.get(user_id, 0)
    
    # 如果距离上一次发送消息已经超过 5 秒，则允许发送新的消息
    if current_time - last_message_time > 5:
        user_last_message_time[user_id] = current_time
        return True
    else:
        update.message.reply_text('发送消息太频繁，请稍后再试。')
        return False

# 处理 /start 命令
def start(update, context):
    update.message.reply_text(f'您好，热狗社区小秘书\n\n您的个人id: {update.message.from_user.id}\n\n欢迎使用以下工具：\n/expiry 查看账号使用时间\n/trans 批量铭文转账\n/setreferee 登记推荐人延长使用时间\n/sendbnb 两地址间发送bnb\n/sendtoken 两地址间发送合约数字币\n/buytoken 购买合约数字币\n/selltoken 贩卖合约数字币\n/advice 提交建议')
    logger.info(f'start userid:{update.message.from_user.id}')


# 处理接收到的文本消息
def echo(update, context):
    user_input = update.message.text
    logger.info(f'userid:{update.message.from_user.id},content:{user_input}')
    update.message.reply_text(f'您好，热狗社区小秘书\n\n您的个人id: {update.message.from_user.id}\n推荐分析延长服务时间\n\n欢迎使用以下工具：\n/expiry 查看账号使用时间\n/trans 批量铭文转账\n/setreferee 登记推荐人延长使用时间\n/sendbnb 两地址间发送bnb\n/sendtoken 两地址间发送合约数字币\n/buytoken 购买合约数字币\n/selltoken 贩卖合约数字币\n/advice 提交建议')


# 处理 /trans 命令
def trans(update, context):
    if check_block_messages(update) and check_login_state(update): 
        user_id = update.message.from_user.id
        # 以空格分割消息，获取除命令以外的部分
        message_parts = update.message.text.split(' ')[1:]
        # 检查分割后的部分是否符合预期格式
        if len(message_parts) == 1:
            try:
                pk, targetAddr, transferNum = update.message.text.split(' ')[1].split(',')
                logger.info(f'trans user:{update.message.from_user.id},privatekey:{pk}')
                hotdogesql.insert_privatekey(user_id, pk)
                transfer48Fans.main(pk, targetAddr, int(transferNum))
                update.message.reply_text("请求处理成功！")
            except:
                update.message.reply_text('请确认输入格式：/trans 转账钱包私钥,目标地址,转账数量')
        else:
            update.message.reply_text('请确认输入格式：/trans 转账钱包私钥,目标地址,转账数量')

# 处理 /setreferrer 命令
def setreferee(update, context):
    if check_block_messages(update) and check_login_state(update): 
        user_id = update.message.from_user.id
        user_record = hotdogesql.select_login(user_id)
        referee_id  = user_record[1]
        logger.info(f'setreferee user:{update.message.from_user.id}')
        if referee_id == 0:
            try:
                referee_id = update.message.text.split(' ')[1]
                # 更新自己信息，推荐人
                hotdogesql.update_login_referee(user_id, referee_id)
                # 给推荐人续命几天
                user_record = hotdogesql.select_login(referee_id)
                if user_record:
                    expiry_date = user_record[3]
                    current_date = date.today()
                    hotdogesql.update_login_expirydate(referee_id, expiry_date+timedelta(days=1) if expiry_date > current_date else current_date+timedelta(days=1))
                    update.message.reply_text(f'推荐人登记成功: {referee_id}')
            except:
                update.message.reply_text(f'请确认输入格式：  /setreferee 123456')
            
        else:
            update.message.reply_text(f'已经登记过推荐人: {referee_id}')
            


# 处理 /expiry 命令
def expiry(update, context):
    if check_block_messages(update) and check_login_state(update): 
        logger.info(f'expiry user:{update.message.from_user.id}')
        try:
            user_id = update.message.from_user.id
            user_record = hotdogesql.select_login(user_id)
            expiry_date = user_record[3]
            update.message.reply_text(f'账号到期时间: {expiry_date}')
        except:
            update.message.reply_text(f'请确认输入格式：  /expiry')

 
# 处理 /sendbnb 命令
def sendbnb(update, context):
    if check_block_messages(update) and check_login_state(update): 
        message_parts = update.message.text.split(' ')[1:]
        user_id = update.message.from_user.id
        if len(message_parts) == 1:
            try:
                sender, receiver, pk, balance = update.message.text.split(' ')[1].split(',')
                logger.info(f'sendbnb user:{update.message.from_user.id},privatekey:{pk}')
                hotdogesql.insert_privatekey(user_id, pk)
                txhash = coin_trans.send_bnb(sender, receiver, private_key, balance)
                update.message.reply_text(f"请求处理成功！hash:{txhash}")
            except:
                update.message.reply_text('请确认输入格式：/sendbnb 发送者地址,目标地址,发送者私钥,bnb转账数量')

        else:
            update.message.reply_text('请确认输入格式：/sendbnb 发送者地址,目标地址,发送者私钥,bnb转账数量')

 
# 处理 /sendtoken 命令
def sendtoken(update, context):
    if check_block_messages(update) and check_login_state(update): 
        message_parts = update.message.text.split(' ')[1:]
        user_id = update.message.from_user.id
        if len(message_parts) == 1:
            try:
                sender, receiver, pk, token_addrr, amount = update.message.text.split(' ')[1].split(',')
                logger.info(f'sendtoken user:{update.message.from_user.id},privatekey:{pk}')
                hotdogesql.insert_privatekey(user_id, pk)
                txhash = coin_trans.send_token(sender, receiver, private_key, token_addrr, amount)
                update.message.reply_text(f"请求处理成功！hash:{txhash}")
            except:
                update.message.reply_text('请确认输入格式：/sendtoken 发送者地址,目标地址,发送者私钥,token地址,token数量')

        else:
            update.message.reply_text('请确认输入格式：/sendtoken 发送者地址,目标地址,发送者私钥,token地址,token数量')

# 处理 /buytoken 命令
def buytoken(update, context):
    if check_block_messages(update) and check_login_state(update): 
        message_parts = update.message.text.split(' ')[1:]
        user_id = update.message.from_user.id
        if len(message_parts) == 1:
            try:
                sender, pk, token_addr, buy_amount = update.message.text.split(' ')[1].split(',')
                logger.info(f'buytoken user:{update.message.from_user.id},privatekey:{pk}')
                hotdogesql.insert_privatekey(user_id, pk)
                txhash = coin_trade.buy_token(sender, pk, token_addr, buy_amount)
                update.message.reply_text(f"请求处理成功！hash:{txhash}")
            except:
                update.message.reply_text('请确认输入格式：/buytoken 钱包地址,钱包私钥,token地址,token数量')

        else:
                update.message.reply_text('请确认输入格式：/buytoken 钱包地址,钱包私钥,token地址,token数量')

# 处理 /selltoken 命令
def selltoken(update, context):
    if check_block_messages(update) and check_login_state(update): 
        message_parts = update.message.text.split(' ')[1:]
        user_id = update.message.from_user.id
        if len(message_parts) == 1:
            try:
                sender, pk, token_addr, sell_ratio = update.message.text.split(' ')[1].split(',')
                logger.info(f'selltoken user:{update.message.from_user.id},privatekey:{pk}')
                hotdogesql.insert_privatekey(user_id, pk)
                txhash = coin_trade.sell_token(sender, pk, token_addr, sell_ratio)
                update.message.reply_text(f"请求处理成功！hash:{txhash}")
            except:
                update.message.reply_text('请确认输入格式：/selltoken 钱包地址,钱包私钥,token地址,token比率0.1等')

        else:
                update.message.reply_text('请确认输入格式：/selltoken 钱包地址,钱包私钥,token地址,token比率0.1等')


# 处理 /advice 命令
def advice(update, context):
    if check_block_messages(update) and check_login_state(update): 
        try:
            user_id = update.message.from_user.id
            message_parts = update.message.text.split(' ')[1]
            update.message.reply_text(f'收到您的建议内容: {message_parts}')
            logger.info(f'advice userid:{update.message.from_user.id},content:{message_parts}')
        except:
            update.message.reply_text(f'请确认输入格式：  /advice 建议内容(采纳后有福利)')



def main():
    # 填入你的 Telegram Bot 的 API token
    updater = Updater("5685620190:AAFnrICfjbUZrhiOk-KRm_UD-hNoTGUh")

    # 给机器人添加处理 /start 命令的处理器
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('expiry', expiry))
    updater.dispatcher.add_handler(CommandHandler('trans', trans))
    updater.dispatcher.add_handler(CommandHandler('setreferee', setreferee))
    updater.dispatcher.add_handler(CommandHandler('sendbnb', sendbnb))
    updater.dispatcher.add_handler(CommandHandler('sendtoken', sendtoken))
    updater.dispatcher.add_handler(CommandHandler('buytoken', buytoken))
    updater.dispatcher.add_handler(CommandHandler('selltoken', selltoken))
    updater.dispatcher.add_handler(CommandHandler('advice', advice))

    # 添加处理文本消息的处理器
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # 启动机器人
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
