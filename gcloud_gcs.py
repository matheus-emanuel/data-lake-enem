from google.cloud import storage

gcs_client = storage.Client()

# Criando um bucket no GCS através de código python
bucket_name = 'enem_analytics'

bucket = gcs_client.bucket(bucket_name) #Com essa linha eu retorno o bucket que eu quero criar
bucket.create()


# Criando uma pasta em um bucket através de código python
folder_name = 'raw_data/'
bucket = gcs_client.bucket(bucket_name) # Retorno o bucket que eu vou criar a pasta
folder = bucket.blob(folder_name) 
folder.upload_from_string('')

folder_name = 'clean_data/'
bucket = gcs_client.bucket(bucket_name)
folder = bucket.blob(folder_name) 
folder.upload_from_string('')

folder_name = 'evaluated_data/'
bucket = gcs_client.bucket(bucket_name=bucket_name)
folder = bucket.blob(blob_name=folder_name)
folder.upload_from_string('')

folder_name = 'code_data/'
bucket = gcs_client.bucket(bucket_name=bucket_name)
folder = bucket.blob(blob_name=folder_name)
folder.upload_from_string('')

# Upload do arquivo microdados_enem_2020
# bucket = gcs_client.bucket(bucket_name)
# archive_enem_2020 = r'C:\Users\freit\OneDrive\Documentos\XP Educacao\Engenheiro de dado Cloud\microdados_enem_2020\DADOS\MICRODADOS_ENEM_2020.csv'

# upload_archive = bucket.blob('enem_analytics/raw_data/MICRODADOS_ENEM_2020.csv')
# upload_archive.upload_from_filename(archive_enem_2020)


