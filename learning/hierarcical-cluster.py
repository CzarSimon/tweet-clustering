import sys
sys.path.append("..")
from database import manager as db
import keywords as kw
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram, cophenet, fcluster
from scipy.spatial.distance import pdist
import matplotlib.pyplot as plt
import vectorize as vec

# Non pure function, gets all stored tweets from the database.
def _get_tweets():
    tweets = map(lambda tweet: [vec.remove_url(tweet["text"]), tweet["followers"]], db.get_tweets())
    return tweets

def print_dendrogram(clustering, n_clust):
    plt.figure()
    dn = dendrogram(clustering, p=n_clust, truncate_mode='lastp', show_contracted=True)
    plt.show()
    pass

def scipy_clustering(tweets):
    vectors = vec.vectorize_tweets(map(lambda item: item[0], tweets))
    clustering = linkage(vectors, method='complete', metric='euclidean')
    _calc_accuracy(clustering, vectors)
    n_clust = _calc_n_clust(clustering)
    clusters = fcluster(clustering, n_clust, criterion='maxclust')
    return _map_tweet_to_cluster(clusters, tweets, n_clust)

def _map_tweet_to_cluster(clusters, tweets, k):
    clust_arr = map(lambda nothing: {"list": [], "score": 0}, [None] * k)
    for tweet_index, clust_index in enumerate(clusters):
        tweet = tweets[tweet_index]
        clust_arr[clust_index - 1]["list"] += [tweet[0]]
        clust_arr[clust_index - 1]["score"] += tweet[1]
    return sorted(clust_arr, key=lambda cluster: -1 * cluster["score"])

def _calc_accuracy(clustering, vectors):
    c, coph_dist = cophenet(clustering, pdist(vectors))
    print c
    pass

def _plot_distance_dropoff(distance, deriv):
    x_axis = map(lambda (index, clust): index, enumerate(distance))
    plt.figure()
    plt.plot(x_axis, distance)
    plt.plot(x_axis[:-1], deriv)
    plt.show()
    pass

def _calc_n_clust(clustering):
    distances = map(lambda cluster: cluster[2], clustering)
    non_zero_dist = filter(lambda d: d > 0, distances)
    dist_1st_deriv = np.diff(non_zero_dist, 1)
    #_plot_distance_dropoff(non_zero_dist, dist_1st_deriv)
    return int(dist_1st_deriv.argmax()) + 2 + len(distances) - len(non_zero_dist)

def main(tweets):
    tweet_clusters = scipy_clustering(tweets)
    print len(tweet_clusters), len(tweets)
    for number, cluster in enumerate(tweet_clusters[:10]):
        print "These are the keywords in cluster:", number + 1, "Length:", len(cluster["list"]), "Score:", cluster["score"]
        print kw.reduce_text_list(kw.get_keywords(kw.reduce_text_list(cluster["list"], as_list=True),5))
        print ""

if __name__ == '__main__':
    main(_get_tweets())
