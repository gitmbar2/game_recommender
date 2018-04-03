import numpy as np

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
        # item 1 and 2 have same weights:
        # return r[0] + np.sum(r[1:] / np.log2(np.arange(2, r.size + 1)))
        # use below for more emphasis on first rank:
        return np.sum(r / np.log2(np.arange(2, r.size + 2)))
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

def spark_ndcg_at_k(
    predictions_rdd,
    k,
    label_row='min_max',
    prediction_row='prediction'
):
    # use actual values for gain
    prediction_count = predictions_rdd.count()

    sampled = predictions_rdd.sample(False, 1, 1)
    ndcg = rdd.map(lambda row: (row[id_col], [(row[label_col], row[prediction_col])])) \
        .reduceByKey(lambda all_data, val: all_data + val) \
        .map(lambda kv: sorted(kv[1], key=lambda x: x[1], reverse=True)) \
        .map(lambda v: ndcg_at_k(np.array(v)[:, 0], k)) \
        .sum()

    # more efficient? dont allocate object for each record
    # rdd.aggregateByKey(zero)(
    # (arr, v) => arr += v,
    # (arr1, arr2) => arr1 + arr2)

    average_ndcg = ndcg / prediction_count
    return (ndcg, average_ndcg)

# Verify RMSE with rdd math
def spark_rmse(predictions, label_column='playtime_min_max'):
    prediction_count = predictions.count()
    predictions_rdd = predictions.rdd
    SSE = predictions_rdd.map(lambda r: (r[label_column] - r['prediction'])**2) \
        .reduce(lambda total, x: total + x)
    math.sqrt(SSE / prediction_count)
