import unittest
import os
from modules.file_utils import read_contract_data, collect_unique_contract_ids_from_file, get_housekeeper_award_list

class TestFileUtils(unittest.TestCase):

    def setUp(self):
        # Specify the path to the ContractData-SH-May_01.csv file
        self.test_file = 'tests\ContractData-SH-May_01.csv'
        # Ensure the file exists before proceeding with the test
        assert os.path.exists(self.test_file), f"File {self.test_file} does not exist."

        # Specify the path to the PerformanceData-SH-May_01.csv file
        self.performance_test_file = 'tests\PerformanceData-SH-May_01.csv'
        # Ensure the file exists before proceeding with the test
        assert os.path.exists(self.performance_test_file), f"File {self.performance_test_file} does not exist."

        # Specify the path to the HousekeeperAwards-SH-May_01.csv file
        self.housekeeper_awards_file = 'tests\PerformanceData-SH-May_01.csv'
        # Ensure the file exists before proceeding with the test
        assert os.path.exists(self.housekeeper_awards_file), f"File {self.housekeeper_awards_file} does not exist."

    def tearDown(self):
        # No cleanup needed as the file is not being deleted
        pass

    def test_read_contract_data(self):
        # Call the function and check the result
        data = read_contract_data(self.test_file)
        print("Contract Data:", data) # Print the contract data
        self.assertEqual(len(data), 2) # Check if the number of data rows is correct
        self.assertEqual(data[0]['合同ID(_id)'], '6997900857389134380') # Check if the content of the data is correct

    def test_collect_unique_contract_ids_from_file(self):
        # Call the function and check the result
        contract_ids = collect_unique_contract_ids_from_file(self.performance_test_file)
        print("Contract IDs:", contract_ids) # Print the contract IDs
        # Assuming the first contract ID in the test file is '1'
        self.assertIn('6997900857389134380', contract_ids)
        # You can add more assertions based on the expected data in your test file

    def test_get_housekeeper_award_list(self):
        # Call the function and check the result
        awards_list = get_housekeeper_award_list(self.housekeeper_awards_file)
        print("Awards List:", awards_list) # Print the awards list
        # Assuming the test file contains at least one housekeeper with awards
        self.assertIn('杨理想', awards_list)
        # You can add more assertions based on the expected data in your test file
        # For example, checking the number of awards for a specific housekeeper
        self.assertEqual(len(awards_list['杨理想']), 0)
        
if __name__ == '__main__':
    unittest.main()