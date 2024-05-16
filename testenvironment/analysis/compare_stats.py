import numpy as np
import pandas as pd
from scipy import stats

def compare_time_series(group1, group2):
    # Ensure the input is a list of numpy arrays
    group1 = np.array(group1)
    group2 = np.array(group2)

    results = {}

    # Descriptive Statistics
    results['mean_diff'] = abs(np.mean([np.mean(ts) for ts in group1]) - np.mean([np.mean(ts) for ts in group2]))
    results['median_diff'] = abs(np.median([np.median(ts) for ts in group1]) - np.median([np.median(ts) for ts in group2]))
    results['std_dev_diff'] = abs(np.mean([np.std(ts) for ts in group1]) - np.mean([np.std(ts) for ts in group2]))

    # Flatten the arrays for statistical testing
    flat_group1 = np.concatenate(group1)
    flat_group2 = np.concatenate(group2)

    results['autocorrelation'] = abs(pd.Series(flat_group1).autocorr() - pd.Series(flat_group2).autocorr())


    # T-test (assuming equal variances)
    t_stat, t_p_val = stats.ttest_ind(flat_group1, flat_group2, equal_var=True)
    results['t_test_stat'] = t_stat
    results['t_test_p_val'] = t_p_val

    # Mann-Whitney U test (non-parametric test)
    u_stat, u_p_val = stats.mannwhitneyu(flat_group1, flat_group2)
    results['mann_whitney_u_stat'] = u_stat
    results['mann_whitney_u_p_val'] = u_p_val

    return results