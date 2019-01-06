from typing import Tuple, Sequence, Union
import discord
from redis import Redis
from .shared import RawResultSet, RawResultItem, ResultSet, ResultItem


def is_staff(user: discord.Member) -> bool:
    '''Check if server member is staff.'''
    return user.guild_permissions.ban_members


def parse_results(client: discord.Client, result_set: RawResultSet) -> ResultSet:
    '''Transforms a redis sorted set of (user id, score) into (User, score)

        returns Sequence[(discord.User, int)]
    '''
    res = []
    for set_item in result_set:
        user_id = int(set_item[0])
        user = client.get_user(user_id)
        if not user:
            user = user_id
        score = int(set_item[1])
        res.append((user, score))
    return res

def filter_by_role(results: RawResultSet, role: discord.Role) -> RawResultSet:
    '''Filter Redis Result Set by Role.'''
    role_member_ids = [mem.id for mem in role.members]
    return [ item for item in results if int(item[0]) in role_member_ids]

def print_top_result_item(count: int, result_item: ResultItem, staff: bool) -> str:
    '''Helper function for printing one result item for top command.'''
    user = result_item[0]
    score = result_item[1]
    user_found = isinstance(user, discord.User)
    name = user.name if user_found else 'User N/A'
    user_id = user.id if user_found else user
    staff_line = f'\t| `<@{user_id}>`' if staff else ''
    response = f'{count:2}. **{name:20.16}** | {score:6d}{staff_line}\n'
    return response
