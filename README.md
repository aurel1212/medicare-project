# Medicare, Part E

## Overview
Medicare is a health insurance program run by the United States federal government that covers tens of millions of Americans. As of 2010, there were approximately 48 million Americans covered by Medicare, most of them over the age of 65. In terms of costs, this translates to about 3% of the country's GDP. These figures are only expected to rise as more Americans reach retirement age and advancements in health care allow the elderly to live longer lives. 

Finding a mechanism to control costs, then, should be a clear imperative for the Medicaid program. This project aims to do that by, first, understanding factors that can be correlated with higher Medicare costs and, secondly, creating a model to predict a  doctor's expected Medicare costs. A model of this nature could be used for projecting future costs as well as to serve as a way to flag costs outside of some expected normal for further analysis.

## Data
Data were obtained for the calendar year 2013 from www.cms.gov. The data used includes the 'Medicare Provider Utilization and Payment Data: Part D Prescriber' as well as the 'Physician and Other Supplier Data CY 2013'. Aggregated physician level files of these data were also used for certain demographic information. Data were also obtained from www.countyhealthrankings.org. This data mainly contained demographic information. 

## EDA and Methodology
The data were aggregated to the county level to explore regional differences in % of beneficiaries with diseases and their relation to cost. This was accomplished with PCA and KMeans clustering. Other demographic trends were explored in their ability to predict rates of disease and/or costs. 

![Alt text](https://github.com/d-tang/medicare-project/blob/county_eda/images/county03.png)

One of the challenges in modeling this dataset was in the disparate classes of information being presented. General practicioners were being compared to oncologists. Physicians with one Medicare patient were being compared to physicians with hundreds (not all of a physician's patients need be Medicare beneficiaries). 

To deal with the latter issue, most numeric data were normalized to be per beneficiary (or charge/service, etc...). However, there may be information in the raw totals that is simply lost with this type of normalization. For the former, the dataset was condensed to examine the charges from one specific discipline, oncologists. 

There are many reasons for costs to vary (per beneficiary) amongst oncologists. Among them are: 1) the number of treatments, 2) the type of treatments, and 3) the type of disease (possibly encompassed by type of treatment). The number of treatments was readily available in the dataset. To explore differences in the type of treatment, each physician's performed services was aggregated and the physicians was split into a non-outlier and outlier group. TFIDF (2-gram) was performed on the list of services to determine differences in the order of feature importance. 

This project is still in progress.
