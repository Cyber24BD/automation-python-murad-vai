from sqlalchemy.orm import Session
from sqlalchemy import func, desc, or_
from typing import List
from . import models, schemas

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_items_count(db: Session):
    return db.query(models.Item).count()

def search_items(db: Session, query: str, skip: int = 0, limit: int = 20):
    search_query = f"%{query}%"
    return db.query(models.Item).filter(
        or_(
            models.Item.name.ilike(search_query),
            models.Item.description.ilike(search_query)
        )
    ).offset(skip).limit(limit).all()

def search_items_count(db: Session, query: str):
    search_query = f"%{query}%"
    return db.query(models.Item).filter(
        or_(
            models.Item.name.ilike(search_query),
            models.Item.description.ilike(search_query)
        )
    ).count()

def create_item(db: Session, item: schemas.ItemCreate):
    media_dict = {
        "media1": item.media1,
        "media2": item.media2,
        "media3": item.media3
    }
    
    db_item = models.Item(
        name=item.name,
        description=item.description,
        price=item.price,
        town_hall_level=item.town_hall_level,
        king_level=item.king_level,
        queen_level=item.queen_level,
        warden_level=item.warden_level,
        champion_level=item.champion_level,
        media={k: v for k, v in media_dict.items() if v is not None}
    )
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    db_item = get_item(db, item_id)
    if db_item:
        update_data = item.dict(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_item, key, value)
        
        media_dict = {
            "media1": item.media1,
            "media2": item.media2,
            "media3": item.media3
        }
        
        # Filter out None values from media_dict and update db_item.media
        updated_media = {k: v for k, v in media_dict.items() if v is not None}
        if updated_media:
            if db_item.media:
                db_item.media.update(updated_media)
            else:
                db_item.media = updated_media

        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

def delete_all_items(db: Session):
    db.query(models.Item).delete()
    db.commit()



def create_items_from_upload(db: Session, items: List[schemas.ItemUpload]):
    for item_upload in items:
        # Convert from ItemUpload with nested media to ItemCreate
        item_create = schemas.ItemCreate(
            name=item_upload.name,
            description=item_upload.description,
            price=item_upload.price,
            town_hall_level=item_upload.town_hall_level,
            king_level=item_upload.king_level,
            queen_level=item_upload.queen_level,
            warden_level=item_upload.warden_level,
            champion_level=item_upload.champion_level,
            media1=item_upload.media.media1,
            media2=item_upload.media.media2,
            media3=item_upload.media.media3
        )
        create_item(db=db, item=item_create)
    return len(items)

def get_dashboard_stats(db: Session):
    stats = {}
    total_items = db.query(models.Item).count()
    stats['total_items'] = total_items

    if total_items == 0:
        stats['average_price'] = "$0.00"
        stats['most_common_th'] = "N/A"
        stats['highest_th'] = "N/A"
        return stats

    # Calculate average price
    prices = db.query(models.Item.price).all()
    total_price = 0
    valid_price_count = 0
    for price_tuple in prices:
        try:
            total_price += float(price_tuple[0])
            valid_price_count += 1
        except (ValueError, TypeError):
            continue
    stats['average_price'] = f"${(total_price / valid_price_count):.2f}" if valid_price_count > 0 else "$0.00"

    # Find most common Town Hall level
    most_common_th_query = db.query(models.Item.town_hall_level, func.count(models.Item.id).label('th_count')).group_by(models.Item.town_hall_level).order_by(desc('th_count')).first()
    stats['most_common_th'] = most_common_th_query[0] if most_common_th_query else "N/A"

    # Find highest Town Hall level
    all_th_levels = db.query(models.Item.town_hall_level).all()
    numeric_th_levels = []
    for th_level_tuple in all_th_levels:
        try:
            numeric_th_levels.append(int(th_level_tuple[0]))
        except (ValueError, TypeError):
            continue
    stats['highest_th'] = max(numeric_th_levels) if numeric_th_levels else "N/A"

    return stats
