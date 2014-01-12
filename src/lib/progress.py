import sys


class ProgressBar:

    def __init__(self, min_value=0, max_value=100, total_width=77):
        """ Initializes the progress bar. """
        self.prog_bar = ""  # This holds the progress bar string
        self.old_prog_bar = ""
        self.min = min_value
        self.max = max_value
        self.span = max_value - min_value
        self.width = total_width
        self.amount = 0  # When amount == max, we are 100% done

        self.update_amount(0)  # Build progress bar string

    def append_amount(self, append=0):
        """ Increases the current amount of the value of append and calls
        update_amount. """
        self.update_amount(self.amount + append)

    def update_amount(self, new_amount=0):
        """ Update the progress bar with the new amount (with min and max
        values set at initialization; if it is over or under, it takes the
        min or max value as a default. """
        if new_amount < self.min:
            new_amount = self.min
        if new_amount > self.max:
            new_amount = self.max
        self.amount = new_amount

        # Figure out the new percent done, round to an integer
        diff_from_min = float(self.amount - self.min)
        percent_done = (diff_from_min / float(self.span)) * 100.0
        percent_done = int(round(percent_done))

        # Figure out how many hash bars the percentage should be
        all_full = self.width - 2
        num_hashes = (percent_done / 100.0) * all_full
        num_hashes = int(round(num_hashes))

        # Build a progress bar with an arrow of equal signs; special cases for
        # empty and full
        if num_hashes == 0:
            self.prog_bar = "[>%s]" % (' '*(all_full-1))
        elif num_hashes == all_full:
            self.prog_bar = "[%s]" % ('='*all_full)
        else:
            self.prog_bar = "[%s>%s]" % ('='*(num_hashes-1), ' '*(all_full-num_hashes))

        # figure out where to put the percentage, roughly centered
        percent_string = str(percent_done) + "%"

        # slice the percentage into the bar
        self.prog_bar = ' '.join([self.prog_bar, percent_string])

    def draw(self):
        """ Draws the progress bar if it has changed from it's previous value.  """
        if self.prog_bar != self.old_prog_bar:
            self.old_prog_bar = self.prog_bar
            sys.stdout.write(self.prog_bar + '\r')
            sys.stdout.flush()  # force updating of screen

    def __str__(self):
        """ Returns the current progress bar. """
        return str(self.prog_bar)

if __name__ == "__main__":
    import time

    p = ProgressBar()
    x = 0
    while x < 101:
        time.sleep(0.2)
        p.update_amount(x)
        p.draw()

        x += 1
