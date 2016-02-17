from pymongo import MongoClient
import operator
import math
# self defined modules
import MongoService
import Scoring

class Recommender(object):

	def calculate_top_5(cls, user_download_history):
		# create a dict to store each other app and its similarity to this app
		app_similarity = {} # {app_id : similarity}

		for apps in user_download_history:
			# calculate the similarity
			similarity = Scoring.Scorer.cosine_similarity([app], apps)
			for other_app in apps:
				if other_app in app_similarity:
					app_similarity[other_app] = app_similarity[other_app] + similarity
				else:
					app_similarity = similarity

		# There could be app without related apps (not in any download history)
		if not app in app_similarity:
			return

		# sort app_similarity dict by value and get the top 5 as recommendation
		app_similarity.pop(app)
		# sort by similarity
		sorted_tups = sorted(app_similarity.item(), key = operator.itemgetter(1), reverse = True)
		top_5_app = [sorted_tups[0][0], sorted_tups[1][0], sorted_tups[2][0], sorted_tups[3][0], sorted_tups[4][0]]
		print("top_5_app for " + str(app) + ":\t" + str(top_5_app))

		# store the top 5
		# DataService.update_app_info({'app_id': app}, {'$set' : {'top_5_app' : top_5_app}})


def main():
	try:
		# get MongoDB client and set it in DataService
		client = MongoClient('localhost', 27017)
		MongoService.DataService.init(client)

		# work flow
		user_download_history = DataService.retrieve_user_download_history()
		Recommender.calculate_top_5('C10107104', user_download_history.values())
	except Exception as e:
		print(e)
	finally:
		# clean up work
		if 'client' in locals():
			client.close()

if __name__ == "__main__":
	main()