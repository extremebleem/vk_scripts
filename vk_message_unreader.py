import vk, time
from helpers import *

def setAllUnreaded(api, conversations):
	for conversation in conversations.get('items'):
		conversationData = conversation.get('conversation')
		
		conversationID = conversationData.get('peer').get('id')
		
		if conversationData.get('is_marked_unread') == True:
			print(f"'{conversationID}' is already marked as unread.")
			continue
		
		lastMessageID = conversationData.get('last_message_id')
		
		api.messages.markAsUnreadConversation(peer_id = conversationID)
		
		time.sleep(0.8)

def main():
	api = getApiMain()

	offset = 0
	conversationsCount = 1
	
	while offset < conversationsCount:
		conversations = api.messages.getConversations(count = 200, offset = offset)
		conversationsCount = conversations.get('count')
		
		setAllUnreaded(api, conversations)

		offset += 200
		
if __name__ == '__main__':
	main()