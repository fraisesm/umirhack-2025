from pony.orm import db_session, select
from datetime import datetime
from backend.db.models import CropRotation, Field, Crop

@db_session
def create_crop_rotation(field_id: int, crop_id: int, year: int, season: str, predecessor_crop_id: int | None, notes: str | None, avg_yield: float | None):
    field = Field.get(id=field_id)
    crop = Crop.get(id=crop_id)
    if not field:
        raise ValueError("Поле не найдено")
    if not crop:
        raise ValueError("Культура не найдена")

    predecessor_crop = Crop.get(id=predecessor_crop_id) if predecessor_crop_id else None

    rotation = CropRotation(
        field=field,
        crop=crop,
        year=year,
        season=season,
        predecessor_crop=predecessor_crop,
        notes=notes,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    if avg_yield:
        # Можно хранить в notes или добавить отдельное поле
        rotation.notes = (notes or "") + f"\nСредняя урожайность: {avg_yield} т/га"

    return rotation.to_dict()

@db_session
def get_all_rotations():
    return [r.to_dict() for r in CropRotation.select()]

@db_session
def get_rotation(rotation_id: int):
    rotation = CropRotation.get(id=rotation_id)
    return rotation.to_dict() if rotation else None

@db_session
def get_rotations_by_field(field_id: int):
    field = Field.get(id=field_id)
    if not field:
        return []
    return [r.to_dict() for r in field.crop_rotations]

@db_session
def update_rotation(rotation_id: int, data: dict):
    rotation = CropRotation.get(id=rotation_id)
    if not rotation:
        return None

    if "crop_id" in data and data["crop_id"]:
        rotation.crop = Crop.get(id=data["crop_id"])
    if "year" in data and data["year"]:
        rotation.year = data["year"]
    if "season" in data and data["season"]:
        rotation.season = data["season"]
    if "predecessor_crop_id" in data and data["predecessor_crop_id"]:
        rotation.predecessor_crop = Crop.get(id=data["predecessor_crop_id"])
    if "notes" in data:
        rotation.notes = data["notes"]

    rotation.updated_at = datetime.utcnow()
    return rotation.to_dict()

@db_session
def delete_rotation(rotation_id: int):
    rotation = CropRotation.get(id=rotation_id)
    if not rotation:
        return False
    rotation.delete()
    return True
