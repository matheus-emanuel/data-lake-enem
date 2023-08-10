# Data Lake ENEM 2020
Eu trabalho como Engenheiro(a) de Dados em uma grande instituição educacional. O gestor da minha área iniciou um novo projeto de inteligência de dados com o objetivo de entender o desempenho de alunos do ensino médio de todo o Brasil no Exame Nacional do Ensino Médio (ENEM). Desse modo, eu estou responsável por construir um Data Lake com os dados do ENEM 2020, realizar o processamento utilizando ferramental adequado e disponibilizar o dado para consultas dos usuários de negócios e analistas de BI.

## Pontos importantes
- [Definindo o ambiente](#definindo-o-ambiente)
- [Conseguindo os dados](#conseguindo-os-dados)
- [Começando a trabalhar os dados](#começando-a-trabalhar-os-dados)
- [Disponibilizando os dados no BigQuery](#disponibilizando-os-dados-no-bigquery)
## Definindo o ambiente
A primeira coisa a se fazer é criar um ambiente virtual em python, para que possamos ter um ambientes específico e "limpo" para instalar-mos as bibliotecas necessárias. Então como primeira parte vamo criar o ambiente, para isso basta abrir o cmd e navegar até a pasta onde você deseja criar o ambiente virtual
```cmd
cd caminho/da/pasta/desejada
```
Para criar o ambiente virtual basta usar o seguinte comando no cmd
```cmd
python -m venv nome-do-ambiente
```
E para ativa-lo é só usar:
```cmd
nome-do-ambiente\Scripts\activate
```
Por fim, com o ambiente virtual já criado basta instalar as bibliotecass que serão usadas nesse projeto. Elas foram disponibilizadas em um requirements.txt com o nome e a versão de cada biblioteca usada. Para instalar todas as bibliotecas de uma vez basta usar o comando pip com o argumento -r, assim ele lerá de um arquivo como o nome do arquivo que foi disponibilizado nesse github é requirments e seu tipo é .txt vamos usar da seguinte forma:
```cmd
pip -r requirements.txt
```
Outro ponto importante é configurar o gsutil para isso a própria google disponibiliza um passo a passo que pode ser encontrado aqui: [Configurando gsutil](https://cloud.google.com/storage/docs/gsutil_install?hl=pt-br)

Pronto, com o ambiente virtual já criado e as bibliotecas necessárias já instaladas podemos ir para o próximo passo.

## Conseguindo os dados
O próximo passo para disponibilizar os dados é conseguir os dados brutos, eles podem vir de várias fontes e em vários formatos. No caso deste projeto ele foi disponibilizado no seguinte [link](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem). Há varias formas de extrair esse dado, usando web scraping, baixando os dados via código com o cURL ou o wget e baixando os dados, a alternativa escolhida foi baixar os dados por 3 motivos
1. Os dados não são excessivamente grandes
2. Será feita uma análise pontual
3. Não será recorrente

Com isso, também já temos os dados baixados e podemos seguir para o ponto seguinte.

## Preparando o ambiente em nuvem
Agora é hora de preparar o ambiente em nuvem, para isso vamos selecionar a cloud e as suas tecnologias. A cloud escolhida foi a GCP (opinião pessoal: é onde desejo me aprofundar) e as tecnologias escolhidas foram, GCS (Google Cloud Storage) para o armazenamento dos dados, Google Dataproc para o processamento massimo usando Spark e o Bigquery para disponibilizar esses dados para consultas em SQL para a criação de relatórios ou análises mais profundas.

Para armazenar os dados no GCS primeiramente é necessários criar os buckets (buckets nada mais são que locais únicos usados para armazenar uma quantidade massiva de dados e de vários tipo), para criar os buckets usaremos o seguinte código python

```python
from google.cloud import storage

gcs_client = storage.Client()

# Criando um bucket no GCS através de código python
bucket_name = 'seu_bucket'

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
```

Após os buckets serem criados criaremos também o nosso cluster no Dataproc, que é responsável por realizar o processamento e conversão dos nossos dados, para criar-mos o cluster do Dataproc podemos usar o seguinte código:

```python
from google.cloud import dataproc_v1 as dataproc

region = 'us-east1'

dataproc_client = dataproc.ClusterControllerClient(
        client_options={"api_endpoint": "{}-dataproc.googleapis.com:443".format(region)}
    )


cluster_dict = {
    'project_id': 'seu-projeto-no-gcp',
    'cluster_name':'cluster-spark-processing-enem2',
    "config": {
            "master_config": {
                "num_instances": 1,
                "machine_type_uri": "n2-highmem-2",
                "disk_config": {"boot_disk_size_gb": 100},
            },
            "worker_config": {
                "num_instances": 2,
                "machine_type_uri": "n2-highmem-2",
                "disk_config": {"boot_disk_size_gb": 100},
            },
        },
}

cluster = dataproc_client.create_cluster(
    request= {'project_id':'seu-projeto-no-gcp', 'region':'us-east1', 'cluster': cluster_dict}
)


result = cluster.result()

print("Cluster created successfully: {}".format(result.cluster_name))
```
Aqui eu selecionei máquinas do tipo n2-highmem-2 pois elas são mais focadas em memória já que para o spark quanto mais memória melhor, optei por escolher uma máquina com processador padrão porém com 16GB de memória. E pronto temos o nosso ambiente pronto, agora o que nos resta fazer é processar os dados e para isso, vamos subir o nosso arquivo



## Começando a trabalhar os dados
Para começarmos a trabalhar com os dados precisamos primeiro fazer o upload dele no GCS e isso pode ser feito de várias formas, mas quero destacar duas usando código em python e usando o gsutil. Eu tive problemas em subir com o código python por conta do servidor da Google que me deu alguns erros, mas depois de alguns testes consegui subir por isso com um toque de opinião pessoal o gsutil é bem mais fácil e rápido de se usar mas irei mostrar as duas formas aqui

### Realizando o Upload dos dados
1. Vamos fazer o upload usando python
```python
import io
import requests

def upload_csv_file(bucket_name, file_name, file_content):

  url = 'https://storage.googleapis.com/upload/storage/v1/b/{}/o'.format(bucket_name)
  headers = {'Content-Type': 'application/octet-stream'}
  data = io.BytesIO(file_content)

  response = requests.post(url, headers=headers, data=data)
  if response.status_code == 200:
    return response.headers['Location']
  else:
    raise Exception('Failed to upload file.')

if __name__ == '__main__':
  bucket_name = 'seu_bucket'
  file_name = 'caminho/do/arquivo/desejado.csv'
  file_content = open(file_name, 'rb').read()

  url = upload_csv_file(bucket_name, file_name, file_content)
  print(url)
```
E aqui temos algumas considerações, caso você use o sistema operacional windows eu  indico copiar o caminho e quando for colocar o caractere 'r' antes da string, isso por que a barra que o windows usa é a barra invertida '\\' que no python significa quebra de linha, logo dará um erro na hora de rodar o código como deu comigo.

2. Agora vamos fazer o upload usando o gsutil
``` bash
gsutil cp seu_arquivo.csv gs://enem_analytics/raw_data/
```
E pronto seu arquivo já está sendo transferido para a nuvem, algumas observações importantes, não coloquei no exemplo, mas para fazer o upload você tem que estar no mesmo diretório que está o seu arquivo outro ponto importante é que se você tiver um sistema de organização no seu bucket é necessário inseri-los na URL do gsutil.

Pronto, com os dados em nuvem vamos começar a processar esses dados o passo mais importante que vamos fazer aqui é converter os dados de .csv para .parquet, pois assim temos uma economia de espaço e processamento. Só para termos uma ideia, o dado em csv tem aproximadamente 1,9GB enquanto o dado convertido para parquet tem em média 420MB, ou seja uma economia de 5X em espaço.

O ideal seria usar delta, porém o BigQuery não consegue converter os dados em delta numa tabela, assim como é possível fazer em parquet, mas temos o conhecimento que delta é uma forma de compressão melhor que parquet. Agora chega de teoria e vamos para o que importa


### Convertendo os dados para Parquet
A primeira coisa que temos que fazer é criar o script em python para converter os dados usando o Pyspark podemos desenvolver esse código localmente ou desenvolver localmente, subir no gcs e depois rodar apenas em job submit no gsutil para rodar esse código no nosso cluster spark

O código desenvolvido é o seguinte:
```python
from pyspark.sql import SparkSession

# Criando uma seção do spark
spark = SparkSession.builder \
        .appName('converting_csv_in_parquet') \
        .getOrCreate()

df = spark.read.csv(
    'gs://seu_bucket/raw_data/microdados_enem_2020.csv',
    header = True,
    inferSchema = True,
    sep=";"
)

df.write.format('parquet').save('gs://seu_bucket/evaluated_data/year=2020')

spark.stop()
```
Com esse código pronto basta rodar mais um comando e nosso arquivo será convertido em parquet
```bash
gcloud dataproc jobs submit pyspark --cluster=cluster-spark-processing-enem convert_csv_in_parquet.py --region=us-east1
```

Agora sim, nosso arquivo já foi convertido e salvo em outra pasta, indicando que ele não é mais um dados raw. Estamos a um passo de ter o nosso dado disponibilizado no bigquery para que outras pessoas possam usa-lo

## Disponibilizando os dados no BigQuery
Para terminar vamos converter os dados em parquet para uma tabela e assim torna-los acessível para outros analistas o primeiro passo é criar um dataset no seu projeto no bigquery da para fazer isso facilmente usando a UI do bigquery ou via código ou ainda usando o gsutil, eu usei a UI por estar mais familiarizado você pode seguir o passo a passo disponibilizado pela própria google de como criar um dataset [Tutorial de como criar um dataset](https://cloud.google.com/bigquery/docs/datasets?hl=pt-br#:~:text=Create%20a%20BigQuery%20Dataset%201%20Open%20the%20BigQuery,choose%20a...%205%20Click%20Create%20dataset.%20See%20More.)

Com o dataset criado vamos criar a nossa tabela via código python
```python
from google.cloud import bigquery

bigquery_client = bigquery.Client()

table_id = 'seu-projeto-no-gcp.enem_2020.dados_enem_2020'

source_uris = ['gs://seu_bucket/evaluated_data/year=2020/*.parquet']

source_uris_str = ",".join(source_uris)

job_config = bigquery.LoadJobConfig()
job_config.source_format = bigquery.SourceFormat.PARQUET
job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE


job = bigquery_client.load_table_from_uri(
    source_uris=source_uris_str, destination=table_id,job_config=job_config
)
```
Como parquet criar vários pequenos arquivos precisamos usar o caractere curinga '*' para ler todos os arquivos e pronto nosso arquivo já está disponível para consulta no GCP de forma rápida e segura

## Conclusão e próximos passos
Essa é só uma das várias formas que podemos realizar este processo, outro ponto importante é que esse processe não é de graça principalmente o cluster que é pago por hora com isso tenha em mente que ao terminar todo o uso desligue tudo para não ter susto com a fatura do cartão no final do mês, uma alternativa interessante é definir alertas de custos um valor que você está disposto a pagar por mês. Outro ponto é usar os $300 que a google disponibiliza para novos usuiários

Como próximos passos podemos automatizar esse processo usando o Cloud Composer (airflow dentro do GCP) bem como criar um código em terraform para que possamos subir o ambiente rapidamente e fazer alterações.






