from enum import Enum, unique


@unique
class DefinitionType(Enum):
    op_constant = 0

    def __int__(self):
        return self.value


definitions = {
    int(DefinitionType.op_constant): {
        'name': 'op_constant',
        'operands_widths': [2],
    }
}


def lookup(op):
    definition = definitions.get(op)
    return definition


def make(op, operands):
    definition = definitions.get(op)
    if definition is None:
        return bytearray()
    instruction_len = 1
    for i in definition['operands_widths']:
        instruction_len += i

    instruction = bytearray()
    instruction.append(op)

    offset = 1
    for i in range(len(operands)):
        width = definition['operands_widths'][i]
        operand = operands[i].to_bytes(2, byteorder="big")
        if width == 2:
            instruction += bytearray(operand)
        offset += width

    return instruction


def test_make():
    op = int(DefinitionType.op_constant)
    operands = [65534]
    instruction = make(op, operands)
    print(instruction)


if __name__ == '__main__':
    test_make()
