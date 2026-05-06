# %%
# CodeGrade step0
# Run this cell without changes

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# %%
# CodeGrade step1
df_boston = pd.read_sql("""
SELECT employees.firstName, employees.lastName, employees.jobTitle FROM employees
JOIN offices ON employees.officeCode = offices.officeCode
WHERE offices.city = 'Boston'
""", conn)

# %%
# CodeGrade step2
df_zero_emp = pd.read_sql("""
SELECT offices.officeCode FROM offices
LEFT JOIN employees ON offices.officeCode = employees.officeCode
WHERE employees.officeCode IS NULL
""", conn)

# %%
# CodeGrade step3
df_employee = pd.read_sql("""
SELECT employees.firstName, employees.lastName, offices.city, offices.state FROM employees
LEFT JOIN offices ON employees.officeCode = offices.officeCode
ORDER BY employees.firstName, employees.lastName;
""", conn)

# %%
# CodeGrade step4
df_contacts = pd.read_sql("""
SELECT customers.contactFirstName, customers.contactLastName, customers.phone, customers.salesRepEmployeeNumber 
FROM customers
LEFT JOIN orders ON customers.customerNumber = orders.customerNumber
WHERE orders.orderNumber IS NULL
ORDER BY customers.contactLastName
""", conn)

# %%
# CodeGrade step5
df_payment = pd.read_sql("""
SELECT customers.contactFirstName, customers.contactLastName, payments.amount, payments.paymentDate
FROM customers
JOIN payments ON customers.customerNumber = payments.customerNumber
ORDER BY CAST(payments.amount AS REAL) DESC
""", conn)

# %%
# CodeGrade step6
df_credit = pd.read_sql("""
SELECT employees.employeeNumber, employees.firstName, employees.lastName, COUNT(customers.customerNumber) as numCustomers
FROM employees
JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY employees.employeeNumber, employees.firstName, employees.lastName
HAVING AVG(customers.creditLimit) > 90000
ORDER BY COUNT(customers.customerNumber) DESC
""", conn)

# %%
# CodeGrade step7
df_products_sold = pd.read_sql("""
SELECT products.productName, COUNT(DISTINCT orders.orderNumber) as numorders, SUM(orderdetails.quantityOrdered) as totalunits
FROM products
JOIN orderdetails ON products.productCode = orderdetails.productCode
JOIN orders ON orderdetails.orderNumber = orders.orderNumber
GROUP BY products.productCode, products.productName
ORDER BY totalunits DESC
""", conn)

# %%
# CodeGrade step8
df_total_customers = pd.read_sql("""
SELECT products.productName, products.productCode, COUNT(DISTINCT customers.customerNumber) as numpurchasers
FROM products
JOIN orderdetails ON products.productCode = orderdetails.productCode
JOIN orders ON orderdetails.orderNumber = orders.orderNumber
JOIN customers ON orders.customerNumber = customers.customerNumber
GROUP BY products.productCode, products.productName
ORDER BY numpurchasers DESC
""", conn)

# %%
# CodeGrade step9
df_customers = pd.read_sql("""
SELECT COUNT(DISTINCT customers.customerNumber) as n_customers, offices.officeCode, offices.city
FROM offices
JOIN employees ON offices.officeCode = employees.officeCode
JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY offices.officeCode, offices.city
ORDER BY offices.officeCode
""", conn)

# %%
# CodeGrade step10
df_under_20 = pd.read_sql("""
SELECT DISTINCT employees.employeeNumber, employees.firstName, employees.lastName, offices.city, offices.officeCode
FROM employees
JOIN offices ON employees.officeCode = offices.officeCode
JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
JOIN orders ON customers.customerNumber = orders.customerNumber
JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
JOIN products ON orderdetails.productCode = products.productCode
WHERE products.productCode IN (
    SELECT products.productCode
    FROM products
    JOIN orderdetails ON products.productCode = orderdetails.productCode
    JOIN orders ON orderdetails.orderNumber = orders.orderNumber
    GROUP BY products.productCode
    HAVING COUNT(DISTINCT orders.customerNumber) < 20
)
ORDER BY employees.lastName
""", conn)

# %%
conn.close()


