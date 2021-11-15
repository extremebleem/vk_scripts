import vk, time

TOKEN = input("Your VK Token: ")
api = vk.API(vk.Session(access_token = TOKEN), v = "5.131", lang = "ru")

ourUserId = int(api.users.get()[0].get("id"))

friends_list = api.friends.get(user_id = ourUserId)

goalCount = friends_list.get("count")
deletedFriends = 1

for friend in friends_list.get("items"):
	print("[" + str(deletedFriends) + "/" + str(goalCount) + "] ID: " + str(friend) + '\n')
	
	if api.friends.delete(user_id = friend) < 3:
		api.account.ban(owner_id = friend)

	deletedFriends = deletedFriends + 1
	time.sleep(0.05)
