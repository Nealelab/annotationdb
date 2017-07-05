WITH RECURSIVE doctree AS (
	
    WITH 
	
	bridge_table AS (
        SELECT parent, annotation, 1 AS is_struct
        FROM docs
		
        UNION ALL
		
        SELECT parent, annotation, 0 AS is_struct
        FROM annotations
    ),
	
	full_table AS (
	    SELECT bt.parent, bt.annotation, bt.is_struct, d.text, d.study_link, d.study_data, d.study_title, d.free_text, d.selectable
		FROM bridge_table AS bt LEFT JOIN docs AS d
		    ON bt.annotation = d.annotation
	)

    SELECT *, 0 as depth
    FROM full_table
    WHERE annotation = 'va'
	
    UNION ALL
	
    SELECT b.*, t.depth + 1 AS depth
    FROM full_table AS b INNER JOIN doctree AS t
        ON b.parent = t.annotation
)

SELECT *
FROM doctree