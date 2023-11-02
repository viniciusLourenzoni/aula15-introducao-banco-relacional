# Introdução a bancos de dados relacionais

## Download beekeeper community

<https://github.com/beekeeper-studio/beekeeper-studio/releases>

## Exemplo 1 - API de fluxo de oficina

Uma oficina está precisando melhorar o processo de fluxo de veículos dentro da oficina.

Para isso, ela precisa de uma API REST para as seguintes operações: CRUD (Create, Retrieve, Update e Delete) do registro de manutenção, contendo os dados do veículo, nome do cliente, nome do mecânico e data e hora de chegada do veículo.

Deve ter uma operação para atualizar o horário de finalização da manutenção. Deve listar todos os veículos que estão em manutenção na oficina no momento. Por fim deve permitir excluir uma manutenção que foi incluída mas ainda não foi finalizada. Os dados devem ser gravados em um banco de dados e vão existir enquanto a aplicação existir.

### Definição da tabela

Nome: manutenção
Campo - tipo:
id - int
placa - texto
marca - texto
modelo - texto
cor - texto
nome cliente - texto
nome mecânico - texto
data e hora chegada - data e hora como texto
data e hora finalização - data e hora como texto

### Normalização

table -> manutencao
fields:
id - SERIAL
placa - TEXT
marca - TEXT
modelo - TEXT
cor - TEXT
nome_cliente - TEXT
nome_mecanico - TEXT
data_hora_chegada - DATETIME
data_hora_finalizacao - DATETIME
