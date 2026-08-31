# Databricks notebook source
import dlt
from pyspark.sql.functions import *


# COMMAND ----------

@dlt.table(name="org_bronze")
def org_bronze():
    return(
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format","CSV")
        .option("header","true")
        .option("inferSchema","true")
        .load("/Volumes/my_catalog/sapana/csv/sample/")
        .withColumn("ingestion_time",current_timestamp())
    )