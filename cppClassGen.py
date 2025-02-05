import sys

# Dict for converting var types to default values
TYPE_TO_VALUE = {
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
	return "\n\t\t".join(f"{var};" for var in vars)

def get_var_copies(vars, indent):
	return ("\n" + "\t" * indent).join(
		f"{var.split()[1]} = other.{var.split()[1]};" for var in vars
		)

def get_var_inits(vars):
	return ", ".join(
		f"{var.split()[1]}({TYPE_TO_VALUE[var.split()[0]]})" for var in vars
		)

# Generate a standard canonical form .hpp file
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

# Generate a standard canonical form .cpp file
def gen_cpp(class_name, vars):
	return (f'''\
#include "./{class_name}.hpp"

{class_name}::{class_name}()
	: {get_var_inits(vars)} {{}}

{class_name}::{class_name}(const {class_name}& other)
{{
	{get_var_copies(vars, indent=1)}
}}

{class_name}& {class_name}::operator=(const {class_name}& other)
{{
	if (this != &other)
	{{
		{get_var_copies(vars, indent=2)}
	}}
	return *this;
}}

{class_name}::~{class_name}() {{}}
''')


if __name__ == "__main__":

	if len(sys.argv) < 2:
		print("Error: pass class name(s) as argument")
		exit()

	class_name = sys.argv[1].title()
	vars = sys.argv[2:]
	with open(f'{class_name}.hpp', "w") as hpp_file:
		hpp_file.write(gen_hpp(class_name, vars))

	with open (f'{class_name.title()}.cpp', "w") as cpp_file:
		cpp_file.write(gen_cpp(class_name, vars))

