#TODO: Add specific messages upon fail
#TODO: Add cmd line options to run subsets of tests https://docs.pytest.org/en/7.1.x/example/simple.html

import os
from edgar.downloader import write_page, download_files_10k

test_url = r"https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm"

# ================================================
# Helper functions:
# ================================================

def check_html_files_are_same(file1_path, file2_path):
    try:
        with open(file1_path, 'r', encoding='utf-8') as file1:
            content1 = file1.read()

        with open(file2_path, 'r', encoding='utf-8') as file2:
            content2 = file2.read()

        if content1 == content2:
            return True
        else:
            return False

    except FileNotFoundError:
        print("One or both of the files were not found.")

# ================================================
# Tests:
# ================================================
        
def test_write_page():
    errors = []
    control_path = r"tests\test_directory\control\amzn-20231231.htm"
    result_path = r"tests\test_directory\result\amzn-20231231.htm"

    if not write_page(test_url, result_path):
        errors.append("write_page() was unsuccessful")

    if not check_html_files_are_same(control_path, result_path):
        errors.append("Did not successfully download the specified html page")

    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_download_files10k():
    errors = []
    control_dir_path = r"tests/test_directory/control/10k_htmls"
    result_dir_path = r"tests/test_directory/result/10k_htmls"
    
    download_files_10k('AAPL', result_dir_path)

    control_files = os.listdir(control_dir_path)
    control_paths = [os.path.join(control_dir_path, file_name) for file_name in control_files]
    result_files = os.listdir(result_dir_path)
    result_paths = [os.path.join(result_dir_path, file_name) for file_name in result_files]

    if len(control_paths) != len(result_paths):
        errors.append("The expected amount of files was not downloaded")

    for ctrl, res in zip(control_paths, result_paths):
        if not check_html_files_are_same(ctrl, res):
            errors.append(f"The contents of {ctrl} did not match the contents of {res}.")    
    
    assert not errors, "errors occured:\n{}".format("\n".join(errors))