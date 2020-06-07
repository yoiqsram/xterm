from .core import *

__all__ = ['Query', 'query', 'queries']


class Query:
    def __init__(self, **kwargs):
        self.prompt_format = str(kwargs.get('format', '? {prompt}:{prompt_hint} '))

        self.input_format = self._validate_format(format=kwargs.get('input_format'),
                                                  format_spec='{input_string}')
        self.input_format_success = self._validate_format(format=kwargs.get('input_format_success'),
                                                          format_spec='{input_string}',
                                                          default=self.input_format)
        self.items = dict()

    @staticmethod
    def _validate_format(format, format_spec: str, default = None):
        if default is None:
            default = format_spec

        if format is not None:
            format = str(format)
            if format_spec not in format:
                format = default if format_spec in default else format_spec

            return format

        return default

    def _check_input(self):
        input_format_split = self.input_format.split('{input_string}', 1)

        cursor_restore()
        clear_line('next')
        query_input = raw_read(input_format_split[0])
        raw_write(input_format_split[1])

        return query_input

    @staticmethod
    def _validate_query_default(query_input: str, input_default):
        if query_input == '' and input_default is not None:
            query_input = input_default

        return query_input

    def _validate_query_required(self, query_input: str, input_required: bool, input_warning_required: str):
        while query_input == '' and input_required:
            if input_warning_required is not None:
                write(input_warning_required)

            query_input = self._check_input()

        return query_input

    def _validate_query_transformer(self, query_input: str, input_transformer, input_warning_transformer: str):
        while True:
            try:
                query_input = input_transformer(query_input)
                break

            except Exception:
                if input_warning_transformer is not None:
                    write(input_warning_transformer)

                query_input = self._check_input()

        return query_input

    def _validate_query_validation(self, query_input: str, input_validation, input_warning_validation: str):
        while True:
            try:
                if not input_validation(query_input):
                    raise ValueError
                else:
                    break

            except ValueError:
                if input_warning_validation is not None:
                    write(input_warning_validation)

                query_input = self._check_input()

        return query_input

    def input(self, name: str, **kwargs):
        prompt = kwargs.get('prompt', '')
        prompt_hint = kwargs.get('hint', '')

        input_type = kwargs.get('type', str)
        input_default = kwargs.get('default')
        input_required = kwargs.get('required', False)
        input_transformer = kwargs.get('transformer', lambda query_input: input_type(query_input))
        input_validation = kwargs.get('validate', lambda query_input: True)

        input_warning_required = kwargs.get('warn_required')
        input_warning_transformer = kwargs.get('warn_transformer')
        input_warning_validation = kwargs.get('warn_validate')

        clear_line()
        input_format_split = self.input_format.split('{input_string}', 1)
        query_input = read(self.prompt_format.format(prompt=prompt, prompt_hint=prompt_hint) + input_format_split[0],
                           end=input_format_split[1] + '\n')

        query_input = self._validate_query_default(query_input, input_default)
        query_input = self._validate_query_required(query_input, input_required, input_warning_required)
        query_input = self._validate_query_transformer(query_input, input_transformer, input_warning_transformer)
        query_input = self._validate_query_validation(query_input, input_validation, input_warning_validation)

        cursor_restore()
        clear_line('next')
        write(self.input_format_success.format(input_string=query_input))

        self.items[name] = query_input
        return query_input


def query(prompt: str, **kwargs):
    query = Query(**kwargs)
    query_input = query.input('query', prompt=prompt, **kwargs)
    return query_input


def queries(query_list: list, **kwargs):
    query = Query(**kwargs)

    for query_kwargs in query_list:
        query.input(**query_kwargs)

    return query.items
