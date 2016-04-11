# EDA

SELECT distinct(specialty_desc) 
FROM npi_drug_13;

# 202 distinct specialties

SELECT count(distinct(NPI)) 
FROM npi_drug_13;

# 808020 distinct npi's total

SELECT count(DISTINCT(NPI)) 
FROM npi_drug_13 
WHERE specialty_desc ='General Practice';

# 8987 distinct npi's in general practice

SELECT specialty_desc, count(distinct(NPI)) as cnt
FROM npi_drug_13
GROUP BY specialty_desc
ORDER BY cnt DESC;

                                      specialty_desc                                        |  cnt
---------------------------------------------------------------------------------------------+--------
 Internal Medicine                                                                           | 104792
 Family Practice                                                                             |  95049
 Dentist                                                                                     |  87034
 Nurse Practitioner                                                                          |  74193
 Physician Assistant                                                                         |  53852
 Emergency Medicine                                                                          |  34628
 Obstetrics/Gynecology                                                                       |  24945
 Psychiatry                                                                                  |  23605
 Cardiology                                                                                  |  21948
 Orthopedic Surgery                                                                          |  19539
 Optometry                                                                                   |  18107
 Ophthalmology                                                                               |  18057
 General Surgery                                                                             |  17252
 Student in an Organized Health Care Education/Training Program                              |  16580
 Podiatry                                                                                    |  12542
 Gastroenterology                                                                            |  12234
 Neurology                                                                                   |  12194
 Dermatology                                                                                 |  11262
 Urology                                                                                     |   9894
 General Practice                                                                            |   8987
 Otolaryngology                                                                              |   8919
 Psychiatry & Neurology                                                                      |   8770
 Pulmonary Disease                                                                           |   8326
 Nephrology                                                                                  |   7591
 Hematology/Oncology                                                                         |   7351
 Physical Medicine and Rehabilitation                                                        |   6646
 Pediatric Medicine                                                                          |   5507
 Endocrinology                                                                               |   5076
 Oral Surgery (dentists only)                                                                |   4931
 Anesthesiology                                                                              |   4379
 Infectious Disease                                                                          |   4296
 Rheumatology                                                                                |   4261
 Pharmacist                                                                                  |   4055
 Allergy/Immunology                                                                          |   3469
 Neurosurgery                                                                                |   3253
 Plastic and Reconstructive Surgery                                                          |   3248
 Radiation Oncology                                                                          |   2890
 Medical Oncology                                                                            |   2515
 Vascular Surgery                                                                            |   2455
 Certified Clinical Nurse Specialist                                                         |   2078
 Specialist                                                                                  |   1980
 Diagnostic Radiology                                                                        |   1938
 Interventional Pain Management                                                              |   1865
 Geriatric Medicine                                                                          |   1821
 Neuropsychiatry                                                                             |   1524
 Pain Management                                                                             |   1359
 Cardiac Electrophysiology                                                                   |   1275
 Thoracic Surgery                                                                            |   1274
 Maxillofacial Surgery                                                                       |   1196
 Colorectal Surgery (formerly proctology)                                                    |   1128
 Hand Surgery                                                                                |   1096
 Orthopaedic Surgery                                                                         |   1035
 Cardiac Surgery                                                                             |   1014
 Critical Care (Intensivists)                                                                |    935
 Gynecological/Oncology                                                                      |    787



SELECT count(*) 
FROM npi_drug_13

#23650520

CREATE TABLE npi_drug_13_internal_med AS (
	SELECT *
	FROM npi_drug_13
	WHERE specialty_desc = 'Internal Medicine');
