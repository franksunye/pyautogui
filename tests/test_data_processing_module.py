import unittest
from modules.data_processing_module import process_data_ctt1mc_shanghai
from modules.file_utils import read_contract_data, collect_unique_contract_ids_from_file, get_housekeeper_award_list

class TestDataProcessingModule(unittest.TestCase):
    def test_process_data_ctt1mc_shanghai(self):
        # 准备测试数据
        contract_data_file = 'tests\ContractData-SH-May_01.csv'
        performance_data_file = 'tests\PerformanceData-SH-May_01.csv'
        housekeeper_awards_file = 'tests\PerformanceData-SH-May_01.csv'
        
        # 从文件中读取数据
        contract_data = read_contract_data(contract_data_file)
        existing_contract_ids = collect_unique_contract_ids_from_file(performance_data_file)
        housekeeper_award_lists = get_housekeeper_award_list(housekeeper_awards_file)

        # 打印读取到的数据
        print("Contract Data:", contract_data)
        print("Existing Contract IDs:", existing_contract_ids)
        print("Housekeeper Award Lists:", housekeeper_award_lists)
        
        # 调用函数并获取结果
        performance_data = process_data_ctt1mc_shanghai(contract_data, existing_contract_ids, housekeeper_award_lists)
        print("Processed Performance Data:", performance_data)

        # 定义期望的结果长度
        expected_length = 1 # 假设期望的结果长度为5，请根据实际情况调整这个值

        # 断言结果
        self.assertEqual(len(performance_data), expected_length)
        # 根据你的预期，添加更多的断言语句

if __name__ == '__main__':
    unittest.main()