import numpy as np

# import findspark
# findspark.init()

# import pyspark
# sc = pyspark.SparkContext(appName="myAppName")

# x = findspark.find()
# print(x)

def sort_predictions_slice(arr, n):
    actual_and_pred = np.array(arr)
    # sort by predictions
    indeces = np.argsort(actual_and_pred[:, 1])
    return actual_and_pred[indeces[::-1]][:n].tolist()

def dcg_at_k(scores, k):
    """
    Discounted cumulative gain
    See http://fastml.com/evaluating-recommender-systems/
    Args:
        r: List - Relevance scores in rank order
        k: Number of results to consider
    Returns:
        Float
    """
    r = np.asfarray(scores)[:k]
    if r.size:
        # item 1 and 2 have same weights
        return r[0] + np.sum(r[1:] / np.log2(np.arange(2, r.size + 1)))
        # use below for more emphasis on first rank
        # return np.sum(r / np.log2(np.arange(2, r.size + 2)))
    return 0.

def ndcg_at_k(scores, k):
    """
    Normalized Discounted cumulative gain
    See http://fastml.com/evaluating-recommender-systems/
    Args:
        r: List - Relevance scores in rank order
        k: Number of results to consider
    Returns:
        Float from 0 to 1
    """
    dcg_max = dcg_at_k(sorted(scores, reverse=True), k)
    if not dcg_max:
        return 0.
    return dcg_at_k(scores, k) / dcg_max

'''
    consider half life evaluation
    need algorithm
'''

'''
    consider fraction of concordant pairs
    pairwise accuracy - is order correct?
'''

def spark_ndcg_at_k(
    predictions_rdd,
    k,
    label_row='min_max',
    prediction_row='prediction'
):
    # use actual values for gain
    prediction_count = predictions_rdd.count()

    sampled = predictions_rdd.sample(False, 1, 1)
    ndcg = sampled.map(lambda row: (row['uid'], [(row[label_row], row[prediction_row])])) \
        .reduceByKey(lambda total, val: total + val) \
        .map(lambda kv: (kv[0], sort_predictions_slice(kv[1], 1000))) \
        .map(lambda kv: ndcg_at_k(np.array(kv[1])[:, 0], k)) \
        .reduce(lambda total, gain: total + gain)
    average_ndcg = ndcg / prediction_count
    return (ndcg, average_ndcg)
