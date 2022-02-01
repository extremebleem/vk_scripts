import vk, time

TOKEN = input("Your VK Token: ")
api = vk.API(vk.Session(access_token = TOKEN), v = "5.131", lang = "ru")

ourUserID = int(api.users.get()[0].get("id"))

ourFollowersList = api.users.getFollowers(user_id = ourUserID, count = "1000")

followersCount = ourFollowersList.get("count")
multiplePasses = True
additionalValue = 0

while multiplePasses:
	iterator = 0
	for userID in ourFollowersList.get("items"):
		if iterator == 0:
			ourFollowersList = api.users.getFollowers(user_id = ourUserID, count = "1000")
			followersCount = ourFollowersList.get("count")
			multiplePasses = True if followersCount / 1000 > 1 else False
			
		api.account.ban(user_id = userID)
		iterator = iterator + 1
		print("[" + str(iterator + additionalValue) + "/" + str(followersCount) + "]")
		if iterator % 30 == 0:
			time.sleep(51)
		else:
			time.sleep(0.1)
		
	additionalValue = additionalValue + 1000