import curses
from curses import ascii


def handle_input(ch_input, prompt, cursor_x):
    push_command = []
    if ch_input == ascii.DEL:
        prompt = prompt[:cursor_x - 1] + prompt[cursor_x:]
        cursor_x = max(cursor_x - 1, 0)
    elif ch_input == 330:
        prompt = prompt[:cursor_x] + prompt[min(len(prompt), cursor_x +1):]
    elif ch_input == ascii.NL:
        push_command = prompt
        prompt = ''
        cursor_x = len(prompt)
    elif ch_input == ascii.TAB:
        prompt += '   '
        cursor_x = len(prompt)
    elif ch_input == ascii.CR:
        prompt = 'CR'
        cursor_x = len(prompt)
    elif ch_input == ascii.NUL:
        prompt = ''
        cursor_x = len(prompt)
    elif ch_input == ascii.SOH:
        prompt = 'SOH'
        cursor_x = len(prompt)
    elif ch_input == ascii.STX:
        prompt = 'STX'
        cursor_x = len(prompt)
    elif ch_input == ascii.ETX:
        prompt = 'ETX'
        cursor_x = len(prompt)
    elif ch_input == ascii.EOT:
        prompt = 'EOT'
        cursor_x = len(prompt)
    elif ch_input == ascii.ENQ:
        prompt = 'ENQ'
        cursor_x = len(prompt)
    elif ch_input == ascii.ACK:
        prompt = 'ACK'
        cursor_x = len(prompt)
    elif ch_input == ascii.BEL:
        prompt = 'BEL'
        cursor_x = len(prompt)
    elif ch_input == ascii.BS:
        prompt = 'BS'
        cursor_x = len(prompt)
    elif ch_input == ascii.HT:
        prompt = 'HT'
        cursor_x = len(prompt)
    elif ch_input == ascii.LF:
        prompt = 'LF'
        cursor_x = len(prompt)
    elif ch_input == ascii.VT:
        prompt = 'VT'
        cursor_x = len(prompt)
    elif ch_input == ascii.FF:
        prompt = 'FF'
        cursor_x = len(prompt)
    elif ch_input == ascii.SO:
        prompt = 'SO'
        cursor_x = len(prompt)
    elif ch_input == ascii.SI:
        prompt = 'SI'
        cursor_x = len(prompt)
    elif ch_input == ascii.DLE:
        prompt = 'DLE'
        cursor_x = len(prompt)
    elif ch_input == ascii.DC1:
        prompt = 'DC1'
        cursor_x = len(prompt)
    elif ch_input == ascii.DC2:
        prompt = 'DC2'
        cursor_x = len(prompt)
    elif ch_input == ascii.DC3:
        prompt = 'DC3'
        cursor_x = len(prompt)
    elif ch_input == ascii.DC4:
        prompt = 'DC4'
        cursor_x = len(prompt)
    elif ch_input == ascii.NAK:
        prompt = 'NAK'
        cursor_x = len(prompt)
    elif ch_input == ascii.SYN:
        prompt = 'SYN'
        cursor_x = len(prompt)
    elif ch_input == ascii.ETB:
        prompt = 'ETB'
        cursor_x = len(prompt)
    elif ch_input == ascii.CAN:
        prompt = 'CAN'
        cursor_x = len(prompt)
    elif ch_input == ascii.EM:
        prompt = 'EM'
        cursor_x = len(prompt)
    elif ch_input == ascii.SUB:
        prompt = 'SUB'
        cursor_x = len(prompt)
    elif ch_input == ascii.ESC:
        prompt = prompt[:cursor_x]
        cursor_x = len(prompt)
    elif ch_input == ascii.FS:
        prompt = 'FS'
        cursor_x = len(prompt)
    elif ch_input == ascii.GS:
        prompt = 'GS'
        cursor_x = len(prompt)
    elif ch_input == ascii.RS:
        prompt = 'RS'
        cursor_x = len(prompt)
    elif ch_input == ascii.US:
        prompt = 'US'
        cursor_x = len(prompt)
    elif ch_input == ascii.SP:
        prompt += ' '
        cursor_x = len(prompt)
    elif ch_input == ascii.DEL:
        prompt = 'DEL'
        cursor_x = len(prompt)
    elif ch_input == curses.KEY_LEFT:
        cursor_x = max(cursor_x - 1, 0)
    elif ch_input == curses.KEY_RIGHT:
        cursor_x = min(cursor_x + 1, len(prompt))
    elif ch_input == curses.KEY_DOWN:
        prompt = ''
        cursor_x = len(prompt)
        push_command = 'DOWN'
    elif ch_input == curses.KEY_UP:
        prompt = ''
        push_command = 'UP'
    elif -1 < ch_input < 256:
        prompt += str(chr(ch_input))
        cursor_x = len(prompt)
    elif ch_input == curses.KEY_RESIZE or ch_input == -1:
        prompt = 'RESIZE'
        cursor_x = len(prompt)
    else:
        prompt = 'Unknown entry {}'.format(ch_input)
        cursor_x = len(prompt)

    return prompt, cursor_x, push_command
