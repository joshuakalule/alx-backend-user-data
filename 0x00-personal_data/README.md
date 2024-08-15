# Personal Data

Handle PII (Personally Identifiable Information), Non-PII and Personal Data

**PII**: Information that can be traced back to a user such as SSN, Passport, NIN etc

## Logging

### Create a logger object (recommended)

`logger = logging.getLogger(__name__)`

### Set logging configurations

`logger.basicConfig(filename, filemode, encoding, level)`

**Note**:

1. code configures the root logger, that means all loggers shall abide by the above set configurations.

2. To configure the logger object itself use;

    `logger.addHandler(logging.StreamHandler(sys.stderr))`
    `logger.setLevel(logging.DEBUG)`

    Yes, why add a handler first? Because the default handler isn't manipulated through the newly created logger. Since it is the 'of last resort' internal handler for the root logger and all created loggers without handlers, it shall remain with its set level as it is the one that *'handles'* the logs.
    More at [stack-overflow](https://stackoverflow.com/questions/43109355/logging-setlevel-is-being-ignored)
