import math

class Scorer(object):

	def cosine_similarity(cls, app_list1, app_list2):
		match_count = cls.count_math(app_list1, app_list2)
		return float(match_count / math.sqrt(len(app_list1) * len(app_list2)))

	def count_math(cls, list1, list2):
		count = 0
		for element in list1:
			if element in list2:
				count += 1
		return count