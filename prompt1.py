PROMPT = [
    """Train a model to understand and execute SQL queries related to product data retrieval from various e-commerce platforms. 
    The goal is to extract information from rb_pdp_10, tb_fact_marketplace_sku_wise_sales_final2 
    and the names of the columns in these tables. 
   
   tb_fact_marketplace_sku_wise_sales_final2 -> this table is also known as sales data table

You also have to add a AND statment in the end of every query if someone like for amazon the below statement the mapping of these pf_id are as 
1:amazon,2:flipkart,3:bigbasket/bb,4:blinkit/grofers,5:amazon fresh,6:nykaa,7:purplle,8:jiomart,9:flipkart grocery,10:myntra,
12:instamart,13:dmart,14:flipkart special,15:hansaplast,16:zepto
 do for a specific pf only when it is told to otherwise dont include pf condition
The names of the columns in rb_pdp_10 are 

"pdp_data_id", "crawl_id", "pdp_crawl_date", "pf_id", "platform_name", "location_id", "location_name", "pincode", 
"pincode_area", "brand_id", "brand_name", "brand_category_id", "brand_category_name", "sku_id", "sku_name", "reseller_id", 
"reseller_name", "reseller_name_crawl", "reseller_type", "seller_rank", "seller_category", "msl", "cluster", "web_pid", 
"pdp_page_url", "pdp_image_url", "url_code", "rb_code", "ean_code", "group_id", "pantry_code", "osa", "osa_remark", 
"osa_last_available_date", "price_rp", "price_sp", "price_variation", "price_remark", "pdp_title_value", "pdp_desc_value", 
"pdp_image_count", "pdp_rating_value", "pdp_review_count", "pdp_rating_count", "pdp_qa_count", "pdp_title_char_count", 
"pdp_desc_char_count", "pdp_title_score", "pdp_desc_score", "pdp_image_score", "pdp_rating_score", "pdp_review_score", 
"pdp_bulletin_score", "pdp_bulletin_count", "pdp_total_score", "pdp_grade", "pdp_ec_image_score", "pdp_ec_image_count", 
"pdp_ec_video_score", "pdp_ec_video_count", "products_count_by_group", "compliance_title_score", "compliance_bullets_score", 
"compliance_description_score", "compliance_image_description_score", "compliance_image_score", "compliance_avg_score", 
"compliance_title_perc", "compliance_bullets_perc", "compliance_description_perc", "compliance_image_description_perc", 
"created_on", "created_by", "modified_on", "modified_by", "week", "month", "quarter", "year", "status", "sales", "rank_seller"

The names of the columns in tb_fact_marketplace_sku_wise_sales_final2 are 
  
marketplace, marketplace_id, city_id, web_pid, sku_description, date, year, quarter, weeknumber, reported_on, 
total_quantity, mrp, sales_price, total_sales, total_mrp, discount, discount_percentage, event_type, event, timeperiod, 
timeperiod_label, instock, bgr    
 
1. give total sales platform/marketplace/pf wise
SELECT marketplace, SUM(total_sales) AS total_sales FROM tb_fact_marketplace_sku_wise_sales_final2 GROUP BY marketplace_id;

3. give pf/platform wise stock availability last 10 days or give osa report 
SELECT
 platform_name AS Platform,
 MAX(CASE WHEN instock_date = CURRENT_DATE() THEN instock_percentage END) AS Today,
 MAX(CASE WHEN instock_date = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY) THEN instock_percentage END) AS Yesterday,
 MAX(CASE WHEN instock_date = DATE_SUB(CURRENT_DATE(), INTERVAL 2 DAY) THEN instock_percentage END) AS Two_days_ago,
 MAX(CASE WHEN instock_date = DATE_SUB(CURRENT_DATE(), INTERVAL 3 DAY) THEN instock_percentage END) AS Three_days_ago,
 MAX(CASE WHEN instock_date = DATE_SUB(CURRENT_DATE(), INTERVAL 4 DAY) THEN instock_percentage END) AS Four_days_ago,
 MAX(CASE WHEN instock_date = DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY) THEN instock_percentage END) AS Five_days_ago,
 MAX(CASE WHEN instock_date = DATE_SUB(CURRENT_DATE(), INTERVAL 6 DAY) THEN instock_percentage END) AS Six_days_ago,
 MAX(CASE WHEN instock_date = DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) THEN instock_percentage END) AS Seven_days_ago,
 MAX(CASE WHEN instock_date = DATE_SUB(CURRENT_DATE(), INTERVAL 8 DAY) THEN instock_percentage END) AS Eight_days_ago,
 MAX(CASE WHEN instock_date = DATE_SUB(CURRENT_DATE(), INTERVAL 9 DAY) THEN instock_percentage END) AS Nine_days_ago,
 MAX(CASE WHEN instock_date = DATE_SUB(CURRENT_DATE(), INTERVAL 10 DAY) THEN instock_percentage END) AS Ten_days_ago
 FROM (
 SELECT
        platform_name,
        DATE(created_on) AS instock_date,
        CONCAT(ROUND((SUM(osa) / COUNT(*)) * 100, 2), '%') AS instock_percentage
 FROM
        rb_pdp_10
 WHERE
        YEAR(created_on) = YEAR(NOW())
 GROUP BY
        platform_name,
        instock_date
 ) AS subquery
 GROUP BY
 platform_name;
 
4. give pincode/location wise stock availability last 10 days
SELECT
 location_name AS Location, pincode,
 MAX(CASE WHEN instock_date = CURRENT_DATE() THEN instock_percentage END) AS Today,
 MAX(CASE WHEN instock_date = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY) THEN instock_percentage END) AS Yesterday,
 MAX(CASE WHEN instock_date = DATE_SUB(CURRENT_DATE(), INTERVAL 2 DAY) THEN instock_percentage END) AS Two_days_ago,
 MAX(CASE WHEN instock_date = DATE_SUB(CURRENT_DATE(), INTERVAL 3 DAY) THEN instock_percentage END) AS Three_days_ago,
 MAX(CASE WHEN instock_date = DATE_SUB(CURRENT_DATE(), INTERVAL 4 DAY) THEN instock_percentage END) AS Four_days_ago,
 MAX(CASE WHEN instock_date = DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY) THEN instock_percentage END) AS Five_days_ago,
 MAX(CASE WHEN instock_date = DATE_SUB(CURRENT_DATE(), INTERVAL 6 DAY) THEN instock_percentage END) AS Six_days_ago,
 MAX(CASE WHEN instock_date = DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) THEN instock_percentage END) AS Seven_days_ago,
 MAX(CASE WHEN instock_date = DATE_SUB(CURRENT_DATE(), INTERVAL 8 DAY) THEN instock_percentage END) AS Eight_days_ago,
 MAX(CASE WHEN instock_date = DATE_SUB(CURRENT_DATE(), INTERVAL 9 DAY) THEN instock_percentage END) AS Nine_days_ago,
 MAX(CASE WHEN instock_date = DATE_SUB(CURRENT_DATE(), INTERVAL 10 DAY) THEN instock_percentage END) AS Ten_days_ago
 FROM (
 SELECT
        location_name, pincode,
        DATE(created_on) AS instock_date,
        CONCAT(ROUND((SUM(osa) / COUNT(*)) * 100, 2), '%') AS instock_percentage
 FROM
        rb_pdp_10
 WHERE
        YEAR(created_on) = YEAR(NOW())
        AND pf_id = 1            
 GROUP BY
        location_name,
        instock_date
 ) AS subquery
 GROUP BY
 location_name;
 
 5. give oos/out of stock report for a particular pf/platform or find details of particular platform for today or give detailed daily report for a particular platform and to do this just change the pf_id to that particular platform
 SELECT web_pid AS Product_ID, pdp_title_value AS Product_Name, pdp_page_url AS Page_URL, UPPER(brand_name) AS Brand, 
 pincode AS Pincode, location_name AS Location, osa_remark AS OSA_Remark, created_on as Date FROM rb_pdp_10 WHERE DATE(created_on) = DATE_SUB(CURRENT_DATE(), INTERVAL 0 DAY) AND pf_id = 10 AND msl = 1 and osa = 0;

6. give sos/share of search/keyword percentage report pf/platform wise 
   SELECT
   platform AS Platform,
   MAX(CASE WHEN sos_date = CURRENT_DATE() THEN SOS END) AS Today,
   MAX(CASE WHEN sos_date = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY) THEN SOS END) AS Yesterday,
   MAX(CASE WHEN sos_date = DATE_SUB(CURRENT_DATE(), INTERVAL 2 DAY) THEN SOS END) AS Two_days_ago,
   MAX(CASE WHEN sos_date = DATE_SUB(CURRENT_DATE(), INTERVAL 3 DAY) THEN SOS END) AS Three_days_ago,
   MAX(CASE WHEN sos_date = DATE_SUB(CURRENT_DATE(), INTERVAL 4 DAY) THEN SOS END) AS Four_days_ago,
   MAX(CASE WHEN sos_date = DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY) THEN SOS END) AS Five_days_ago,
   MAX(CASE WHEN sos_date = DATE_SUB(CURRENT_DATE(), INTERVAL 6 DAY) THEN SOS END) AS Six_days_ago,
   MAX(CASE WHEN sos_date = DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) THEN SOS END) AS Seven_days_ago,
   MAX(CASE WHEN sos_date = DATE_SUB(CURRENT_DATE(), INTERVAL 8 DAY) THEN SOS END) AS Eight_days_ago,
   MAX(CASE WHEN sos_date = DATE_SUB(CURRENT_DATE(), INTERVAL 9 DAY) THEN SOS END) AS Nine_days_ago,
   MAX(CASE WHEN sos_date = DATE_SUB(CURRENT_DATE(), INTERVAL 10 DAY) THEN SOS END) AS Ten_days_ago
   FROM (
   SELECT
      platform,
      DATE(created_on) AS sos_date,
      CONCAT(ROUND((COUNT(CASE WHEN brand_crawl = 'Nivea' THEN 1 END) / COUNT(*)) * 100, 2), '%') AS SOS
   FROM
      rb_kw_sos_overall_10
   WHERE
      YEAR(created_on) = YEAR(NOW())
   GROUP BY
      platform,
      sos_date
   ) AS subquery
   GROUP BY
   platform;

      7.Find those products which have 0 image count.
       Select * from rb_pdp_10 where date(created_on) = date(now())-1 and pdp_image_count = 0;

       8.Find those products which have been OOS for a week .
       SELECT pf_id, pincode, web_pid, pdp_title_value, pdp_page_url
       FROM (
       SELECT pf_id, pincode, web_pid, DATE(created_on), osa, pdp_title_value, pdp_page_url,
              ROW_NUMBER() OVER (PARTITION BY pf_id, pincode, web_pid ORDER BY DATE(created_on) DESC) AS rn
       FROM rb_pdp_10
       WHERE osa = 0 AND DATE(created_on) >= DATE_SUB(CURRENT_DATE()-1, INTERVAL 7 DAY)
       ) subquery
       WHERE rn = 7;

      9.Find list of those products which have more than 30% discount.
       Select * from rb_pdp_10 where date(created_on) = date(now())-1 and price_variation > 30;

       10. Give count of keyword platform/pf wise
       SELECT pf_id,COUNT(*),DATE(created_on) FROM rb_kw_sos_overall_10 WHERE DATE(created_on)=DATE_ADD(CURRENT_DATE(), INTERVAL -1 DAY) GROUP BY pf_id;

       11. Give distinct keyword platform/pf wise
       SELECT pf_id,COUNT(DISTINCT(keyword)),DATE(created_on) FROM rb_kw_sos_overall_10 WHERE DATE(created_on)=DATE_ADD(CURRENT_DATE(), INTERVAL 0 DAY) GROUP BY pf_id;

       12. Give average/avg rating platform wise for last 4 months month wise
       SELECT
       platform_name AS Platform,
       MAX(CASE WHEN instock_date = MONTH(CURRENT_DATE()) THEN average_rating END) AS Current_Month,
       MAX(CASE WHEN instock_date = MONTH(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH)) THEN average_rating END) AS Last_Month,
       MAX(CASE WHEN instock_date = MONTH(DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH)) THEN average_rating END) AS Two_Months_Ago,
       MAX(CASE WHEN instock_date = MONTH(DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH)) THEN average_rating END) AS Three_Months_Ago,
       MAX(CASE WHEN instock_date = MONTH(DATE_SUB(CURRENT_DATE(), INTERVAL 4 MONTH)) THEN average_rating END) AS Four_Months_Ago    
       FROM (
       SELECT
              platform_name,
              MONTH(created_on) AS instock_date,
              ROUND(AVG(pdp_rating_value), 2) AS average_rating
       FROM
              rb_pdp_10
       WHERE
              YEAR(created_on) = YEAR(NOW()) AND pdp_rating_value > 0 AND
              msl = 0
       GROUP BY
              platform_name,
              instock_date
       ) AS subquery
       GROUP BY
       platform_name;
       
       13. Give average/avg rating platform wise for today day wise
       SELECT
       platform_name AS Platform,
       ROUND(AVG(pdp_rating_value), 2) AS Average_Rating
       FROM rb_pdp_10
       WHERE
       DATE(created_on) = DATE(CURDATE()) AND pdp_rating_value > 0 AND msl = 0 
       GROUP BY
       platform_name;
       
       14. Give sku wise discount and if user says for a particular platform then write where condition using pf_id for that platform
       SELECT pf_id,sku_name,web_pid, MAX(price_variation) AS max_price_variation
       FROM rb_pdp_10 where pf_id = 10
       GROUP BY pf_id, web_pid;
       
       15. Give average/avg rating sku wise
       SELECT
       sku_name AS ProductName,
       web_pid AS ProductId,
       MAX(CASE WHEN instock_date = DATE_ADD(CURRENT_DATE(), INTERVAL 0 DAY) THEN average_rating END) AS Today,
       MAX(CASE WHEN instock_date = DATE_ADD(CURRENT_DATE(), INTERVAL -1 DAY) THEN average_rating END) AS Yesterday,
       MAX(CASE WHEN instock_date = DATE_ADD(CURRENT_DATE(), INTERVAL -2 DAY) THEN average_rating END) AS Two_Days_Ago,
       MAX(CASE WHEN instock_date = DATE_ADD(CURRENT_DATE(), INTERVAL -3 DAY) THEN average_rating END) AS Three_Days_Ago,
       MAX(CASE WHEN instock_date = DATE_ADD(CURRENT_DATE(), INTERVAL -4 DAY) THEN average_rating END) AS Four_Days_Ago    
       FROM (
       SELECT
              sku_name,
              web_pid,
              DATE(created_on) AS instock_date,
              ROUND(AVG(pdp_rating_value), 2) AS average_rating
       FROM
              rb_pdp_10
       WHERE
              YEAR(created_on) = YEAR(NOW()) AND pdp_rating_value > 0 AND
              msl = 0 AND web_pid = "B08DG11P3C"
       GROUP BY
              sku_name,
              instock_date
       ) AS subquery
       GROUP BY
       sku_name;

       16. give sku wise total sales of B00DRE0SPI product
       SELECT
          pf_id,
          web_pid,
          sku_name,
          sales,
          sos_rank,
          pincode,
          keyword,
          osa,
          created_on
      FROM
          product_overall_data_final WHERE pf_id IN(1,2) AND created_on = "2024-04-29" AND web_pid = "B00DRE0SPI"
      ORDER BY
      pf_id limit 100;

      17. Give pincode wise sales in Amazon
      SELECT * FROM tb_wh_geosales WHERE orderYear = "2023" AND web_pid IN ("B0154BS40W", "B00FRDAAUA", "B00NW7NTTW", "B00IJ72QWQ", "B07VKM2HR5") AND pincode IN ("600064", "700159", "201009");
    Ensure the model can comprehend and execute queries with the DATE() and CURDATE() functions, and handle variations in table and column names for different e-commerce platforms should not contain triple backticks in the beginning or end.\n"""
  ]