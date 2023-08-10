from google.cloud import bigquery

bigquery_client = bigquery.Client()

table_id = 'lambda-architeture-on-gcp.enem_2020.dados_enem_2020'

source_uris = ['gs://enem_analytics/evaluated_data/year=2020/*.parquet']

source_uris_str = ",".join(source_uris)

job_config = bigquery.LoadJobConfig()
job_config.source_format = bigquery.SourceFormat.PARQUET
job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE


job = bigquery_client.load_table_from_uri(
    source_uris=source_uris_str, destination=table_id,job_config=job_config
)