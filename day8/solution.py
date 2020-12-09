from typing import List, Optional, Tuple


def run_program(code: List[str], start_ip: int = 0) -> Tuple[int, Optional[int], List[int]]:
    """
    Runs the program line by line and quits if it finds a loop
    returning the current accumulator, the repeated line index and a trace of executed instructions (indices of lines)
    in that order
    """
    # (3) get some meta info
    loc = len(code)

    # (4) setup the state of our `machine´
    ip = start_ip   # the instruction pointer (which line we are currently)
    acc = 0         # our storage (accumulator)
    trace_ips = []  # will store the instructions we visited

    # each line has a flag indicating the visited-state
    visited_instructions = [False for _ in range(loc)]

    # stores the line where the instruction repeated (if any)
    repeated_line_idx: Optional[int] = None


    # (4) execute the program
    while True:
        # (4.1) state checks
        # ... if we just went through the code and mark it visited if not and also check
        if ip == loc:  # end of program
            break

        # ... if we visited the line already
        if visited_instructions[ip] is True:
            repeated_line_idx = ip
            break  # end the program forcefully
        else:
            # ... mark line as it visited
            visited_instructions[ip] = True

        trace_ips.append(ip)

        # (4.2) read one line of code
        c = code[ip]

        # (4.3) parse the line
        op_code, argument = c.split(' ')

        # (4.4) execute the operation
        if op_code == 'nop':  # do nothing operation
            pass

        elif op_code == 'acc':  # change storage
            acc += int(argument)
        elif op_code == 'jmp':  # jump to another line
            ip += int(argument) - 1  # (-1: we will increase by one through the loop)
        else:
            print(f"Unrecognized command {op_code} at line {ip + 1}. Ignoring that one (Code: 9384293084)")

        # increase instruction pointer (go to next instruction)
        ip += 1

    return acc, repeated_line_idx, trace_ips


def repair_program(original_code: Optional[List[str]]):
    """
    Will find the one instruction to repair
    (nop -> jmp OR jmp to nop)
    if we succeed we return the completely repaired program, otherwise `None´

    :param original_code:
    :return: code or None
    """

    # we copy the program in order to change instructions inside
    # without hurting the main program
    repaired_program = original_code.copy()

    # get the loop trace. the error can ONLY be within this trace
    # since only one change is allowed
    _, _, trace = run_program(original_code)

    for trace_ip in trace:
        # check if it is a nop or jmp instruction
        op_code_original, argument_original = original_code[trace_ip].split(' ')

        # we only change jmp and nop operations
        if op_code_original in ('jmp', 'nop'):
            new_code = 'jmp'
            if op_code_original == 'jmp':
                # switch to to nop
                new_code = 'nop'

            # patch the program
            instruction_new = f"{new_code} {argument_original}"
            repaired_program[trace_ip] = instruction_new

            # run patched program and check if we still cycle
            _, repeated_line_idx, _ = run_program(repaired_program,
                                                  start_ip=trace_ip)

            # set back program if we find a cycle still
            if repeated_line_idx is not None:
                repaired_program[trace_ip] = original_code[trace_ip]
            else:
                return repaired_program

    # no valid repair found
    return None


if __name__ == '__main__':

    # (1) read the file
    code: List[str]
    with open("input.txt", "r", encoding='utf-8') as f:
        code = f.readlines()

    # (2) sanitize it a bit
    code = [*map(lambda l: l.strip().lower(), code)]

    # Run the program (should trigger a loop)
    acc, repeated_line_idx, _ = run_program(code)

    # Output some information
    if repeated_line_idx is not None:
        print(f"first repeated line: {repeated_line_idx + 1}")
    else:
        print("No repeated instruction found")

    print("Value of accumulator (acc): ", acc)

    print("Trying to repair program")
    repaired_program = repair_program(code)

    if repaired_program is None:
        print("Could not repair the program")
    else:
        # repairment found
        acc, repeated_line_idx, _ = run_program(repaired_program)
        if repeated_line_idx is None:
            print("Acc of repaired program: ", acc)
        else:
            print("Repaired program still cycles at line", repeated_line_idx + 1)