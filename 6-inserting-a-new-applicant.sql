INSERT INTO public.applicants
  VALUES(11,'Markus','Schaffarzyk','003620/725-2666','djnovus@groovecoverage.com',54823);
SELECT applicants.application_code FROM public.applicants WHERE applicants.application_code=54823;