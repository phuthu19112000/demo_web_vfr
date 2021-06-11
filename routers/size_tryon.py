from starlette.responses import JSONResponse
from pydantic import BaseModel
import cv2
import base64
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Optional
from recom_client_api.client_api import Client
from recom_client_api.api_requests.user_api import GetUserValues
import requests
import base64

router = APIRouter()
templates = Jinja2Templates(directory="templates")
client = Client()

dict_category = {
    "top":["long sleeve dress","short sleeve dress","short sleeve top","long sleeve top","vest","long sleeve outwear"],
    "bottom":["trousers","skirt"]
}



def resize_image(img,scale_percent):
    width = int(img.shape[1]*(scale_percent/100))
    height = int(img.shape[0]*(scale_percent/100))
    dim = (width,height)
    img = cv2.resize(img,dim,interpolation=cv2.INTER_AREA)
    return img

def convert_to_file(result_image):
    pass
  

#SIZE FITTING
@router.get("/products", response_class=HTMLResponse)
async def api_fitsize(request: Request):
    """
    Recommend size with each category
    """
    return templates.TemplateResponse("inner-page-fix.html",{"request":request})

@router.get("/predict", response_class=JSONResponse)
async def api_findsize(request: Request):
    """
    Recommend size using data and Deep learning
    """
    return templates.TemplateResponse("index.html", {"request":request})

#TRY ON
@router.get("/tryon", response_class=HTMLResponse)
async def api_tryon(request: Request):
    return templates.TemplateResponse("tryon.html",{"request":request})


data = {
    "id_ao": None,
    "category_ao": None,
    "id_quan": None,
    "category_quan": None,
    "body": 4985
    }

@router.get("/result")
async def api_get_result(iid:str, category:str, request: Request):
    """
    with each certain pants or shirt, proceed to try on the mannequin and return, display image to UI 
    """
    
    if category == "long sleeve dress" or category == "short sleeve dress":
        data["id_ao"] = iid
        data["category_ao"] = category
        data["id_quan"] = None
        data["category_quan"] = None

    if category == "short sleeve top" or category == "long sleeve top" or category == "vest" or category == "long sleeve outwear":
        data["id_ao"] = iid
        data["category_ao"] = category

    if category == "trousers" or category == "skirt":
        data["id_quan"] = iid
        data["category_quan"] = category

    #url = "http://192.168.50.69:5849/{}/{}/{}/{}/{}".format(data["id_ao"],data["category_ao"],data["id_quan"],data["category_quan"],data["body"])
    response = requests.get(url="http://192.168.50.69:5849/4990/trousers/5013/long_sleeve_top/4985")
    result = response.content
    image = base64.b64decode(result.content)
    filename = '/home/hieuld/project_RS_VFR/demo_web_VFR/static/public/tryon-image/anh-tach-nen/image.png'
    
    with open(filename, 'wb') as f:
        f.write(image)

    message = "DONE!"
    return templates.TemplateResponse("tryon.html",{"request":request,"message":message})