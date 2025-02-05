import sys

# Dict for converting var types to default values
type_to_value = {
					"std::string":'""',
					"char[]":'""',
					"char*":'""',
					"char":0,
					"bool":0,
					"int":0,
					"unsigned int":0,
					"float":0,
					"unsigned float":0,
					"double":0,
					"unsigned double":0,
					"long":0,
					"unsigned long":0,
				}

# Functions for generating var declarations, initializations + copying
def get_prv_vars(vars):
	str = ""
	for var in vars:
		str += f"{var};\n		"
	return (str)

def get_var_copies(vars, no_tabs):
	str = ""
	for var in vars:
		name = var.split()[1]
		str += f"{name} = other.{name};"
		if var != vars[-1]:
			str += "\n"
			str += "	"* no_tabs
	return (str)

def get_var_inits(vars):
	str = ""
	for var in vars:
		type, name = var.split()
		str += f"{name}({type_to_value[type]})"
		if var != vars[-1]:
			str += ", "
	return (str)


# Generate a standard canonical form .hpp file for a given class name and list of private vars
def gen_hpp(class_name, vars):
	return (f'''\
#ifndef {class_name.upper()}_HPP
#define {class_name.upper()}_HPP

#include <iostream>

class {class_name}
{{
	private:
		{get_prv_vars(vars)}
	public:
		{class_name}();
		{class_name}(const {class_name}& other);
		{class_name}& operator=(const {class_name}& other);
		~{class_name}();
}};

#endif
''')

# Generate a standard canonical form .cpp file for a given class name and list of private vars
def gen_cpp(class_name, vars):
	return (f'''\
#include "./{class_name}.hpp"

{class_name}::{class_name}()
	: {get_var_inits(vars)} {{}}

{class_name}::{class_name}(const {class_name}& other)
{{
	{get_var_copies(vars, no_tabs=1)}
}}

{class_name}& {class_name}::operator=(const {class_name}& other)
{{
	if (this != &other)
	{{
		{get_var_copies(vars, no_tabs=2)}
	}}
	return *this;
}}

{class_name}::~{class_name}() {{}}
''')


if __name__ == "__main__":

	if len(sys.argv) < 2:
		print("Error: pass class name(s) as argument")
		exit()

	class_name = sys.argv[1]
	vars = sys.argv[2:]
	with open(f'{class_name.title()}.hpp', "w") as hpp_file:
		hpp_file.write(gen_hpp(class_name.title(), vars))

	with open (f'{class_name.title()}.cpp', "w") as cpp_file:
		cpp_file.write(gen_cpp(class_name.title(), vars))

