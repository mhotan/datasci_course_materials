SELECT A.docid as docid, B.docid as docid, SUM(A.count * B.count) as count
FROM Frequency A
JOIN Frequency B ON B.term = A.term
WHERE A.docid='10080_txt_crude' AND B.docid='17035_txt_earn'
GROUP BY A.docid, B.docid