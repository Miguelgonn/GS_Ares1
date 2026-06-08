# 🚀 GS-ARES-1 — Sistema Inteligente de Monitoramento de uma Base Autônoma em Marte

## 👥 Equipe

| Nome | RM |
|------|----|
| Ana Gabriela     | rm571312 |
| Felipe Reges     | rm570534 |
| Kaique           | rm570533 |
| Miguel Antunes   | rm573643 |
| Miguel Gonçalves | rm573793 |



# 📖 Resumo do Problema

As missões espaciais modernas dependem de sistemas inteligentes capazes de monitorar continuamente recursos críticos, detectar falhas operacionais e auxiliar na tomada de decisões em tempo real.

O projeto **ARES-1** simula uma base autônoma localizada em Marte que enfrenta uma tempestade de poeira severa. Durante esse evento, a geração solar diminui drasticamente, a comunicação com a Terra é comprometida, os níveis de radiação aumentam e um sensor apresenta leituras inconsistentes.

O sistema desenvolvido é responsável por:

- Ler dados de telemetria de um arquivo CSV;
- Monitorar módulos críticos da missão;
- Detectar situações de alerta e falha;
- Identificar inconsistências em sensores;
- Gerar alertas automáticos;
- Prever o comportamento da reserva energética;
- Emitir recomendações operacionais priorizadas.



# 🎯 Objetivo

Desenvolver um sistema inteligente de monitoramento operacional capaz de interpretar dados de uma missão espacial experimental, diagnosticar situações críticas, prever riscos futuros e auxiliar na tomada de decisões para garantir a sobrevivência da missão.



# 🗂 Estruturas de Dados Utilizadas

## 1. Listas

Utilizadas para armazenar séries temporais de:

- geração de energia;
- consumo energético;
- reserva energética;
- horários das leituras.

Exemplo:

```python
lista_geracao = [10, 30, 45, 40, 20, 8]
lista_consumo = [45, 48, 52, 58, 62, 65]
```

Permitem análise cronológica e aplicação da regressão linear.



## 2. Fila (FIFO)

Utilizada para armazenar alertas pendentes.

O primeiro alerta recebido é o primeiro a ser tratado.

Exemplo:

```python
fila_alertas = []
```

Aplicação:

- tempestade de poeira;
- falha de comunicação;
- reserva energética crítica.



## 3. Pilha (LIFO)

Utilizada para registrar eventos críticos analisados.

O evento mais recente possui prioridade de consulta.

Exemplo:

```python
pilha_criticos = []
```

Aplicação:

- falha de comunicação;
- erro de sensor.



## 4. Dicionário (Tabela Hash)

Utilizado para acesso rápido aos módulos da missão.

```python
{
    "suporte_vida": 1,
    "energia": 1,
    "comunicacao": 0,
    "habitat": 1
}
```

Benefício:

- busca em tempo constante O(1).



## 5. Hierarquia (Árvore)

Representa a estrutura organizacional da missão.

```text
ARES-1
├── Energia
│   ├── Solar
│   └── Bateria
├── Habitat
│   ├── Oxigênio
│   ├── Temperatura
│   └── Comunicação
└── Ciência
    ├── Laboratório
    └── Armazenamento
```

---

## 6. Matriz

Representa as leituras energéticas ao longo do tempo.

| Hora | Geração | Consumo | Reserva |
|--------|--------|--------|--------|
| 06:00 | 10 | 45 | 80 |
| 08:00 | 30 | 48 | 75 |
| 10:00 | 45 | 52 | 68 |
| 12:00 | 40 | 58 | 55 |
| 14:00 | 20 | 62 | 38 |
| 16:00 | 8 | 65 | 22 |



# 🧠 Regras Lógicas do Diagnóstico

O sistema utiliza estruturas:

- IF
- ELIF
- ELSE
- AND
- OR
- NOT

## Expressão Booleana Principal

```text
CRITICO =
(suporte_vida == 0)
OR
(energia == 0)
OR
(reserva < 25)
OR
(radiacao > 3.0 AND comunicacao == 0)

ALERTA =
(comunicacao == 0)
OR
(reserva < 50)
OR
(radiacao > 2.0)
OR
(NOT laboratorio)

NORMAL =
NOT CRITICO AND NOT ALERTA
```



## Regras Implementadas

| Regra | Operadores | Resultado |
|---------|-----------|-----------|
| Falha simultânea em suporte à vida e energia | AND | CRÍTICO |
| Reserva abaixo de 25% | AND | CRÍTICO |
| Radiação elevada e comunicação indisponível | AND | CRÍTICO |
| Comunicação indisponível ou qualidade abaixo de 20% | OR | CRÍTICO |
| Laboratório desligado | NOT | ALERTA |


# 🚨 Alertas Automáticos

O sistema classifica eventos em três níveis:

| Nível | Significado |
|---------|------------|
| NORMAL | Operação estável |
| ALERTA | Atenção necessária |
| CRÍTICO | Risco imediato para a missão |

Exemplos detectados:

- Falha no módulo de comunicação;
- Radiação acima do limite seguro;
- Reserva energética abaixo do mínimo;
- Sensor defeituoso.



# 🔍 Detecção de Inconsistências

Foi inserida propositalmente uma inconsistência para testar o sistema.

### Sensor TI-04

```text
Temperatura interna = 847°C
```

Resultado:

```text
ERRO: valor fisicamente impossível para um habitat habitado.
```

Ação tomada:

```text
Sensor marcado como defeituoso.
Utilização da última leitura válida (22°C).
```



# 📈 Técnica de Previsão

## Método

Regressão Linear Simples.

Implementada manualmente sem uso de:

- NumPy;
- Pandas;
- Scikit-Learn.



## Variável Analisada

Reserva de Energia (%)

Dados utilizados:

```text
80%
75%
68%
55%
38%
22%
```

Modelo:

```text
Y = a + bX
```

Onde:

```text
b = Σ(xi-x̄)(yi-ȳ) / Σ(xi-x̄)²
a = ȳ - b·x̄
```



## Resultado Obtido

- Taxa média de queda: -11,83% por ciclo
- Reserva atual: 22%
- Reserva prevista para o próximo ciclo: 14,9%
- Esgotamento total previsto em aproximadamente 1,3 ciclos

---

## Impacto na Decisão

A previsão energética influencia diretamente as recomendações automáticas emitidas pelo sistema.

Como a reserva prevista é inferior a 15%, o sistema recomenda:

- ativação do modo de hibernação;
- desligamento de sistemas não essenciais;
- priorização do suporte à vida.



# ▶️ Como Executar

## Estrutura do Projeto

```text
ARES-1/
│
├── src/
│   └── sistema.py
│
├── data/
│   └── dados.csv
│
├── docs/
│   ├── relatorio.pdf
│   ├── link_video.txt
│   └── uso_ia.md
│
└── README.md
```

## Executar

```bash
python src/sistema.py
```


# 📥 Exemplo de Entrada

```text
Comunicação = OFF
Reserva = 22%
Radiação = 4.7 mSv/h
Qualidade da comunicação = 15%
Temperatura sensor TI-04 = 847°C
```



# 📤 Exemplo de Saída

```text
STATUS GERAL DA MISSÃO: CRÍTICO

[CRÍTICO]
Reserva energética abaixo do mínimo.

[CRÍTICO]
Comunicação comprometida.

[CRÍTICO]
Radiação elevada.

[ERRO]
Sensor TI-04 retornou leitura inválida.
```



# 🛠 Recomendações Geradas

1. Manter suporte à vida ativo.
2. Ativar comunicação de emergência.
3. Direcionar energia para sistemas essenciais.
4. Desligar laboratório e equipamentos não prioritários.
5. Abrigar tripulação contra radiação.
6. Iniciar modo de hibernação energética.
7. Registrar eventos para análise posterior.
8. Verificar sensor TI-04.



# 🎥 Vídeo de Apresentação

Link:

```text
COLE_AQUI_O_LINK_DO_YOUTUBE
```



# 📚 Conclusões e Aprendizados

O projeto ARES-1 permitiu aplicar de forma integrada os conteúdos das três primeiras fases do curso, incluindo estruturas de dados, lógica computacional, análise de dados e técnicas simples de inteligência artificial.

O sistema foi capaz de interpretar dados de telemetria, detectar falhas críticas, identificar inconsistências em sensores, prever o comportamento energético da missão e gerar recomendações automáticas justificadas pelos dados.

A implementação da regressão linear sem bibliotecas externas reforçou a compreensão matemática do método, enquanto o uso de filas, pilhas, dicionários, hierarquias e matrizes demonstrou a importância da escolha adequada das estruturas de dados para resolver problemas reais de engenharia e monitoramento espacial.
