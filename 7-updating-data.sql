-- Jemima Foreman, an applicant called us, that her phone number changed to: 003670/223-7459
-- Write an UPDATE query, that changes this data in the database for this applicant.
-- Also, write a SELECT query, that checks the phone_number column of this applicant.
-- Use both of her name partsin the conditions!

UPDATE public.applicants
  SET applicants.phone_number='003670/223-7459'
WHERE applicants.first_name='Jemina' AND applicants.last_name='Foreman';
SELECT applicants.phone_number FROM public.applicants WHERE phone_number='003670/223-7459';
