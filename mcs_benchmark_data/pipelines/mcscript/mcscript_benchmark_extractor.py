import json
import xmltodict

from mcs_benchmark_data._extractor import _Extractor

from mcs_benchmark_data.path import DATA_DIR_PATH


class MCScriptBenchmarkExtractor(_Extractor):
    def __init__(
        self,
        dev_file_name: str,
        test_file_name: str,
        train_file_name: str,
        **kwds,
    ):
        self.__dev_file_name = dev_file_name
        self.__test_file_name = test_file_name
        self.__train_file_name = train_file_name

    def extract(self, **kwds):

        if self.__dev_file_name.split(".")[-1] == "xml":
            dev_json_file_name = self.xml_to_json(self.__dev_file_name)
        else:
            dev_json_file_name = self.__dev_file_name

        if self.__test_file_name.split(".")[-1] == "xml":
            test_json_file_name = self.xml_to_json(self.__test_file_name)
        else:
            test_json_file_name = self.__test_file_name

        if self.__dev_file_name.split(".")[-1] == "xml":
            train_json_file_name = self.xml_to_json(self.__train_file_name)
        else:
            train_json_file_name = self.__train_file_name

        extracted_data_dir_path = DATA_DIR_PATH / "extracted" / "MCScript"
        return {
            "benchmark_json_file_path": extracted_data_dir_path / "metadata.json",
            "dev_json_file_path": extracted_data_dir_path / dev_json_file_name,
            "test_json_file_path": extracted_data_dir_path / test_json_file_name,
            "train_json_file_path": extracted_data_dir_path / train_json_file_name,
        }

    def xml_to_json(self, xml_file_name: str, **kwds):

        loaded_data_dir_path = DATA_DIR_PATH / "raw" / "MCScript"

        parsed_file_name = xml_file_name.split(".")[0]

        json_file_name = f"{parsed_file_name}.json"

        with open(loaded_data_dir_path / xml_file_name) as xml_file:
            data_dict = xmltodict.parse(xml_file.read())

        xml_file.close()

        json_data = json.dumps(data_dict)

        extracted_data_dir_path = DATA_DIR_PATH / "extracted" / "MCScript"

        with open(extracted_data_dir_path / json_file_name, "w") as json_file:
            json_file.write(json_data)

        json_file.close()

        return json_file_name


if __name__ == "__main__":
    MCScriptBenchmarkExtractor(
        dev_xml_file_name="dev-data.xml",
        test_xml_file_name="test-data.xml",
        train_xml_file_name="train-data.xml",
    ).extract()
