#!/usr/bin/python3
import subprocess
import re

stat = {
    'correct': 0,
    'incorrect': 0
}


def run(command_list):
    process = subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error = process.stderr.decode("utf-8")  # returning the stderr text, if any
    if len(error) > 0:
        return error
    return process.stdout.decode("utf-8")


def run_sql_file(file_name):
    return run(['psql', '-f', file_name])


def build_regex_for_line(line_elements):
    # if len(line_elements) < 2:
    #     raise ValueError('regex can be ceated for minimum 2 columns!')
    regex = r'\s' + line_elements[0].strip()
    for elem in line_elements[1:]:
        regex += r'\s*\|\s' + elem.strip()

    return regex


def clear_sql_output_line(line):
    return re.sub(r'\s*\|\s*', ', ', line)


def test_output(checked, headers, expected, prefix_lines=None):
    splitted = checked.split('\n')

    if prefix_lines is not None:
        for i in range(len(prefix_lines)):
            if prefix_lines[i] != splitted[i]:
                _expected = prefix_lines[i]
                got = clear_sql_output_line(splitted[i]).strip()
                if _expected != got:
                    return {
                        'error': 'Output error before the SELECT',
                        'expected': _expected + ' | length: ' + str(len(_expected)),
                        'got': got + ' | length: ' + str(len(got))
                    }

        for i in range(len(prefix_lines)):
            splitted.pop(0)

    if re.match(build_regex_for_line(headers), splitted[0]) is None:
        _expected = ', '.join(headers)
        got = clear_sql_output_line(splitted[0]).strip()
        if _expected != got:
            return {
                'error': 'Error in headers',
                'expected': _expected + ' | length: ' + str(len(_expected)),
                'got': got + ' | length: ' + str(len(got))
            }

    data_lines = splitted[2:-3]
    if len(data_lines) != len(expected):
        return {
            'error': 'Wrong number of output lines',
            'expected': str(len(expected)) + ' lines',
            'got': str(len(data_lines)) + ' lines'
        }

    for i in range(len(data_lines)):
        if re.match(build_regex_for_line(expected[i]), data_lines[i]) is None:
            _expected = ', '.join(expected[i])
            got = clear_sql_output_line(data_lines[i]).strip()
            if _expected != got:
                return {
                    'error': 'Output error',
                    'expected': _expected + ' | length: ' + str(len(_expected)),
                    'got': got + ' | length: ' + str(len(got))
                }

    return True


def test_sql_file(file_name, headers, expected_values, prefix_lines=None):
    global stat

    output = run_sql_file(file_name)
    test_result = test_output(output, headers, expected_values, prefix_lines)
    if test_result is True:
        print(file_name + ' works as expected')
        stat['correct'] += 1
    else:
        print('\n!! Error detected')
        print('File: ', file_name)
        print('Error: ' + test_result['error'])
        print('Expected: ' + test_result['expected'])
        print('Got: ' + test_result['got'])
        print('Full output:\n' + output + '\n')
        stat['incorrect'] += 1


def main():
    global stat

    run_sql_file('build-mentors-table.sql')
    run_sql_file('build-applicants-table.sql')

    test_sql_file(
        '1-list-mentors.sql',
        ['first_name', 'last_name'],
        [
            ['Attila', 'Molnár'],
            ['Pál', 'Monoczki'],
            ['Sándor', 'Szodoray'],
            ['Dániel', 'Salamon'],
            ['Miklós', 'Beöthy'],
            ['Tamás', 'Tompa'],
            ['Mateusz', 'Ostafil']
        ]
    )

    test_sql_file(
        '2-list-mentors-from-miskolc.sql',
        ['nick_name'],
        [
            ['Atesz'],
            ['Pali'],
            ['Szodi']
        ]
    )

    test_sql_file(
        '3-greatest-favourite-number.sql',
        ['max'],
        [
            ['42']
        ]
    )

    test_sql_file(
        '4-specific-applicant-by-first-name.sql',
        ['full_name', 'phone_number'],
        [
            ['Carol Arnold', '003630/179-1827']
        ]
    )

    test_sql_file(
        '5-specific-applicant-by-email-domain.sql',
        ['full_name', 'phone_number'],
        [
            ['Jane Forbes', '003670/653-5392']
        ]
    )

    test_sql_file(
        '6-inserting-a-new-applicant.sql',
        ['id', 'first_name', 'last_name', 'phone_number', 'email', 'application_code'],
        [
            ['11', 'Markus', 'Schaffarzyk', '003620/725-2666', 'djnovus@groovecoverage.com', '54823']
        ],
        [
            'INSERT 0 1'
        ]
    )

    test_sql_file(
        '7-updating-data.sql',
        ['phone_number'],
        [
            ['003670/223-7459']
        ],
        [
            'UPDATE 1'
        ]
    )

    test_sql_file(
        '8-deleting-applicants.sql',
        ['count'],
        [
            ['0']
        ],
        [
            'DELETE 2'
        ]
    )

    print(
        '\n\n' + str(stat['correct'] + stat['incorrect']) +
        ' tests ran: \n\t' + str(stat['correct']) +
        ' correct\n\t' + str(stat['incorrect']) + ' incorrect')

    return stat

if __name__ == '__main__':
    main()
