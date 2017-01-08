-- Arsenio, an applicant called us, that he and his friend applied to Codecool.
-- They both want to cancel the process, because they got an investor for the site they run: mauriseu.net

-- Write DELETE query to remove all the applicants, who applied with emails for this domain. (e-mail address has this domain after the @ sign)
-- After the DELETE, write a COUNT SELECT query to check the result: search for all applicants with this e-mail domain.

DELETE FROM public.applicants WHERE applicants.email LIKE '%mauriseu.net';
SELECT COUNT(applicants.first_name) WHERE applicants.email LIKE '%mauriseu.net';
