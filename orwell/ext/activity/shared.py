from typing import Tuple, Sequence, Union
import discord

RawResultItem = Tuple[bytes, float]
RawResultSet = Sequence[RawResultItem]
ResultItem = Tuple[Union[discord.User, int], int]
ResultSet = Tuple[ResultItem]

