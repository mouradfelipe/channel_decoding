# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = "/mnt/c/Users/1513 MXTI/ITA/PROF/2SEM/ELE-32-L/LAB3/vasconsa/lab03clean"

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = "/mnt/c/Users/1513 MXTI/ITA/PROF/2SEM/ELE-32-L/LAB3/vasconsa/lab03clean/cmake-build-debug"

# Include any dependencies generated for this target.
include CMakeFiles/labvariacao1.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/labvariacao1.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/labvariacao1.dir/flags.make

CMakeFiles/labvariacao1.dir/labvariacao1.c.o: CMakeFiles/labvariacao1.dir/flags.make
CMakeFiles/labvariacao1.dir/labvariacao1.c.o: ../labvariacao1.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="/mnt/c/Users/1513 MXTI/ITA/PROF/2SEM/ELE-32-L/LAB3/vasconsa/lab03clean/cmake-build-debug/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/labvariacao1.dir/labvariacao1.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/labvariacao1.dir/labvariacao1.c.o   -c "/mnt/c/Users/1513 MXTI/ITA/PROF/2SEM/ELE-32-L/LAB3/vasconsa/lab03clean/labvariacao1.c"

CMakeFiles/labvariacao1.dir/labvariacao1.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/labvariacao1.dir/labvariacao1.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E "/mnt/c/Users/1513 MXTI/ITA/PROF/2SEM/ELE-32-L/LAB3/vasconsa/lab03clean/labvariacao1.c" > CMakeFiles/labvariacao1.dir/labvariacao1.c.i

CMakeFiles/labvariacao1.dir/labvariacao1.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/labvariacao1.dir/labvariacao1.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S "/mnt/c/Users/1513 MXTI/ITA/PROF/2SEM/ELE-32-L/LAB3/vasconsa/lab03clean/labvariacao1.c" -o CMakeFiles/labvariacao1.dir/labvariacao1.c.s

CMakeFiles/labvariacao1.dir/labvariacao1.c.o.requires:

.PHONY : CMakeFiles/labvariacao1.dir/labvariacao1.c.o.requires

CMakeFiles/labvariacao1.dir/labvariacao1.c.o.provides: CMakeFiles/labvariacao1.dir/labvariacao1.c.o.requires
	$(MAKE) -f CMakeFiles/labvariacao1.dir/build.make CMakeFiles/labvariacao1.dir/labvariacao1.c.o.provides.build
.PHONY : CMakeFiles/labvariacao1.dir/labvariacao1.c.o.provides

CMakeFiles/labvariacao1.dir/labvariacao1.c.o.provides.build: CMakeFiles/labvariacao1.dir/labvariacao1.c.o


# Object files for target labvariacao1
labvariacao1_OBJECTS = \
"CMakeFiles/labvariacao1.dir/labvariacao1.c.o"

# External object files for target labvariacao1
labvariacao1_EXTERNAL_OBJECTS =

labvariacao1: CMakeFiles/labvariacao1.dir/labvariacao1.c.o
labvariacao1: CMakeFiles/labvariacao1.dir/build.make
labvariacao1: libpcg.a
labvariacao1: CMakeFiles/labvariacao1.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir="/mnt/c/Users/1513 MXTI/ITA/PROF/2SEM/ELE-32-L/LAB3/vasconsa/lab03clean/cmake-build-debug/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable labvariacao1"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/labvariacao1.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/labvariacao1.dir/build: labvariacao1

.PHONY : CMakeFiles/labvariacao1.dir/build

CMakeFiles/labvariacao1.dir/requires: CMakeFiles/labvariacao1.dir/labvariacao1.c.o.requires

.PHONY : CMakeFiles/labvariacao1.dir/requires

CMakeFiles/labvariacao1.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/labvariacao1.dir/cmake_clean.cmake
.PHONY : CMakeFiles/labvariacao1.dir/clean

CMakeFiles/labvariacao1.dir/depend:
	cd "/mnt/c/Users/1513 MXTI/ITA/PROF/2SEM/ELE-32-L/LAB3/vasconsa/lab03clean/cmake-build-debug" && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" "/mnt/c/Users/1513 MXTI/ITA/PROF/2SEM/ELE-32-L/LAB3/vasconsa/lab03clean" "/mnt/c/Users/1513 MXTI/ITA/PROF/2SEM/ELE-32-L/LAB3/vasconsa/lab03clean" "/mnt/c/Users/1513 MXTI/ITA/PROF/2SEM/ELE-32-L/LAB3/vasconsa/lab03clean/cmake-build-debug" "/mnt/c/Users/1513 MXTI/ITA/PROF/2SEM/ELE-32-L/LAB3/vasconsa/lab03clean/cmake-build-debug" "/mnt/c/Users/1513 MXTI/ITA/PROF/2SEM/ELE-32-L/LAB3/vasconsa/lab03clean/cmake-build-debug/CMakeFiles/labvariacao1.dir/DependInfo.cmake" --color=$(COLOR)
.PHONY : CMakeFiles/labvariacao1.dir/depend

