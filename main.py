from core.core import YAMLDialogBuilder

if __name__ == '__main__':
    dialogs = YAMLDialogBuilder.build(yaml_dir_path='data', yaml_file_name='dialogs.yaml')
