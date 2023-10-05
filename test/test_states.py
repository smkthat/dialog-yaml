import pytest
from aiogram.fsm.state import StatesGroup, State

from core.exceptions import InvalidTagName, DialogYamlException, InvalidTagDataType, StatesGroupNotFoundError
from core.states import YAMLStatesBuilder


@pytest.fixture
def get_empty_yaml_states_builder() -> YAMLStatesBuilder:
    states_holder = YAMLStatesBuilder()
    states_holder._states_groups_map_ = {}
    return states_holder


@pytest.fixture
def get_none_empty_yaml_states_builder() -> YAMLStatesBuilder:
    states_holder = YAMLStatesBuilder()
    group_name = 'group1'
    states = {'state1': State('state1'), 'state2': State('state2')}
    group_class = type(group_name, (StatesGroup,), states)
    group1 = group_class()
    states_holder._states_groups_map_ = {
        'group1': group1,
        **{state.state: state
           for state_name, state in states.items()}
    }
    return states_holder


class TestYAMLStatesHBuilder:

    def test_build_states_groups(self, get_empty_yaml_states_builder):
        # Given
        yaml_states_builder = get_empty_yaml_states_builder

        # When
        yaml_states_builder._build_states_groups({'group1': [], 'group2': []})

        # Then
        assert isinstance(yaml_states_builder.get_by_name('group1'), StatesGroup)
        assert isinstance(yaml_states_builder.get_by_name('group2'), StatesGroup)

    def test_build_states(self, get_empty_yaml_states_builder):
        # Given
        yaml_states_builder = get_empty_yaml_states_builder

        # When
        result = yaml_states_builder._build_states({'state1', 'state2', 'state3'})

        # Then
        assert all(isinstance(state, State) for state in result.values())

    def test_get_by_name(self, get_none_empty_yaml_states_builder):
        # Given
        yaml_states_builder = get_none_empty_yaml_states_builder

        # When
        result = yaml_states_builder.get_by_name('group1:state1')

        # Then
        assert isinstance(result, State)

    def test_get_by_names(self, get_none_empty_yaml_states_builder):
        # Given
        yaml_states_builder = get_none_empty_yaml_states_builder

        # When
        result = yaml_states_builder.get_by_names('group1', 'state1')

        # Then
        assert isinstance(result, State)

    def test_add_state_to_map(self, get_none_empty_yaml_states_builder):
        # Given
        yaml_states_builder = get_none_empty_yaml_states_builder
        group_name = 'group1'
        state = State('new_state', group_name)

        # When
        yaml_states_builder.add_state_to_map(group_name, state)

        # Then
        assert isinstance(yaml_states_builder.get_by_name('group1:new_state'), State)

    def test_add_state_to_map_without_group_name(self, get_none_empty_yaml_states_builder):
        # Given
        yaml_states_builder = get_none_empty_yaml_states_builder
        group_name = 'other_group'
        state = State('new_state', 'group1')

        # When, Then
        with pytest.raises(StatesGroupNotFoundError):
            yaml_states_builder.add_state_to_map(group_name, state)

    def test_add_states_to_map(self, get_none_empty_yaml_states_builder):
        # Given
        yaml_states_builder = get_none_empty_yaml_states_builder
        group_name = 'group1'
        states = {
            'new_state1': State('new_state1', group_name),
            'new_state2': State('new_state2', group_name)
        }

        # When
        yaml_states_builder.add_states_to_map(group_name, states)

        # Then
        assert isinstance(yaml_states_builder.get_by_name('group1:new_state1'), State)
        assert isinstance(yaml_states_builder.get_by_name('group1:new_state2'), State)

    def test_valid_raw_states_with_group_name(self, get_empty_yaml_states_builder):
        # Given
        raw_states_list = {'group1:state1', 'group1:state2', 'group2:state3', 'group2:state4'}
        yaml_states_builder = get_empty_yaml_states_builder

        # When
        parsed_states = yaml_states_builder.parse_raw_states_from_list(raw_states_list)

        # Then
        assert len(parsed_states) == 6
        assert isinstance(parsed_states['group1'], StatesGroup)
        assert isinstance(parsed_states['group1'].state1, State)
        assert isinstance(parsed_states['group1'].state2, State)
        assert isinstance(parsed_states['group2'], StatesGroup)
        assert isinstance(parsed_states['group2'].state3, State)
        assert isinstance(parsed_states['group2'].state4, State)

    def test_valid_raw_states_without_group_name(self, get_empty_yaml_states_builder):
        # Given
        raw_states_list = {'state1', 'state2', 'state3'}
        yaml_states_builder = get_empty_yaml_states_builder

        # When/Then
        with pytest.raises(DialogYamlException):
            parsed_states = yaml_states_builder.parse_raw_states_from_list(raw_states_list)

    def test_empty_raw_states_list(self, get_empty_yaml_states_builder):
        # Given
        raw_states_list = set()
        yaml_states_builder = get_empty_yaml_states_builder

        # When
        parsed_states = yaml_states_builder.parse_raw_states_from_list(raw_states_list)

        # Then
        assert len(parsed_states) == 0

    def test_invalid_raw_states_format(self, get_empty_yaml_states_builder):
        # Given
        raw_states_list = {'group1:state1', 'group2', 'state3'}
        yaml_states_builder = get_empty_yaml_states_builder

        # When/Then
        with pytest.raises(DialogYamlException):
            yaml_states_builder.parse_raw_states_from_list(raw_states_list)

    def test_invalid_group_name(self, get_empty_yaml_states_builder):
        # Given
        raw_states_list = {'group1:state1', ':state2', 'group2:state3'}
        yaml_states_builder = get_empty_yaml_states_builder

        # When/Then
        with pytest.raises(DialogYamlException):
            yaml_states_builder.parse_raw_states_from_list(raw_states_list)

    def test_invalid_state_name(self, get_empty_yaml_states_builder):
        # Given
        raw_states_list = {'group1:state1', 'group2:', 'group2:state3'}
        yaml_states_builder = get_empty_yaml_states_builder

        # When/Then
        with pytest.raises(DialogYamlException):
            yaml_states_builder.parse_raw_states_from_list(raw_states_list)

    def test_formatted_states(self, get_empty_yaml_states_builder):
        # Given
        group_name = 'group1'
        state_name = 'state1'
        yaml_states_builder = get_empty_yaml_states_builder

        # When
        actual_raw_state_name = yaml_states_builder.format_state_name(group_name, state_name)

        # Then
        assert actual_raw_state_name == f'{group_name}:{state_name}'


class TestLoadStatesFromYAMLData:

    def test_valid_data(self, get_empty_yaml_states_builder):
        # Given
        yaml_states_builder = get_empty_yaml_states_builder
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
        yaml_states_builder.load_states_from_yaml_data(data)

        # Then
        assert isinstance(yaml_states_builder.get_by_name('group1'), StatesGroup)
        assert isinstance(yaml_states_builder.get_by_name('group2'), StatesGroup)
        assert isinstance(yaml_states_builder.get_by_name('group1:state1'), State)
        assert isinstance(yaml_states_builder.get_by_name('group1:state2'), State)
        assert isinstance(yaml_states_builder.get_by_name('group2:state3'), State)
        assert isinstance(yaml_states_builder.get_by_name('group2:state4'), State)

    def test_invalid_data_type(self, get_empty_yaml_states_builder):
        # Given
        yaml_states_builder = get_empty_yaml_states_builder
        data = 'invalid_data'

        # When, Then
        with pytest.raises(DialogYamlException):
            yaml_states_builder.load_states_from_yaml_data(data)

    def test_empty_data(self, get_empty_yaml_states_builder):
        # Given
        yaml_states_builder = get_empty_yaml_states_builder
        data = {}

        # When, Then
        with pytest.raises(InvalidTagName):
            yaml_states_builder.load_states_from_yaml_data(data)

    def test_other_tags(self, get_empty_yaml_states_builder):
        # Given
        yaml_states_builder = get_empty_yaml_states_builder
        data = {'other_tag': {}}

        # When, Then
        with pytest.raises(InvalidTagName):
            yaml_states_builder.load_states_from_yaml_data(data)

    def test_missing_windows_tag(self, get_empty_yaml_states_builder):
        # Given
        yaml_states_builder = get_empty_yaml_states_builder
        data = data = {
            'dialogs': {
                'group1': {'not_windows_tag': {}},
                'group2': {'not_windows_tag': {}}
            }
        }

        # When, Then
        with pytest.raises(InvalidTagName):
            yaml_states_builder.load_states_from_yaml_data(data)

    def test_load_states_from_invalid_dialogs_data_type(self, get_empty_yaml_states_builder):
        # Given
        yaml_states_builder = get_empty_yaml_states_builder
        data = data = {
            'dialogs': {
                'group1': {'windows': 'invalid_data'},
            }
        }

        # When, Then
        with pytest.raises(InvalidTagDataType):
            yaml_states_builder.load_states_from_yaml_data(data)

    def test_load_states_from_invalid_windows_data_type(self, get_empty_yaml_states_builder):
        # Given
        yaml_states_builder = get_empty_yaml_states_builder
        data = data = {
            'dialogs': {
                'group1': 'invalid_data',
            }
        }

        # When, Then
        with pytest.raises(DialogYamlException):
            yaml_states_builder.load_states_from_yaml_data(data)


class TestExtractGroupAndStateNames:

    def test_valid_raw_states_group_with_one_delimiter(self, get_empty_yaml_states_builder):
        # Given
        raw_states_group = 'group1:state1'
        expected_group_name = 'group1'
        expected_state_name = 'state1'
        yaml_states_builder = get_empty_yaml_states_builder

        # When
        group_name, state_name = yaml_states_builder.extract_group_and_state_names(raw_states_group)

        # Then
        assert group_name == expected_group_name
        assert state_name == expected_state_name

    def test_valid_raw_states_group_with_two_delimiters(self, get_empty_yaml_states_builder):
        # Given
        raw_states_group = 'group1:state1:state2'
        yaml_states_builder = get_empty_yaml_states_builder

        # When/Then
        with pytest.raises(DialogYamlException):
            yaml_states_builder.extract_group_and_state_names(raw_states_group)

    def test_empty_raw_states_group(self, get_empty_yaml_states_builder):
        # Given
        raw_states_group = ''
        yaml_states_builder = get_empty_yaml_states_builder

        # When/Then
        with pytest.raises(DialogYamlException):
            yaml_states_builder.extract_group_and_state_names(raw_states_group)

    def test_invalid_type_raw_states_group(self, get_empty_yaml_states_builder):
        # Given
        raw_states_group = 123
        yaml_states_builder = get_empty_yaml_states_builder

        # When/Then
        with pytest.raises(DialogYamlException):
            yaml_states_builder.extract_group_and_state_names(raw_states_group)
