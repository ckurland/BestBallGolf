from random import randint
import json
import codecs


#f = codecs.open("full_puerto.json",'r','utf-8-sig')
f = codecs.open("tourney_rd_1_puerto.json",'r','utf-8-sig')
board = json.load(f)
f.close()

for a in board["Players"]:
	for r in a["Rounds"]:
		tot_score = 0
		for h in r["Holes"]:
			tmp = randint(2,6)
			h["Score"] = tmp
			tot_score += tmp
		r["Score"] = tot_score

t = board["Tournament"]
t["StartDate"] = "2020-05-06T00:00:00"
t["EndDate"] = "2020-05-09T00:00:00"

t = t["Rounds"]
for s in t:
	if int(s["Number"]) == 1:
		s["Day"] = "2020-05-06T00:00:00"
	elif int(s["Number"]) == 2:
		s["Day"] = "2020-05-07T00:00:00"
	elif int(s["Number"]) == 3:
		s["Day"] = "2020-05-08T00:00:00"
	elif int(s["Number"]) == 4:
		s["Day"] = "2020-05-09T00:00:00"


#a_file = codecs.open("full_puerto.json",'w','utf-8-sig')
a_file = codecs.open("tourney_rd_1_puerto.json",'w','utf-8-sig')
json.dump(board, a_file)
a_file.close()


