import re
import os
import plistlib

# 目标字符串集合
file_timestamp_apis = ['NSFileCreationDate', 'NSFileModificationDate', 'fileModificationDate',
 'NSURLContentModificationDateKey', 'NSURLCreationDateKey', 'getattrlist', 'getattrlistbulk', 
 'fgetattrlist', 'stat ', 'fstat', 'fstatat', 'lstat', 'getattrlistat']
file_timestamp_reasons = [('DDA9.1', '显示文件时间戳。出于此原因访问的信息或任何派生信息可能不会发送到设备外。'),
('C617.1', '访问应用程序容器、应用程序组容器、CloudKit容器内文件的时间戳、大小或其他元数据。'),
('3B52.1', '访问用户明确授予访问权限的文件或目录的时间戳、大小或其他元数据，例如使用文档选择器视图控制器。'),
('0A2A.1', '第三方 SDK 提供文件时间戳 API 的包装函数供应用程序使用，并且您仅在应用程序调用您的包装函数时才访问文件时间戳 API，请声明此原因。 此原因只能由第三方 SDK 声明。')]

system_boot_time_apis = ['systemUptime', 'mach_absolute_time']
system_boot_time_reasons = [('35F9.1', '访问系统启动时间，以便测量应用程序内发生的事件之间经过的时间量或执行计算以启用计时器。目前只能选择这个'),
('8FFB.1', '访问系统启动时间，以计算应用程序内发生的事件的绝对时间戳，例如与 UIKit 或 AVFAudio 框架相关的事件。'),
('3D61.1', '使用设备的人选择提交的可选错误报告中包含系统启动时间信息。 系统启动时间信息必须作为报告的一部分显着地向人员显示。')]

disk_space_apis = ['NSURLVolumeAvailableCapacityKey', 'NSURLVolumeAvailableCapacityForImportantUsageKey',
'NSURLVolumeAvailableCapacityForOpportunisticUsageKey', 'NSURLVolumeTotalCapacityKey', 'NSFileSystemFreeSize',
'NSFileSystemSize', 'statfs', 'statvfs', 'fstatfs', 'fstatvfs', 'getattrlist', 'fgetattrlist', 'getattrlistat']
disk_space_reasons = [('85F4.1', '向使用该设备的人员显示磁盘空间信息。'),
('E174.1', '检查是否有足够的磁盘空间来写入文件，或者检查磁盘空间是否不足，以便应用程序可以在磁盘空间不足时删除文件。'),
('7D9E.1', '使用设备的人员选择提交的可选错误报告中包含磁盘空间信息。'),
('B728.1', '设备健康研究应用程序，并且您访问此 API 类别来检测并通知研究参与者磁盘空间不足影响研究数据收集，请声明此原因。')]

active_keyboard_apis = ['activeInputModes']
active_keyboard_reasons = [('3EC4.1', '应用程序是自定义键盘应用程序，并且您访问此 API 类别以确定设备上处于活动状态的键盘，请声明此原因。'),
('54BD.1', '访问活动键盘信息，以便向使用该设备的人员呈现正确的自定义用户界面。')]

user_defaults_apis = ['NSUserDefaults']
user_defaults_reasons = [('CA92.1', '访问用户默认读取和写入只能由应用程序本身访问的信息。'),
('1C8F.1', '访问用户默认值以读取和写入仅可由与应用程序本身属于同一应用程序组的成员的应用程序、应用程序扩展和应用程序剪辑访问的信息。'),
('C56D.1', '第三方 SDK 围绕用户默认 API 提供包装函数供应用程序使用，并且您仅在应用程序调用您的包装函数时才访问用户默认 API，请声明此原因。 此原因只能由第三方 SDK 声明。'),
('AC6B.1', '访问用户默认读取 com.apple.configuration.managed 密钥以检索 MDM 设置的托管应用程序配置。')]

file_timestamp_found_strings = []
system_boot_time_found_strings = []
disk_space_found_strings = []
active_keyboard_found_strings = []
user_defaults_found_strings = []

def scan_content(apis, content, file_path):
    file_found_strings = []
    for target_string in apis:
        pattern = re.escape(target_string)
        matches = re.findall(pattern, content)
        if matches:
            file_found_strings.append((file_path, target_string, matches))
    return file_found_strings

def scan_for_string_set(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.swift', '.m', '.mm', '.cpp', '.c')):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    file_timestamp_found_strings.extend(scan_content(file_timestamp_apis, content, file_path))

                    system_boot_time_found_strings.extend(scan_content(system_boot_time_apis, content, file_path))

                    disk_space_found_strings.extend(scan_content(disk_space_apis, content, file_path))

                    active_keyboard_found_strings.extend(scan_content(active_keyboard_apis, content, file_path))
                    
                    user_defaults_found_strings.extend(scan_content(user_defaults_apis, content, file_path))


def print_result(title, found_strings, reasons):
    print((title + ':'))
    for usage in found_strings:
        print(f"File: {usage[0]}, String: {usage[1]}, Count: {len(usage[2])}")
    print()
    print('reasons:')
    for usage in reasons:
        print(f"type: {usage[0]}, reson: {usage[1]}")
    print()


# 项目目录
project_directory = '*******'
output_path = './PrivacyInfo.xcprivacy'

# 执行扫描
scan_for_string_set(project_directory)


# 打印结果
print_result('File timestamp APIs', file_timestamp_found_strings, file_timestamp_reasons)
print_result('System boot time APIs', system_boot_time_found_strings, system_boot_time_reasons)
print_result('Disk space APIs', disk_space_found_strings, disk_space_reasons)
print_result('Active keyboard APIs', active_keyboard_found_strings, active_keyboard_reasons)
print_result('User defaults APIs', user_defaults_found_strings, user_defaults_reasons)


privacy_info = {
    'NSPrivacyTracking': False,
    'NSPrivacyTrackingDomains':[],
    'NSPrivacyCollectedDataTypes': [],
    'NSPrivacyAccessedAPITypes': []
}

if len(file_timestamp_found_strings) > 0:
    privacy_info['NSPrivacyAccessedAPITypes'].append({'NSPrivacyAccessedAPIType':'NSPrivacyAccessedAPICategoryFileTimestamp',
     'NSPrivacyAccessedAPITypeReasons': ['DDA9.1', 'C617.1', '3B52.1']})

if len(system_boot_time_found_strings) > 0:
    privacy_info['NSPrivacyAccessedAPITypes'].append({'NSPrivacyAccessedAPIType':'NSPrivacyAccessedAPICategorySystemBootTime',
     'NSPrivacyAccessedAPITypeReasons': ['35F9.1']})

if len(disk_space_found_strings) > 0:
    privacy_info['NSPrivacyAccessedAPITypes'].append({'NSPrivacyAccessedAPIType':'NSPrivacyAccessedAPICategoryDiskSpace',
     'NSPrivacyAccessedAPITypeReasons': ['85F4.1', 'E174.1', '7D9E.1']})

if len(active_keyboard_found_strings) > 0:
    privacy_info['NSPrivacyAccessedAPITypes'].append({'NSPrivacyAccessedAPIType':'NSPrivacyAccessedAPICategoryActiveKeyboard',
     'NSPrivacyAccessedAPITypeReasons': ['3EC4.1', '54BD.1']})

if len(user_defaults_found_strings) > 0:
    privacy_info['NSPrivacyAccessedAPITypes'].append({'NSPrivacyAccessedAPIType':'NSPrivacyAccessedAPICategoryUserDefaults',
     'NSPrivacyAccessedAPITypeReasons': ['CA92.1', '1C8F.1']})

# 写入文件
with open(output_path, 'wb') as file:
    plistlib.dump(privacy_info, file)
