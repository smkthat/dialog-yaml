from typing import List, Dict

from aiogram.fsm.state import State, StatesGroup

from core.decorators import singleton


@singleton
class YAMLDialogStatesHolder(dict):

    def load_data(self, data: Dict = None, states: List[StatesGroup] = None) -> 'YAMLDialogStatesHolder':
        if data:
            self._load_states(data)
        if states:
            self.add_states(states)
        return self

    def __missing__(self, key):
        return self.setdefault(key, {})

    def get_by_names(self, group: str, state: str) -> State:
        name = f'{group}:{state}'
        if found := self.get_by_name(name):
            return found

    def get_by_name(self, name: str) -> State:
        if found := self.get(name):
            return found
        raise ValueError(f'State {name!r} does\'t exist.')

    @classmethod
    def _build_states(cls, values: tuple) -> Dict[str, State]:
        return {state_name: State(state_name) for state_name in values}

    @classmethod
    def _build_states_group(cls, group_name: str, states: Dict[str, State]) -> type:
        return type(group_name, (StatesGroup,), states)

    def _load_states(self, data: Dict) -> None:
        try:
            dialogs_data = data['dialogs']
            if not isinstance(dialogs_data, dict):
                raise TypeError(f'Tag "dialogs" must be a non-empty dict. Found {type(dialogs_data)}')

            for group_name, value in dialogs_data.items():
                if value:
                    try:
                        windows_data = value['windows']
                        if not isinstance(windows_data, dict) or not windows_data:
                            raise ValueError('Tag "windows" must be a non-empty dict.')

                        states = self._build_states(tuple(windows_data.keys()))
                        states_group = self._build_states_group(group_name, states)
                        for state_name, state in states.items():
                            self[f'{group_name}:{state_name}'] = state
                        self[group_name] = states_group

                    except KeyError as e:
                        raise ValueError(f'Key {e.args[0]!r} not found in dialogs[{group_name!r}].')
                    except ValueError as e:
                        raise ValueError(f'Invalid value for dialogs[{group_name!r}]["windows"]: {e}')
        except KeyError:
            raise ValueError('Tag "dialogs" not provided')

    def parse_objs(self, raw_states_group_list: list[str]):
        """
         example: ['ExampleSG:e1', 'ExampleSG:e2', 'ExampleSG:e3', ]

         will provide ExampleSG state group with e1, e2, e3 states
        """
        data = {}
        for raw_state_group in raw_states_group_list:
            group_name, state_name = raw_state_group.split(':')
            group = data.get(group_name, [])
            group.append(state_name)
            data[group_name] = group

        for group_name, raw_states in data.items():
            states = self._build_states(tuple(raw_states))
            states_group = self._build_states_group(group_name, states)
            for state_name, state in states.items():
                self[f'{group_name}:{state_name}'] = state
            self[group_name] = states_group

    def add_states(self, states_group_list: List[StatesGroup]) -> None:
        for states_group in states_group_list:
            group_name = states_group.__class__.__name__
            states = {
                state.state: state
                for state in states_group.__states__
                if isinstance(state, State)
            }
            states_group = self._build_states_group(group_name, states)
            for state_name, state in states.items():
                self[f'{group_name}:{state_name}'] = state
            self[group_name] = states_group
