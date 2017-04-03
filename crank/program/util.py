def generate_percents(low=.05, high=1., step=.05):
    return (low + step * i for i in range(round((high - low) / step) + 1))


def calculate_weights(weight, start, step=.1):
    pct = start
    while pct < 1.:
        yield round(weight * pct)
        pct += step


def print_sets(weight, reps, percent):
    sets = zip(calculate_weights(weight, percent), reps)
    print(', '.join("{:d} x {:d}".format(w, r) for w, r in sets))
