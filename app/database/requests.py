from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User, Password


class Database:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_is_registered(self, id: int) -> bool:
        """Возвращает True, если зарегистрирован. Иначе - False"""
        user = await self.session.get(User, id)
        if user:
            return True
        return False

    async def add_user(self, id: int, username: str | None, hashed_master_password: str) -> None:
        """Создание нового пользователя с переданными id телеграмма, username'ом и захэшированным мастре-паролем"""
        user = await self.session.get(User, id)
        if not user:
            user = User(
                id=id,
                username=username,
                master_password=hashed_master_password
            )
            self.session.add(user)
        await self.session.commit()

    async def add_password(self, owner_id: int, name: str, hashed_password: str, comment: str = None):
        password = Password(
            service_name=name,
            hashed_password=hashed_password,
            comment=comment,
            owner_id=owner_id
        )
        self.session.add(password)
        await self.session.commit()

    # async def add_bookmark(self, user_id: int):
    #     user = await self.session.get(User, user_id)
    #     stmt = select(Bookmark).where(and_(Bookmark.user_id == user_id, Bookmark.page == user.page))
    #     res = await self.session.execute(stmt)
    #     res = res.first()
    #
    #     if not res:
    #         bookmark = Bookmark(
    #             user_id=user_id,
    #             page=user.page
    #         )
    #         self.session.add(bookmark)
    #     await self.session.commit()

    async def get_user_data(self, id: int) -> User:
        user = await self.session.get(User, id)
        return user

    async def update_user_data(self, id: int, page: int) -> User:
        user = await self.session.get(User, id)
        user.page = page

        await self.session.commit()
        return user

    # async def delete_bookmark(self, user_id: int, page: int):
    #     stmt = delete(Bookmark).where(
    #         and_(user_id == Bookmark.user_id, page == Bookmark.page)
    #     )
    #     await self.session.execute(stmt)
    #     await self.session.commit()
    #
    # async def get_all_bookmarks(self, user_id) -> List[int]:
    #     stmt = select(Bookmark.page).where(Bookmark.user_id == user_id)
    #     result = await self.session.execute(stmt)
    #     result = [i[0] for i in result.all()]
    #     return result
