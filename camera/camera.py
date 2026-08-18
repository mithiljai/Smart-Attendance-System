import cv2
import config


class Camera:

    def __init__(self):

        self.camera = cv2.VideoCapture(
            config.CAMERA_INDEX
        )

        self.camera.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            config.FRAME_WIDTH
        )

        self.camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            config.FRAME_HEIGHT
        )

        if not self.camera.isOpened():
            raise RuntimeError(
                "ERROR: Could not open USB webcam."
            )

    def read(self):

        success, frame = self.camera.read()

        if not success:
            return None

        return frame

    def release(self):

        if self.camera.isOpened():
            self.camera.release()
