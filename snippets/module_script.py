import example_package
import example_package.submodule


def main():
	example_package.some_value
	example_package.some_func()
	example_package.submodule.sub_value
	example_package.submodule.sub_func()

if __name__ == '__main__':
	main()