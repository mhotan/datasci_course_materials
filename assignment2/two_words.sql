SELECT DISTINCT(r.docid)
FROM ((SELECT * FROM Frequency WHERE 'transactions'=term) a JOIN (SELECT * FROM Frequency WHERE 'world'=term) b 
	ON a.docid = b.docid) as r