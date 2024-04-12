# sacn_privacy_for_ios
扫码目录是否存在隐私清单API，并生成隐私清单

此项目特别适合扫描第三方库，生成隐私清单文件，不需要分析代码具体原因如何

目的：可以扫描目录下的文件，找到使用隐私清单api的地方，并生成隐私清单文件

运行环境：python3

目标产物：PrivacyInfo.xcprivacy，此文件为iOS项目的隐私清单

参数：

project_directory：项目目录，扫描的目录

output_path：输出文件路径

注意：

可以修改privacy_info字典，来确定使用API的理由和生成文件的细节，看需要，目前取最大原因的合集
