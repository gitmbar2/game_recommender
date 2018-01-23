import time
from pyspark import SparkContext, SparkConf
import logging
import json
import subprocess

def sleep_mapper(seconds):
    time.sleep(seconds)


if __name__ == "__main__":
    conf = SparkConf().setAppName("Test_App")
    sc = SparkContext(conf=conf)

    logging.getLogger("py4j").setLevel(logging.ERROR)

    subprocess.call(
        ["hadoop", "fs", "-get", "/user/thomas/go_to_sleep.in"]
    )

    with open("go_to_sleep.in", 'r') as f_in:
        data = json.load(f_in)

    sc.\
        parallelize(
            [data.get("duration") for number in xrange(10000)]
        ).\
        map(sleep_mapper)

    with open("go_to_sleep.out", "w") as f:
        f.write("Congratulations!")
        f.write("\n")

    sc.\
    parallelize(["Congratulations!"]).\
    saveAsTextFile("go_to_sleep.out")

    subprocess.call(
        ["hadoop", "fs", "-put", "go_to_sleep.out", "/test/go_to_sleep.out"]
    )
