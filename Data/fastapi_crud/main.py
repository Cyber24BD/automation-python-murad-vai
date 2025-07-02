from fastapi import FastAPI, Request, Depends, Form, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse, StreamingResponse, RedirectResponse
import io
import csv
import json
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from typing import List, Optional
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="fastapi_crud/static"), name="static")

templates = Jinja2Templates(directory="fastapi_crud/templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(request: Request, db: Session = Depends(get_db)):
    stats = crud.get_dashboard_stats(db)
    return templates.TemplateResponse("index.html", {"request": request, "stats": stats})

@app.get("/api/items")
def get_items(request: Request, db: Session = Depends(get_db), page: int = 1, page_size: int = 20):
    skip = (page - 1) * page_size
    items = crud.get_items(db, skip=skip, limit=page_size)
    total_items = crud.get_items_count(db)
    return {"items": items, "total_items": total_items}

@app.get("/api/search")
def search_items(request: Request, db: Session = Depends(get_db), query: str = "", page: int = 1, page_size: int = 20):
    skip = (page - 1) * page_size
    items = crud.search_items(db, query=query, skip=skip, limit=page_size)
    total_items = crud.search_items_count(db, query=query)
    return {"items": items, "total_items": total_items}

@app.get("/up-down-data")
def up_down_data_page(request: Request):
    return templates.TemplateResponse("up_down_data.html", {"request": request})


@app.get("/download/json")
def download_json(db: Session = Depends(get_db)):
    items = crud.get_items(db)
    output_items = []
    for item in items:
        media_data = item.media if isinstance(item.media, dict) else {}
        output_item = {
            "name": item.name,
            "description": item.description,
            "price": item.price,
            "Town Hall Level": item.town_hall_level,
            "King Level": item.king_level,
            "Queen Level": item.queen_level,
            "Warden Level": item.warden_level,
            "Champion Level": item.champion_level,
            "media": {
                "media1": media_data.get("media1"),
                "media2": media_data.get("media2"),
                "media3": media_data.get("media3"),
            }
        }
        output_items.append(output_item)
    
    json_data = json.dumps(output_items, indent=2)
    return StreamingResponse(
        io.StringIO(json_data),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=all_items.json"}
    )

@app.get("/download/csv")
def download_csv(db: Session = Depends(get_db)):
    items = crud.get_items(db)
    output = io.StringIO()
    writer = csv.writer(output)
    
    headers = [
        "name", "description", "price", "town_hall_level", "king_level", 
        "queen_level", "warden_level", "champion_level", "media1", "media2", "media3"
    ]
    writer.writerow(headers)
    
    for item in items:
        media_data = item.media if isinstance(item.media, dict) else {}
        row = [
            item.name, item.description, item.price, item.town_hall_level,
            item.king_level, item.queen_level, item.warden_level, item.champion_level,
            media_data.get("media1"), media_data.get("media2"), media_data.get("media3")
        ]
        writer.writerow(row)
    
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=all_items.csv"})


@app.get("/download/sample-csv")
def download_sample_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    headers = [
        "name", "description", "price", "town_hall_level", "king_level", 
        "queen_level", "warden_level", "champion_level", "media1", "media2", "media3"
    ]
    writer.writerow(headers)
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=sample_template.csv"})


@app.post("/upload/csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        return JSONResponse(status_code=400, content={"success": False, "message": "Invalid file type. Please upload a CSV file."})

    content = await file.read()
    decoded_content = content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(decoded_content))
    
    errors = []
    created_count = 0

    for i, row in enumerate(csv_reader):
        try:
            # Validate row data using the ItemCreate schema
            item_schema = schemas.ItemCreate(**row)
            # If valid, create the item in the database
            crud.create_item(db=db, item=item_schema)
            created_count += 1
        except ValidationError as e:
            errors.append({"row": i + 2, "errors": e.errors()}) # i+2 to account for header and 0-indexing
        except Exception as e:
            errors.append({"row": i + 2, "error": str(e)})

    if errors:
        return JSONResponse(
            status_code=422,
            content={"success": False, "message": f"CSV validation failed. {created_count} items were added, but some had errors.", "errors": errors}
        )

    return {"success": True, "message": f"Successfully added {created_count} items from CSV."}


# -------------------- JSON UPLOAD --------------------

@app.post("/upload/json")
async def upload_json(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        if not isinstance(data, list):
            return JSONResponse(status_code=400, content={"success": False, "message": "Upload must be a list of JSON objects."})

        created = 0
        errors = []
        for idx, itm in enumerate(data, start=1):
            try:
                item_create = schemas.ItemCreate(
                    name=itm.get("name"),
                    description=itm.get("description"),
                    price=itm.get("price"),
                    town_hall_level=itm.get("Town Hall Level"),
                    king_level=itm.get("King Level"),
                    queen_level=itm.get("Queen Level"),
                    warden_level=itm.get("Warden Level"),
                    champion_level=itm.get("Champion Level"),
                    media1=itm.get("media", {}).get("media1"),
                    media2=itm.get("media", {}).get("media2"),
                    media3=itm.get("media", {}).get("media3"),
                )
                crud.create_item(db=db, item=item_create)
                created += 1
            except ValidationError as ve:
                errors.append({"item": idx, "errors": ve.errors()})
            except Exception as ex:
                errors.append({"item": idx, "errors": str(ex)})

        if errors:
            return JSONResponse(status_code=422, content={"success": False, "message": f"Added {created} items, but some entries had errors.", "errors": errors})

        return {"success": True, "message": f"Successfully added {created} items."}

    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "message": "Server error.", "errors": [str(e)]})

@app.get("/json")
def get_all_items_as_json(db: Session = Depends(get_db)):
    """
    Public endpoint that returns all items as JSON.
    Any media field that is either `None` or an empty string ("") is omitted from the
    response.  If all three media fields are missing/empty for an item, the entire
    `media` object is left out of that item's JSON representation.
    """
    # Pull all items from DB (safeguard limit just in case)
    items = crud.get_items(db=db, skip=0, limit=1000)

    cleaned_items = []
    for itm in items:
        # Some rows may store `media` as a JSON/dict, others may store as plain str.
        raw_media: dict = itm.media if isinstance(itm.media, dict) else {}
        # Retain only keys whose value is truthy (filters out None and "")
        media_filtered = {k: v for k, v in raw_media.items() if v}

        # Build the dict using the alias names expected by clients
        item_dict = {
            "name": itm.name,
            "description": itm.description,
            "price": itm.price,
            "Town Hall Level": itm.town_hall_level,
            "King Level": itm.king_level,
            "Queen Level": itm.queen_level,
            "Warden Level": itm.warden_level,
            "Champion Level": itm.champion_level,
        }

        if media_filtered:
            item_dict["media"] = media_filtered

        cleaned_items.append(item_dict)

    return JSONResponse(content=cleaned_items)


@app.post("/add")
def add_item(
    request: Request,
    db: Session = Depends(get_db),
    name: str = Form(...),
    description: str = Form(...),
    price: str = Form(...),
    town_hall_level: str = Form(...),
    king_level: str = Form(...),
    queen_level: str = Form(...),
    warden_level: str = Form(...),
    champion_level: str = Form(...),
    media1: str = Form(...),
    media2: Optional[str] = Form(None),
    media3: Optional[str] = Form(None),
):
    try:
        item = schemas.ItemCreate(
            name=name,
            description=description,
            price=price,
            town_hall_level=town_hall_level,
            king_level=king_level,
            queen_level=queen_level,
            warden_level=warden_level,
            champion_level=champion_level,
            media1=media1,
            media2=media2,
            media3=media3,
        )
        created_item = crud.create_item(db=db, item=item)
        
        # Check if request is AJAX (has specific headers)
        if request.headers.get("X-Requested-With") == "XMLHttpRequest" or "application/json" in request.headers.get("Accept", ""):
            return JSONResponse(content={
                "success": True, 
                "message": "Item added successfully!",
                "item": {
                    "id": created_item.id,
                    "name": created_item.name,
                    "description": created_item.description,
                    "price": created_item.price,
                    "town_hall_level": created_item.town_hall_level
                }
            })
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
            
    except Exception as e:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest" or "application/json" in request.headers.get("Accept", ""):
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": f"Error adding item: {str(e)}"}
            )
        else:
            raise HTTPException(status_code=400, detail=f"Error adding item: {str(e)}")

@app.post("/update/{item_id}")
def update_item_data(
    item_id: int,
    request: Request,
    db: Session = Depends(get_db),
    name: str = Form(...),
    description: str = Form(...),
    price: str = Form(...),
    town_hall_level: str = Form(...),
    king_level: str = Form(...),
    queen_level: str = Form(...),
    warden_level: str = Form(...),
    champion_level: str = Form(...),
    media1: str = Form(...),
    media2: Optional[str] = Form(None),
    media3: Optional[str] = Form(None),
):
    try:
        item_data = schemas.ItemCreate(
            name=name,
            description=description,
            price=price,
            town_hall_level=town_hall_level,
            king_level=king_level,
            queen_level=queen_level,
            warden_level=warden_level,
            champion_level=champion_level,
            media1=media1,
            media2=media2,
            media3=media3,
        )
        updated_item = crud.update_item(db=db, item_id=item_id, item=item_data)
        
        if not updated_item:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Item not found"}
            )
        
        return JSONResponse(content={
            "success": True,
            "message": "Item updated successfully!",
            "id": updated_item.id,
            "name": updated_item.name,
            "description": updated_item.description,
            "price": updated_item.price,
            "town_hall_level": updated_item.town_hall_level
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": f"Error updating item: {str(e)}"}
        )


@app.post("/delete/{item_id}")
def delete_item_data(item_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        deleted_item = crud.delete_item(db, item_id=item_id)
        
        if not deleted_item:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest" or "application/json" in request.headers.get("Accept", ""):
                return JSONResponse(
                    status_code=404,
                    content={"success": False, "message": "Item not found"}
                )
            else:
                raise HTTPException(status_code=404, detail="Item not found")
        
        # Check if request is AJAX
        if request.headers.get("X-Requested-With") == "XMLHttpRequest" or "application/json" in request.headers.get("Accept", ""):
            return JSONResponse(content={
                "success": True,
                "message": "Item deleted successfully!"
            })
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
            
    except Exception as e:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest" or "application/json" in request.headers.get("Accept", ""):
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": f"Error deleting item: {str(e)}"}
            )
        else:
            raise HTTPException(status_code=400, detail=f"Error deleting item: {str(e)}")

@app.post("/delete-all")
def delete_all_items_data(db: Session = Depends(get_db)):
    try:
        crud.delete_all_items(db)
        return JSONResponse(content={"success": True, "message": "All items deleted successfully!"})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Error deleting all items: {str(e)}"}
        )
