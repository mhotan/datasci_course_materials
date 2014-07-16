select count(*)
    FROM (select docid, sum(count) as terms
        from Frequency
        group by docid
        having sum(count) > 300);