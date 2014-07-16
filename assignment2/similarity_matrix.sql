SELECT F1.docid AS f1_docid, F2.docid as f2_docid, SUM(F1.count * F2.count) as count
FROM Frequency F1
JOIN Frequency F2 ON F2.term = F2.term
WHERE F1.docid='10080_txt_crude' AND F2.docid='17035_txt_earn'
GROUP By F1.docid, F2.docid
