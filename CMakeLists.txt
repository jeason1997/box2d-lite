# 路径以及项目名称定义，该CMakeLists.txt可以到不同项目使用，只需要修改下面3个变量定义即可
set(INCLUDE_DIR "include")          # 定义包含目录位置
set(SOURCE_DIR "src")               # 定义源文件目录位置
set(PROJECT_NAME "box2d")           # 定义项目名称

############ 第一部分：常规定义 #############
cmake_minimum_required(VERSION 3.8)

project(${PROJECT_NAME} LANGUAGES CXX)

# 设置位置无关代码
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
############################################


############ 第二部分：C++引入 ##############
# 包含目录
include_directories(${Python3_INCLUDE_DIRS} ${INCLUDE_DIR})

# 自动查找C++源文件库
file(GLOB_RECURSE SOURCE_FILES "${SOURCE_DIR}/*.cpp")  # 查找src目录及子目录下的所有 .cpp 文件
set(clib "${PROJECT_NAME}Lib")
add_library(${clib} ${SOURCE_FILES})  # 使用自动查找到的源文件
############################################



############ 第三部分：SWIG生成 #############
# 设置SWIG相关的政策
cmake_policy(SET CMP0078 NEW)  # Use standard target names
cmake_policy(SET CMP0086 NEW)  # SWIG honors SWIG_MODULE_NAME

# 查找SWIG
find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})  # 包含SWIG库

# 查找所有头文件
file(GLOB_RECURSE HEADERS "${INCLUDE_DIR}/*.h")

# 动态生成*.i文件
set(SWIG_INTERFACE_FILE "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}.i")  # 生成的i文件将存放在build目录下
file(WRITE ${SWIG_INTERFACE_FILE} "%module ${PROJECT_NAME}\n\n")

# 将头文件内容写入到*.i中
foreach(HEADER ${HEADERS})
    get_filename_component(HEADER_NAME "${HEADER}" NAME)  # 只取得文件名
    file(APPEND ${SWIG_INTERFACE_FILE} "%{\n#include \"../${INCLUDE_DIR}/${HEADER_NAME}\"\n%}\n")  # 添加头文件引用
    file(APPEND ${SWIG_INTERFACE_FILE} "%include \"../${INCLUDE_DIR}/${HEADER_NAME}\"\n")  # 添加头文件引用
endforeach()

# 设置SWIG的接口文件属性
set_source_files_properties(${SWIG_INTERFACE_FILE} PROPERTIES CPLUSPLUS ON)

# 创建SWIG目标
set(pythonlib ${PROJECT_NAME})
swig_add_library(${pythonlib} LANGUAGE python SOURCES ${SWIG_INTERFACE_FILE})
swig_link_libraries(${pythonlib} ${clib})
############################################


############ 第四部分：链接 #################
# 查找Python
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

# 目标的包含目录
target_include_directories(${pythonlib} PRIVATE ${Python3_INCLUDE_DIRS})

# 确保链接Python库
target_link_libraries(${pythonlib} ${Python3_LIBRARIES})
############################################