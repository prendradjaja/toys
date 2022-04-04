from datetime import datetime
import math


# TODO Maybe: Show numbers in the bar like [==1==2==3==4] or [===1==2=48] etc. What about multi-digit numbers? Probably prefix them with _ e.g.
#                                                            [===1==2_16]

# TODO Maybe: Add 'remark' option

# TODO Maybe: Use a different formula for indeterminate bars so it can truly never go over

# TODO Maybe: Add an option for indeterminate bars to not provide a value (but the ProgressBar simply keeps a counter internally)


class ProgressPrinter:
    def show(self, text):
        print(text)

    def done(self):
        print('Done.')


class ProgressBar:
    def __init__(self, total_value, /, width=20, indeterminate_scale=3):
        if total_value is not None:
            self.total_value = total_value
            self.indeterminate = False
        else:
            self.total_value = '?'
            self.indeterminate = True
            self.indeterminate_scale = indeterminate_scale
        self.width = width
        self.starttime = datetime.now()

    def show(self, value):
        bar = self._get_bar(value)
        timer = human_readable(datetime.now() - self.starttime)

        # Warning: If a print is shorter than the previous print, it won't overwrite the whole thing
        print(
            '\r',
            bar + ' ',
            f'{value:,}/{self.total_value:,} ',
            f'({value/self.total_value:.2%}) ',
            f'@ {timer}',

            end='',
            flush=True,
            sep=''
        )

    def done(self):
        bar = f'[{self.width * "="}]'
        timer = human_readable(datetime.now() - self.starttime)
        print(
            '\r',
            bar + ' ',
            'Done ',
            f'@ {timer}',
            '                                 ',  # 'Done' is probably shorter than output of show(), so need to force overwrite

            end='\n',
            sep=''
        )

    def _get_bar(self, value):
        if not self.indeterminate:
            filledwidth = int(value / self.total_value * self.width)
            emptywidth = self.width - filledwidth
            char = '='
        else:
            filledwidth = min(
                math.floor(math.log10(value) * self.indeterminate_scale),
                self.width
            )
            emptywidth = self.width - filledwidth
            char = '?'
        return f'[{filledwidth * char}{emptywidth * " "}]'


def human_readable(delta):
    raw = str(delta)
    timer = raw[:raw.index('.')+3] if '.' in raw else timer_raw

    if timer.startswith('0:00:'):
        return timer[5:].lstrip('0') + ' s'
    return timer
