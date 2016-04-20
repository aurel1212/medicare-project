import pandas as pd 
import numpy as np 
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.cm as cm


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
    pay_cols = ['num_hcpcs_norm',
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
    df_agg.reset_index(level=['county'], inplace=True)

    return pd.merge(df_payments[pay_cols], df_county_ranks[ranks_cols], left_index=True, right_index=True)

def cluster(df, num_clusters=4):
    #cluster_cols = [
    #                'num_asthma_norm',
    #                'num_alzheimers_dementia_norm',
    #                'num_artrial_fibrillation_norm',
    #                'num_cancer_norm',
    #                'num_chronic_obstructive_pulmonary_norm',
    #                'num_depression_norm',
    #                'num_diabetes_norm',
    #                'num_heart_failure_norm',
    #                'num_hypertension_norm',
    #                'num_ischemic_heart_norm',
    #                'num_osteoporosis_norm',
    #                'num_rheumatoid_arthritis_osteoarthirtis_norm',
    #                'num_schizophrenia_psychotic_norm',
    #                'num_stroke_norm',
    #                'total_hcc_risk_norm',
    #                'Poor or fair health_% Fair/Poor',
    #                'Poor mental health days_Mentally Unhealthy Days',
    #                'Smokers_% Smokers',
    #                'Adult obesity_% Obese',
    #                'Physical inactivity_% Physically Inactive',
    #                'Excessive Drinking_% Excessive Drinking',
    #                'Uninsured_% Uninsured',
    #                'Preventable hospital stays (Ambulatory Care Sensitive Conditions)_ACSC Rate'
    #                ]
    scale = StandardScaler()
    df_scale = scale.fit_transform(df[cluster_cols])
    km_mod = KMeans(n_clusters = num_clusters, n_jobs=-1, random_state=13, verbose=2)
    preds = km_mod.fit_predict(df_scale)

    return km_mod, preds

def get_cluster_assignments(df, preds):
    df['predictions'] = preds
    return zip(df['county'], preds)

def cluster_plot(X,n_clusters):
    '''
    plot silhouette and clusters
    :param x: numpy array
    :param nrange: int, range of cluster numbers
    :return: plots
    '''

    # Create a subplot with 1 row and 2 columns
    fig, ax1 = plt.subplots(1)
    fig.set_size_inches(7, 5)

    # The 1st subplot is the silhouette plot
    # The silhouette coefficient can range from -1, 1 but in this example all
    # lie within [-0.1, 1]
    ax1.set_xlim([-0.1, 1])
    # The (n_clusters+1)*10 is for inserting blank space between silhouette
    # plots of individual clusters, to demarcate them clearly.
    ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])

    # Initialize the clusterer with n_clusters value and a random generator
    # seed of 10 for reproducibility.
    clusterer = KMeans(n_clusters=n_clusters, random_state=0)
    cluster_labels = clusterer.fit_predict(X)

    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed
    # clusters
    silhouette_avg = silhouette_score(X, cluster_labels)
    print("For n_clusters =", n_clusters,
          "The average silhouette_score is :", silhouette_avg)

    # Compute the silhouette scores for each sample
    sample_silhouette_values = silhouette_samples(X, cluster_labels)
    
    y_lower = 10
    for i in range(n_clusters):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = \
            sample_silhouette_values[cluster_labels == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.spectral(float(i) / n_clusters)
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples

    ax1.set_title("The silhouette plot for the various clusters (K = "+str(n_clusters)+")")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    # The vertical line for average silhoutte score of all the values
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])


def get_silhouette_score(X,nclust):
    '''
    calculate average silhouette score
    :param nclust: int, number of clusters
    :param X: numpy array, data set to cluster
    :return: float, average silhouette score
    '''
    km = KMeans(nclust, random_state=30)
    km.fit(X)
    sil_avg = silhouette_score(X, km.labels_)
    return sil_avg

def plot_silhouette(X,nrange):
    '''
    plot average silhouette score against the number of clusters
    :param nrange: int, indicates range of cluster numbers
    :param X: numpy array, data set to cluster
    :raise: plot
    '''
    sil_scores = [get_silhouette_score(X,i) for i in xrange(2,nrange)]
    plt.plot(range(2,nrange), sil_scores)
    plt.xlabel('K')
    plt.ylabel('Silhouette Score')
    plt.title('Silhouette Score vs K')

def transform_pca(df, n_comp=3):
    pca = PCA(n_components=n_comp)
    df_pca = pca.fit_transform(df)
    
    return df_pca, df_pca[:,0], df_pca[:,1], df_pca[:,2]

def plot_clusters(df, n):
    mod, pred = cluster(df, n)
    z, xs, ys, zs = transform_pca(df)

    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.scatter(xs, ys, zs, c=pred, alpha=.3)
    plt.show()
    #ax.view_init(30,300)

