from sklearn.feature_extraction.text import TfidfVectorizer
import stopwords

test_text = ["Ukraine has filed a complaint at the World Trade Organization to challenge Russia over restrictions on freight transit, the WTO said in a statement on Thursday. Ukraine says Russia has put conditions that break WTO rules, such as requiring Ukrainian trucks to use identification seals and to move in convoy, and by putting restrictions on Ukrainian drivers entering Russia from Belarus. Russia has 60 days to settle the complaint. After that, Ukraine could ask the WTO to adjudicate."]
test_cluster = ["Ukraine has filed a complaint at the World Trade Organization to challenge Russia over restrictions on freight transit, the WTO said in a statement on Thursday.",
                "Ukraine says Russia has put conditions that break WTO rules, such as requiring Ukrainian trucks to use identification seals and to move in convoy, and by putting restrictions on Ukrainian drivers entering Russia from Belarus.",
                "Russia has 60 days to settle the complaint. After that, Ukraine could ask the WTO to adjudicate."]


def reduce_text_list(text_list, as_list=False):
    reduced_text = reduce(lambda all_text, text: all_text + " " + text, text_list)
    if as_list:
        return [reduced_text]
    else:
        return reduced_text

def _extract_words_and_score(text):
    sw = stopwords.english + ['accenture', 'acn']
    tf_idf = TfidfVectorizer(analyzer='word', stop_words='english')
    scores = tf_idf.fit_transform(text).toarray()[0]
    words = tf_idf.get_feature_names()
    return [words, scores]

def get_keywords(text, number=5):
    words, scores = _extract_words_and_score(text)
    word_scores = map(lambda (index, word): (word, scores[index]), enumerate(words))
    sorted_words = sorted(word_scores, key=lambda w: w[1] * -1)[:min(len(words), number)]
    return map(lambda word_and_score: word_and_score[0], sorted_words)
