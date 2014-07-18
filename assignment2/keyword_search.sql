CREATE VIEW keyword_view AS SELECT * FROM frequency
UNION
SELECT 'q' as docid, 'washington' as term, 1 as count
UNION
SELECT 'q' as docid, 'taxes' as term, 1 as count
UNION
SELECT 'q' as docid, 'treasury' as term, 1 as count;

SELECT SUM(A.count * B.count) as count
FROM keyword_view A
JOIN keyword_view B ON B.term = A.term
WHERE A.docid='q'
GROUP BY A.docid, B.docid
ORDER BY count DESC LIMIT 1;

DROP VIEW keyword_view;