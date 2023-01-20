import uvicorn
from fastapi import FastAPI
import cam

app = FastAPI()

@app.get("/")
def root():
    # cam()
    Left_count, Right_count, Smile_left, Smile_right, img_as_text = cam.capture()
    # print(type(data))
    # print(data)
    # tag, prob = cam.detection()
    return {"Left_count": Left_count,
     "Right_count": Right_count,
      "Smile_left": Smile_left,
      "Smile_right": Smile_right,
      "img_as_text":img_as_text
      }

if __name__ == "__main__":
    uvicorn.run("app:app", port=8000)

