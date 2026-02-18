import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, avg, sum
from pyspark.sql.types import StructType, StringType, DoubleType
os.environ["TZ"] = "Asia/Kolkata" 

# Environment paths
project_root = r"D:\BDA\spotify_project"
os.environ["HADOOP_HOME"] = os.path.join(project_root, "hadoop")
os.environ["PATH"] += os.pathsep + os.path.join(os.environ["HADOOP_HOME"], "bin")

spark = SparkSession.builder \
    .appName("SpotifyAnalytics") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.5.0") \
    .config("spark.hadoop.fs.permissions.umask-mode", "000") \
    .config("spark.driver.host", "localhost") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .config("spark.local.dir", r"D:\BDA\spotify_project\logs") \
    .config("spark.driver.extraJavaOptions", "-Duser.timezone=Asia/Kolkata")\
    .config("spark.executor.extraJavaOptions", "-Duser.timezone=Asia/Kolkata")\
    .getOrCreate()
    
if not os.path.exists(r"D:\BDA\spotify_project\logs"):
    os.makedirs(r"D:\BDA\spotify_project\logs")

schema = StructType().add("genre", StringType()).add("streams", DoubleType()).add("skip_rate", DoubleType())

# 1. Read from Kafka
df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092").option("subscribe", "spotify_topic").load()

# 2. Process JSON
parsed = df.selectExpr("CAST(value AS STRING)").select(from_json(col("value"), schema).alias("data")).select("data.*")

# 3. Aggregate stats
stats = parsed.groupBy("genre").agg(avg("skip_rate").alias("avg_skip"), sum("streams").alias("total_streams"))

# 4. Save to DB
def write_to_db(batch_df, batch_id):
    batch_df.write.format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/spotify_db") \
        .option("driver", "org.postgresql.Driver") \
        .option("dbtable", "spotify_stats") \
        .option("user", "admin") \
        .option("password", "admin_password") \
        .mode("overwrite").save()

query = stats.writeStream.foreachBatch(write_to_db).outputMode("complete").start()
query.awaitTermination()