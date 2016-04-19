import pandas as pd 
import numpy as np 

def norm_agg_payments(df):
    """
    Takes pandas df of county aggregated data and normalizes/cleans necessary columns (by unique_bene)
    """

    sum_cols = ['num_hcpcs',
                'num_services',
                'total_submitted_charges',
                'total_medicare_allowed_amt',
                'total_medicare_payment_amt',
                #'num_hcpcs_associated_drug_srvc',
                #'num_drug_srvc',
                #'num_unique_bene_with_drug_srvc',
                'total_drug_submitted_charges', 
                'total_drug_medicare_allowed_amt',
                'total_drug_medicare_payment_amt',
                'num_hcpcs_associated_med_srvc',
                'num_med_srvc', 
                'num_unique_bene_with_med_srvc', 
                'total_med_submitted_charges',
                'total_med_medicare_allowed_amt', 
                'total_med_medicare_payment_amt',
                'num_bene_le65',
                'num_bene_65to74',
                'num_bene_75to84',
                'num_bene_ge84', 
                'num_female', 
                'num_male',
                'num_non_his_white',
                'num_african_american',
                'num_asian',
                'num_hispanic', 
                'num_american_indian', 
                #'num_no_race',
                'num_asthma', 
                'num_alzheimers_dementia',
                'num_artrial_fibrillation',
                'num_cancer',
                'num_chronic_obstructive_pulmonary',
                'num_depression',
                'num_diabetes',
                'num_heart_failure',
                'num_hypertension',
                'num_ischemic_heart',
                'num_osteoporosis',
                'num_rheumatoid_arthritis_osteoarthirtis',
                'num_schizophrenia_psychotic',
                'num_stroke',
                'total_age',
                'total_hcc_risk'
                ]
    for name in sum_cols:
        df['{}_norm'.format(name)] = df[name].divide(df['num_unique_bene']) 

def create_health_set(df_payments, df_county_ranks):
    pay_cols = ['county_fips',
                'num_hcpcs_norm',
                'num_services_norm',
                'total_submitted_charges_norm',
                'total_medicare_payment_amt_norm',
                'total_drug_submitted_charges_norm',
                'total_drug_medicare_payment_amt_norm',
                'num_hcpcs_associated_med_srvc_norm',
                'num_med_srvc_norm',
                'total_med_submitted_charges_norm',
                'total_med_medicare_payment_amt_norm',
                'num_asthma_norm',
                'num_alzheimers_dementia_norm',
                'num_artrial_fibrillation_norm',
                'num_cancer_norm',
                'num_chronic_obstructive_pulmonary_norm',
                'num_depression_norm',
                'num_diabetes_norm',
                'num_heart_failure_norm',
                'num_hypertension_norm',
                'num_ischemic_heart_norm',
                'num_osteoporosis_norm',
                'num_rheumatoid_arthritis_osteoarthirtis_norm',
                'num_schizophrenia_psychotic_norm',
                'num_stroke_norm',
                'total_hcc_risk_norm',
                ]

    ranks_cols =    [  
                    'county',
                    'Poor or fair health_% Fair/Poor',
                    'Poor mental health days_Mentally Unhealthy Days',
                    'Smokers_% Smokers',
                    'Adult obesity_% Obese',
                    'Physical inactivity_% Physically Inactive',
                    'Excessive Drinking_% Excessive Drinking',
                    'Uninsured_% Uninsured',
                    'Preventable hospital stays (Ambulatory Care Sensitive Conditions)_ACSC Rate'
                    ]
