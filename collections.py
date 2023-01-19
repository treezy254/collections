"""
This module implements specialized container datatypes providing alternative's to python's general purpose built-in containers, dict, list, set and tuple

namedtuple() :- factory funtion for creating tuple subclasses with named fields
deque :- list-like container with fast appends and pops on either ends
ChainMap :- dict-like class for creating a single view of multiple mappings
Counter :- dict subclass for counting hashable objects
OrderedDict :- dict subclass tha remembers the order entries were added
defaultdict :- dict subclass that calls a factory function to supply missing values
UserDict :- wrapper around dictionary objects for easier dict subclassing
UserList :- wrapper around list objects for easier list subclassing
UserString :- wrapper around string objetd for easier string subclassing
"""

# Chainmap objects
"""
A chainmap class is provided for quickly linking of mappings s they can be treated as a single unit. It is often much faster than creating a new dictionary and running multiple update() calls.

class collections.Chainmaps(*maps)

A chainmap groups multiple dicts or other mappings together
to create a single, updateable view. If no maps are specified, a single empty dictionary
is provided so that a new cain always has at least one mapping.


"""

baseline = {'music': 'bach', 'art': 'rembrandt'}
adjustments = {'art': 'van gogh', 'opera': 'carmen'}
list(ChainMap(adjustements, baseline))
>>> ['music', 'art', 'opera']

combined = baseline.copy()
combined.update(adjustements)
list(combined)
>>> ['music', 'art', 'opera']

# ChainMap Examples and Recipes
# example of simulating python internal lookup chain:
import builtins
pylookup = ChainMap(locals(), globals(), vars(builtins))

import os, argparse

defaults = {'color': 'red', 'user': 'guest'}

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user')
parser.add_argument('-c', '--color')
namespace = parser.parser_args()
command_line_args ={k: v for k, v in vars(namespace).items() if v is not None}

combined = ChainMap(command_line_args, os.environ, defaults)
print(combined['color'])
print(combined['user'])


# ----------------------------

# Examples patterns for using the ChainMap class to simulate nested contexts:

c = ChainMap 		# Create root context
d = c.new_child()	# create nested child context
e = c.new_child()	# Child of c, independent from d
e.maps[0]			# Current context dictionary -- like Python's locals()
e.maps{-1}			# Root context -- like Pythons globals()
e.parents			# Enclosing context chain -- like Python's nonlocals

d['x'] = 1			# set value in current context
d['x']				# # Get first key in the chain of contexts
del d['x']			# Delete from current conetxt
list(d)				# All nested values
k in d 				# Check all nested values
len(d)				# Number of nested values
d.items()			# All nested items
dict(d)				# Flatten into a regular dictionary

#-----------------------------

class DeepChainMap(ChainMap):
	# ' variant of chainmap that allows direct updates to inner scopes'

	def __setitem__(self, key, value):
		for mapping in self.maps:
			if key in mapping:
				mapping[key] = value
				return
		self.maps[0][key] = value


	def __delitem__(self, key):
		for mapping in self.maps:
			if key in mapping:
				del mapping[key]
				return
		raise KeyError(key)

d = DeepChainMap({'zebra': 'black'}, {'elephant': 'blue'}, {'lion': 'yellow'})
d['lion'] = 'orange' 		# update an existing key two levels down
d['snake'] = 'red'			# new keys get added to the topmost dict
del d['elephant']			# remove an existing key one level down
d 							# display result


# ----------------------------

# COunter Objects

""" A counter tool is provided to support convenient and rapid tallies."""

cnt = Counter()
for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
	cnt[word] += 1

print(cnt)

import re
words = re.findall(r'\w+', open('hamlet.txt').read().lower())
Counter(words).most_common(10)

"""
A Counter is a dict subclass for counting hashable objects. 
It is a collection where elements are stored as dictionary keys and their counts are stored as dictionary values. 
COunts are allowed to be any integer value including zero or negative counts.
The counter class is similar to bags or multisets in other langs"""

c = Counter()
c = Counter('gallahad')
c = Counter({'red': 4, 'blue': 2})
c = Counter(cats=4, dogs=8)

c = Counter(['eggs', 'ham'])
c['bacon']

c['sausage'] = 0
del c['sausage']

# COunter objects suppport additional methods beyond available for all dictionaries:

"""
elements()
Return an iterator over elements repeating ech as many times as it count. Elements are returned in the order first encountered. 
If an elements count is less than one, elements() will ignore it
"""
c = counter(a=4, b=2, c=0, d=-2)
sortedd(c.elements())

"""
most_common()
Return a list of the n most common elements and their counts from the most common to the least.
Elements with equal counts are ordered in the order first encountered:
"""
COunter('abracadabra').most_common(3)

"""
subtract([iterable-or-mapping])
Elements are subtracted from an iterable or from another mapping(or counter)
Like dict.update() but subtracts counts instead of replaicng them"""

c = counter(a=4, b=2, c=0, d=-2)
d = Counter(a=1, b=2, c=3, d=4)
c.subtract(d)
c

"""
total()
compute the sum of the counts
"""

c = Counter(a=10, b=5, c=0)
c.total()


#----------------------

# deque
"""
Return s a new deque object initializerd left-to-right (using append()) with data from iterable. 
If iterable is not specified, the new deque is empty.
Deque are a generalization of stacks and queues.

methods :
	 append(x)
	 	-add x to the right side of the deque

	 appendleft(x)
	 	-add x to the left side of the deque

	 clear()
	 	- remove all elements from the deque leaving it with length 0

	 copy()
	 	- create a shallow copy of the deque

	 count(x)
	 	-count the number of deque elements equal to x

	 extend(iterable)
	 	- extend the right side of the deque by appending elements from the iterable arguement
		
	 extendleft(iterable)

	 index(x[, start[, stop]])

	 insert(i, x)

	 pop()

	 popleft()

	 remove(value)
	 	- removes the first occurence of value. If not found, raises a ValueError

	 reverse()
	 	- reverse the elments of the deque in-place and then return None

	 rotate(n=1)
	 	- rotate the deque n steps to teh right. If n is negative, rotate to the left

	 maxlen
	 	- maximizes size of a deque or None if unbounded

"""

from collections import deque
d = deque('ghi')
for elem in d:
	print(elem.upper())

d.append('j')
d.appendleft('f')
d

d.pop()
d.popleft()

list(d)

d[0]

d[-1]

list(reversed(d))

'h' in deque
d.extend('jkl')
d

d.rotate(1)
d 

d.rotate(-1)
d 

deque(reversed(d))

d.clear()
d.pop()

d.extendleft('abc')
d

# deque Recipes


# -------------------------------

# defaultdict objects

class collection.defaultdict(default_factory=None, /[, ...])
""" returns a new dictionary-like object.
It overrides one method and adds one writable instance variable. 
The remaining functionality is the same as for the dict class.

The first argument provides the initial value for the default-factory attribute; 
it defaults to None. All remaining arguments are treated the same as
if they were passed to the dict constructor, including keyword arguements.
"""

s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
d = defaultdict(list)
for k, v in s:
	d[k].append(v)

sorted(d.items())

s = 'mississippi'
d = defaultdict(int)
for k in s:
	d[k] += 1

sorted(d.items())

def constant_factory(value):
	return lambda: value

d = defaultdict(conatnt_factory('<missing>'))
d.update(name='John', action='ran')
'%(name)s %(action)s to %(object)s' % d 

s = [('red', 1), ('blue', 2), ('red', 3), ('blue', 4), ('red', 1), ('blue', 4)]
d = defaultdict(set)
for k, v in s:
	d[k].add(v)

sorted(d.items())


# ---------------------------------

# nametuple()
"""
named tuples assign meaning to each position in a tuppple and allow for more readable, self-documenting code.
They can be used whrever regular tuples are used, and they add the ability to access fields by name instead of position index.
"""
collections.namedtuple(typename, field_names, *, rename=False, defaults=None, module=None)

# Basic example
Point = namedtuple('Point', ['x', 'y'])
p = Point(11, y=22)
p[0] + p[1]

x, y = p
x, y

p.x + p.y 

print

EmployeeRecord = namedtuple('EmployeeRecord', 'name, age, title, department, paygrade')

import csv
for emp in map(EmployeeRecord._make, csv.reader(open("employees.csv", 'rb'))):
	print(emp.name, emp.title)

import sqlite3
conn = sqlite3.connect('/companydata')
cursor = conn.cursor()
cursor.execute('SELECT name, age, title, departement, pargrade FROM employees')
for emp inmap(EmployeeRecord._make, cursor.fetchall()):
	print(emp.name, emp.title)

# additional methods and attributes
"""
	somenamedtuple._make(iterable)
		- class method that makes a new instance from an existing sequence or iterable

	somenamedtuple._asdict()
		- returns a new dict which maps field name sto their corresponding values

	somenamedtuple._replace(**kwargs)
		- return a new instance of the named tuple replacing specified fields with new values

	somenamedtuple._fields
		-tuple of strings listing the field name. Useful for introspection and creating new named tuple types from existing named tuples

	somenamedtuple._fields_defaults
		- dictionary mapping field names to default values

"""


# ------------------------------------

# the rest are for advanced problems

# OrderdDict object
# UserList
# UserString
# UserDict

