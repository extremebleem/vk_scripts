import vk, os, time, random
from datetime import datetime

TOKEN = input("Your VK Token: ")
api = vk.API(vk.Session(access_token = TOKEN), v = "5.131", lang = "ru")

lastMessageID = 0

chatID = 0
chatLabel = input("label: ")

conversations = api.messages.getConversations().get("items")

for n in range(0, len(conversations) - 1):
	conversation = conversations[n].get("conversation")
	if conversation:
		currentChatID = conversation.get("peer").get("id")
		if currentChatID < 0:
			groupData = api.groups.getById(group_id = -1 * int(currentChatID))
			groupLabel = groupData[0].get("name")
			if groupLabel == chatLabel:
				chatID = currentChatID
				break
		else:
			chat_settings = conversation.get("chat_settings")
			if chat_settings and chat_settings.get("title") == chatLabel:
				chatID = currentChatID
				break

if chatID == 0:
	print("Chat not found")
	chatID = input("ID: ")

os.system("cls")

while(True):
	messagesHistory = api.messages.getHistory(count = 1, peer_id = chatID)
	
	messageItems = messagesHistory.get("items")[0]
	currentMessageID = int(messageItems.get("id"))
	
	print(messagesHistory.get("items")[0])

	time.sleep(20)