import string


def read_until_valid(prompt, valid_inputs=None, lmbda=None):
    """Loop until a valid input has been received.

    It is up to the caller to handle exceptions that occur outside the realm of
    calling their lambda, such as KeyboardInterrupts (^c, a.k.a C-c).

    :arg str prompt: Prompt to display.
    :kwarg ``Iterable`` valid_inputs: Acceptable inputs. If none are provided,
        then the first non-exceptional value entered will be returned.
    :arg ``func`` lmbda: Function to call on received inputs. Any errors will
        result in a re-prompting.
    """
    if valid_inputs:
        prompt += ' ' + str(valid_inputs) + ') '
    while True:
        user_input = input(prompt).strip(string.whitespace)
        # Apply a given function
        if lmbda is not None:
            try:
                user_input = lmbda(user_input)
            except:         # Any errors are assumed to be bad input
                continue    # So keep trying
        if valid_inputs is not None:
            if user_input in valid_inputs:
                return user_input
        else:
            return user_input


def confirm_input(string):
    """Confirm the input looks good."""
    x = read_until_valid("Does this look good? [y/n] =>\n{}\n".format(string),
                         ['y', 'n'])
    return x == 'y'
