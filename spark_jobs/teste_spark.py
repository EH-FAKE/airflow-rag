from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession.builder.appName("TesteSubmit").getOrCreate()
    df = spark.createDataFrame([(1, "Airflow"), (2, "Spark")], ["id", "value"])
    df.show()
    spark.stop()