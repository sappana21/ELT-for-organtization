# Databricks notebook source
import dlt


# COMMAND ----------

@dlt.table(name="org_silver")
def org_silver():
    return(
        dlt.read("org_bronze")
        .select(
            "Organization_Id",
            "Country",
            "Founded",
            "Number_of_employees",
            "Industry"

        ).dropDuplicates(["Organization_Id"])
    )