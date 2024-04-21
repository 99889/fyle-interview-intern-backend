-- Write query to get number of assignments for each state

SELECT
    student_id,
    COUNT(*) AS num_graded_assignments
FROM
    assignments
WHERE
    state = 'GRADED'
GROUP BY
    student_id;
