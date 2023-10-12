import os

import yaml
from yamlinclude import YamlIncludeConstructor


class YAMLReader:
    """The YAMLReader class is responsible for reading data
    from a YAML file and returning it as a dictionary.
    """

    @classmethod
    def read_data_to_dict(
        cls, data_file_path: str, data_dir_path: str = ""
    ) -> dict:
        """Reads data from a YAML file and returns it as a dictionary.

        :param data_file_path: Path to the YAML file.
        :param data_dir_path: Path to the directory containing the YAML file.

        :return: A dictionary with the data from the YAML file.
        :rtype: dict

        :raises FileNotFoundError: If the YAML file is not found.
        """

        YamlIncludeConstructor.add_to_loader_class(
            loader_class=yaml.FullLoader, base_dir=data_dir_path
        )

        abs_data_file_path = os.path.abspath(
            os.path.join(data_dir_path, data_file_path)
        )

        if not os.path.exists(abs_data_file_path):
            raise FileNotFoundError(f"File not found {abs_data_file_path!r}.")

        with open(abs_data_file_path, "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        return data
