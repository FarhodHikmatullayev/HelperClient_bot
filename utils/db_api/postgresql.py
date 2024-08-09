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
    async def create_user(self, phone, username, full_name, telegram_id):
        sql = "INSERT INTO Users (phone, username, full_name, telegram_id) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, phone, username, full_name, telegram_id, fetchrow=True)

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

    async def create_department_filial(self, department_id, filial_id):
        sql = "INSERT INTO Department_Filial (department_id, filial_id) VALUES($1, $2) returning *"
        return await self.execute(sql, department_id, filial_id, fetchrow=True)

    # for comments
    async def create_comment(self, message, user_id, mark, department_id, branch_id, employee_code):
        sql = "INSERT INTO Fikr (message, user_id, mark) VALUES($1) returning *"
        return await self.execute(sql, message, user_id, mark, fetchrow=True)

    async def create_comment_mark(self, department_id, branch_id, employee_code, user_id, mark, message):
        sql = "INSERT INTO Fikr (department_id, branch_id, employee_code, user_id, mark, message) VALUES($1, $2, $3, $4, $5, $6) returning *"
        return await self.execute(sql, department_id, branch_id, employee_code, user_id, mark, message, fetchrow=True)

    async def select_comment(self, user_id, employee_code, department_id, branch_id):
        sql = "SELECT * FROM Fikr WHERE user_id=$1 AND employee_code=$2 AND department_id=$3 AND branch_id=$4"
        return await self.execute(sql, user_id, employee_code, department_id, branch_id, fetch=True)

    async def select_all_comments(self):
        sql = "SELECT * FROM Fikr"
        return await self.execute(sql, fetch=True)

    async def select_comments(self, **kwargs):
        sql = "SELECT * FROM Fikr WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    # for promo codes
    async def create_promo_code(self, promo_code, user_id):
        sql = "INSERT INTO Promocodes (promocode, user_id) VALUES($1, $2) returning *"
        return await self.execute(sql, promo_code, user_id, fetchrow=True)

    async def select_all_promo_codes(self):
        sql = "SELECT * FROM Promocodes"
        return await self.execute(sql, fetch=True)

    async def delete_all_promocodes(self):
        sql = "DELETE FROM Promocodes"
        return await self.execute(sql, execute=True)

    # for employees
    async def create_employee(self, full_name, department_id, filial_id, code):
        sql = "INSERT INTO Employee (full_name, department_id, filial_id, code) VALUES($1, $2, $3, $4) RETURNING *"
        return await self.execute(sql, full_name, department_id, filial_id, code, fetchrow=True)

    async def update_employee(self, id, full_name=None, department_id=None, filial_id=None, code=None):
        sql = "UPDATE Employee SET "
        parameters = {}
        if full_name is not None:
            sql += "full_name=$1, "
            parameters["full_name"] = full_name
        if department_id is not None:
            sql += "department_id=$2, "
            parameters["department_id"] = department_id
        if filial_id is not None:
            sql += "filial_id=$3, "
            parameters["filial_id"] = filial_id
        if code is not None:
            sql += "code=$4, "
            parameters["code"] = code
        sql = sql.rstrip(", ") + " WHERE id=$5 RETURNING *"
        parameters["id"] = id
        return await self.execute(sql, *parameters.values(), fetchrow=True)

    async def delete_all_employees(self):
        sql = "DELETE FROM Employee"
        return await self.execute(sql, execute=True)

    async def delete_employee(self, id):
        sql = "DELETE FROM Employee WHERE id=$1 RETURNING *"
        return await self.execute(sql, id, fetchrow=True)

    async def select_employee(self, **kwargs):
        sql = "SELECT * FROM employee WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_all_employees(self):
        sql = "SELECT * FROM Employee"
        return await self.execute(sql, fetch=True)
