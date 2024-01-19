from sqlalchemy.orm import Session
import database as db


class SqlAlchemyLocation:
    """
    SQLAlchemy ORM implementation for handling a database as storage
    """
    # def __init__(self, db: Session):
    #     self.db = db

    def add(self, location_data: db.schemas.EnergyDataCreate):
        with db.get_db() as db_session:
            db_surfspot = db.models.EnergyData(**location_data.dict())
            db_session.add(db_surfspot)
            db_session.commit()
            db_session.refresh(db_surfspot)
        # return db_surfspot

    # def get_by_id(self, location_id: int) -> schemas.LocationResponse | None:
    #     location_query = self._get_location_by_id_query(location_id)
    #     return location_query.first()
    #
    # def get_by_name(self, location_name: str) -> schemas.LocationResponse | None:
    #     return self.db.query(EnergyData).filter(EnergyData.name == location_name).first()
    #
    # def list(self) -> list[schemas.LocationResponse]:
    #     return self.db.query(EnergyData).all()
    #
    # def update(self, location_id: int, updated_location: schemas.LocationBase) -> schemas.LocationResponse:
    #     spot_query = self._get_location_by_id_query(location_id)
    #     spot_query.update(updated_location.dict(), synchronize_session=False)
    #     self.db.commit()
    #     return spot_query.first()
    #
    # def delete(self, location_id: int) -> bool:
    #     location_query = self._get_location_by_id_query(location_id)
    #     location_data = location_query.first()
    #
    #     if location_data is None:
    #         return False
    #     else:
    #         location_query.delete(synchronize_session=False)
    #         self.db.commit()
    #         return True
    #
    # def _get_location_by_id_query(self, location_id: int) -> any:
    #     return self.db.query(EnergyData).filter(EnergyData.id == location_id)
