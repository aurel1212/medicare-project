# Reduced column view from aggregate prescriber data

SELECT 	npi
		, last_name
		, first_name
		, provider_zip
		, provider_state
		, specialty_desc
		, bene_count
		, total_claim_count
		, total_drug_cost
		, total_day_supply
		, brand_claim_count
		, brand_claim_cost
		, generic_claim_count
		, generic_claim_cost
		, other_claim_count
		, other_claim_cost
		, mapd_claim_count
		, mapd_claim_cost
		, pdp_claim_count
		, pdp_claim_cost
		, lis_claim_count
		, lis_claim_cost
		, nonlis_claim_count
		, nonlis_claim_cost
FROM npi_13; 


# Join indictments data with NPI lookup to get the NPI out

SELECT n.npi
	, indict.first_name
	, indict.last_name
	, indict.npi_status
FROM indictments_2013 indict
	, npi_name n
WHERE lower(indict.first_name) = lower(n.providerfirstname)
AND lower(indict.last_name) = lower(n.providerlastnamelegalname);

# Also incorporating state on join, previous join had numerous duplicates
SELECT n.npi
            , indict.first_name
            , indict.last_name
            , indict.npi_status
        FROM indictments_2013 indict
            , npi_name n
        WHERE lower(indict.first_name) = lower(n.providerfirstname)
        AND lower(indict.last_name) = lower(n.providerlastnamelegalname)
        AND lower(indict.state) = lower(n.providerbusinessmailingaddressstatename);