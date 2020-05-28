import bq_helper
from bq_helper import BigQueryHelper
stackOverflow = bq_helper.BigQueryHelper(active_project="bigquery-public-data",
                                   dataset_name="stackoverflow")

bq_assistant = BigQueryHelper("bigquery-public-data", "stackoverflow")
# print(bq_assistant.list_tables())

# print(bq_assistant.head("comments", num_rows=20))

query1 = """SELECT
  EXTRACT(YEAR FROM creation_date) AS Year,
  COUNT(*) AS Number_of_Questions,
  ROUND(100 * SUM(IF(answer_count > 0, 1, 0)) / COUNT(*), 1) AS Percent_Questions_with_Answers
FROM
  `bigquery-public-data.stackoverflow.posts_questions`
GROUP BY
  Year
HAVING
  Year > 2008 AND Year < 2016
ORDER BY
  Year;
        """
response1 = stackOverflow.query_to_pandas_safe(query1)

print(response1.head(10))