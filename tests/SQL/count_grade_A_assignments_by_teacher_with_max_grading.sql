-- Write query to find the number of grade A's given by the teacher who has graded the most assignments

-- Finds Teacher id with max number of Graded assignments
WITH graded_assignments AS (
    SELECT
        teacher_id,
        COUNT(*) AS total_graded_assignments
    FROM
        assignments
    WHERE
        state = 'GRADED'
    GROUP BY
        teacher_id
),
grade_a_count AS (
    SELECT
        teacher_id,
        COUNT(*) AS grade_a_count
    FROM
        assignments
    WHERE
        state = 'GRADED'
        AND grade = 'A'
    GROUP BY
        teacher_id
)
SELECT
    ga.teacher_id,
    ga.total_graded_assignments,
    COALESCE(gac.grade_a_count, 0) AS grade_a_count
FROM
    graded_assignments ga
LEFT JOIN
    grade_a_count gac ON ga.teacher_id = gac.teacher_id
ORDER BY
    ga.total_graded_assignments DESC
LIMIT 1;
