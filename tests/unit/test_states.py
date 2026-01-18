"""Unit tests for YAMLStatesManager component."""

import pytest
from aiogram.fsm.state import StatesGroup, State

from dialog_yml.exceptions import DialogYamlException, StatesGroupNotFoundError
from dialog_yml.states import YAMLStatesManager


class TestYAMLStatesManager:
    """Unit tests for YAMLStatesManager functionality."""

    @pytest.fixture
    def empty_states_manager(self) -> YAMLStatesManager:
        """Fixture for empty states manager."""
        states_manager = YAMLStatesManager()
        states_manager._states_groups_map_ = {}
        return states_manager

    @pytest.fixture
    def populated_states_manager(self) -> YAMLStatesManager:
        """Fixture for populated states manager."""
        states_manager = YAMLStatesManager()
        states = states_manager.parse_raw_states_from_list(
            {
                "group1:state1",
                "group1:state2",
                "group1:state3",
                "group2:state1",
                "group2:state2",
            }
        )
        states_manager._states_groups_map_.update(states)
        return states_manager

    def test_build_states_groups(self, empty_states_manager: YAMLStatesManager):
        """Test building states groups."""
        # Given
        states_manager = empty_states_manager

        # When
        states_manager._build_states_groups({"group1": [], "group2": []})

        # Then
        assert isinstance(states_manager.get_by_name("group1"), StatesGroup)
        assert isinstance(states_manager.get_by_name("group2"), StatesGroup)

    def test_build_states(self, empty_states_manager: YAMLStatesManager):
        """Test building individual states."""
        # Given
        states_manager = empty_states_manager

        # When
        result = states_manager._build_states({"state1", "state2", "state3"})

        # Then
        assert all(isinstance(state, State) for state in result.values())

    def test_get_by_name(self, populated_states_manager: YAMLStatesManager):
        """Test retrieving state by full name."""
        # Given
        states_manager = populated_states_manager

        # When
        result = states_manager.get_by_name("group1:state1")

        # Then
        assert isinstance(result, State)

    def test_get_by_names(self, populated_states_manager: YAMLStatesManager):
        """Test retrieving state by group and state names."""
        # Given
        states_manager = populated_states_manager

        # When
        result = states_manager.get_by_names("group1", "state1")

        # Then
        assert isinstance(result, State)

    def test_add_state_to_map(self, populated_states_manager: YAMLStatesManager):
        """Test adding a state to the map."""
        # Given
        states_manager = populated_states_manager
        group_name = "group1"
        state = State("new_state", group_name)

        # When
        states_manager.add_state_to_map(group_name, state)

        # Then
        assert isinstance(states_manager.get_by_name("group1:new_state"), State)

    def test_add_state_to_map_without_group_name(
        self, populated_states_manager: YAMLStatesManager
    ):
        """Test adding state without group name raises error."""
        # Given
        states_manager = populated_states_manager
        none_existed_group_name = None
        state = State("new_state")

        # When, Then
        with pytest.raises(StatesGroupNotFoundError):
            states_manager.add_state_to_map(none_existed_group_name, state)

    @pytest.mark.parametrize(
        "raw_states_list,expected_count,has_groups",
        [
            (
                {
                    "group1:state1",
                    "group1:state2",
                    "group2:state3",
                    "group2:state4",
                },
                6,
                True,
            ),
            (set(), 0, False),
            ({"group1:state1", "group1:state2", "group1:state3"}, 4, True),
        ],
    )
    def test_parse_raw_states_from_list(
        self,
        empty_states_manager: YAMLStatesManager,
        raw_states_list,
        expected_count,
        has_groups,
    ):
        """Test parsing raw states from list."""
        # Given
        states_manager = empty_states_manager

        # When
        parsed_states = states_manager.parse_raw_states_from_list(raw_states_list)

        # Then
        assert len(parsed_states) == expected_count
        if has_groups:
            # Check that at least one group exists
            assert any(isinstance(value, StatesGroup) for value in parsed_states.values())

    @pytest.mark.parametrize(
        "raw_states_list,expected_exception",
        [
            ({"group1:state1", "group2"}, DialogYamlException),
            (
                {"group1:state1", ":state2", "group2:state3"},
                DialogYamlException,
            ),
            (
                {"group1:state1", "group2:", "group2:state3"},
                DialogYamlException,
            ),
        ],
    )
    def test_invalid_raw_states_formats(
        self,
        empty_states_manager: YAMLStatesManager,
        raw_states_list,
        expected_exception,
    ):
        """Test invalid raw states formats raise exceptions."""
        # Given
        states_manager = empty_states_manager

        # When/Then
        with pytest.raises(expected_exception):
            states_manager.parse_raw_states_from_list(raw_states_list)


class TestBuildStatesFromYAMLData:
    """Tests for building states from YAML data."""

    @pytest.fixture
    def empty_states_manager(self) -> YAMLStatesManager:
        """Fixture for empty states manager."""
        states_manager = YAMLStatesManager()
        states_manager._states_groups_map_ = {}
        return states_manager

    @pytest.mark.parametrize(
        "yaml_data,expected_groups,expected_states",
        [
            (
                {
                    "dialogs": {
                        "group1": {"windows": {"state1": {}, "state2": {}}},
                        "group2": {"windows": {"state3": {}, "state4": {}}},
                    }
                },
                ["group1", "group2"],
                [
                    "group1:state1",
                    "group1:state2",
                    "group2:state3",
                    "group2:state4",
                ],
            ),
            (
                {"dialogs": {"main": {"windows": {"start": {}}}}},
                ["main"],
                ["main:start"],
            ),
        ],
    )
    def test_valid_data(
        self,
        empty_states_manager: YAMLStatesManager,
        yaml_data,
        expected_groups,
        expected_states,
    ):
        """Test building states from valid YAML data."""
        # Given
        states_manager = empty_states_manager

        # When
        states_manager.build_states_from_yaml_data(yaml_data)

        # Then
        for group in expected_groups:
            assert isinstance(states_manager.get_by_name(group), StatesGroup)
        for state in expected_states:
            assert isinstance(states_manager.get_by_name(state), State)

    @pytest.mark.parametrize(
        "invalid_data,expected_exception",
        [
            ("invalid_data", DialogYamlException),
            ({}, DialogYamlException),
            ({"other_tag": {}}, DialogYamlException),
            (
                {"dialogs": {"group1": {"not_windows_tag": {}}}},
                DialogYamlException,
            ),
            (
                {"dialogs": {"group1": {"windows": "invalid_data"}}},
                DialogYamlException,
            ),
        ],
    )
    def test_invalid_data(
        self,
        empty_states_manager: YAMLStatesManager,
        invalid_data,
        expected_exception,
    ):
        """Test building states from invalid YAML data raises exceptions."""
        # Given
        states_manager = empty_states_manager

        # When, Then
        with pytest.raises(expected_exception):
            states_manager.build_states_from_yaml_data(invalid_data)


class TestExtractGroupAndStateNames:
    """Tests for extracting group and state names from raw strings."""

    @pytest.fixture
    def empty_states_manager(self) -> YAMLStatesManager:
        """Fixture for empty states manager."""
        states_manager = YAMLStatesManager()
        states_manager._states_groups_map_ = {}
        return states_manager

    @pytest.mark.parametrize(
        "raw_states_group,expected_group,expected_state",
        [
            ("group1:state1", "group1", "state1"),
            ("main:start", "main", "start"),
            ("test:action", "test", "action"),
        ],
    )
    def test_valid_raw_states_groups(
        self,
        empty_states_manager: YAMLStatesManager,
        raw_states_group,
        expected_group,
        expected_state,
    ):
        """Test extracting group and state names from valid strings."""
        # Given
        states_manager = empty_states_manager

        # When
        group_name, state_name = states_manager.extract_group_and_state_names(
            raw_states_group
        )

        # Then
        assert group_name == expected_group
        assert state_name == expected_state

    @pytest.mark.parametrize(
        "invalid_raw_states_group,expected_exception",
        [
            ("group1:state1:state2", DialogYamlException),  # Too many colons
            ("", DialogYamlException),  # Empty string
            (123, DialogYamlException),  # Non-string
        ],
    )
    def test_invalid_raw_states_groups(
        self,
        empty_states_manager: YAMLStatesManager,
        invalid_raw_states_group,
        expected_exception,
    ):
        """Test extracting names from invalid strings raises exceptions."""
        # Given
        states_manager = empty_states_manager

        # When/Then
        with pytest.raises(expected_exception):
            states_manager.extract_group_and_state_names(invalid_raw_states_group)


class TestIncludeStatesGroupsByClass:
    """Tests for including states groups by class."""

    class MyStatesGroup(StatesGroup):
        STATE_1 = State()
        STATE_2 = State()

    class NotAStatesGroup:
        pass

    def test_includes_new_states_group_subclass_successfully(self):
        """Test successfully including a new states group subclass."""
        # Given
        manager = YAMLStatesManager()

        # When
        manager.include_states_group_by_class(self.MyStatesGroup)

        # Then
        assert manager.get_by_name("MyStatesGroup") is not None

    def test_includes_new_states_group_with_all_states_successfully(self):
        """Test including a states group with all its states."""
        # Given
        manager = YAMLStatesManager()

        # When
        manager.include_states_group_by_class(self.MyStatesGroup)

        # Then
        assert len(manager._states_groups_map_) == 3  # Group + 2 states
        assert manager.get_by_name("MyStatesGroup") is not None
        assert manager.get_by_name("MyStatesGroup:STATE_1") is not None
        assert manager.get_by_name("MyStatesGroup:STATE_2") is not None

    def test_raises_exception_if_custom_state_class_not_subclass_of_states_group(
        self,
    ):
        """Test raising exception when class is not a StatesGroup subclass."""
        # Given
        manager = YAMLStatesManager()

        # When/Then
        with pytest.raises(DialogYamlException):
            manager.include_states_group_by_class(self.NotAStatesGroup)

    def test_raises_exception_if_states_group_states_attribute_empty(self):
        """Test raising exception when states group has no states."""
        # Given
        manager = YAMLStatesManager()

        class EmptyStatesGroup(StatesGroup):
            pass

        # When/Then
        with pytest.raises(DialogYamlException):
            manager.include_states_group_by_class(EmptyStatesGroup)
