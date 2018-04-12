# This reads in data about each person's weight at each tick and calculates averages, 
# standard deviations, and draws plots and histograms to visualize the data.
# Data collected through Repast Simphony

import os
import csv
import numpy as np
import pandas as pd
import numpy.polynomial.polynomial as poly
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

plt.style.use('seaborn-colorblind')

maxTick = 200

# Reads the parameter groupings to find which runs correspond to which parameters
# Data comes in format of 
# run, seed, satisficing radius, rewiring probability
def readParamData():

	print 'reading parameter data'

	paramFiles = [file for file in os.listdir('.') if file.startswith('ind') and 'param' in file]
	
	lowRad_lowRP = []
	highRad_lowRP = []
	lowRad_highRP = []
	highRad_highRP = []

	for eachFile in paramFiles:
		reader = csv.reader(open(eachFile, 'r'))
		next(reader)
		for run, seed, sat_radius, rew_prob in reader:
			run = int(run)
			if [sat_radius, rew_prob] == ['0.0', '0.1']:
				lowRad_lowRP.append(run)
			elif [sat_radius, rew_prob] == ['0.4', '0.1']:
				highRad_lowRP.append(run)
			elif [sat_radius, rew_prob] == ['0.0', '0.9']:
				lowRad_highRP.append(run)
			elif [sat_radius, rew_prob] == ['0.4', '0.9']:
				highRad_highRP.append(run)
			else:
				print 'error error'

	return (lowRad_lowRP, highRad_lowRP, lowRad_highRP, highRad_highRP)

# Reads the individual BMI data. 
# There are two files with data that is formatted like:
# run, bmi, tick
def readData():

	print 'reading data'

	dataFiles = [file for file in os.listdir('.') if file.startswith('ind') and 'param' not in file]

	initial_conditions = []
	final_conditions = {}
	all_weights = {}

	for eachFile in dataFiles:
		reader = csv.reader(open(eachFile, 'r'))
		next(reader)
		lastTick = 1
		bmiArray = []
		for run, bmi, tick in reader:
			tick = int(float(tick))
			bmi = float(bmi)
			run = int(run)

			if tick != lastTick and lastTick == 1:
				initial_conditions.append(bmiArray)

			if tick != lastTick and lastTick == maxTick:
				print run
				final_conditions[int(lastRun)] = bmiArray

			if tick == lastTick:
				bmiArray.append(bmi)

			elif tick != lastTick:
				if lastRun in all_weights:
					all_weights[lastRun][lastTick] = bmiArray
				else:
					all_weights[lastRun] = {lastTick: bmiArray}

				bmiArray = [bmi]

			lastRun = run
			lastTick = tick

		all_weights[run][tick] = bmiArray
		final_conditions[int(run)] = bmiArray

	return all_weights, initial_conditions, final_conditions

# Visualize histograms of initial conditions
# Averages for the counts in each  bin for all the runs to find an average histogram
def initial(initial_conditions):

	maxVal = int(round(max(map(lambda x: max(x), initial_conditions))))
	minVal = min(map(lambda x: min(x), initial_conditions))

	averages = []

	list_histogram_data = []
	for sample in initial_conditions:
		hist, bin_edges = np.histogram(sample, bins = range(maxVal)) 

		list_histogram_data.append(hist)
		averages.append(np.mean(sample))


	avg_hist = np.average(list_histogram_data, axis=0)

	print np.mean(averages)

	plt.bar(bin_edges[:-1], avg_hist, width = 1)
	plt.xlim(min(bin_edges), max(bin_edges))
	plt.ylabel('Count')
	plt.xlabel('Initial BMI')
	plt.title('Average Initial Distribution Across Runs')
	plt.show()  

def final(final_conditions, param_lists):

	(lowRad_lowRP, highRad_lowRP, lowRad_highRP, highRad_highRP) = param_lists

	final_conditions_values = {}
	print final_conditions[1]

	fig, axes = plt.subplots(nrows = 2, ncols = 2)
	ax0, ax1, ax2, ax3 = axes.flatten()

	for param in param_lists:
		list_histogram_data = []
		for run in param:
			BMI_list =  final_conditions[run]
			hist, bin_edges = np.histogram(BMI_list, bins = range(20,45)) 

			list_histogram_data.append(hist)

		avg_hist = np.average(list_histogram_data, axis=0)


		if param[0] == 1:
			ax0.bar(bin_edges[:-1], avg_hist, width = 1)
			ax0.set_title('Low Sat Rad, Low Rewiring Prob')
			ax0.set_ylim([0, 45])
		elif param[0] == 3:
			ax1.bar(bin_edges[:-1], avg_hist, width = 1)
			ax1.set_title('High Sat Rad, Low Rewiring Prob')
			ax1.set_ylim([0, 45])

		elif param[0] == 2:
			ax2.bar(bin_edges[:-1], avg_hist, width = 1)
			ax2.set_title('Low Sat Rad, High Rewiring Prob')
			ax2.set_ylim([0, 45])
		elif param[0] == 4:
			ax3.bar(bin_edges[:-1], avg_hist, width = 1)
			ax3.set_title('High Sat Rad, High Rewiring Probab')
			ax3.set_ylim([0, 45])


		print param
	fig.tight_layout()
	plt.show()

# Calculates the variance of the data at each tick 
def variances(all_weights, param_lists):

	(lowRad_lowRP, highRad_lowRP, lowRad_highRP, highRad_highRP) = param_lists


	x_axis = range(maxTick)
	legend = []

	for param in param_lists:

		list_variance_data = []

		for run in param:

			tick_dicts =  all_weights[run]
			run_variance = []

			for key, value in tick_dicts.items():
				run_variance.append(np.std(value))

			list_variance_data.append(run_variance)

		avg_variances = np.average(list_variance_data, axis=0)

		m = np.polyfit(x_axis, avg_variances,2)
		print 'equation'
		print param[0]
		print m



		if param[0] == 1:
			plt.plot(avg_variances, label = 'Low Sat Rad, Low Rewiring Prob')
			legend.append('Low Sat Rad, Low Rewiring Prob')

		elif param[0] == 3:
			plt.plot(avg_variances, label = 'High Sat Rad, Low Rewiring Prob')
			legend.append('High Sat Rad, Low Rewiring Prob')

		elif param[0] == 2:
			plt.plot(avg_variances, label = 'Low Sat Rad, High Rewiring Prob')
			legend.append('Low Sat Rad, High Rewiring Prob')

		elif param[0] == 4:
			plt.plot(avg_variances, label = 'High Sat Rad, High Rewiring Prob')
			legend.append('High Sat Rad, High Rewiring Prob')



	plt.ylim((0, 8 ))
	plt.xlim((0, maxTick))
	plt.title('Standard Deviation of BMI Distribution Over Time')
	plt.legend(legend)
	plt.show()

# Calculates the average of the data at each tick 
def averages(all_weights, param_lists):

	(lowRad_lowRP, highRad_lowRP, lowRad_highRP, highRad_highRP) = param_lists


	x_axis = range(maxTick)
	legend = []

	for param in param_lists:

		list_mean_data = []

		for run in param:
			tick_dicts =  all_weights[run]
			run_mean = []

			for key, value in tick_dicts.items():
				run_mean.append(np.mean(value))
				
			list_mean_data.append(run_mean)
			
		avg_means = np.average(list_mean_data, axis=0)

		if param[0] == 1:
			plt.plot(avg_means,  label = 'Low Sat Rad, Low Rewiring Prob')
			legend.append('Low Sat Rad, Low Rewiring Prob')

		elif param[0] == 3:
			plt.plot(avg_means, label = 'High Sat Rad, Low Rewiring Prob')
			legend.append('High Sat Rad, Low Rewiring Prob')

		elif param[0] == 2:
			plt.plot(avg_means, label = 'Low Sat Rad, High Rewiring Prob')
			legend.append('Low Sat Rad, High Rewiring Prob')

		elif param[0] == 4:
			plt.plot(avg_means, label = 'High Sat Rad, High Rewiring Prob')
			legend.append('High Sat Rad, High Rewiring Prob')


	plt.ylim((25, 35 ))
	plt.xlim((0, maxTick))
	plt.title('Average BMI Over Time')
	plt.legend(legend, loc = 2)
	plt.show()


def main():
	parameter_lists = readParamData()
	all_weights, initial_conditions, final_conditions = readData()

	initial(initial_conditions)
	final(final_conditions, parameter_lists)
	variances(all_weights, parameter_lists)
	averages(all_weights, parameter_lists)

if __name__ == "__main__":
	main()