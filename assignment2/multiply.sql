SELECT value 
FROM(SELECT A.row_num as row_num, B.col_num as col_num, SUM(A.value * B.value) as value
FROM A
JOIN B ON B.row_num = A.col_num
GROUP BY A.row_num, B.col_num)
WHERE row_num=2 AND col_num=3