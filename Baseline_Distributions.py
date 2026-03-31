import numpy as np
#Data from Yilmaz et al. 2017 'Occupant behaviour modelling in domestic buildings: the case of household electrical appliances'
#Datapoints = avg. hourly number of switch-on events (based on a UK study with UK participants)
#This code transforms these datapoints to probabilities, assigning a high probability if the appliance has a high switch-on rate
data = {
    "Dishwasher":[0.016,0.0071,0.0071,0.0044,0.0044,0.0017,0.008,0.0266,0.038,0.032,0.03,0.021,0.024,0.034,0.025,0.025,0.0196,0.027,0.0577,0.06577,0.0524,0.0328,0.0488,0.0355],
    "Washing":[0.00525,0.00617,0.00795,0.00527,0.00354,0.01777,0.03021,0.11463,0.15107,0.2061,0.2213,0.1812,0.1412,0.12976,0.0871,0.08,0.07466,0.0879,0.0613,0.05594,0.05596,0.038221,0.03464,0.01422],
    "Tumble Drier":[0.004,0,0,0,0.00266,0.00177,0.01155,0.0231,0.0311,0.0391,0.0462,0.0524,0.0506,0.03,0.02,0.03,0.025,0.02,0.0453,0.0435,0.0426,0.0293,0.0204,0.0088],
    "Cooker":[0.00259,0.00259,0.0103,0.01168,0.01168,0.02727,0.048,0.11,0.1221,0.111,0.1051,0.1233,0.148,0.05,0.04,0.03,0.08,0.1,0.15,0.1519,0.0883,0.0494,0.0337,0.01168],
    "Oven":[0.00259,0.00519,0.00649,0.00259,0.00519,0.00519,0.0337,0.0688,0.0467,0.0337,0.03636,0.0415,0.0688,0.018,0.014,0.02,0.02,0.014,0.0987,0.0753,0.03636,0.0259,0.035,0.0324],
    "Grill":[0,0,0.0012,0.0026,0.002597,0.00129,0.0012,0.0091,0.00779,0.00779,0.00259,0.01558,0.0519,0.01,0.002,0.001,0.025,0.03,0.0311,0.01558,0.0103,0.0011,0.00259,0.0026],
    "Hob":[0.0025,0.0013,0.0026,0.00389,0.001298,0.00389,0.0155,0.0909,0.112,0.0688,0.061,0.0493,0.0727,0.01,0.03,0.02,0.04,0.08,0.13,0.089,0.0584,0.04025,0.01039,0.00779],
    "TV Total":[0.0497,0.0135,0.01917,0.07123,0.042831,0.07345,0.1345,0.2,0.23,0.2228,0.17986,0.08254,0.12102,0.117024,0.0817,0.11195,0.168505,0.18,0.210705,0.36,0.35,0.31,0.3078,0.0904],
    "Electronics":[0.02485,0.00675,0.009585,0.035615,0.0214155,0.036725,0.06725,0.1,0.115,0.1114,0.08993,0.04127,0.06051,0.058512,0.04085,0.055975,0.0842525,0.09,0.1053525,0.18,0.175,0.155,0.1539,0.0452]
  #Add Electronic Vehicle (maybe already normalized)
}
normalized_data = {} #Where actual probabilites will be stored

for appliance, hourly_vals in data.items():
    vals = np.array(hourly_vals)
    probs = vals / vals.sum()
    normalized_data[appliance] = probs
  
""" -> To use if splitting probabilities is preferred over picking an hour and then a random quarter hour
quarter_data = {}

for appliance, hourly_vals in normalized_data.items():
    qvals = []
    for lam in hourly_vals:
        p = 1 - np.exp(-lam/4)
        qvals.extend([p]*4)
    quarter_data[appliance] = qvals

quarters = range(96)
"""

