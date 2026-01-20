# Olist E-commerce Analysis

##  Contexto

Este projeto realiza uma análise exploratória de dados (EDA) utilizando **SQL e Python (Pandas, Matplotlib e Seaborn)** a partir do dataset público de e-commerce brasileiro da **Olist**. Devido aos insights relevados foram adicionado a análise de Cohort e Churn.

## Objetivo
O objetivo é entender o comportamento dos clientes, padrões de compra, retenção, churn e métricas de negócio relevantes para tomada de decisão.



## Métricas
- Valor médio do ticket
- ​​Frequência de compra
- Valor vitalício estimado (LTV)
- Retenção da coorte
- Taxa de cancelamento


---

## Visão Geral dos Dados

* **Total de pedidos:** 99.441
* **Total de clientes (registros):** 99.441
* **Total de clientes únicos (`customer_unique_id`):** 96.096
* **Total de produtos:** 32.951

### Insight inicial

A base apresenta uma relação próxima de **1:1 entre clientes e pedidos**, sugerindo um comportamento de compra pontual, no qual a maioria dos clientes realizou apenas um pedido durante o período analisado.

---

##  Status dos Pedidos

A grande maioria dos pedidos (**~97%**) foi entregue com sucesso, indicando uma operação logística bem estabelecida. Os pedidos cancelados ou indisponíveis representam uma parcela pequena do total, sugerindo que falhas de estoque, pagamento ou logística ocorrem de forma pontual.

Além disso, observa-se um número muito reduzido de pedidos em estágios iniciais do fluxo (created, approved, processing), indicando eficiência no processamento dos pedidos ao longo do funil.

---

##  Distribuição Geográfica dos Clientes

Observa-se uma forte concentração de clientes na **região Sudeste**, com destaque para o estado de **São Paulo**, que representa aproximadamente **42% da base total**. Os estados do Rio de Janeiro e Minas Gerais aparecem em seguida, reforçando a importância econômica da região para o negócio.

As regiões Sul e Sudeste concentram a maior parte dos clientes, enquanto os estados do Norte apresentam participação reduzida, indicando possíveis desafios logísticos ou menor penetração de mercado nessas regiões.

---

## Clientes Reais vs Registros

A base apresenta **99.441 registros de clientes**, mas apenas **96.096 clientes reais** (`customer_unique_id`), indicando que uma parcela dos clientes realizou mais de um pedido ao longo do período analisado.

Esse comportamento sugere oportunidades para estratégias de fidelização e aumento do **Lifetime Value (LTV)** dos clientes recorrentes.

---

## Análises de Negócio (SQL)

### Pergunta: Quais são as categorias de produtos mais vendidas?

As categorias com maior volume de vendas são **cama_mesa_banho**, **beleza_saude** e **esporte_lazer**, indicando preferência dos clientes por produtos de consumo recorrente e utilidades domésticas.

Esse padrão sugere uma base de clientes orientada a compras funcionais, com potencial para estratégias de **recompra** e **cross-sell**.

---

### Pergunta: Qual é o tempo médio de entrega dos pedidos?

O tempo médio de entrega dos pedidos foi de aproximadamente **12,6 dias**. Observa-se alta variabilidade entre pedidos, com entregas que variam de poucos dias até mais de 30 dias, indicando diferenças logísticas entre regiões e sellers.

---

### Pergunta: Como a receita se distribui entre os estados?

A receita está fortemente concentrada na **região Sudeste**, com destaque para **São Paulo**, que representa a maior parcela do faturamento total. Esse comportamento reflete tanto a densidade populacional quanto a maturidade do e-commerce na região.

---

### Pergunta: Qual é o ticket médio por pedido?

O ticket médio por pedido é de aproximadamente **R$ 160**, indicando um e-commerce de consumo intermediário, sem forte dependência de produtos de alto valor unitário.

---

##  Análises em Python (Pandas)

### Pergunta: Quanto um cliente gasta, em média, por pedido?

O ticket médio por pedido foi de aproximadamente **R$ 137,75**. Esse valor indica um e-commerce com foco em produtos de consumo intermediário.

Esse comportamento sugere oportunidades para estratégias de **upsell** e **cross-sell**, visando aumentar o valor médio das compras.

---

### Pergunta: Qual a proporção de clientes recorrentes?

A análise mostra que apenas **3,12%** dos clientes realizam mais de uma compra, indicando um comportamento predominantemente pontual.

Esse padrão reforça a necessidade de estratégias de **retenção**, como programas de fidelidade, campanhas de recompra e personalização de ofertas.

---

### Pergunta: Quanto tempo os clientes levam para recomprar?

A distribuição do tempo entre compras apresenta forte assimetria à direita, com concentração de recompras em curto prazo e uma cauda longa representando clientes que retornam após longos períodos.

* **Média:** ~78 dias (~2,5 meses)
* **Mediana:** 28 dias
* **Q1:** 0 dias (clientes que fizeram dois pedidos no mesmo dia)
* **Máximo:** 608 dias (~2 anos)

O baixo percentual de clientes recorrentes aliado ao longo intervalo médio entre compras sugere um **Lifetime Value limitado**, indicando oportunidades para estratégias de retenção e fidelização.

---

###  Pergunta: Qual é o Lifetime Value (LTV) médio dos clientes?

O **LTV médio estimado** é de **R$ 142,55**, fortemente impactado pela baixa frequência de compra (**1,03 pedidos por cliente**).

>  Este LTV é uma **estimativa simplificada**, calculada como ticket médio × frequência média de compra, e não considera margem, custos ou tempo de vida completo do cliente.

Esse resultado indica que a maior parte da receita é gerada na **primeira compra**, reforçando a dependência de aquisição de novos clientes.

---

##  Análise de Cohortes

###  Pergunta: Como a retenção evolui ao longo do tempo?

A matriz de retenção mostra que praticamente todos os cohorts apresentam retenção muito baixa após o primeiro mês (**< 1%**).

Esse comportamento indica um modelo de negócio com **compra pontual**, no qual o cliente realiza a compra por uma necessidade específica e não retorna com frequência. Esse padrão é típico de **marketplaces**, diferentemente de modelos de assinatura ou SaaS.

---

##  Churn (Perda de Clientes)

## Definição de cancelamento
Os clientes foram considerados como tendo cancelado a compra se realizaram apenas uma compra.


###  Pergunta: Qual é a taxa de churn dos clientes?

A análise de coortes evidenciou retenção muito baixa após o primeiro mês. Para aprofundar, foi calculada a taxa de churn considerando **90 dias sem recompra**.

A **taxa de churn em 90 dias foi de 30,37%**, confirmando um comportamento de compra pontual típico de marketplaces.

---

###  Pergunta: O churn varia por estado?

A análise de churn por estado mostrou taxas elevadas e homogêneas em todas as regiões, indicando que a baixa recorrência é um **padrão geral do marketplace**, e não um problema regional específico.

---

###  Pergunta: O churn varia por categoria de produto?

Categorias com **churn de 100%** correspondem majoritariamente a produtos de compra pontual ou sazonal, o que explica a ausência de recompra e reforça o perfil não recorrente do marketplace.

---

###  Pergunta: O tempo de entrega impacta o churn?

O tempo médio de entrega não apresentou diferença relevante entre clientes que churnaram e clientes retidos, sugerindo que a baixa recorrência está mais relacionada à **natureza pontual das compras** do que à experiência logística.

**Definições utilizadas:**

* Clientes retidos: realizaram mais de uma compra
* Clientes churn: não realizaram nova compra dentro de 90 dias após a primeira compra

---

##  Conclusão

O projeto evidencia que o e-commerce analisado possui um modelo fortemente orientado a **compras pontuais**, com baixa retenção e LTV limitado. Os resultados sugerem que estratégias de retenção, recompra e fidelização representam as principais oportunidades de geração de valor para o negócio.
