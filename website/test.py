from __init__ import player_details

playerDetails = player_details.find_one(
    {"_id": "2247da4532f5428e8971465e5ec2acbd"}, {"profile-picture": 1, "profile-picture-type": 1})

print(playerDetails)
