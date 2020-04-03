import prediction
import ml
import numpy as np
import matplotlib.pyplot as plt

# ===============================VITAL DYNAMICS===============================
birth_rate_per_day = 17.592/(1000*365) # https://www.macrotrends.net/countries/IND/india/birth-rate
death_rate_per_day = 7.309/(1000*365) # https://www.macrotrends.net/countries/IND/india/death-rate

# =============================STATIC PARAMETERS==============================
proportion_of_exposed_who_become_symptomatic_infectious = 0.20
proportion_of_recovered_who_can_recontract = 0.0
days_non_symptomatic_remain_infectious = 15
days_symptomatic_remain_infectious = 15
days_before_an_exposed_becomes_non_symptomatic_infectious = 4
days_before_an_exposed_becomes_symptomatic_infectious = 4
days_before_a_recovered_recontracts = 30

# =======================CONSTRAINTS ON DYNAMIC PARAMETERS====================
# constraints on people_exposed_by_each_non_symptomatic_individual
# constraints on people_exposed_by_each_symptomatic_individual
# constraints on proportion_of_symptomatic_infectious_who_recover
min_R0 = 0
max_R0 = 20
step_size_R0 = 1
min_recovery = 0.20
max_recovery = 1.0
step_size_recovery = 0.1

# ===============================PARAMETERS===================================
p = {}

# Births per day as a proportion of total population
p[0] = birth_rate_per_day

# Non infection related deaths per day as a proportion of total population 
p[1] = death_rate_per_day

# Number of virus exposures caused by each infected non-symptomatic individual per day. 
# Exposures caused by non-symptomatic infectious individuals / Days non-symptomatic person remains infectious
p[2] = people_exposed_by_each_non_symptomatic_individual/days_non_symptomatic_remain_infectious

# Number of virus exposures caused by each infected symptomatic individual per day. 
# Exposures caused by symptomatic infectious individuals / Days symptomatic person remains infectious
p[3] = people_exposed_by_each_symptomatic_individual/days_symptomatic_remain_infectious

# Proportion of exposed who become non-symptomatic infectious per day
# Proportion of exposed who become non-symptomatic infectious / days an exposed person takes to become non-symptomatic infectious
p[4] = (1 - proportion_of_exposed_who_become_symptomatic_infectious)/days_before_an_exposed_becomes_non_symptomatic_infectious

# Proportion of exposed who become symptomatic infectious per day
# Proportion of exposed who become symptomatic infectious / days an exposed person takes to become symptomatic infectious
p[5] = proportion_of_exposed_who_become_symptomatic_infectious/days_before_an_exposed_becomes_symptomatic_infectious

# Proportion of non-symptomatic infectious people who recover per day
# = Proportion of non-symptomatic infectious people who recover / Days non-symptomatic person remains infectious
p[6] = 1/days_non_symptomatic_remain_infectious

# Proportion of symptomatic infectious people who recover per day
# = Proportion of symptomatic infectious people who recover / Days symptomatic person remains infectious
p[7] = proportion_of_symptomatic_infectious_who_recover/days_symptomatic_remain_infectious

# Proportion of symptomatic infectious people who die per day
# = Proportion of symptomatic infectious people who die / Days symptomatic person remain infectious before dying
p[8] = (1 - proportion_of_symptomatic_infectious_who_recover)/days_symptomatic_remain_infectious

# Proportion of recovered who re-contrat virus per day
# = Proportion of recovered who re-contrat virus / Days before a recovered virus recontracts
p[9] = proportion_of_recovered_who_can_recontract/days_before_a_recovered_recontracts

# ==============================INITIAL CONDITION===============================
# [S E I C R D]
z0 = [1330000000, 200, 0, 0, 0, 0]
# time step
t = np.arange(0,356*1,1)

# get values
predictor = prediction.predictor(p, z0, t)
prediction = predictor.predict()
prediction_S = prediction[:, 0]
prediction_E = prediction[:, 1]
prediction_I = prediction[:, 2]
prediction_C = prediction[:, 3]
prediction_R = prediction[:, 4]
prediction_D = prediction[:, 5]




# plot results
# l1 = plt.plot(t,prediction_S, color=(191/255,191/255,191/255,1), linestyle = '-', label = 'Susceptible')
l2 = plt.plot(t,prediction_E, color=(250/255,224/255,164/255,1), linestyle = '-', label = 'Exposed')
l3 = plt.plot(t,prediction_I, color=(255/255,192/255,0/255,1), linestyle = '-', label = 'Non-symptomatic')
l4 = plt.plot(t,prediction_C, color=(239/255,73/255,81/255,1), linestyle = '-', label = 'Symptomatic')
# l5 = plt.plot(t,prediction_R, color=(0/255,176/255,80/255,1), linestyle = '-', label = 'Recovered')
l6 = plt.plot(t,prediction_D, color=(0/255,0/255,0/255,1), linestyle = '-', label = 'Dead')
plt.xlabel('days')
plt.legend()
plt.show()
