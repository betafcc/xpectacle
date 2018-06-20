from subprocess import check_call, check_output


def run(command):
    check_output(command, shell=True)


def lines(command):
    return output(command).split('\n')


def output(command):
    return check_output(command, shell=True).decode('utf-8')
