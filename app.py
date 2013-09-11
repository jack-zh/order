#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handlers.mainhandler import main
from log import logger


if __name__ == "__main__":
    logger.info("app start")
    main()
