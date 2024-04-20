-- Write query to find the number of grade A's given by the teacher who has graded the most assignments

--  Finds Teacher id with max number of Graded assignments
WITH MAXGRADER AS (SELECT 
    teacher_id, COUNT(state) as teacher_grade_count 
FROM 
   assignments 
WHERE
   state = "GRADED"
GROUP By 
   teacher_id 
ORDER BY
   teacher_grade_count DESC 
 LIMIT 1
 )
 
--  Counts the number of assignment with grade A of MAXGRADER teacher
 SELECT 
  COUNT(*)
 FROM 
   assignments 
 Where 
    grade = "A" and teacher_id = (SELECT teacher_id FROM Maxgrader)
