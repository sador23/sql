SELECT 
  applicants.first_name, 
  applicants.last_name, 
  applicants.phone_number
FROM 
  public.applicants
WHERE
  applicants.email LIKE '%@adipiscingenimmi.edu'

