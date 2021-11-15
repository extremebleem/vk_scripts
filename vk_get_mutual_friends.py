import vk, os

TOKEN = input("Your VK Token: ")
api = vk.API(vk.Session(access_token = TOKEN), v = "5.131", lang = "ru")

os.system("cls")

firstTarget = input("First UserID: ")
secondTarget = input("Second UserID: ")

mutualFriendsList = api.friends.getMutual(source_uid = firstTarget, target_uid = secondTarget)

mutualFriendCount = len(mutualFriendsList)

print("Count: " + str(mutualFriendCount))

iterator = 1

for mutualFriend in mutualFriendsList:
	userData = api.users.get(user_ids = mutualFriend, fields = "domain")[0]
	print("Serial Number: " + str(iterator))
	print("Name: " + userData.get("first_name") + " " + userData.get("last_name"))
	print("Link: vk.com/" + str(userData.get("domain")))
	iterator = iterator + 1