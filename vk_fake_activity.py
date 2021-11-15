import vk, time, os, threading, random

TOKEN = input("Your VK Token: ")
api = vk.API(vk.Session(access_token = TOKEN), v = "5.131", lang = "ru")

class IndexedThread:
	current_thread: threading = None
	index: int = 0
	close: bool = False
	peerID: int = 0

threads = []

ourUserID = int(api.users.get()[0].get("id"))
lastMessageID = 0

waitingUserID = False
waitingThreadIndex = 0

def get_peer_id(chatLabel):
	chatID = 0
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
	return chatID


def thread_set_activity(activityType, label, index):

	peerID = get_peer_id(label)

	global waitingUserID
	global waitingThreadIndex
	global threads
	
	if peerID == 0:
		api.messages.send(peer_id = ourUserID, random_id = random.randint(1, 999999999), message = "Чат не найдет\nВведите айди пользователя")
		waitingUserID = True
		waitingThreadIndex = index
	
	while True:
		time.sleep(5)
		if threads[index].close == True:
			break
		
		if peerID == 0:
			peerID = threads[index].peerID
			continue
		
		api.messages.setActivity(peer_id = peerID, type = "typing" if activityType == 1 else "audiomessage")

if __name__ == "__main__":
	while True:
		messagesHistory = api.messages.getHistory(count = 1, peer_id = ourUserID)
	
		messageItems = messagesHistory.get("items")[0]
		currentMessageID = int(messageItems.get("id"))
		
		if lastMessageID == currentMessageID:
			time.sleep(5)
			continue
		
		lastMessageID = currentMessageID
		
		messageText = messageItems.get("text")

		if len(messageText) < 4:
			continue

		if waitingUserID == True and messageText[0] != "[":
			threads[waitingThreadIndex].peerID = int(messageText)
			waitingUserID = False
			api.messages.send(peer_id = ourUserID, random_id = random.randint(1, 999999999), message = "Для потока " + str(waitingThreadIndex + 1) + " айди получателя был изменен.")
		elif messageText[0] == "_":
		
			if messageText[1:4] == "add":
				activityType = int(messageText[5])

				new_thread = IndexedThread()
				new_thread.index = len(threads)
				new_thread.current_thread = threading.Thread(target = thread_set_activity, args = (activityType, messageText[7:], new_thread.index), daemon = True)	
				new_thread.label = messageText[7:]
				
				threads.append(new_thread)
				
				new_thread.current_thread.start()
				
				api.messages.edit(message_id = currentMessageID, peer_id = ourUserID, message = "Поток для " + messageText[7:] + " типа " + str(activityType) + " добавлен")
				
			elif messageText[1:7] == "remove":
				index = int(messageText[8])
				
				if index > len(threads):
					continue
					
				threads[index - 1].close = True
				
				api.messages.edit(message_id = currentMessageID, peer_id = ourUserID, message = "Поток номер " + str(index) + " удален")
			
			elif messageText[1:7] == "active":
				
				activeThreads = ""
				for n in threads:
					if n.close == True:
						continue
					activeThreads += "[" + str(n.index + 1) + "] Название чата: " + n.label + "\n"
					
				if activeThreads == "":
					activeThreads = "Активных потоков нет"
					
				api.messages.edit(message_id = currentMessageID, peer_id = ourUserID, message = activeThreads)