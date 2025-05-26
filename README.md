# Backend Beber Água

## Modelos

Os modelos são responsáveis por representar as tabelas do banco de dados e servir de base para as operações. Eles estão definidos usando SQLAlchemy.


## Modelo **ConsumoDiario**
### Campos:

- id: Integer	 
- nome_usuario: String	 
- data: Date	 
- horario: Time	 
- consumo_ml: Float	 
 

## Modelo **MetaUsuario**
### Campos:
- id: Integer
- nome_usuario: String
- meta_litros: Float

# Rotas
As rotas são responsáveis por expor as funcionalidades da aplicação, permitindo a interação com os dados de consumo e metas dos usuários. Elas estão organizadas em diversos endpoints no padrão RESTful utilizando **FastAPI**.

### consumo
Endpoint: /consumo
Método: POST
Body:
{
  "nome_usuario": "Victor",
  "consumo_ml": 250
}

Exemplo de Resposta:
{
  "mensagem": "Consumo registrado com sucesso!",
  "dados": {
    "nome_usuario": "Victor",
    "data": "2025-05-24",
    "horario": "15:00:00",
    "consumo_ml": 250,
    "consumo_total_hoje_ml": 1050,
    "meta_litros": 2.5,
    "litros_faltantes": 1.45,
    "percentual_atingido": 42.0
  }
}


#### Registra um novo consumo para o usuário e retorna o progresso atualizado.

### Histórico do Dia
Endpoint: /historico
Método: GET
Parâmetros:
- nome_usuario (string, obrigatório)
- data (string, obrigatório - formato YYYY-MM-DD)

Body:
{
  "nome_usuario": "joao.silva",
  "data": "2025-05-26"
}

Exemplo de Resposta:
{
  "mensagem": "Histórico de Victor em 2025-05-23:",
  "registros": [
    { "consumo_ml": 500, "horario": "09:00" },
    { "consumo_ml": 750, "horario": "14:30" }
  ],
  "progresso": {
    "consumo_total_hoje_ml": 1250,
    "meta_litros": 2.5,
    "litros_faltantes": 1.25,
    "percentual_atingido": 50.0
  }
}

#### Retorna o histórico completo de consumo de um dia específico, incluindo progresso.

### Registrar/Atualizar Meta
Endpoint: /meta
Método: POST
Body:
{
  "nome_usuario": "Victor",
  "peso_kg": 70
}

#### Calcula a meta diária (35ml por kg de peso) e registra/atualiza a meta do usuário.

 Exemplo de Resposta:
 {
  "mensagem": "Meta registrada com sucesso!",
  "dados": {
    "id": 1,
    "nome_usuario": "Victor",
    "meta_litros": 2.45
  }
}


### Progresso do Dia
Endpoint: /progresso
Método: GET
Parâmetro:
- nome_usuario (string, obrigatório)

Body:
{
  "nome_usuario": "joao.silva"
}

Exemplo de Resposta:
{
  "mensagem": "Progresso de Victor em 2025-05-24:",
  "dados": {
    "consumo_total_hoje_ml": 1250,
    "meta_litros": 2.5,
    "litros_faltantes": 1.25,
    "percentual_atingido": 50.0
  }
}

#### Retorna o progresso atual do usuário com base nos consumos registrados hoje.


### Dias com Registros
Endpoint: /registros
Método: GET
Parâmetro:
- nome_usuario (string, obrigatório)
Body:
{
  "nome_usuario": "joao.silva"
}


Exemplo de Resposta:
{
  "dias": [
    { "data": "2025-05-23", "objetivoAlcancado": true },
    { "data": "2025-05-24", "objetivoAlcancado": false }
  ]
}


#### Retorna uma lista de dias que têm registros de consumo, informando se a meta foi atingida.


# Schemas
Os **schemas** são responsáveis por definir a estrutura dos dados que serão enviados ou recebidos pela API. Eles são implementados utilizando **Pydantic** e garantem validações automáticas, além de facilitar a documentação das rotas.


## ** ConsumoDiarioCreateSchema**
**Descrição:** Representa o payload necessário para criar um novo registro de consumo.

**Campos:**
| Campo          | Tipo   | Descrição                                      |
|-----------------|--------|-----------------------------------------------|
| nome_usuario   | string | Nome do usuário que está registrando consumo   |
| consumo_ml     | float  | Quantidade de água consumida em mililitros     |


### ** ConsumoDiarioSchema**
**Descrição:** Define a estrutura de resposta para um registro de consumo.

**Campos:**
| Campo          | Tipo   | Descrição                                      |
|-----------------|--------|-----------------------------------------------|
| nome_usuario   | string | Nome do usuário                                |
| data           | string | Data do consumo no formato `YYYY-MM-DD`        |
| horario        | string | Horário do consumo no formato `HH:MM:SS`       |
| consumo_ml     | float  | Quantidade consumida em mililitros             |


### **MetaUsuarioCreateSchema**
**Descrição:** Representa o payload necessário para registrar ou atualizar a meta de consumo de um usuário.

**Campos:**
| Campo          | Tipo   | Descrição                                          |
|-----------------|--------|-----------------------------------------------------|
| nome_usuario   | string | Nome do usuário                                     |
| peso_kg        | float  | Peso do usuário em quilogramas (usado para calcular a meta) |


### **MetaUsuarioSchema**
**Descrição:** Define a estrutura de resposta ao registrar ou atualizar uma meta de consumo.

 **Campos:**
| Campo          | Tipo   | Descrição                                           |
|-----------------|--------|-----------------------------------------------------|
| id             | int    | ID da meta registrada                                |
| nome_usuario   | string | Nome do usuário                                      |
| meta_litros    | float  | Meta de litros de água recomendada para o usuário    |