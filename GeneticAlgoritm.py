import random
import math
from numpy.random import choice

class GeneticAlgoritm():
	def __init__(self, weight_markers, parameters):
		self.weight_markers=weight_markers
		self.population_size=parameters[0]
		self.number_game=parameters[1]
		self.duration_of_game=parameters[2]
		self.generations=parameters[3]

	def initialized_population(self):
		return [[ random.uniform(-1.0,0) if not self.weight_markers[i] and i!=1 else random.uniform(0,1.0) if not self.weight_markers[i] else 0 for i in range(len(self.weight_markers))] for _ in range(self.population_size)]

	def tournament_selection(self, member_results):
		one_hundred_percent = len(member_results)
		ten_percent = (one_hundred_percent * 10)//100
		fifty_percent = (one_hundred_percent * 50)//100
		tmp_array = []
		descendant_array = []

		if ten_percent < 2:		
			descendant = self.crossover(*sorted(sorted(member_results, key=lambda x: x[2]), key=lambda x:x[1])[-2:])
			descendant_array.append(descendant)
			return descendant_array
		else:
			for _ in range(fifty_percent):
				chromosome_prev = None
				while len(tmp_array) != ten_percent:
					chromosome = random.choice(member_results)
					if chromosome != chromosome_prev:
						tmp_array.append(chromosome)
						chromosome_prev = chromosome
				
				descendant = self.crossover(*sorted(sorted(tmp_array, key=lambda x: x[2]), key=lambda x:x[1])[-2:])
				if descendant:
					descendant_array.append(descendant)
				tmp_array = []
			return descendant_array

	
	def crossover(self, *fav_chrom, crossover_method=True):
		# Arithmetic mean of two vectors
		if crossover_method:
			chrom_list = [ chrom[0] for chrom in fav_chrom]
			if choice([True,False], p=[0.05,0.95]): # Mutation probability
				return self.mutation_operator([sum(x)/2 if len(x) > 1 else x[0]  for x in zip(*chrom_list)])				
			return [sum(x)/2 if len(x) > 1 else x[0]  for x in zip(*chrom_list)]
		# Two-point and k-point crossover
		else:
			l = len(fav_chrom[0])
			chrom_list = [ chrom[0] for chrom in fav_chrom]
			points = sorted([random.randrange(l), random.randrange(l), random.randrange(l)])
			return chrom_list[1][:points[0]] + chrom_list[0][points[0]:points[1]] + chrom_list[1][points[1]:points[2]] + chrom_list[0][points[2]:]


	def mutation_operator(self, vector):
		if len(vector):
			vector[random.randrange(len(vector))] += random.uniform(-0.2,0.2)
			vector_norm = math.sqrt(sum(list(map(lambda x: x**2, vector))))
			return list(map(lambda x: x/vector_norm, vector))
		return []
