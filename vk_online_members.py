import vk, time, random

TOKEN = input("Your VK Token: ")
api = vk.API(vk.Session(access_token = TOKEN), v = "5.131", lang = "ru")

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

conversationMembers = api.messages.getConversationMembers(peer_id = chatID, fields = "online").get("profiles")

textMessage = "Онлайн сейчас:"

for member in conversationMembers:
	if member.get("online") == 1:
		textMessage += "\n[id" + str(member.get("id")) + "|" + member.get("first_name")[:1] + ". " + member.get("last_name") + "]"

if textMessage != "Онлайн сейчас:":
	api.messages.send(peer_id = chatID, random_id = random.randint(1, 999999999), message = textMessage, disable_mentions = 1)
