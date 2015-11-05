import argparse, os, sys

# Parse all parameters
parser = argparse.ArgumentParser()
parser.add_argument('ctfdir', type=str, help='Directory containing all tasks and descriptions, e.g. example-ctf-2015/')
parser.add_argument('info', type=str, help='Default info file name containing the task description, e.g. info')
parser.add_argument('ctfname', type=str, help='Name of the CTF')
args = parser.parse_args()

# Define components of each challenge README.md:
#	Header:			Defines CTF Name and Year
#	Preamble:		Defines Categroy, Points, #Solves, Description
#	Postscript:		Contains Local and External Writeups
#
head = '# ' + args.ctfname + ' 2015: '
pre = ''
pre += '**Category:** \n'
pre += '**Points:** \n'
pre += '**Solves:** \n'
pre += '**Description:**\n\n'
post = """

## Write-up

(TODO)

## Other write-ups and resources

* none yet
"""

# Define components of each CTF root README.md:
#	RootHeader:		Defines CTF Name
#	RootPreamble:	Contains Link to CTF, scoreboards (external and local), Completed Writeups, External Writeups and Missing Writeups
roothead = '# ' + args.ctfname + ' CTF write-ups'
rootpre = roothead + '\n'
rootpre += """
* <TODO>
* [Scoreboard](TODO) or [local alternative](TODOLOCAL)

## Completed write-ups

* none yet

## External write-ups only

* none yet

## Missing write-ups
"""

# Create root README.md
rootdir = open(args.ctfdir+'/README.md', 'w')
rootdir.write(rootpre)

# Create the .gitignore
gitignore = open(args.ctfdir+'/.gitignore','w')

# os.walk returns: dirpath (args.ctfdir), dirnames, filenames
# For each challenge directory, create a README.md and add files >10Mb to .gitignore
for root, dirs, files in os.walk(args.ctfdir):
	for f in files:
		# Case: info file containing the descriptions.
		if f == args.info:
			# Get the filename and directory into one set
			ok = os.path.split(root)
			# Create the header of the readme with the directory name as the challenge name
			readme = head + ok[len(ok)-1] + "\n\n" + pre

			# Add the content of the info file to the readme and append the post
			for line in open(os.path.join(root, f), 'rw').readlines():
				readme += "> " + line
			readme += post

			# Get the ctf directory name, challenge type and challenge name in an array
			ok = root.split('/')

			# Add the task reference to the root README.md
			taskref = ''
			for x in range(1,len(ok)-1): taskref += ok[x] + "/"
			taskref += ok[len(ok)-1]
			rootdir.write('\n'+'* ['+taskref+']('+taskref+')')

			# Create a README.md for the challenge
			with open(root + '/' + 'README.md', 'w') as f:
				f.write(readme)
				f.close()
		# Case: files required for the challenge
		else:
			# TODO: Rename ok, move to beginning of for loop. Refactor code...
			ok = root.split('/')
			fname = ''
			for x in range(1,len(ok)-1): fname += ok[x] + "/"
			fname += ok[len(ok)-1] + '/' + f
			if os.stat(os.path.join(root,f)).st_size > 10485760:
				gitignore.write(fname)
