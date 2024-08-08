from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    # for users
    async def create_user(self, phone, username, telegram_id):
        sql = "INSERT INTO Users (phone, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, phone, username, telegram_id, fetchrow=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_users(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    # for departments
    async def create_department(self, name):
        sql = "INSERT INTO Department (name) VALUES($1) returning *"
        return await self.execute(sql, name, fetchrow=True)

    async def select_departmetns(self, **kwargs):
        sql = "SELECT * FROM Department WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_department(self, id):
        sql = "SELECT * FROM Department WHERE id=$1"
        return await self.execute(sql, id, fetchrow=True)

    async def select_all_departments(self):
        sql = "SELECT * FROM Department"
        return await self.execute(sql, fetch=True)

    async def get_department(self):
        sql = "SELECT * FROM Department"
        return await self.execute(sql, fetch=True)

    # for branches
    async def create_branch(self, name):
        sql = "INSERT INTO Filial (name) VALUES($1) returning *"
        return await self.execute(sql, name, fetchrow=True)

    async def select_branch(self, id):
        sql = "SELECT * FROM Filial WHERE id=$1"
        return await self.execute(sql, id, fetchrow=True)

    async def select_branches(self, **kwargs):
        sql = "SELECT * FROM Filial WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_all_branches(self):
        sql = "SELECT * FROM Filial"
        return await self.execute(sql, fetch=True)

    async def get_branch(self):
        sql = "SELECT * FROM Filial"
        return await self.execute(sql, fetch=True)

    # for department_filial table
    async def select_department_filial(self, **kwargs):
        sql = "SELECT * FROM Department_filial WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    # for comments
    async def create_comment(self, message, user_id, mark):
        sql = "INSERT INTO Filial (message, user_id, mark) VALUES($1) returning *"
        return await self.execute(sql, message, user_id, mark, fetchrow=True)

    async def create_comment_mark(self, department_id, branch_id, employee_id, user_id, mark, message):
        sql = "INSERT INTO Fikr (department_id, branch_id, employee_id, user_id, mark, message) VALUES($1, $2, $3, $4, $5, $6) returning *"
        return await self.execute(sql, department_id, branch_id, employee_id, user_id, mark, message, fetchrow=True)
