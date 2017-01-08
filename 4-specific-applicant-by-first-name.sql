SELECT
  CONCAT(applicants.last_name,' ',applicants.first_name),
  applicants.phone_number
FROM 
  public.applicants
WHERE
  public.applicants.first_name='Carol';
