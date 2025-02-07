import asyncio
import base64
import io
import os
import sys
import traceback
import pyautogui
import cv2
import pyaudio
import PIL.Image
import mss
import time
import ast
def is_valid_python(code):
   try:
       ast.parse(code)
   except SyntaxError:
       return False
   return True
import argparse

from google import genai

if sys.version_info < (3, 11, 0):
    import taskgroup, exceptiongroup

    asyncio.TaskGroup = taskgroup.TaskGroup
    asyncio.ExceptionGroup = exceptiongroup.ExceptionGroup

FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 2024

MODEL = "models/gemini-2.0-flash-exp"

DEFAULT_MODE = "screen"

client = genai.Client(http_options={"api_version": "v1alpha"})

# While Gemini 2.0 Flash is in experimental preview mode, only one of AUDIO or
# TEXT may be passed here.
CONFIG = {"generation_config": {"response_modalities": ["TEXT"]}}
syspmessage="""You are a helpful assistant. Your responses will be parsed and executed directly. The platform is MACOS. Respond to all messages in the format:
# TEXT TO BE SHOWN TO USER
```python
code to execute
```
All lines that start with a hashtag will be spoken to the user. All lines between the python markdown formatting will be executed automatically.
If the user asks a question that requires a response, put it in a line that starts with a hashtag before the code. Not every prompt will require a code response. 
If the user asks you to complete a task, complete the task using the python library pyautogui to control the user's keyboard and mouse. Ensure that the code you write will work.
Use your visual abilities to complete a task. Don't assume anything about the user's filesystem or clipboard unless specified in the prompt or visualized on the screen.
DO NOT USE PYAUTOGUI IMAGE SEARCH EVER. THAT VIOLATES THE RULE AGAINST ASSUMING ABOUT THE USER'S FILESYSTEM. USE YOUR VISION/CODE TO GET MOUSE POSITIONS.
Do not assume a task must continue. If a task is not followed up on, wait for the next instruction. 
IMPORTANTLY, MAKE SURE YOUR CODE IS COMPLETE. DISFUNCTIONAL CODE IS BETTER THAN INCOMPLETE CODE. DO NOT COMMENT YOUR CODE OR PRINT A MESSAGE TO THE USER YOU STATED IN A LINE THAT STARTS WITH A HASHTAG.
"""
systemPrompt=f"SYSTEM INSTRUCTIONS (DO NOT RESPOND TO THIS): {syspmessage}"
pya = pyaudio.PyAudio()


class AudioLoop:
    def __init__(self, video_mode=DEFAULT_MODE):
        self.video_mode = video_mode

        self.audio_in_queue = None
        self.out_queue = None

        self.session = None

        self.send_text_task = None
        self.receive_audio_task = None
        self.play_audio_task = None

    async def send_text(self):
        while True:
            text = await asyncio.to_thread(
                input,
                "message > ",
            )
            if text.lower() == "q":
                break
            await self.session.send(input=text or ".", end_of_turn=True)

    def _get_frame(self, cap):
        # Read the frameq
        ret, frame = cap.read()
        # Check if the frame was read successfully
        if not ret:
            return None
        # Fix: Convert BGR to RGB color space
        # OpenCV captures in BGR but PIL expects RGB format
        # This prevents the blue tint in the video feed
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = PIL.Image.fromarray(frame_rgb)  # Now using RGB frame
        #img.thumbnail([1024, 1024])

        image_io = io.BytesIO()
        img.save(image_io, format="jpeg")
        image_io.seek(0)

        mime_type = "image/jpeg"
        image_bytes = image_io.read()
        return {"mime_type": mime_type, "data": base64.b64encode(image_bytes).decode()}

    async def get_frames(self):
        # This takes about a second, and will block the whole program
        # causing the audio pipeline to overflow if you don't to_thread it.
        cap = await asyncio.to_thread(
            cv2.VideoCapture, 0
        )  # 0 represents the default camera

        while True:
            frame = await asyncio.to_thread(self._get_frame, cap)
            if frame is None:
                break

            await asyncio.sleep(1.0)

            await self.out_queue.put(frame)

        # Release the VideoCapture object
        cap.release()

    def _get_screen(self):
        sct = mss.mss()
        monitor = sct.monitors[0]

        i = sct.grab(monitor)

        mime_type = "image/jpeg"
        image_bytes = mss.tools.to_png(i.rgb, i.size)
        img = PIL.Image.open(io.BytesIO(image_bytes))

        image_io = io.BytesIO()
        img.save(image_io, format="jpeg")
        image_io.seek(0)

        image_bytes = image_io.read()
        return {"mime_type": mime_type, "data": base64.b64encode(image_bytes).decode()}

    async def get_screen(self):

        while True:
            frame = await asyncio.to_thread(self._get_screen)
            if frame is None:
                break

            await asyncio.sleep(1.0)

            await self.out_queue.put(frame)

    async def send_realtime(self):
        while True:
            msg = await self.out_queue.get()
            await self.session.send(input=msg)

    async def listen_audio(self):
        mic_info = pya.get_default_input_device_info()
        self.audio_stream = await asyncio.to_thread(
            pya.open,
            format=FORMAT,
            channels=CHANNELS,
            rate=SEND_SAMPLE_RATE,
            input=True,
            input_device_index=mic_info["index"],
            frames_per_buffer=CHUNK_SIZE,
        )
        if __debug__:
            kwargs = {"exception_on_overflow": False}
        else:
            kwargs = {}
        while True:
            data = await asyncio.to_thread(self.audio_stream.read, CHUNK_SIZE, **kwargs)
            await self.out_queue.put({"data": "", "mime_type": "audio/pcm"})

    async def receive_audio(self):
        "Background task to reads from the websocket and write pcm chunks to the output queue"
        while True:
            turn = self.session.receive()
            ftext=""
            toPrint=""
            code=""
            stopBool=False
            async for response in turn:
                if data := response.data:
                    self.audio_in_queue.put_nowait(data)
                    continue
                if text := response.text:
                    #print(text, end="")
                    ftext+=text
            for line in ftext.split("\n"):
                if line.startswith("#") and not stopBool:
                    toPrint+=line[1:]
                elif line.startswith("```"):
                    stopBool=True
                elif stopBool:
                    code+=line+"\n"
            with open("prog.py","wt") as f:
                f.write(code)
            print(toPrint)
            time.sleep(2)
            if is_valid_python(code):
                try:
                    exec(code)
                except Exception as e:
                    print(f"CODE_EXEC: Python Invalid. Error: {e}")
                    print("message > ",end="")
            else:
                print("CODE_AST: Python Code was not valid. Did not execute.")
                print("message > ",end="")
                

            # If you interrupt the model, it sends a turn_complete.
            # For interruptions to work, we need to stop playback.
            # So empty out the audio queue because it may have loaded
            # much more audio than has played yet.
            while not self.audio_in_queue.empty():
                self.audio_in_queue.get_nowait()

    async def play_audio(self):
        '''stream = await asyncio.to_thread(
            pya.open,
            format=FORMAT,
            channels=CHANNELS,
            rate=RECEIVE_SAMPLE_RATE,
            output=True,
        )
        while True:
            bytestream = await self.audio_in_queue.get()
            await asyncio.to_thread(stream.write, bytestream)'''
        pass

    async def run(self):
        try:
            async with (
                client.aio.live.connect(model=MODEL, config=CONFIG) as session,
                asyncio.TaskGroup() as tg,
            ):
                self.session = session

                self.audio_in_queue = asyncio.Queue()
                self.out_queue = asyncio.Queue(maxsize=5)

                send_text_task = tg.create_task(self.send_text())
                tg.create_task(self.send_realtime())
                tg.create_task(self.listen_audio())
                if self.video_mode == "camera":
                    tg.create_task(self.get_frames())
                elif self.video_mode == "screen":
                    tg.create_task(self.get_screen())

                tg.create_task(self.receive_audio())
                tg.create_task(self.play_audio())
                await self.session.send(input=systemPrompt, end_of_turn=False)
                await send_text_task
                raise asyncio.CancelledError("User requested exit")

        except asyncio.CancelledError:
            pass
        #except ExceptionGroup as EG:
        #    self.audio_stream.close()
        #    traceback.print_exception(EG)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        type=str,
        default=DEFAULT_MODE,
        help="pixels to stream from",
        choices=["camera", "screen", "none"],
    )
    args = parser.parse_args()
    main = AudioLoop(video_mode=args.mode)
    asyncio.run(main.run())


