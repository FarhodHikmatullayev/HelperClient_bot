from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
import datetime

from keyboards.default.menu import back_menu_keyboard
from keyboards.inline.confirmation import confirm_keyboard
from keyboards.inline.departments_keyboard import departments_keyboard, department_callback_data
from keyboards.inline.employee_or_department import check_markup, department_or_employee_callback_data
from keyboards.inline.filiallar_keyboard import branch_callback_data, branches_keyboard
from keyboards.inline.marks_inline import marks_keyboard, mark_callback_data
from loader import dp, db, bot
from states.mark_states import Mark
from utils.generate_promocode import create_promocode


@dp.callback_query_handler(text='back_to_branches')
async def back_to_branches(call: CallbackQuery):
    markup = await branches_keyboard()
    await call.message.edit_text(text="Quyidagi filiallardan birini tanlang", reply_markup=markup)


# @dp.callback_query_handler(branch_callback_data.filter())
# async def set_departments(call: CallbackQuery, callback_data: dict):
#     branch_id = int(callback_data.get('id'))
#     department_filial = await db.select_department_filial(filial_id=branch_id)
#     departments_id = []
#
#     for dep_fil in department_filial:
#         department_id = dep_fil['department_id']
#         departments_id.append(department_id)
#     text = "Lavozimlar ro'yxati\n" \
#            "Baho berish uchun ulardan birini tanlang"
#     markup = await departments_keyboard(departments_id, branch_id=branch_id)
#     await call.message.edit_text(text=text, reply_markup=markup)


@dp.callback_query_handler(branch_callback_data.filter())
async def set_employee_or_department(call: CallbackQuery, callback_data: dict):
    branch_id = int(callback_data.get('id'))
    markup = await check_markup(branch_id=branch_id)
    text = "Mahsulotga baho berasizmi yoki xodimga"
    await call.message.edit_text(text=text, reply_markup=markup)


@dp.callback_query_handler(department_or_employee_callback_data.filter())
async def for_employee_or_department(call: CallbackQuery, callback_data: dict, state: FSMContext):
    branch_id = callback_data.get('branch_id')

    user_telegram_id = call.from_user.id
    users = await db.select_user(telegram_id=user_telegram_id)
    user_id = users[0]['id']
    department_employee = callback_data.get('department_or_employee')
    await state.update_data(
        {
            'branch_id': branch_id,
            'user_id': user_id
        }
    )
    if department_employee == 'employee':
        text = 'Xodimning ID raqamini kiriting'
        await call.message.answer(text=text, reply_markup=back_menu_keyboard)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await Mark.employee_id.set()
    elif department_employee == 'department':
        text = 'Mahsulotga baho bering\n'
        await call.message.edit_text(text=text, reply_markup=marks_keyboard)
        await Mark.grade.set()


@dp.message_handler(state=Mark.employee_id)
async def get_employee_id(message: Message, state: FSMContext):
    user_telegram_id = message.from_user.id
    users = await db.select_user(telegram_id=user_telegram_id)
    user_id = users[0]['id']
    employee_id = message.text
    data = await state.get_data()
    branch_id = data.get('branch_id')
    # department_id = data.get('department_id')

    try:
        employee_id = int(employee_id)

        marks = 0
        if employee_id:
            marks = await db.select_comments(user_id=user_id, employee_code=employee_id)

        today = datetime.date.today()

        if marks and marks[0]['created_at'].date() == today:
            mark = marks[0]
            time = mark['created_at']
            date = time.date()
            text = "Siz bugun bu xodim uchun fikr bildirgansiz\n" \
                   "Boshqa xodimlarga fikr bildirib ko'ring"
            await Mark.employee_id.set()
            await message.answer(text=text, reply_markup=back_menu_keyboard)

        else:
            employees = await db.select_employee(code=str(employee_id), filial_id=int(branch_id))
            if employees:
                # if xodimlar listidan id ni qidirish amali

                await state.update_data(
                    {
                        'employee_id': employee_id
                    }
                )
                text = "Xodimning ishiga baho bering"
                await message.answer(text=text, reply_markup=marks_keyboard)
                await Mark.grade.set()
            else:
                text = f"Bu filialda ID raqami {employee_id} bo'lgan xodim mavjud emas\n" \
                       f"Iltimos xodimning raqamini tog'ri kiriting\n"
                await message.answer(text=text, reply_markup=back_menu_keyboard)
                await Mark.employee_id.set()

    except:
        text = "Xodim ID raqamini notog'ri kiritdingiz\n" \
               "Yoki bunday xodim mavjud emas\n" \
               "Iltimos, uni tog'ri kiriting"
        await message.answer(text=text)
        await Mark.employee_id.set()


@dp.callback_query_handler(mark_callback_data.filter(), state=Mark.grade)
async def get_mark(call: CallbackQuery, callback_data: dict, state: FSMContext):
    mark = callback_data.get('mark')
    await state.update_data(
        {
            'grade': mark
        }
    )
    data = await state.get_data()
    employee_id = data.get('employee_id', None)
    if not employee_id:
        text = "Nega bunday ball berganingizga izoh yozing\n" \
               "Masalan: \n" \
               "1. Men izlagan mahsulot yo'q ekan\n" \
               "2. 'mahsulot nomi' ning yaroqlilik muddati tugabdi"
    else:
        text = "Nega bunday ball berganingizga izoh yozing"
    await call.message.edit_text(text=text)
    await Mark.comment.set()


@dp.message_handler(state=Mark.comment)
async def get_comment(message: Message, state: FSMContext):
    comment = message.text
    await state.update_data(
        {
            'comment': comment
        }
    )

    data = await state.get_data()
    employee_id = data.get('employee_id', None)

    comment = data.get('comment')
    grade = data.get('grade')
    user_id = data.get('user_id')
    branch_id = int(data.get('branch_id'))
    branch = await db.select_branch(id=branch_id)
    branch_name = branch['name']

    text = ""
    text += f"Filial nomi: {branch_name.capitalize()}\n"
    if employee_id:
        text += f"Xodim ID raqami: {employee_id}\n"
    text += f"Siz qo'ygan ball: {grade}\n"
    text += f"Bu ballni qo'yishingizga sabab: {comment}\n\n"
    text += "Siz qo'ygan ball quyidagicha bo'ldi\nUni saqlashni xohlaysizmi?"

    await message.answer(text=text, reply_markup=confirm_keyboard)


@dp.callback_query_handler(state=Mark.comment, text='ok')
async def confirm_creating_mark(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    employee_id = data.get('employee_id', None)
    # department_id = int(data.get('department_id'))
    comment = data.get('comment')
    grade = int(data.get('grade'))
    user_id = int(data.get('user_id'))
    branch_id = int(data.get('branch_id'))

    marks = 0
    if employee_id:
        marks = await db.select_comments(user_id=user_id, employee_code=employee_id)

    today = datetime.date.today()

    if marks and marks[0]['created_at'].date() == today:
        mark = marks[0]
        time = mark['created_at']
        date = time.date()
        text = "Siz bugun bu xodim uchun fikr bildirgansiz\n" \
               "Boshqa xodimlarga fikr bildirib ko'ring"
        await state.finish()
        await call.message.answer(text=text, reply_markup=back_menu_keyboard)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


    else:
        mark_comment = await db.create_comment_mark(
            branch_id=branch_id,
            employee_code=employee_id,
            user_id=user_id,
            mark=grade,
            message=comment,
            created_at=datetime.datetime.now()
        )
        text = "Siz baholash jarayonidan muvaffaqiyatli o'tdingiz"
        # await call.message.edit_text(text=text)
        # promocode = await create_promocode()
        #
        # user_promo_code = await db.create_promo_code(promo_code=promocode, user_id=user_id,
        #                                              created_at=datetime.datetime.now())
        #
        # text = f"Tabriklaymiz! Siz yordamchi mijoz o'yini ishtirokchisiga aylandingiz\n" \
        #        f"Sizning promocodingiz '{promocode}'"
        await state.finish()
        await call.message.answer(text=text, reply_markup=back_menu_keyboard)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(state=Mark.comment, text='cancel')
async def cancel_confirmation_mark(call: CallbackQuery, state: FSMContext):
    # await call.message.answer("Siz saqlashni rad etdingiz", reply_markup=back_menu_keyboard)
    await call.message.answer("Siz saqlashni rad etdingiz", reply_markup=back_menu_keyboard)

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()
