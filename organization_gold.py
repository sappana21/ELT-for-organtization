# Databricks notebook source
import dlt
from pyspark.sql.functions import count, avg, sum, col

# COMMAND ----------

@dlt.table(name="gold_country_summary")
def gold_country_summary():
    return(
        dlt.read("org_silver")
        .groupBy("Country")
        .agg(
            count("*").alias("org_count"),
            avg("Number_of_employees").alias("avg_employees")
        ) .orderBy(col("org_count").desc())
    )
@dlt.table(name="gold_industry_summary")
def gold_industry_summary():
    return(
        dlt.read("org_silver")
        .groupBy("Industry")
        .agg(
            count("*").alias("org_count"),
            sum("Number_of_employees").alias("total_employees")
        ).orderBy(col("org_count").desc())
    )
