from random import randint
import json
import codecs


f = codecs.open("full_tourney.json",'r','utf-8-sig')
#f = codecs.open("tourney_rd_1.json",'r','utf-8-sig')
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
			


a_file = codecs.open("full_tourney.json",'w','utf-8-sig')
#a_file = codecs.open("tourney_rd_1.json",'w','utf-8-sig')
json.dump(board, a_file)
a_file.close()


