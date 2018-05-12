import RAKE

# txt = "Poverty Is Not Only Lack of Income But also: Poor health : 9 million children every year die under the age of 5, mainly of preventable disease. Poor education : 50% of children enrolled in school in India cannot read a simple paragraph. Poor quality of life: hours collecting water instead of playing, working, learning. Difficulty to realize your ambition: Get a loan for a business, be insured for the risk of your farm.Amartya Sen: Development as Freedom"

def extract_keywords(text):
	Rake = RAKE.Rake(RAKE.SmartStopList())
	return Rake.run(text, maxWords = 10)