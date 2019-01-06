from typing import List, Optional, Union
from discord import Message
from datetime import date, datetime

ActivityDate = Union[date, datetime]

def to_key(keys: List, prefix='activity', sep=':') -> str:
    '''Builds the redis key using an array of namespaces'''
    ks = [str(k) for k in keys]
    ks.insert(0, str(prefix))
    return sep.join(ks)


def weekly(message: Message, date: Optional[ActivityDate] = None) -> str:
    '''Get the activity key for a given date or message.created_at by default.'''
    date: ActivityDate = date if date else message.created_at
    week = date.isocalendar()[1]
    keys = [message.guild.id, 'week', week]
    return to_key(keys)


def monthly(message: Message, date: Optional[ActivityDate] = None) -> str:
    '''Get the monthly activity key.'''
    date: ActivityDate = date if date else message.created_at
    keys = [message.guild.id, 'month', date.month]
    return to_key(keys)

def total(message: Message) -> str:
    '''Get total activity key.'''
    keys = [message.guild.id, 'total']
    return to_key(keys)
