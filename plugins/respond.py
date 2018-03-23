# -*- coding: utf-8 -*
from pymongo import MongoClient

HOST = 'localhost'
PORT = 27071


def access_db(conn, name, content, at_times):
    db = conn.qq_history
    history = db.qq_history_gay_group
    history_file = {'user': name, 'content': content, 'at_times': at_times}
    history.insert_one(history_file)


def gain_at_times(conn, name):
    db = conn.qq_history
    history = db.qq_history_gay_group
    target = history.findOne({"user": name})
    target.at_times += 1
    history.update({'user': name}, target)
    return target.at_times


def reset_at_times(conn, name):
    db = conn.qq_history
    history = db.qq_history_gay_group
    target = history.find_one({"user": name})
    target.at_times = 0
    history.update({'user': name}, target)


def onQQMessage(bot, contact, member, content):
    conn = MongoClient('localhost', 27017)
    access_db(conn, member.name, content, 1)
    test_dict = {'h': '又可以来黑h了'}
    if member.name == '羊':
        if content == 'konnichiwa':
            bot.SendTo(contact, 'Searching modules...\nSearching plugins...\nBoot Successfully!')
        elif content == 'oyasumi':
            bot.SendTo(contact, 'Shutting down...おやすみなさい！')
    if '@ME' in content:
        current_at_times = gain_at_times(conn, member.name)
        if current_at_times > 3:
            bot.SendTo(contact, member.name + '你好烦啊，杀了你哦')
            reset_at_times(conn, member.name)
        else:
            bot.SendTo(contact, member.name + ', Personalized Responding System is still under development')
    if '添加梗' not in content and '梗' in content and not bot.isMe(contact, member):
        #  format 添加梗 name：xxx# meme:xxxx#
        bot.SendTo(contact, '可以随意添加梗，以后当内容出现关键字时就会有十分ky的句子跳出来，鬼知道为什么这个功能要存在\n格式：梗 name:xxx#(以#结束） meme:xxx#(以#结束）')
    """
    for key in test_dict:
        print(key)
        if key in content and not bot.isMe(contact, member):
            print(test_dict[key])
            bot.SendTo(contact, test_dict[key])
            break
    """
