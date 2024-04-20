-- Write query to get number of assignments for each state

SELECT 
   state, COUNT(*) As Number_of_Assignments
 FROM 
   assignments
 GROUP BY
   state
