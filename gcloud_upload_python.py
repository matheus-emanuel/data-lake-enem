import io
import requests

def upload_csv_file(bucket_name, file_name, file_content):
  """Uploads a CSV file to Cloud Storage.

  Args:
    bucket_name: The name of the bucket to upload the file to.
    file_name: The name of the file to upload.
    file_content: The content of the file to upload.

  Returns:
    The URL of the uploaded file.
  """

  url = 'https://storage.googleapis.com/upload/storage/v1/b/{}/o'.format(bucket_name)
  headers = {'Content-Type': 'application/octet-stream'}
  data = io.BytesIO(file_content)

  response = requests.post(url, headers=headers, data=data)
  if response.status_code == 200:
    return response.headers['Location']
  else:
    raise Exception('Failed to upload file.')

if __name__ == '__main__':
  bucket_name = 'enem_analytics'
  file_name = r'C:\Users\freit\OneDrive\Documentos\XP Educacao\Engenheiro de dado Cloud\microdados_enem_2020\DADOS\MICRODADOS_ENEM_2020.csv'
  file_content = open(file_name, 'rb').read()

  url = upload_csv_file(bucket_name, file_name, file_content)
  print(url)