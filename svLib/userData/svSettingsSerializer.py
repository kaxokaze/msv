import re
from pydoc import locate

from dicttoxml import dicttoxml
import xmltodict
from xml.dom.minidom import parseString
from svLib.log import svLogger
from svLib.utils import stdHelper


####
# Obsolete format for backward compatibility
####

def parseResolutionsFile(file_path):
    parsed_resolutions = ""

    try:
        with open(file_path, 'r') as resolutions_file:
            parsed_resolutions = resolutions_file.read()
    except FileNotFoundError:
        pass  # don't care, obsolete anyway
    except Exception as e:
        pass

    return parsed_resolutions


def parseUserCfgFile(file_path, res_file_path = None):
    num_settings_fields = 11
    result_dict = None
    try:
        with open(file_path, 'r') as config_file:
            entries = stdHelper.loadFileEntries(config_file)

            if len(entries) >= num_settings_fields:
                try:
                    result_dict = {
                        'min_page_time': float(entries[0]),
                        'max_page_time': float(entries[1]),
                        'timeout_interval': int(entries[2]),
                        'success_page_min_size': int(entries[3]),
                        'max_prox_fails': int(entries[4]),
                        'do_snapshots': entries[5] == 'True',
                        'count_success_only': entries[6] == 'True',
                        'use_js_ref_inj': entries[7] == 'True',
                        'js_ref_inj_timeout': int(entries[8]),
                        'after_script_wait': float(entries[9]),
                        'enable_alexa': entries[10] == 'True'
                    }
                except Exception as e:
                    svLogger.log_error('Reading data from the config file failed somehow:', e)
    except FileNotFoundError:
        pass  # old user config not found, don't care

    resolutions = parseResolutionsFile(res_file_path)

    return result_dict, resolutions

####
# End of obsolete section
####


def parseUserXMLFile(file_path):
    dictionary = None

    try:
        with open(file_path, 'r') as config_file:
            xml_string = config_file.read()
            xml_ordered_dictionary = xmltodict.parse(xml_string)['root']
            dictionary = {}
            for field_name in xml_ordered_dictionary:
                dictionary[field_name] = convert_od_field(xml_ordered_dictionary[field_name])
    except Exception as e:
        svLogger.log_error('Reading data from the config file failed somehow:', e)

    return dictionary


def convert_od_field(od_field):
    field_type = od_field["@type"]

    value = None
    if "#text" in od_field:
        value = convert_to_type(od_field["#text"], field_type)
    elif locate(field_type) == list:
        items = od_field["item"]
        value = []

        for item in items:
            value.append(convert_od_field(item))

    return value


def convert_to_type(param, field_type):
    v_type = locate(field_type)
    if v_type is bool:
        return param == "True"
    else:
        return v_type(param)


def serializeUserXMLFile(file_path, value):
    try:
        with open(file_path, 'w+') as xml_file:
            xml_string = dicttoxml.dicttoxml(value).decode()
            xml_obj = parseString(xml_string)
            xml_string_formatted = xml_obj.toprettyxml()
            xml_file.write(xml_string_formatted)
    except Exception as e:
        svLogger.log_error('Saving config to a file failed somehow:', e)


def parseScriptsFile(file_path):
    user_scripts = []
    try:
        with open(file_path, 'r') as scripts_file:
            entries = stdHelper.loadFileEntries(scripts_file)
            for script in entries:
                script_fields = re.findall(r'\"[^"]+\"|""', script)
                for i in range(len(script_fields)):
                    script_fields[i] = script_fields[i][1:-1]
                user_scripts.append(script_fields)
    except Exception as e:
        svLogger.log_event('Reading data from the scripts file failed:', e)

    return user_scripts


def serializeScriptsFile(file_path, value):
    try:
        with open(file_path, 'w+') as scripts_file:
            for script in value:
                script_str = '"' + '" "'.join(map(str, script)) + '"'
                scripts_file.write(script_str + '\n')
    except Exception as e:
        svLogger.log_error('Saving userscripts to a file failed somehow:', e)
