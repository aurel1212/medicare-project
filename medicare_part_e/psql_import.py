import psycopg2 as pg2
import src.psql_helper as ph
import pandas as pd
import string
import re

DATABASE = 'medicare'
USER = 'postgres'

conn = pg2.connect(dbname=DATABASE, user=USER)
cur = conn.cursor()

# Insert provider/drug data into psql

query = '''
        CREATE TABLE npi_drug_13 (
            npi integer
            , last_name text
            , first_name varchar(50)
            , provider_city varchar(50)
            , provider_state varchar(5)
            , specialty_desc text
            , description_flag varchar(5)
            , drug_name varchar(50)
            , generic_name varchar(50)
            , bene_count integer
            , total_claims integer
            , total_day_supply integer
            , total_drug_cost float
            , bene_count_ge65 integer
            , bene_count_ge65_redact varchar(5)
            , total_claim_count_ge65 integer
            , ge65_redact_flag varchar(5)
            , total_day_supply_ge65 integer
            , total_drug_cost_ge65 float
            );
        '''
cur.execute(query)

query = '''
        COPY npi_drug_13
        FROM '/home/ubuntu/medicare-project/data/pp_npi_drug_13.tab' 
        DELIMITER '\t' 
        HEADER
        CSV;
        '''
cur.execute(query)
conn.commit()

# Insert provider summary into psql

query = '''
        CREATE TABLE npi_13 (
            npi integer
            , last_name text
            , first_name varchar(50)
            , middle_initial varchar(5)
            , credentials varchar(20)
            , gender varchar(5)
            , entity_code varchar(10)
            , provider_street1 text
            , prover_street2 text
            , provider_city varchar(40)
            , provider_zip varchar(20)
            , provider_state varchar(5)
            , provider_country varchar(20)
            , specialty_desc text
            , description_flag varchar(10)
            , bene_count float
            , total_claim_count integer
            , total_drug_cost float
            , total_day_supply integer
            , bene_count_ge65 float
            , bene_count_ge65_redact varchar(5)
            , total_claim_count_ge65 int
            , ge65_redact_flag varchar(5)
            , total_drug_cost_ge65 float
            , total_day_supply_ge65 float
            , brand_claim_count float
            , brand_redact_flag varchar(5)
            , brand_claim_cost float
            , generic_claim_count float
            , generic_redact_flag varchar(5)
            , generic_claim_cost float
            , other_claim_count float
            , other_redact_flag varchar(5)
            , other_claim_cost float
            , mapd_claim_count float
            , mapd_redact_flag varchar(5)
            , mapd_claim_cost float
            , pdp_claim_count float
            , pdp_redact_flag varchar(5)
            , pdp_claim_cost float
            , lis_claim_count float
            , lis_redact_flag varchar(5)
            , lis_claim_cost float
            , nonlis_claim_count float
            , nonlis_redact_flag varchar(5)
            , nonlis_claim_cost float
            );
        '''
cur.execute(query)

query = '''
        COPY npi_13
        FROM '/home/ubuntu/medicare-project/data/pp_npi_13.tab' 
        DELIMITER '\t' 
        HEADER
        CSV;
        '''
cur.execute(query)
conn.commit()


#originally run with Ming's psql helper code here

df = pd.read_csv('../data/npidata_20050523-20160313FileHeader.csv')
header = df.columns.values.tolist()

# function to replace all the whitespace and punctuation in columns names
def remove_white_punc(lst):
    '''
    Input: List of strings (with whitespaces/punctuation)
    Output: List of strings (with whitespace/punctuation removed)
    '''
    regex = re.compile('[%s]'%re.escape(string.punctuation))
    
    for ix, name in enumerate(lst):
        lst[ix] = regex.sub('', name).replace(' ', '_')
    
    return lst


header_strip = remove_white_punc(header)
header_strip[3]

# Insert NPI lookup file into psql

psql = ph.PsqlConnection(db=DATABASE, user=USER)
psql.create_table(header_strip, 'npi_name')
psql.insert_csv('npi_name', "/home/ubuntu/medicare-project/data/npidata_20050523-20160313.csv")

# Change npi column in NPI lookup to integer

query = '''
        ALTER TABLE npi_name
        ALTER COLUMN npi
        TYPE integer 
        USING npi::integer;
        '''
cur.execute(query)
conn.commit()

# Insert healthcare provider taxonomy code description into psql

df = pd.read_csv('data/nucc_taxonomy_160.csv')

# Drop definition and notes columns - not needed
# Write out to csv

df_taxonomy_striped = df[['Code', 'Grouping', 'Classification', 'Specialization']]
df_taxonomy_striped.to_csv('data/nucc_taxonomy_160_stripped.csv', index=False, na_rep='None')

# non-utf8 character in file, stripped using unix 

query = '''
        CREATE TABLE taxonomy_lookup (
            code varchar(15)
            , grouping varchar(100)
            , classification varchar(100)
            , specialization varchar(100)
            );
        '''
cur.execute(query)

query = '''
        COPY taxonomy_lookup
        FROM '/home/ubuntu/medicare-project/data/nucc_taxonomy_160_stripped_clean.csv' 
        DELIMITER ',' 
        HEADER
        CSV;
        '''
cur.execute(query)
conn.commit()


# ### Insert Medicare Provider Payments into PSQL
# Header was stripped from file and placed into its own file using unix
misc_payments_header = pd.read_csv('../data/Medicare_Provider_Util_Payment_PUF_CY2013_header.txt', sep='\t')
misc_payments_header.columns

query = '''
        CREATE TABLE util_payments_2013 (
            npi integer
            , last_name varchar(100)
            , first_name varchar(50)
            , middle_initial varchar(20)
            , credentials varchar(50)
            , gender varchar(5)
            , entity_code varchar(20)
            , street1 varchar(100)
            , street2 varchar(100)
            , city varchar(50)
            , zip varchar(20)
            , state varchar(10)
            , country varchar(10)
            , provider_type varchar(50)
            , medicare_participation_indicator varchar(10)
            , place_of_service varchar(10)
            , hcpcs_code varchar(15)
            , hcpcs_desc text
            , hcpcs_drug_indicator varchar(10)
            , line_srvc_count float
            , bene_unique_count integer
            , bene_day_srvc_count integer
            , avg_medicare_allowed_amt float
            , stddev_medicare_allowed_amt float
            , avg_submitted_chg_amt float
            , stddev_submitted_chg_amt float
            , avg_medicare_payment_amt float
            , stddev_medicare_payment_amt float
            );
        '''
cur.execute(query)

query = '''
        COPY util_payments_2013
        FROM '/home/ubuntu/medicare-project/data/Medicare_Provider_Util_Payment_PUF_CY2013_Strip.txt' 
        DELIMITER '\t' 
        CSV;
        '''
cur.execute(query)
conn.commit()

# ### Insert Medicare Provider Payments Aggregate into PSQL

query = '''
        CREATE TABLE util_payments_agg_2013 (
            index integer
            , npi integer
            , last_name varchar(100)
            , first_name varchar(50)
            , middle_initial varchar(20)
            , credentials varchar(50)
            , gender varchar(5)
            , entity_code varchar(20)
            , street1 varchar(100)
            , street2 varchar(100)
            , city varchar(50)
            , zip varchar(20)
            , state varchar(10)
            , country varchar(10)
            , provider_type varchar(50)
            , medicare_participation_indicator varchar(10)
            , num_hcpcs integer
            , num_services float
            , num_unique_bene integer
            , total_submitted_charges float
            , total_medicare_allowed_amt float
            , total_medicare_payment_amt float
            , drug_suppress_indicator varchar(10)
            , num_hcpcs_associated_drug_srvc float
            , num_drug_srvc float
            , num_unique_bene_with_drug_srvc float
            , total_drug_submitted_charges float
            , total_drug_medicare_allowed_amt float
            , total_drug_medicare_payment_amt float
            , medical_suppress_indicator varchar(10)
            , num_hcpcs_associated_med_srvc float
            , num_med_srvc float
            , num_unique_bene_with_med_srvc float
            , total_med_submitted_charges float
            , total_med_medicare_allowed_amt float
            , total_med_medicare_payment_amt float
            , avg_age_bene float
            , num_bene_le65 float
            , num_bene_65to74 float
            , num_bene_75to84 float
            , num_bene_ge84 float
            , num_female float
            , num_male float
            , num_non_his_white float
            , num_african_american float
            , num_asian float
            , num_hispanic float
            , num_american_indian float
            , num_no_race float
            , num_medicare_only float
            , num_medicare_medicaid float
            , pcnt_alzheimers_dementia float
            , pcnt_asthma float
            , pcnt_artrial_fibrillation float
            , pcnt_cancer float
            , pcnt_chronic_kidney float
            , pcnt_chronic_obstructive_pulmonary float
            , pcnt_depression float
            , pcnt_diabetes float
            , pcnt_heart_failure float
            , pcnt_hyperlipidemia float
            , pcnt_hypertension float
            , pcnt_ischemic_heart float
            , pcnt_osteoporosis float
            , pcnt_rheumatoid_arthritis_osteoarthirtis float
            , pcnt_schizophrenia_psychotic float
            , pcnt_stroke float
            , avg_hcc_risk_score float
            );
        '''
cur.execute(query)

query = '''
        COPY util_payments_agg_2013
        FROM '/home/ubuntu/medicare-project/data/Medicare-Physician-and-Other-Supplier-NPI-Aggregate-CY2013.csv' 
        DELIMITER ',' 
        HEADER
        CSV;
        '''
cur.execute(query)
conn.commit()

# ### Input label data into psql

query = '''
        CREATE TABLE indictments_2013 (
            first_name varchar(50)
            , middle_name varchar(15)
            , last_name varchar(50)
            , state varchar(5)
            , npi_status boolean
            , link text
            , status varchar(50)
            , year_start integer
            , year_end integer
            , company varchar(50)
            );
        '''
cur.execute(query)

query = '''
        COPY indictments_2013
        FROM '/home/ubuntu/medicare-project/data/medicare_fraud_data.csv' 
        DELIMITER ',' 
        HEADER
        CSV;
        '''
cur.execute(query)
conn.commit()

# ### Input zip/county lookup into psql

query = '''
        CREATE TABLE zip_county_lookup (
            index integer
            , state varchar(3)
            , state_fips varchar(3)
            , city varchar(50)
            , city_fips varchar(5)
            , county_fips varchar(30)
            , county varchar(100)
            , county_fips_1 varchar(5)
            , county_1 varchar(50)
            , county_fips_full varchar(50)
            );
        '''
cur.execute(query)

query = '''
        COPY zip_county_lookup
        FROM '/home/ubuntu/medicare-project/zip_county_lookup.csv' 
        DELIMITER ',' 
        HEADER
        CSV;
        '''
cur.execute(query)
conn.commit()

# ### Input county health rankings with zip and county name into psql

query = '''
        CREATE TABLE county_health_rankings (
            fips varchar(10)
            , state varchar(20)
            , county varchar(50)
            , zscore_1 float
            , rank_1 varchar(5)
            , zscore_2 float
            , rank_2 varchar(5)
            , zip varchar(10)
            , county_fips varchar(10)
            );
        '''
cur.execute(query)

query = '''
        COPY county_health_rankings
        FROM '/home/ubuntu/medicare-project/data/county_health_ranks.csv' 
        DELIMITER ',' 
        HEADER
        CSV;
        '''
cur.execute(query)
conn.commit()