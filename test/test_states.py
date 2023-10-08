import pytest
from aiogram.fsm.state import StatesGroup, State

from core.exceptions import DialogYamlException, StatesGroupNotFoundError
from core.states import YAMLStatesManager


@pytest.fixture
def get_empty_states_manager() -> YAMLStatesManager:
    states_manager = YAMLStatesManager()
    states_manager._states_groups_map_ = {}
    return states_manager


@pytest.fixture
def get_none_empty_states_manager() -> YAMLStatesManager:
    states_manager = YAMLStatesManager()
    states = states_manager.parse_raw_states_from_list({
        'group1:state1',
        'group1:state2',
        'group1:state3',
        'group2:state1',
        'group2:state2',
    })
    states_manager._states_groups_map_.update(states)
    return states_manager


class TestYAMLStatesManager:

    def test_build_states_groups(self, get_empty_states_manager):
        # Given
        states_manager = get_empty_states_manager

        # When
        states_manager._build_states_groups({'group1': [], 'group2': []})

        # Then
        assert isinstance(states_manager.get_by_name('group1'), StatesGroup)
        assert isinstance(states_manager.get_by_name('group2'), StatesGroup)

    def test_build_states(self, get_empty_states_manager):
        # Given
        states_manager = get_empty_states_manager

        # When
        result = states_manager._build_states({'state1', 'state2', 'state3'})

        # Then
        assert all(isinstance(state, State) for state in result.values())

    def test_get_by_name(self, get_none_empty_states_manager):
        # Given
        states_manager = get_none_empty_states_manager

        # When
        result = states_manager.get_by_name('group1:state1')

        # Then
        assert isinstance(result, State)

    def test_get_by_names(self, get_none_empty_states_manager):
        # Given
        states_manager = get_none_empty_states_manager

        # When
        result = states_manager.get_by_names('group1', 'state1')

        # Then
        assert isinstance(result, State)

    def test_add_state_to_map(self, get_none_empty_states_manager):
        # Given
        states_manager = get_none_empty_states_manager
        group_name = 'group1'
        state = State('new_state', group_name)

        # When
        states_manager.add_state_to_map(group_name, state)

        # Then
        assert isinstance(states_manager.get_by_name('group1:new_state'), State)

    def test_add_state_to_map_without_group_name(self, get_none_empty_states_manager):
        # Given
        states_manager = get_none_empty_states_manager
        none_existed_group_name = None
        state = State('new_state')

        # When, Then
        with pytest.raises(StatesGroupNotFoundError):
            states_manager.add_state_to_map(none_existed_group_name, state)

    def test_add_state_to_map_with_none_existed_group(self, get_none_empty_states_manager):
        # Given
        states_manager = get_none_empty_states_manager
        none_existed_group_name = 'none_existed_group'
        state = State('new_state', 'group1')

        # When, Then
        with pytest.raises(StatesGroupNotFoundError):
            states_manager.add_state_to_map(none_existed_group_name, state)

    def test_add_states_to_map(self, get_none_empty_states_manager):
        # Given
        states_manager = get_none_empty_states_manager
        group_name = 'group1'
        states = {
            'new_state1': State('new_state1', group_name),
            'new_state2': State('new_state2', group_name)
        }

        # When
        states_manager.add_states_to_map(group_name, states)

        # Then
        assert isinstance(states_manager.get_by_name('group1:new_state1'), State)
        assert isinstance(states_manager.get_by_name('group1:new_state2'), State)

    def test_valid_raw_states_with_group_name(self, get_empty_states_manager):
        # Given
        raw_states_list = {'group1:state1', 'group1:state2', 'group2:state3', 'group2:state4'}
        states_manager = get_empty_states_manager

        # When
        parsed_states = states_manager.parse_raw_states_from_list(raw_states_list)

        # Then
        assert len(parsed_states) == 6
        assert isinstance(parsed_states['group1'], StatesGroup)
        assert isinstance(parsed_states['group1'].state1, State)
        assert isinstance(parsed_states['group1'].state2, State)
        assert isinstance(parsed_states['group2'], StatesGroup)
        assert isinstance(parsed_states['group2'].state3, State)
        assert isinstance(parsed_states['group2'].state4, State)

    def test_valid_raw_states_without_group_name(self, get_empty_states_manager):
        # Given
        raw_states_list = {'state1', 'state2', 'state3'}
        states_manager = get_empty_states_manager

        # When/Then
        with pytest.raises(DialogYamlException):
            parsed_states = states_manager.parse_raw_states_from_list(raw_states_list)

    def test_empty_raw_states_list(self, get_empty_states_manager):
        # Given
        raw_states_list = set()
        states_manager = get_empty_states_manager

        # When
        parsed_states = states_manager.parse_raw_states_from_list(raw_states_list)

        # Then
        assert len(parsed_states) == 0

    def test_invalid_raw_states_format(self, get_empty_states_manager):
        # Given
        raw_states_list = {'group1:state1', 'group2', 'state3'}
        states_manager = get_empty_states_manager

        # When/Then
        with pytest.raises(DialogYamlException):
            states_manager.parse_raw_states_from_list(raw_states_list)

    def test_invalid_group_name(self, get_empty_states_manager):
        # Given
        raw_states_list = {'group1:state1', ':state2', 'group2:state3'}
        states_manager = get_empty_states_manager

        # When/Then
        with pytest.raises(DialogYamlException):
            states_manager.parse_raw_states_from_list(raw_states_list)

    def test_invalid_state_name(self, get_empty_states_manager):
        # Given
        raw_states_list = {'group1:state1', 'group2:', 'group2:state3'}
        states_manager = get_empty_states_manager

        # When/Then
        with pytest.raises(DialogYamlException):
            states_manager.parse_raw_states_from_list(raw_states_list)

    def test_formatted_states(self, get_empty_states_manager):
        # Given
        group_name = 'group1'
        state_name = 'state1'
        states_manager = get_empty_states_manager

        # When
        actual_raw_state_name = states_manager.format_state_name(group_name, state_name)

        # Then
        assert actual_raw_state_name == f'{group_name}:{state_name}'


class TestBuildStatesFromYAMLData:

    def test_valid_data(self, get_empty_states_manager):
        # Given
        states_manager = get_empty_states_manager
        data = {
            'dialogs': {
                'group1': {
                    'windows': {
                        'state1': {},
                        'state2': {}
                    }
                },
                'group2': {
                    'windows': {
                        'state3': {},
                        'state4': {}
                    }
                }
            }
        }

        # When
        states_manager.build_states_from_yaml_data(data)

        # Then
        assert isinstance(states_manager.get_by_name('group1'), StatesGroup)
        assert isinstance(states_manager.get_by_name('group2'), StatesGroup)
        assert isinstance(states_manager.get_by_name('group1:state1'), State)
        assert isinstance(states_manager.get_by_name('group1:state2'), State)
        assert isinstance(states_manager.get_by_name('group2:state3'), State)
        assert isinstance(states_manager.get_by_name('group2:state4'), State)

    def test_invalid_data_type(self, get_empty_states_manager):
        # Given
        states_manager = get_empty_states_manager
        data = 'invalid_data'

        # When, Then
        with pytest.raises(DialogYamlException):
            states_manager.build_states_from_yaml_data(data)

    def test_empty_data(self, get_empty_states_manager):
        # Given
        states_manager = get_empty_states_manager
        data = {}

        # When, Then
        with pytest.raises(DialogYamlException):
            states_manager.build_states_from_yaml_data(data)

    def test_other_tags(self, get_empty_states_manager):
        # Given
        states_manager = get_empty_states_manager
        data = {'other_tag': {}}

        # When, Then
        with pytest.raises(DialogYamlException):
            states_manager.build_states_from_yaml_data(data)

    def test_missing_windows_tag(self, get_empty_states_manager):
        # Given
        states_manager = get_empty_states_manager
        data = {
            'dialogs': {
                'group1': {'not_windows_tag': {}},
                'group2': {'not_windows_tag': {}}
            }
        }

        # When, Then
        with pytest.raises(DialogYamlException):
            states_manager.build_states_from_yaml_data(data)

    def test_build_states_from_invalid_dialogs_data_type(self, get_empty_states_manager):
        # Given
        states_manager = get_empty_states_manager
        data = {
            'dialogs': {
                'group1': {'windows': 'invalid_data'},
            }
        }

        # When, Then
        with pytest.raises(DialogYamlException):
            states_manager.build_states_from_yaml_data(data)

    def test_build_states_from_invalid_windows_data_type(self, get_empty_states_manager):
        # Given
        states_manager = get_empty_states_manager
        data = {
            'dialogs': {
                'group1': 'invalid_data',
            }
        }

        # When, Then
        with pytest.raises(DialogYamlException):
            states_manager.build_states_from_yaml_data(data)


class TestExtractGroupAndStateNames:

    def test_valid_raw_states_group_with_one_delimiter(self, get_empty_states_manager):
        # Given
        raw_states_group = 'group1:state1'
        expected_group_name = 'group1'
        expected_state_name = 'state1'
        states_manager = get_empty_states_manager

        # When
        group_name, state_name = states_manager.extract_group_and_state_names(raw_states_group)

        # Then
        assert group_name == expected_group_name
        assert state_name == expected_state_name

    def test_valid_raw_states_group_with_two_delimiters(self, get_empty_states_manager):
        # Given
        raw_states_group = 'group1:state1:state2'
        states_manager = get_empty_states_manager

        # When/Then
        with pytest.raises(DialogYamlException):
            states_manager.extract_group_and_state_names(raw_states_group)

    def test_empty_raw_states_group(self, get_empty_states_manager):
        # Given
        raw_states_group = ''
        states_manager = get_empty_states_manager

        # When/Then
        with pytest.raises(DialogYamlException):
            states_manager.extract_group_and_state_names(raw_states_group)

    def test_invalid_type_raw_states_group(self, get_empty_states_manager):
        # Given
        raw_states_group = 123
        states_manager = get_empty_states_manager

        # When/Then
        with pytest.raises(DialogYamlException):
            states_manager.extract_group_and_state_names(raw_states_group)


class TestIncludeStatesGroupsByClass:
    def test_includes_new_states_group_subclass_successfully(self):
        # Given
        manager = YAMLStatesManager()

        class MyStatesGroup(StatesGroup):
            STATE_1 = State()
            STATE_2 = State()

        # When
        manager.include_states_group_by_class(MyStatesGroup)

        # Then
        assert manager.get_by_name('MyStatesGroup') is not None

    def test_includes_new_states_group_with_all_states_successfully(self):
        # Given
        manager = YAMLStatesManager()

        class MyStatesGroup(StatesGroup):
            STATE_1 = State()
            STATE_2 = State()

        # When
        manager.include_states_group_by_class(MyStatesGroup)

        # Then
        assert len(manager._states_groups_map_) == 3
        assert manager.get_by_name('MyStatesGroup') is not None
        assert manager.get_by_name(manager.format_state_name('MyStatesGroup', 'STATE_1')) is not None
        assert manager.get_by_name(
            manager.format_state_name('MyStatesGroup', 'STATE_2')
        ) is not None

    def test_raises_exception_if_custom_state_class_not_subclass_of_states_group(self):
        # Given
        manager = YAMLStatesManager()

        class MyStatesGroup:
            pass

        # When/Then
        with pytest.raises(DialogYamlException):
            manager.include_states_group_by_class(MyStatesGroup)

    def test_raises_exception_if_states_group_states_attribute_empty(self):
        # Given
        manager = YAMLStatesManager()

        class MyStatesGroup(StatesGroup):
            pass

        # When/Then
        with pytest.raises(DialogYamlException):
            manager.include_states_group_by_class(MyStatesGroup)
