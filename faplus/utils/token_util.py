#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: token_util.py
Author: lvyuanxiang
Date: 2024/11/15 17:20:09
Description: token工具
"""
import logging
from typing import Optional
from datetime import datetime, timedelta, timezone

import jwt  # PyJWT库

from faplus import settings


SECRET_KEY = getattr(settings, "SECRET_KEY", "urTlH17dYxLPE_NhF9ENl-yWIrkA8oHNAMtfLJ1N7pA")
ALGORITHM = getattr(settings, "ALGORITHM", "HS256")
ACCESS_TOKEN_EXP = getattr(settings, "ACCESS_TOKEN_EXP", 30)


logger = logging.getLogger(__package__)



def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXP)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str | None) -> dict | None:
    if not token: 
        return
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        logger.error("", exc_info=True)
        return