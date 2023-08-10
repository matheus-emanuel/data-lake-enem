# Data Lake ENEM 2020
Eu trabalho como Engenheiro(a) de Dados em uma grande instituição educacional. O gestor da minha área iniciou um novo projeto de inteligência de dados com o objetivo de entender o desempenho de alunos do ensino médio de todo o Brasil no Exame Nacional do Ensino Médio (ENEM). Desse modo, eu estou responsável por construir um Data Lake com os dados do ENEM 2020, realizar o processamento utilizando ferramental adequado e disponibilizar o dado para consultas dos usuários de negócios e analistas de BI.
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

Pronto, com o ambiente virtual já criado e as bibliotecas necessárias já instaladas podemos ir para o próximo passo.

## Conseguindo os dados
O próximo passo para disponibilizar os dados é conseguir os dados brutos, eles podem vir de várias fontes e em vários formatos. No caso deste projeto ele foi disponibilizado no seguinte [link](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem). Há varias formas de extrair esse dado, usando web scraping, baixando os dados via código com o cURL ou o wget e baixando os dados, a alternativa escolhida foi baixar os dados por X motivos
1. Os dados não são excessivamente grandes
2. Será feita uma análise pontual
3. Não será recorrente

Com isso, também já temos os dados baixados e podemos seguir para o ponto seguinte.
