# Top level module for generating basic approximations
import time
import cPickle
import types

from skc.basic_approx.file import *
from skc.utils import *

##############################################################################
# GLOBAL VARIABLES
simplify_engine = None
iset = None

##############################################################################
# Recursive helper method which enumerates all possible combinations of
# operators, given prefix an array containing all operators so far concatenated
# (multiplied into a single matrix)
def gen_basic_approx_generation(prefixes):
	# Start with a clean slate
	reset_global_sequences()
	reset_generation_stats()
	
	simplified_ancestors = []

	# Simplifies the given "new" prefix within this generation.
	# If it simplifies to something already generated, then
	# return True so that the outer loop knows to continue.
	# otherwise returns False, so that we generate from this
	# (now simplified) prefix
	def simplify_new(new_op):
		# Simplify the prefix before we generaet from it
		# since we may already have done it this level
		(simplify_length, simplified_sequence) = \
			simplify_engine.simplify(new_op.ancestors)
		#if (simplify_length > 0):
		#		print "Simplified " + str(new_op.ancestors) + \
		#			" to " + str(simplified_sequence)
		ancestor_string = list_as_string(simplified_sequence)
		already_done = (ancestor_string in simplified_ancestors)
		new_op.ancestors = simplified_sequence
		#if (already_done):
		#	print "Already did " + str(ancestor_string)
		# This is a hard-coded hack for now
		if (simplified_sequence == ['I'] or already_done):
			return True
		# Add this to our list so we don't add it again this generation
		simplified_ancestors.append(ancestor_string)
		return False
	#------------------------------------------------------------------------
	for prefix in prefixes:
		# Enumerate over iset, appending one op to end of prefix each
		for insn in iset:
			new_op = prefix.add_ancestors(insn)
			(simplify_length, new_sequence) = \
				simplify_engine.simplify(new_op.ancestors)
			
			already_done = simplify_new(new_op)
			if (already_done):
				continue
			#print str(new_sequence)
			#if (simplify_length > 0):
			#	print str(simplify_length) + " simplified"
			append_sequence(new_op)
			
	# Dump whatever's left this generation into one last file
	save_chunk_to_file()

##############################################################################
## Generate table of basic approximations as preprocessing
# l_0 - fixed length of sequences to generate for preprocessing table
def basic_approxes(l_0, settings):
	global simplify_engine, iset
	
	iset = settings.iset
	simplify_engine = settings.simplify_engine

	reset_global_stats()
	
	set_filename_suffix("g1")
	# Kick things off by generating the first generation
	# (one-operator sequences for each instruction)
	# Passing an empty list will cause iset to be used as prefixes
	gen_basic_approx_generation([settings.identity])
	print_generation_stats(1)
	
	# Iterate over 1 to l_0, generating sequences of increasing length
	for i in range(1,l_0):
		# Set the generation's filename suffix
		set_filename_suffix("g" + str(i+1))
		
		# Check whether an generation file already exists for the current
		# generation that we can use
		already_exists = generation_file_exists(i+1)
		if (already_exists):
			print "Yay! Generation " + str(i+1) + " file already found, skipping"
			# less work for us. Assume it's correct.
			continue
		# Generate a new generation using the previous one as prefixes
		# we pass in the generation num of the one that just passed
		map_to_file_chunks(i, gen_basic_approx_generation)
		print_generation_stats(i+1)
	
	print_global_stats()

##############################################################################
# Externally visible function, does top-level timing, etc.
def generate_approxes(l0, settings):

	set_filename_suffix("iset")
	settings.print_iset()
	dump_to_file(settings.iset)

	# Start the generate timer
	begin_time = time.time()
	
	# Do it!
	basic_approxes(l0, settings)
	
	gen_time = time.time() - begin_time
	print "Generation time: " + str(gen_time)

