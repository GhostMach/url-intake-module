# Authored by: Adam H. Meadvin 
# Email: h3rbert@proton.me
# GitHub: @GhostMach 
# Creation Date: 08 June 2023

import re
import os
import pandas

# main function called to initiate terminal prompt for URL(s)
def accept_input():
    def confirm_answer(counter_arg, arg_choice):
        confirm_verify_counter = 0
        response_answer = input(counter_arg)
        while (confirm_verify_counter < 3): 
            if arg_choice == "letters":
                if response_answer.lower() in ["yes", "y"]:
                    return True
                elif response_answer.lower() in ["no", "n"]:
                    return False
                else:
                    confirm_verify_counter += 1
                    response_answer = input(counter_arg)                
            if arg_choice == "numeric": 
                if response_answer in ["1", "2"]:
                    return response_answer
                else:
                    confirm_verify_counter += 1
                    response_answer = input(counter_arg)                     
        if confirm_verify_counter == 3:
            print('You\'ve reached the maximum attempts--this program will now exit.')
            exit()
    
    def term_program(func_arg):
        term_verified= func_arg
        if term_verified:
            exit()
        else:
            return term_verified

    def is_valid_url(url_arg):
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
            r'localhost|' # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        url_nospace = url_arg.replace(" ", "")
        if url_nospace is not None and regex.search(url_nospace):
            return True
        else:
            return False
    
    def read_dataframe(data_input_arg, isvalid_func_arg):
        cross = "\u2717" # ascii code
        checkmark = "\u2713" # ascii code
        raw_url = []
        # verifies if data rows are populated--skipping empty cells.           
        for index, row in data_input_arg.iterrows():
            w = row.iloc[0]
            if w == "":
                continue
            elif isvalid_func_arg(w):
                raw_url.append(w)
            else:
                print(f'{cross} The following entry, "{w}" will not be processed because it\'s not a valid URL.')
        processed_url_series = pandas.Series(raw_url, name='Verified URLs', dtype=object)
        urls_to_process = len(processed_url_series.drop_duplicates().index)
        if urls_to_process == 0:
            print(f"\n{cross} {urls_to_process} URL(s) will be processed because of bad data or missing values.")
            return None
        else:
            print(f"\n{checkmark} {urls_to_process} URL(s) will be processed--any duplicate enteries were removed.")            
            return processed_url_series.str.lower().drop_duplicates()

    final_answer = True
    verified_urls = None
    single_verified_url = None
    while final_answer: 
        numeric_response = 'Enter "1" [File] or "2" [URL]: '
        verified_numeric_response = confirm_answer(numeric_response, "numeric")            
        if verified_numeric_response == '1': 
            file_verify_counter = 0              
            while (file_verify_counter < 3):
                format_file_path = ''
                file_path = input("Enter a valid file path; empty files will not be processed - type or copy location and paste: ")
                format_file_path = file_path.replace('"', '')                           
                if os.path.exists(format_file_path) and os.path.isfile(format_file_path):
                    try:
                        root, ext = os.path.splitext(format_file_path)  
                        if ext == '.csv':
                            web_url_raw = pandas.read_csv(format_file_path, header=None)
                            verified_urls = read_dataframe(web_url_raw, is_valid_url)
                            break
                        elif ext == '.txt':
                            web_url_raw = pandas.read_fwf(format_file_path, header=None)
                            verified_urls = read_dataframe(web_url_raw, is_valid_url)
                            break
                        elif ext == '.xlsx': # need to install python package "openpyxl" to run this routine.
                            web_url_raw = pandas.concat(pandas.read_excel(format_file_path, na_filter=False, sheet_name=None, header=None), ignore_index=True)
                            verified_urls = read_dataframe(web_url_raw, is_valid_url)
                            break                           
                        else:                          
                            print('Invalid File Extension. Try Again.')
                            file_verify_counter += 1
                    except pandas.errors.EmptyDataError:
                        print(f'No columns to parse from file, "{format_file_path}"')
                        file_verify_counter += 1
                else:                            
                    print('Invalid Entry. Try Again.')
                    file_verify_counter += 1        
            if file_verify_counter == 3:
                term_opt = 'Would you like to exit this program - Enter (Y)es or (N)o: '
                term_program(confirm_answer(term_opt, "letters"))    
        else:
            URL_verify_counter = 0
            while (URL_verify_counter < 3):
                single_web_url_raw = input("Enter only one website url: ")
                if is_valid_url(single_web_url_raw):
                    single_verified_url = single_web_url_raw.lower()
                    break
                else:                           
                    print('Invalid Entry. Try Again.')
                    URL_verify_counter += 1
            if URL_verify_counter == 3:
                term_opt = 'Would you like to exit this program - Enter (Y)es or (N)o: '
                term_program(confirm_answer(term_opt, "letters"))
        final_confirm = "Would you like to (re)enter a new web link or file path? - Enter (Y)es or (N)o: "
        final_answer = confirm_answer(final_confirm, "letters")

    if type(verified_urls) == pandas.core.series.Series or type(verified_urls) == pandas.core.frame.DataFrame:
        return verified_urls.tolist() # outputs object class as a "list" and not a pandas object.
    elif single_verified_url:
        return [single_verified_url] # variable placed in "array" so the object class output is a "list" item and not a pandas object.
    else:
        return None
