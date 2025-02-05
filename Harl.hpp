#ifndef HARL_HPP
#define HARL_HPP

#include <iostream>

class Harl
{
	private:
		void hello(void);
		std::string hey(int count);

	public:
		Harl();
		Harl(const Harl& other);
		Harl& operator=(const Harl& other);
		~Harl();
};

#endif
