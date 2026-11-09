
from pathlib import Path
from typing import Annotated

from fastapi import BackgroundTasks, Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pytubefix.exceptions import VideoUnavailable

from . import config
from .Routers_20 import video,search

background_tasks = BackgroundTasks()
app = FastAPI()
app.include_router(video.router)
app.include_router(search.router)

@app.exception_handler(VideoUnavailable)
async def VideoUnavailable_exception_handler(request: Request, ex: VideoUnavailable):
    return JSONResponse(
        status_code=500,
        content={"message": f"Can not get video. {ex.error_string}"},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allow all origins, change to specific origins for security (e.g., ["http://localhost:5500"])
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/heartbeat")
async def root(settings: Annotated[config.Settings, Depends(config.get_settings)]):
    return {"message": "I'm alive!",
             "author": settings.creator,
             "fullSettings": settings,
             "Path": list(Path("./blobs").iterdir())}
