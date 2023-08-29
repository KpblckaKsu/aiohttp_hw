import json
from aiohttp import web
from models import engine, Base, Advertisement, Session
from sqlalchemy.exc import IntegrityError

app = web.Application()


async def orm_context(app):
    print("Start")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    print("Stop")


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request["session"] = session
        response = await handler(request)
        return response


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


async def get_adv(adv_id: int, session: Session) -> Advertisement:
    adv = await session.get(Advertisement, adv_id)
    if adv is None:
        raise web.HTTPNotFound(
            text=json.dumps({"error": "adv not found"}), content_type="application/json"
        )
    return adv


class AdvertisementsView(web.View):
    @property
    def session(self) -> Session:
        return self.request["session"]

    @property
    def adv_id(self) -> int:
        return int(self.request.match_info["adv_id"])

    async def get(self):
        adv = await get_adv(self.adv_id, self.session)
        return web.json_response(
            {
                "id": adv.id,
                "title": adv.title,
                "description": adv.description,
                "created_at": int(adv.created_at.timestamp()),
                "owner": adv.owner,
            }
        )

    async def post(self):
        json_data = await self.request.json()
        adv = Advertisement(**json_data)
        self.session.add(adv)
        try:
            await self.session.commit()
        except IntegrityError as er:
            raise web.HTTPConflict(
                text=json.dumps({"error": "adv already exists"}),
                content_type="application/json",
            )
        return web.json_response(
            {
                "id": adv.id,
            }
        )

    async def patch(self):
        json_data = await self.request.json()
        adv = await get_adv(self.adv_id, self.session)
        for field, value in json_data.items():
            setattr(adv, field, value)
        self.session.add(adv)
        await self.session.commit()
        return web.json_response({"id": adv.id})

    async def delete(self):
        adv = await get_adv(self.adv_id, self.session)
        await self.session.delete(adv)
        await self.session.commit()
        return web.json_response({"status": "success"})


app.add_routes(
    [
        web.get("/adv/{adv_id:\d+}", AdvertisementsView),
        web.patch("/adv/{adv_id:\d+}", AdvertisementsView),
        web.delete("/adv/{adv_id:\d+}", AdvertisementsView),
        web.post("/adv/", AdvertisementsView),
    ]
)

if __name__ == "__main__":
    web.run_app(app)
