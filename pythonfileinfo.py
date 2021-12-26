import os
import hashlib

class pythonfileinfo():
	def __init__(self,file):
		fcontent = open(file,"r").read()
		lines = fcontent.split("\n")
		self.imports = []
		self.functions = []
		self.classes = []
		self.variables = []
		self.strings = []
		self.vars = {}
		# general file information
		self.fileinfo = {}
		self.fileinfo["md5"] = hashlib.md5(open(file,"rb").read()).hexdigest()
		self.fileinfo["sha256"] = hashlib.sha256(open(file,"rb").read()).hexdigest()
		self.fileinfo["size"] = os.path.getsize(file)
		self.fileinfo["lines"] = len(lines)
		for line in lines:
			# imports
			if line.startswith("import ") and "," not in line:
				impname = line[7:]
				self.imports.append(impname)
			elif line.startswith("import ") and "," in line:
				impname = line[7:]
				alli = impname.split(",")
				for i in alli:
					self.imports.append(i)
			elif line.startswith("from ") and len(line.split(" ")) > 3:
				impname = line.split(" ")[1]
				self.imports.append(impname)
			elif line.startswith(" ") and "import" in line and "from" not in line and "," not in line and ")" not in line and "=" not in line and "." not in line and ":" not in line and line.startswith("#") != True:
				line_r = line.split(" ")
				line_end = ""
				reached = False
				for part in line_r:
					if "import" in line_end:
						reached = True
					if reached:
						line_end += " {}".format(part)
					else:
						line_end += part
				if len(line_end.split(" ")) == 2:
					impname = line_end.split(" ")[1]
					self.imports.append(impname)
					
			# functions
			if line.startswith("def ") and "):" in line:
				funcname = line[4:].split("(")[0]
				self.functions.append(funcname)
			# classes
			if line.startswith("class ") and "=" not in line and "):" in line:
				classname = line[6:].split("(")[0]
				self.classes.append(classname)
			# variables
			if line.startswith("def") == False:
				if len(line.split(" = ")) == 2:
					self.variables.append(line.split(" = ")[1])
					self.vars[line.split(" = ")[0]] = line.split(" = ")[1]
			# strings
			if line.startswith("def") == False and line.startswith("class") == False:
				if len(line.split(" = ")) == 2:
					if line.split(" = ")[1].startswith("\"") == True and line.split(" = ")[1].endswith("\"") == True and ("\" + \"" not in line and  "\"+\"" not in line):
						if line.startswith("	"):
							line_r = line.split("	")
							line_end = ""
							reached = False
							for e in line_r:
								if "=" in e:
									reached = True
								if reached:
									line_end += "	" + e
								else:
									line_end += e
							self.strings.append(line_end.split(" = ")[1][1:-1])
						else:
							self.strings.append(line.split(" = ")[1][1:-1])

if __name__ == "__main__":
	print("----- PythonFileInfo -----")
	name = input("Enter a file to scan: ")

	fdata = pythonfileinfo(name)
	print("\n----- Results for {} -----".format(name))
	print("\n----- General file data -----")
	print("File MD5: {}".format(fdata.fileinfo["md5"]))
	print("File SHA256: {}".format(fdata.fileinfo["sha256"]))
	print("File size: {}".format(fdata.fileinfo["size"]))
	print("Total lines: {}".format(fdata.fileinfo["lines"]))
	print("\n----- Imports -----")
	for imp in fdata.imports:
		print("{}".format(imp))
	print("\n----- Functions -----")
	for func in fdata.functions:
		print("{}".format(func))
	print("\n----- Classes -----")
	for classname in fdata.classes:
		print("{}".format(classname))
	print("\n----- Variables -----")
	for var in fdata.variables:
		print("{}".format(var))
	print("\n----- Strings -----")
	for str in fdata.strings:
		print("{}".format(str))
	input()
