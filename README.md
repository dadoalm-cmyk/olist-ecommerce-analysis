# Olist E-commerce Analysis

## Context

This project performs an Exploratory Data Analysis (EDA) using **SQL and Python (Pandas, Matplotlib, and Seaborn)** based on the public Brazilian e-commerce dataset from **Olist**. Due to the insights revealed, Cohort Analysis and Churn Analysis were also added.

## Objective

The objective is to understand customer behavior, purchasing patterns, retention, churn, and relevant business metrics for decision-making.

## Metrics

* Average Order Value
* Purchase Frequency
* Estimated Lifetime Value (LTV)
* Cohort Retention
* Churn Rate

---

## Data Overview

* **Total orders:** 99,441
* **Total customers (records):** 99,441
* **Total unique customers (`customer_unique_id`):** 96,096
* **Total products:** 32,951

### Initial Insight

The dataset presents a nearly **1:1 relationship between customers and orders**, suggesting a one-time purchase behavior, where most customers placed only a single order during the analyzed period.

---

## Order Status

The vast majority of orders (**~97%**) were successfully delivered, indicating a well-established logistics operation. Canceled or unavailable orders represent a small portion of the total, suggesting that inventory, payment, or logistics failures occur only occasionally.

Additionally, there is a very small number of orders in the initial stages of the process (created, approved, processing), indicating efficiency in order processing throughout the funnel.

---

## Customer Geographic Distribution

There is a strong concentration of customers in the **Southeast region**, particularly in the state of **São Paulo**, which represents approximately **42% of the total customer base**. The states of Rio de Janeiro and Minas Gerais follow, reinforcing the region's economic importance to the business.

The South and Southeast regions account for most customers, while Northern states have lower participation, indicating possible logistical challenges or lower market penetration in these areas.

---

## Real Customers vs. Customer Records

The dataset contains **99,441 customer records**, but only **96,096 unique customers** (`customer_unique_id`), indicating that some customers placed more than one order during the analyzed period.

This behavior suggests opportunities for customer loyalty strategies and increasing the **Customer Lifetime Value (LTV)** of returning customers.

---

## Business Analysis (SQL)

### Question: Which product categories sell the most?

The categories with the highest sales volume are **bed_bath_table**, **health_beauty**, and **sports_leisure**, indicating customer preference for recurring-consumption products and household essentials.

This pattern suggests a customer base focused on functional purchases, with potential opportunities for **repurchase** and **cross-selling** strategies.

---

### Question: What is the average delivery time?

The average delivery time was approximately **12.6 days**. There is considerable variability among orders, with deliveries ranging from a few days to more than 30 days, indicating logistical differences across regions and sellers.

---

### Question: How is revenue distributed across states?

Revenue is heavily concentrated in the **Southeast region**, especially in **São Paulo**, which represents the largest share of total revenue. This behavior reflects both population density and the maturity of e-commerce in the region.

---

### Question: What is the average order value?

The average order value is approximately **R$160**, indicating an e-commerce business focused on mid-range consumer products, without a strong dependence on high-ticket items.

---

## Python Analysis (Pandas)

### Question: How much does a customer spend on average per order?

The average order value per order was approximately **R$137.75**. This indicates an e-commerce business focused on mid-range consumer products.

This behavior suggests opportunities for **upselling** and **cross-selling** strategies aimed at increasing the average purchase value.

---

### Question: What is the proportion of repeat customers?

The analysis shows that only **3.12%** of customers made more than one purchase, indicating a predominantly one-time purchase behavior.

This pattern reinforces the need for **retention strategies**, such as loyalty programs, repurchase campaigns, and personalized offers.

---

### Question: How long do customers take to make a repeat purchase?

The distribution of time between purchases is highly right-skewed, with repeat purchases concentrated in short periods and a long tail representing customers who return after extended periods.

* **Mean:** ~78 days (~2.5 months)
* **Median:** 28 days
* **Q1:** 0 days (customers who placed two orders on the same day)
* **Maximum:** 608 days (~2 years)

The low percentage of repeat customers combined with the long average interval between purchases suggests a **limited Lifetime Value**, highlighting opportunities for retention and loyalty strategies.

---

### Question: What is the average Customer Lifetime Value (LTV)?

The estimated **average LTV** is **R$142.55**, heavily impacted by the low purchase frequency (**1.03 orders per customer**).

> This LTV is a **simplified estimate**, calculated as average order value × average purchase frequency, and does not consider margins, costs, or the customer's full lifetime.

This result indicates that most revenue is generated from the **first purchase**, reinforcing the company's dependence on acquiring new customers.

---

## Cohort Analysis

### Question: How does retention evolve over time?

The retention matrix shows that virtually all cohorts experience very low retention after the first month (**<1%**).

This behavior indicates a business model driven by **one-time purchases**, where customers buy to satisfy a specific need and do not frequently return. This pattern is typical of **marketplaces**, unlike subscription-based or SaaS business models.

---

## Churn Analysis

## Churn Definition

Customers were considered churned if they made only one purchase.

### Question: What is the customer churn rate?

The cohort analysis revealed very low retention after the first month. To investigate further, the churn rate was calculated considering **90 days without a repeat purchase**.

The **90-day churn rate was 30.37%**, confirming the one-time purchase behavior typical of marketplaces.

---

### Question: Does churn vary by state?

The churn analysis by state showed high and relatively homogeneous rates across all regions, indicating that low repeat purchasing is a **general marketplace pattern**, rather than a region-specific issue.

---

### Question: Does churn vary by product category?

Categories with **100% churn** mostly correspond to products with one-time or seasonal purchase behavior, which explains the absence of repeat purchases and reinforces the marketplace's non-recurring nature.

---

### Question: Does delivery time impact churn?

The average delivery time did not show any significant difference between churned and retained customers, suggesting that low repeat purchasing is more related to the **one-time nature of purchases** than to the logistics experience.

**Definitions used:**

* Retained customers: made more than one purchase
* Churned customers: did not make another purchase within 90 days after their first purchase

---

## Conclusion

This project demonstrates that the analyzed e-commerce business is strongly driven by **one-time purchases**, with low retention and limited LTV. The results suggest that retention, repurchase, and customer loyalty strategies represent the main opportunities for generating additional business value.
