"""
This file runs 5 days on 50 random_states with 500 agents. It was used to gather the baseline usage per agent per hour for the price estimator.
"""

all_runs_hourly = []
n = 50
agents = 500
for seed in range(1, n+1):
    print(f"Iteration {seed}/{n}")
    results, profiles = run_simulation(
        days=5,
        random_state=seed,
        agents=agents,
        plots=None,
        shifting=None, median_plot=False
    )

    #convert results to array:
    results = np.array(results)

    #average over days 
    mean_15min = results.mean(axis=0)

    #convert 15-min to hourly
    hourly = mean_15min.reshape(24, 4).mean(axis=1)

    #per agent normalization to make it more scale invariant, though the price model will always benefit from higher agent caunts for a less chaotic mean
    hourly_per_agent = hourly / agents

    all_runs_hourly.append(hourly_per_agent)


#final baseline across all seeds
all_runs_hourly = np.array(all_runs_hourly)

baseline_per_hour_per_agent = all_runs_hourly.mean(axis=0)

print(baseline_per_hour_per_agent)

"""
returns:

baseline_usage_per_h = [0.43953643, 0.42574971, 0.43836126, 0.47233758, 0.53141863, 0.60753253, 
                        0.66313066, 0.67250915, 0.6465164, 0.66876732, 0.5535738, 0.50941658, 
                        0.52060918, 0.56453714, 0.63382294, 0.72724222, 0.84408718, 0.91658533, 
                        0.91394429, 0.85904491, 0.77586794, 0.6689581, 0.57338553, 0.50967155]
Used to calculate the delta between baseline and simulated
"""
