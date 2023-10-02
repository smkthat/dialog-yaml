import logging
import os

import yaml
from yamlinclude import YamlIncludeConstructor

logger = logging.getLogger(__name__)


class YAMLReader:
    @classmethod
    def read_data_to_dict(cls, data_file_path: str, data_dir_path: str = None) -> dict:
        data = {}

        YamlIncludeConstructor.add_to_loader_class(
            loader_class=yaml.FullLoader,
            base_dir=data_dir_path
        )

        abs_data_file_path = os.path.abspath(os.path.join(data_dir_path, data_file_path))
        logger.debug(f'Read {abs_data_file_path!r}')

        if os.path.exists(abs_data_file_path):
            with open(abs_data_file_path, 'r') as file:
                data = yaml.load(file, Loader=yaml.FullLoader)
        else:
            logger.error(f'File not found {abs_data_file_path!r}')

        return data
