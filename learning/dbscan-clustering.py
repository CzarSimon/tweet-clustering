import sys
sys.path.append('..')
from database import manager as db
import vectorize as vec
from sklearn.cluster import DBSCAN
from collections import defaultdict

def _get_tweets():
    tweets = map(lambda tweet: [vec.remove_url(tweet["text"]), tweet["followers"]], db.get_tweets())
    return tweets

def dbscan_clustering(vectors, tweets):
    dbscan = DBSCAN()
    clustering = dbscan.fit_predict(vectors)
    clusters = _reduce_by_key(_filter_noise(_map_to_index(clustering)))
    for cluster in clusters.items():
        print cluster[0], cluster[1]    

def _map_to_index(clusters_list):
    return map(lambda (index, clust_no): (clust_no, index), enumerate(clusters_list))

def _filter_noise(clusters_list):
    return filter(lambda tweet: tweet[0] != -1, clusters_list)

def _reduce_by_key(tuple_list):
    reduction = defaultdict(list)
    for key, val in tuple_list:
        reduction[key].append(val)
    return reduction

def _main(tweets):
    tweet_vectors = vec.vectorize_tweets(map(lambda item: item[0], tweets))
    dbscan_clustering(tweet_vectors, tweets)

if __name__ == '__main__':
    _main(_get_tweets())
