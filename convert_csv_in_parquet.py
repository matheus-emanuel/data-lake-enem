from pyspark.sql import SparkSession

# Criando uma seção do spark
spark = SparkSession.builder \
        .appName('converting_csv_in_parquet') \
        .getOrCreate()

df = spark.read.csv(
    'gs://enem_analytics/raw_data/microdados_enem_2020.csv',
    header = True,
    inferSchema = True,
    sep=";"
)

df.write.format('parquet').save('gs://enem_analytics/evaluated_data/year=2020')

spark.stop()

# script do arquivo usando o gcloud
#gcloud dataproc jobs submit pyspark --cluster=cluster-spark-processing-enem convert_csv_in_parquet.py --region=us-east1
# Esse script funciona para rodar o código localmente